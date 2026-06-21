"""Standalone test: fire one gpt-image-1 call and save the result to a PNG.

Run from repo root:
    python scripts/test_image.py

Requires IMAGE_API_KEY to be set in server/.env (or the environment).
"""
from __future__ import annotations

import base64
import sys
from pathlib import Path

# Allow importing server modules (config.py lives there)
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

from config import settings  # noqa: E402

if not settings.image_api_key:
    sys.exit("ERROR: IMAGE_API_KEY is not set. Check server/.env")

import openai  # noqa: E402

IMAGE_MODEL = "gpt-image-1"
PROMPT = "A friendly cartoon sun reading a book in a bright classroom, children's illustration style"
OUTPUT_PATH = Path(__file__).parent / "test_output.png"


def main() -> None:
    client = openai.OpenAI(api_key=settings.image_api_key)

    print(f"Calling {IMAGE_MODEL} …")
    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=PROMPT,
        size="1024x1024",
    )

    b64 = response.data[0].b64_json
    if not b64:
        sys.exit("ERROR: response contained no b64_json data")

    print(f"Success — base64 length: {len(b64):,} chars")

    img_bytes = base64.b64decode(b64)
    OUTPUT_PATH.write_bytes(img_bytes)
    print(f"Saved PNG → {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
