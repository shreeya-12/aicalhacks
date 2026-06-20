import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")

    browserbase_api_key: str = os.environ.get("BROWSERBASE_API_KEY", "")
    browserbase_project_id: str = os.environ.get("BROWSERBASE_PROJECT_ID", "")
    # Stagehand's own LLM calls (for page.act/page.extract reasoning) use this key,
    # separate from our ANTHROPIC_API_KEY usage in agents/storyteller.py and quiz_master.py.
    stagehand_model_api_key: str = os.environ.get("MODEL_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    stagehand_api_url: str = os.environ.get("STAGEHAND_API_URL", "")

    # No official Midjourney API exists; this is whatever unofficial proxy
    # or alternative image service the team ends up wiring in. See agents/images.py.
    image_api_key: str = os.environ.get("IMAGE_API_KEY", "")
    image_api_base_url: str = os.environ.get("IMAGE_API_BASE_URL", "")

    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl_seconds: int = int(os.environ.get("CACHE_TTL_SECONDS", "86400"))

    sentry_dsn: str = os.environ.get("SENTRY_DSN", "")

    # BAND platform (https://www.band.ai/) — a multi-agent "rooms" coordination
    # platform where each agent has its own agent_id/api_key. STUBBED: no Band
    # account exists yet, so nothing reads these fields except this file. See
    # pipeline.py's module docstring for the intended integration seam.
    band_rest_url: str = os.environ.get("BAND_REST_URL", "")
    band_ws_url: str = os.environ.get("BAND_WS_URL", "")
    band_api_key: str = os.environ.get("BAND_API_KEY", "")
    band_agent_id: str = os.environ.get("BAND_AGENT_ID", "")

    cors_origins: list[str] = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")


settings = Settings()
