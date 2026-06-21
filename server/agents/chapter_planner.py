"""Chapter planner — splits a topic into 3 chapters before any research happens.

Runs first in the pipeline. Each chapter gets a display title and a separate
research_query: a plain, search-engine-friendly phrase used to drive that
chapter's own Browserbase/Stagehand research (a stylized title like "The
Hungry Leaf" makes a poor Wikipedia/Google search term).
"""

from anthropic import AsyncAnthropic

from agents._age_group_style import AUDIENCE_STYLE
from agents._tool_schemas import input_schema_for
from config import settings
from models import AgeGroup, ChapterOutline

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_OUTLINE_TOOL = {
    "name": "submit_outline",
    "description": "Submit the 3 chapter outlines for this topic.",
    "input_schema": input_schema_for(ChapterOutline, "chapters", 3),
}

_SYSTEM_PROMPT = """You are an expert curriculum planner. Split a complex topic into \
exactly 3 chapters that build on each other in order, appropriate for the requested \
age group. For each chapter, provide:
- title: a short display title for the chapter
- research_query: a separate, plain, search-engine-friendly phrase (not stylized) \
that could be typed directly into Wikipedia or Google to research that chapter's \
specific subtopic

Call the submit_outline tool exactly once with your final result."""


def _build_user_prompt(topic: str, age_group: AgeGroup) -> str:
    return f"Topic: {topic}\nAudience: {AUDIENCE_STYLE[age_group]}"


async def plan_chapters(topic: str, age_group: AgeGroup) -> list[ChapterOutline]:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=_SYSTEM_PROMPT,
        tools=[_OUTLINE_TOOL],
        tool_choice={"type": "tool", "name": "submit_outline"},
        messages=[{"role": "user", "content": _build_user_prompt(topic, age_group)}],
    )

    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    return [ChapterOutline(**c) for c in tool_use_block.input["chapters"]]
