"""Chapter planner — splits a topic into chapters before any research happens.

Runs first in the pipeline. Each chapter gets a display title and a separate
research_query: a plain, search-engine-friendly phrase used to drive that
chapter's own Browserbase/Stagehand research (a stylized title like "The
Hungry Leaf" makes a poor Wikipedia/Google search term).

Chapter count scales with age group (see CHAPTER_COUNT_RANGE) — Claude picks
within that range based on how much depth the topic actually warrants, not a
fixed number, so the tool schema/prompt are built per-call rather than once
at module load time.
"""

from anthropic import AsyncAnthropic

from agents._age_group_style import AUDIENCE_STYLE, CHAPTER_COUNT_RANGE
from agents._tool_schemas import input_schema_for
from config import settings
from models import AgeGroup, ChapterOutline

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_SYSTEM_PROMPT = """You are an expert curriculum planner. Split a complex topic into \
chapters that build on each other in order, appropriate for the requested age group \
and chapter count range. Use the topic's actual depth to decide how many chapters to \
produce within that range — a narrow topic warrants fewer, a sprawling one warrants \
more. For each chapter, provide:
- title: a short display title for the chapter
- research_query: a separate, plain, search-engine-friendly phrase (not stylized) \
that could be typed directly into Wikipedia or Google to research that chapter's \
specific subtopic

Call the submit_outline tool exactly once with your final result."""


def _build_outline_tool(age_group: AgeGroup) -> dict:
    min_count, max_count = CHAPTER_COUNT_RANGE[age_group]
    return {
        "name": "submit_outline",
        "description": f"Submit the chapter outlines for this topic ({min_count}-{max_count} chapters).",
        "input_schema": input_schema_for(ChapterOutline, "chapters", min_count, max_count),
    }


def _build_user_prompt(topic: str, age_group: AgeGroup) -> str:
    min_count, max_count = CHAPTER_COUNT_RANGE[age_group]
    return (
        f"Topic: {topic}\n"
        f"Audience: {AUDIENCE_STYLE[age_group]}\n"
        f"Chapter count: choose between {min_count} and {max_count} chapters, based on "
        "how much depth this specific topic warrants for this audience."
    )


async def plan_chapters(topic: str, age_group: AgeGroup) -> list[ChapterOutline]:
    outline_tool = _build_outline_tool(age_group)
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=_SYSTEM_PROMPT,
        tools=[outline_tool],
        tool_choice={"type": "tool", "name": "submit_outline"},
        messages=[{"role": "user", "content": _build_user_prompt(topic, age_group)}],
    )

    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    return [ChapterOutline(**c) for c in tool_use_block.input["chapters"]]
