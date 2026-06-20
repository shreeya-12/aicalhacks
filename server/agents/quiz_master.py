"""Agent 3: The Quiz Master.

Owned by Member 1. Takes Agent 2's final chapter text (never the raw research)
and writes a 3-question multiple-choice quiz strictly grounded in that text,
to keep the quiz consistent with what the user actually read.
"""

import json

from anthropic import AsyncAnthropic

from config import settings
from models import QuizPayload, QuizQuestion, StoryDraft

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

_SYSTEM_PROMPT = """You are a quiz writer. Given story chapters, write exactly 3 \
multiple-choice questions that test comprehension of facts stated in those \
chapters. Do not introduce facts that aren't in the text.

Each question must have exactly 4 choices and one correct_index (0-3).

Respond with ONLY a JSON object matching this exact shape, no markdown fences, \
no commentary:

{
  "quiz": [
    {"question": "...", "choices": ["...", "...", "...", "..."], "correct_index": 0},
    {"question": "...", "choices": ["...", "...", "...", "..."], "correct_index": 0},
    {"question": "...", "choices": ["...", "...", "...", "..."], "correct_index": 0}
  ]
}
"""


def _build_user_prompt(draft: StoryDraft) -> str:
    chapters_text = "\n\n".join(f"{c.title}\n{c.text}" for c in draft.chapters)
    return f"Story chapters:\n\n{chapters_text}"


async def write_quiz(draft: StoryDraft) -> list[QuizQuestion]:
    response = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(draft)}],
    )

    raw_text = response.content[0].text
    data = json.loads(raw_text)
    payload = QuizPayload(**data)
    return payload.quiz
