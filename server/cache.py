from __future__ import annotations

import re

import redis.asyncio as redis

from config import settings
from models import StoryPayload

_client: redis.Redis | None = None


def _get_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(settings.redis_url, decode_responses=True)
    return _client


def cache_key(topic: str, age_group: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    return f"storystream:{slug}:{age_group}"


async def get_cached_story(topic: str, age_group: str) -> StoryPayload | None:
    raw = await _get_client().get(cache_key(topic, age_group))
    if raw is None:
        return None
    return StoryPayload.model_validate_json(raw)


async def set_cached_story(payload: StoryPayload) -> None:
    key = cache_key(payload.topic, payload.age_group.value)
    await _get_client().set(key, payload.model_dump_json(), ex=settings.cache_ttl_seconds)
