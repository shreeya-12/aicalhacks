"""Standalone test: verify Redis set/get round-trip.

Run from repo root:
    python scripts/test_cache.py

Requires a local redis-server running (or REDIS_URL set in .env).
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

from cache import cache_key, get_cached_story, set_cached_story  # noqa: E402
from config import settings  # noqa: E402
from models import AgeGroup, Chapter, QuizQuestion, StoryPayload  # noqa: E402

TOPIC = "test-topic"
AGE_GROUP = AgeGroup.ELEMENTARY

SAMPLE = StoryPayload(
    topic=TOPIC,
    age_group=AGE_GROUP,
    chapters=[
        Chapter(
            title="Chapter 1",
            text="Once upon a time…",
            image_prompt="A sunny day",
            image_url="data:image/png;base64,abc123",
        )
    ],
    quiz=[
        QuizQuestion(question="What?", choices=["A", "B", "C", "D"], correct_index=0),
        QuizQuestion(question="Why?", choices=["A", "B", "C", "D"], correct_index=1),
        QuizQuestion(question="How?", choices=["A", "B", "C", "D"], correct_index=2),
    ],
)


async def main() -> None:
    print(f"Redis URL : {settings.redis_url}")
    print(f"Cache key : {cache_key(TOPIC, AGE_GROUP.value)}")
    print(f"TTL       : {settings.cache_ttl_seconds}s")

    print("\nWriting to cache …")
    await set_cached_story(SAMPLE)
    print("Write OK")

    print("Reading from cache …")
    result = await get_cached_story(TOPIC, AGE_GROUP.value)
    assert result is not None, "Cache miss — nothing returned!"
    assert result.topic == TOPIC
    assert result.chapters[0].image_url == "data:image/png;base64,abc123"
    print("Read OK — data round-tripped correctly")
    print(f"\nimage_url preview: {result.chapters[0].image_url[:40]}…")


if __name__ == "__main__":
    asyncio.run(main())
