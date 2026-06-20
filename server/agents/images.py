from __future__ import annotations

import logging

from openai import AsyncOpenAI

from config import settings

logger = logging.getLogger(__name__)

IMAGE_MODEL = "gpt-image-1"
_FALLBACK = "https://placehold.co/1024x1024?text=Image+unavailable"


async def generate_image(prompt: str) -> str:
    client = AsyncOpenAI(api_key=settings.image_api_key)
    try:
        response = await client.images.generate(
            model=IMAGE_MODEL,
            prompt=prompt,
            size="1024x1024",
        )
        b64 = response.data[0].b64_json
        if not b64:
            raise ValueError("Empty b64_json in response")
        return f"data:image/png;base64,{b64}"
    except Exception:
        logger.exception("Image generation failed for prompt %r — using fallback", prompt[:60])
        return _FALLBACK
