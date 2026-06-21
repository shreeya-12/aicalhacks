from __future__ import annotations

import re

import redis.asyncio as redis

from config import settings
from models import HistoryItem, StoryPayload

_client: redis.Redis | None = None

# A Redis LIST of HistoryItem JSON, most-recent-first, capped to _HISTORY_LIMIT
# entries — gives GET /api/history a free recency ordering without needing a
# separate timestamp/sorted-set.
_HISTORY_KEY = "storystream:history"
_HISTORY_LIMIT = 50


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
    client = _get_client()
    key = cache_key(payload.topic, payload.age_group.value)
    await client.set(key, payload.model_dump_json(), ex=settings.cache_ttl_seconds)

    history_item = HistoryItem(topic=payload.topic, age_group=payload.age_group)
    await client.lpush(_HISTORY_KEY, history_item.model_dump_json())
    await client.ltrim(_HISTORY_KEY, 0, _HISTORY_LIMIT - 1)


async def list_history(limit: int = 20) -> list[HistoryItem]:
    raw_items = await _get_client().lrange(_HISTORY_KEY, 0, _HISTORY_LIMIT - 1)
    seen: set[tuple[str, str]] = set()
    items: list[HistoryItem] = []
    for raw in raw_items:
        item = HistoryItem.model_validate_json(raw)
        dedupe_key = (item.topic, item.age_group.value)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        items.append(item)
        if len(items) >= limit:
            break
    return items
