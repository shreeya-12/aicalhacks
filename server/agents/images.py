"""Media step: turns Agent 2's image prompts into URLs.

Owned by Member 3. Midjourney has no official public API — access is normally
via Discord, or an unofficial paid proxy that wraps the Discord bot. Until the
team picks and configures one (or an alternative like Stability/Replicate),
this returns placeholder images so the pipeline runs end-to-end.

Real implementation sketch (depends entirely on the chosen provider, e.g. an
unofficial Midjourney proxy with a submit/poll-for-result flow):

    async def generate_image(prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            submit = await client.post(
                f"{settings.image_api_base_url}/imagine",
                headers={"Authorization": f"Bearer {settings.image_api_key}"},
                json={"prompt": prompt},
            )
            task_id = submit.json()["task_id"]
            # then poll a /fetch/{task_id} endpoint until status == "completed"
            ...
        return image_url
"""

import urllib.parse


async def generate_image(prompt: str) -> str:
    # TODO(Member 3): replace with a real Midjourney proxy or alternative image API call.
    return f"https://placehold.co/512x512?text={urllib.parse.quote(prompt[:30])}"
