"""Agent 2: The Storyteller.

Writes ONE chapter at a time: takes that chapter's own research (gathered by
Agent 1 scoped to the chapter's research_query, not the whole topic) and
turns it into age-appropriate chapter text plus a descriptive Midjourney
image prompt. The chapter's title comes from chapter_planner.py and is not
re-generated here.

Uses the Anthropic Claude API directly (model and message-claude calls are
not BAND-specific, so they don't need to wait on BAND's integration details).
"""

from anthropic import AsyncAnthropic

from agents._age_group_style import AUDIENCE_STYLE, IMAGE_PROMPT_STYLE
from agents._tool_schemas import single_input_schema_for
from config import settings
from models import AgeGroup, ChapterContent, ResearchFacts

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_CHAPTER_TOOL = {
    "name": "submit_chapter",
    "description": "Submit this chapter's final text and image prompt.",
    "input_schema": single_input_schema_for(ChapterContent),
}

_SYSTEM_PROMPT = """You are an expert educational storyteller. You convert raw research \
text into one short chapter tailored to a specific age group, plus one descriptive \
Midjourney image prompt in the visual style requested.

Call the submit_chapter tool exactly once with your final result."""


def _build_user_prompt(chapter_title: str, facts: ResearchFacts, age_group: AgeGroup) -> str:
    return (
        f"Chapter title: {chapter_title}\n\n"
        f"Research facts for this chapter:\n{facts.raw_text}\n\n"
        f"Write for: {AUDIENCE_STYLE[age_group]}\n"
        f"Image prompt visual style: {IMAGE_PROMPT_STYLE[age_group]}\n"
        "Write the chapter text under this title, grounded in the research facts above."
    )


async def write_chapter(chapter_title: str, facts: ResearchFacts, age_group: AgeGroup) -> ChapterContent:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=_SYSTEM_PROMPT,
        tools=[_CHAPTER_TOOL],
        tool_choice={"type": "tool", "name": "submit_chapter"},
        messages=[{"role": "user", "content": _build_user_prompt(chapter_title, facts, age_group)}],
    )

    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    return ChapterContent(**tool_use_block.input)
