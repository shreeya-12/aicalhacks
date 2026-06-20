"""Sequential orchestration: Agent 1 -> Agent 2 -> Agent 3 -> images -> cache.

Written as plain async functions rather than against a specific framework.
The "BAND platform" (https://www.band.ai/) mentioned in the build plan is
expected to slot in here once its actual API/SDK is confirmed — e.g. if BAND
turns out to provide its own agent-execution/orchestration calls, swap the
direct agent calls below for BAND equivalents without changing the contract
of run_pipeline().
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
