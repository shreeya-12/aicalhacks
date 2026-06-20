"""Sequential orchestration: Agent 1 -> Agent 2 -> Agent 3 -> images -> cache.

State flowing through the pipeline is just the Pydantic models in models.py —
each agent's output is the next agent's input, with no separate state-machine
object needed:

    topic (str)
        -> research()      -> ResearchFacts   (Agent 1: raw scraped text)
        -> write_story()    -> StoryDraft      (Agent 2: list[ChapterDraft], no image_url yet)
        -> write_quiz()     -> list[QuizQuestion]  (Agent 3: grounded only in StoryDraft text)
        -> generate_image() -> attaches image_url, producing the final Chapter
        -> StoryPayload     (cached in Redis, returned to the frontend)

Written as plain async functions rather than against a specific framework.

BAND (https://www.band.ai/) is a multi-agent *rooms* coordination platform —
each agent gets its own agent_id/api_key and agents communicate over a shared
room via BAND_REST_URL/BAND_WS_URL, rather than a simple function-call
pipeline. That's a heavier model than what we have here, and we don't have
Band credentials yet, so this file makes no Band calls. Config fields
(band_rest_url, band_ws_url, band_api_key, band_agent_id) exist in config.py
for when real credentials arrive. If/when that happens, the natural
integration point is to replace the direct `await research(...)` /
`await write_story(...)` / `await write_quiz(...)` calls below with
equivalent calls routed through a Band room, without changing
run_pipeline()'s signature or its StoryPayload return contract.
"""

import asyncio

from agents.images import generate_image
from agents.quiz_master import write_quiz
from agents.researcher import research
from agents.storyteller import write_story
from cache import get_cached_story, set_cached_story
from models import AgeGroup, Chapter, StoryPayload


async def run_pipeline(topic: str, age_group: AgeGroup) -> StoryPayload:
    cached = await get_cached_story(topic, age_group.value)
    if cached is not None:
        return cached

    facts = await research(topic)
    draft = await write_story(facts, age_group)
    quiz = await write_quiz(draft)

    image_urls = await asyncio.gather(*(generate_image(c.image_prompt) for c in draft.chapters))
    chapters = [
        Chapter(title=c.title, text=c.text, image_prompt=c.image_prompt, image_url=url)
        for c, url in zip(draft.chapters, image_urls)
    ]

    payload = StoryPayload(topic=topic, age_group=age_group, chapters=chapters, quiz=quiz)
    await set_cached_story(payload)
    return payload
