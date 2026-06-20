"""Agent 3: The Quiz Master.

Owned by Member 1. Takes Agent 2's final chapter text (never the raw research)
and writes a 3-question multiple-choice quiz strictly grounded in that text,
to keep the quiz consistent with what the user actually read.
"""

from anthropic import AsyncAnthropic

from agents._tool_schemas import input_schema_for
from config import settings
from models import QuizPayload, QuizQuestion, StoryDraft

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_QUIZ_TOOL = {
    "name": "submit_quiz",
    "description": "Submit the final quiz of exactly 3 multiple-choice questions.",
    "input_schema": input_schema_for(QuizQuestion, "quiz", 3),
}

_SYSTEM_PROMPT = """You are a quiz writer. Given story chapters, write exactly 3 \
multiple-choice questions that test comprehension of facts stated in those \
chapters. Do not introduce facts that aren't in the text.

Each question must have exactly 4 choices and one correct_index (0-3).

Call the submit_quiz tool exactly once with your final result."""


def _build_user_prompt(draft: StoryDraft) -> str:
    chapters_text = "\n\n".join(f"{c.title}\n{c.text}" for c in draft.chapters)
    return f"Story chapters:\n\n{chapters_text}"


async def write_quiz(draft: StoryDraft) -> list[QuizQuestion]:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=_SYSTEM_PROMPT,
        tools=[_QUIZ_TOOL],
        tool_choice={"type": "tool", "name": "submit_quiz"},
        messages=[{"role": "user", "content": _build_user_prompt(draft)}],
    )

    tool_use_block = next(b for b in response.content if b.type == "tool_use")
    payload = QuizPayload(**tool_use_block.input)
    return payload.quiz
