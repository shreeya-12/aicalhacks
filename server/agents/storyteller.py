"""Agent 2: The Storyteller.

Owned by Member 1. Takes Agent 1's raw research text and turns it into 3
age-appropriate chapters, each paired with a descriptive Midjourney prompt.

Uses the Anthropic Claude API directly (model and message-claude calls are
not BAND-specific, so they don't need to wait on BAND's integration details).
"""

from anthropic import AsyncAnthropic

from agents._tool_schemas import input_schema_for
from config import settings
from models import AgeGroup, ChapterDraft, ResearchFacts, StoryDraft

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_CHAPTERS_TOOL = {
    "name": "submit_chapters",
    "description": "Submit the final set of exactly 3 story chapters.",
    "input_schema": input_schema_for(ChapterDraft, "chapters", 3),
}

_AGE_GROUP_STYLE = {
    AgeGroup.ELEMENTARY: "a curious 8-year-old. Use simple words, short sentences, and fun analogies.",
    AgeGroup.HIGH_SCHOOL: "a high school student. Use clear, engaging language with accurate terminology.",
    AgeGroup.ADULT: "an informed adult. Use precise, nuanced language and don't oversimplify.",
}

_IMAGE_PROMPT_STYLE = {
    AgeGroup.ELEMENTARY: "Pixar-style 3D render, bright, friendly, whimsical",
    AgeGroup.HIGH_SCHOOL: "clean educational diagram or realistic illustration, labeled if relevant",
    AgeGroup.ADULT: "hyper-realistic, detailed, documentary-style",
}

_SYSTEM_PROMPT = """You are an expert educational storyteller. You convert raw research \
text into exactly 3 short chapters tailored to a specific age group, and write one \
descriptive Midjourney image prompt per chapter in the visual style requested.

Call the submit_chapters tool exactly once with your final result."""


def _build_user_prompt(facts: ResearchFacts, age_group: AgeGroup) -> str:
    return (
        f"Topic: {facts.topic}\n\n"
        f"Research facts:\n{facts.raw_text}\n\n"
        f"Write for: {_AGE_GROUP_STYLE[age_group]}\n"
        f"Image prompt visual style: {_IMAGE_PROMPT_STYLE[age_group]}\n"
        "Produce exactly 3 chapters covering different facets of the topic, "
        "building on each other in order."
    )


async def write_story(facts: ResearchFacts, age_group: AgeGroup) -> StoryDraft:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=_SYSTEM_PROMPT,
        tools=[_CHAPTERS_TOOL],
        tool_choice={"type": "tool", "name": "submit_chapters"},
        messages=[{"role": "user", "content": _build_user_prompt(facts, age_group)}],
    )

    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    chapters = [ChapterDraft(**chapter) for chapter in tool_use_block.input["chapters"]]

    return StoryDraft(topic=facts.topic, age_group=age_group, chapters=chapters)
