"""Per-chapter orchestration: plan -> research each chapter -> write each
chapter + its quiz -> images -> cache.

    topic, age_group
        -> plan_chapters()        -> list[ChapterOutline]   (title + research_query; count varies by age group, see agents/_age_group_style.CHAPTER_COUNT_RANGE)
        -> research(outline.research_query)   -> ResearchFacts   (Agent 1, mega-crawler, once per chapter)
        -> write_chapter(...)     -> ChapterContent          (Agent 2, scoped to that chapter's research)
        -> write_quiz_for_chapter(...) -> list[QuizQuestionContent]  (Agent 3, 2 questions + explanations per chapter, grounded only in that chapter's text)
        -> (chapter_index assigned here, not by Agent 3, producing the final QuizQuestion)
        -> generate_image()       -> attaches image_url, producing the final Chapter
        -> StoryPayload           (N chapters, 2N quiz questions — cached in Redis, returned to the frontend)

Chapter count scales with age group: elementary is fixed at 3, but
middle_school/high_school/college get progressively wider ranges (Claude
picks within the range based on topic depth) — so the number of chapters,
and proportionally the number of sequential research crawls and total quiz
questions, is no longer always 3.

Each chapter's research runs sequentially (a single Browserbase plan may
only allow one concurrent browser session), but once all research is done,
all chapters' write_chapter + write_quiz_for_chapter calls run concurrently
via asyncio.gather — Claude calls have no shared-session concurrency limit,
so this is free latency savings. Note: for the larger chapter counts
(high_school/college), this means up to ~10 sequential Stagehand crawls,
which can take several minutes total — accepted for now, not yet optimized.

BAND (https://www.band.ai/) is a multi-agent *rooms* coordination platform —
each agent gets its own agent_id/api_key and agents communicate over a shared
room via BAND_REST_URL/BAND_WS_URL, rather than a simple function-call
pipeline. That's a heavier model than what we have here, and we don't have
Band credentials yet, so this file makes no Band calls. Config fields
(band_rest_url, band_ws_url, band_api_key, band_agent_id) exist in config.py
for when real credentials arrive.
"""

import asyncio

from agents.chapter_planner import plan_chapters
from agents.images import generate_image
from agents.quiz_master import write_quiz_for_chapter
from agents.researcher import research
from agents.storyteller import write_chapter
from cache import get_cached_story, set_cached_story
from models import AgeGroup, Chapter, ChapterDraft, QuizQuestion, ResearchFacts, StoryPayload


async def _write_chapter_and_quiz(
    chapter_index: int, title: str, facts: ResearchFacts, age_group: AgeGroup
) -> tuple[ChapterDraft, list[QuizQuestion]]:
    content = await write_chapter(title, facts, age_group)
    draft = ChapterDraft(
        title=title,
        text=content.text,
        image_prompt=content.image_prompt,
        key_terms=content.key_terms,
    )
    quiz_contents = await write_quiz_for_chapter(draft)
    quiz = [
        QuizQuestion(**question.model_dump(), chapter_index=chapter_index) for question in quiz_contents
    ]
    return draft, quiz


async def run_pipeline(topic: str, age_group: AgeGroup) -> StoryPayload:
    cached = await get_cached_story(topic, age_group.value)
    if cached is not None:
        return cached

    outlines = await plan_chapters(topic, age_group)

    facts_list = [await research(outline.research_query) for outline in outlines]

    results = await asyncio.gather(
        *(
            _write_chapter_and_quiz(i, outline.title, facts, age_group)
            for i, (outline, facts) in enumerate(zip(outlines, facts_list))
        )
    )
    chapter_drafts = [draft for draft, _ in results]
    quiz_questions = [question for _, questions in results for question in questions]

    image_urls = await asyncio.gather(*(generate_image(c.image_prompt) for c in chapter_drafts))
    chapters = [
        Chapter(
            title=c.title,
            text=c.text,
            image_prompt=c.image_prompt,
            image_url=url,
            key_terms=c.key_terms,
        )
        for c, url in zip(chapter_drafts, image_urls)
    ]

    payload = StoryPayload(topic=topic, age_group=age_group, chapters=chapters, quiz=quiz_questions)
    await set_cached_story(payload)
    return payload
