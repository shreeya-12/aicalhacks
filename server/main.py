from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import GenerateRequest, StoryPayload
from pipeline import run_pipeline
from sentry_init import init_sentry

init_sentry()

app = FastAPI(title="StoryStream API")

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
