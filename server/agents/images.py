from __future__ import annotations

import asyncio
import logging

from openai import AsyncOpenAI

from config import settings

logger = logging.getLogger(__name__)

IMAGE_MODEL = "gpt-image-1"
IMAGE_SIZE = "1024x1024"
_FALLBACK = "https://placehold.co/1024x1024?text=Image+unavailable"

# Stop waiting on a single image after this many seconds so a slow/stuck
# generation can't hang the whole demo.
_TIMEOUT_SECONDS = 60.0
# One extra attempt on transient failures (rate limits, flaky network).
_MAX_ATTEMPTS = 2

# Reuse one client across all calls instead of constructing one per image.
_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.image_api_key)
    return _client


async def generate_image(prompt: str) -> str:
    """Generate one image and return a base64 data URI.

    Never raises: on timeout/empty/API error it logs and returns a placeholder
    URL so the pipeline keeps running during a live demo.
    """
    prompt = (prompt or "").strip()
    if not prompt:
        logger.warning("Empty image prompt — using fallback")
        return _FALLBACK

    client = _get_client()
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = await asyncio.wait_for(
                client.images.generate(
                    model=IMAGE_MODEL,
                    prompt=prompt,
                    size=IMAGE_SIZE,
                ),
                timeout=_TIMEOUT_SECONDS,
            )
            b64 = response.data[0].b64_json
            if not b64:
                raise ValueError("Empty b64_json in response")
            return f"data:image/png;base64,{b64}"
        except asyncio.TimeoutError:
            logger.warning(
                "Image generation timed out (attempt %d/%d) for prompt %r",
                attempt, _MAX_ATTEMPTS, prompt[:60],
            )
        except Exception:
            logger.exception(
                "Image generation failed (attempt %d/%d) for prompt %r",
                attempt, _MAX_ATTEMPTS, prompt[:60],
            )

    logger.error("Image generation gave up after %d attempts — using fallback", _MAX_ATTEMPTS)
    return _FALLBACK
