"""Agent 2: The Storyteller.

Writes ONE chapter at a time: takes that chapter's own research (gathered by
Agent 1 scoped to the chapter's research_query, not the whole topic) and
turns it into age-appropriate chapter text plus a descriptive Midjourney
image prompt. The chapter's title comes from chapter_planner.py and is not
re-generated here.

Uses the Anthropic Claude API directly (model and message-claude calls are
not BAND-specific, so they don't need to wait on BAND's integration details).
"""

import logging

from anthropic import AsyncAnthropic
from pydantic import ValidationError

from agents._age_group_style import AUDIENCE_STYLE, IMAGE_PROMPT_STYLE
from agents._tool_schemas import single_input_schema_for
from config import settings
from models import AgeGroup, ChapterContent, ResearchFacts

logger = logging.getLogger(__name__)

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_CHAPTER_TOOL = {
    "name": "submit_chapter",
    "description": "Submit this chapter's final text and image prompt.",
    "input_schema": single_input_schema_for(ChapterContent),
}

_SYSTEM_PROMPT = """You are an expert educational storyteller. You convert raw research \
text into one engaging chapter tailored to a specific age group, plus one descriptive \
Midjourney image prompt in the visual style requested.

Write the chapter as 3-4 distinct paragraphs separated by a blank line (\\n\\n). Each \
paragraph should cover one clear idea so the text is easy to read and scan — do not \
return a single dense block of text. Aim for substance: explain the concept, give a \
concrete example or analogy, and connect it to why it matters.

Wrap the 3-6 most important terms or phrases in **double asterisks** the first time \
they appear in the text. For each one you bolded, add an entry to key_terms with the \
exact term (matching the bolded text) and a one-sentence, age-appropriate definition. \
The definition is shown when the reader hovers the highlighted term, so keep it short \
and self-contained.

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
        max_tokens=3000,
        system=_SYSTEM_PROMPT,
        tools=[_CHAPTER_TOOL],
        tool_choice={"type": "tool", "name": "submit_chapter"},
        messages=[{"role": "user", "content": _build_user_prompt(chapter_title, facts, age_group)}],
    )

    tool_use_block = next((b for b in response.content if b.type == "tool_use"), None)
    try:
        return ChapterContent(**(tool_use_block.input if tool_use_block else {}))
    except ValidationError:
        # A truncated/incomplete tool call (e.g. stop_reason == "max_tokens")
        # can yield empty or partial input. Don't let one chapter crash the
        # whole lesson — fall back to whatever text we can salvage.
        logger.warning(
            "write_chapter got incomplete tool input for %r (stop_reason=%s); using fallback",
            chapter_title, response.stop_reason,
        )
        partial = tool_use_block.input if tool_use_block else {}
        return ChapterContent(
            text=partial.get("text") or "This chapter could not be fully generated. Please try again.",
            image_prompt=partial.get("image_prompt") or f"educational illustration about {chapter_title}",
        )
