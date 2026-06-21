"""Agent 3: The Quiz Master.

Takes ONE finished chapter (Agent 2's final title + text, never the raw
research) and writes exactly 2 multiple-choice questions strictly grounded in
that chapter's text, to keep each chapter's quiz consistent with what the
user actually read for that chapter. Runs once per chapter; pipeline.py
concatenates every chapter's 2 questions into the final quiz (so total quiz
length scales with chapter count, which varies by age group).
"""

import json
import logging

from anthropic import AsyncAnthropic
from pydantic import ValidationError

from agents._tool_schemas import input_schema_for
from config import settings
from models import ChapterDraft, QuizPayload, QuizQuestionContent

logger = logging.getLogger(__name__)

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_QUIZ_TOOL = {
    "name": "submit_quiz",
    "description": "Submit exactly 2 multiple-choice questions for this chapter.",
    "input_schema": input_schema_for(QuizQuestionContent, "quiz", 2),
}

_SYSTEM_PROMPT = """You are a quiz writer. Given one story chapter, write exactly 2 \
multiple-choice questions that test comprehension of facts stated in that chapter. \
Do not introduce facts that aren't in the text.

Each question must have exactly 4 choices and one correct_index (0-3). Each question \
also needs an explanation: 1-2 sentences, grounded only in this chapter's text, shown \
to the user if they answer incorrectly to help them understand the right answer.

Call the submit_quiz tool exactly once with your final result."""


def _build_user_prompt(chapter: ChapterDraft) -> str:
    return f"Chapter: {chapter.title}\n\n{chapter.text}"


async def write_quiz_for_chapter(chapter: ChapterDraft) -> list[QuizQuestionContent]:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=_SYSTEM_PROMPT,
        tools=[_QUIZ_TOOL],
        tool_choice={"type": "tool", "name": "submit_quiz"},
        messages=[{"role": "user", "content": _build_user_prompt(chapter)}],
    )

    tool_use_block = next((b for b in response.content if b.type == "tool_use"), None)
    raw = dict(tool_use_block.input) if tool_use_block else {}

    # Claude sometimes returns the quiz array as a JSON-encoded string rather
    # than an actual list — decode it before validation.
    if isinstance(raw.get("quiz"), str):
        try:
            raw["quiz"] = json.loads(raw["quiz"])
        except (ValueError, TypeError):
            pass

    try:
        return QuizPayload(**raw).quiz
    except ValidationError:
        # Don't let one chapter's malformed/truncated quiz 502 the whole
        # lesson — skip this chapter's questions instead.
        logger.warning(
            "write_quiz_for_chapter got invalid quiz for %r (stop_reason=%s); skipping its questions",
            chapter.title, response.stop_reason,
        )
        return []
