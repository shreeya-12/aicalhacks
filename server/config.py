import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")

    browserbase_api_key: str = os.environ.get("BROWSERBASE_API_KEY", "")
    browserbase_project_id: str = os.environ.get("BROWSERBASE_PROJECT_ID", "")

    # No official Midjourney API exists; this is whatever unofficial proxy
    # or alternative image service the team ends up wiring in. See agents/images.py.
    image_api_key: str = os.environ.get("IMAGE_API_KEY", "")
    image_api_base_url: str = os.environ.get("IMAGE_API_BASE_URL", "")

    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl_seconds: int = int(os.environ.get("CACHE_TTL_SECONDS", "86400"))

    sentry_dsn: str = os.environ.get("SENTRY_DSN", "")

    # BAND platform (https://www.band.ai/) integration point. Left unset until
    # the team confirms BAND's actual API/SDK surface — see pipeline.py.
    band_api_key: str = os.environ.get("BAND_API_KEY", "")

    cors_origins: list[str] = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")


settings = Settings()
