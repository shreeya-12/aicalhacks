import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from cache import list_history
from config import settings
from models import GenerateRequest, HistoryItem, StoryPayload
from pipeline import run_pipeline
from sentry_init import init_sentry

logger = logging.getLogger(__name__)

init_sentry()

app = FastAPI(title="StoryLearn Ai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/generate", response_model=StoryPayload)
async def generate(req: GenerateRequest) -> StoryPayload:
    try:
        return await run_pipeline(req.topic, req.age_group)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/history", response_model=list[HistoryItem])
async def history() -> list[HistoryItem]:
    # History is a nice-to-have sidebar, not a critical path — fail open to
    # an empty list (e.g. if Redis is unreachable) rather than a 500.
    try:
        return await list_history()
    except Exception:
        logger.exception("Failed to fetch history, returning empty list")
        return []
