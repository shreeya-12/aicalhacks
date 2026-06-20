# StoryStream backend

FastAPI service that runs the 3-agent pipeline: Researcher -> Storyteller -> Quiz Master,
attaches generated images, and caches the result in Redis.

## Setup

```
cd server
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in ANTHROPIC_API_KEY at minimum
uvicorn main:app --reload --port 8000
```

Requires a local Redis instance for caching (`redis-server`, or `docker run -p 6379:6379 redis`).

## Layout

- `main.py` - FastAPI app, `/api/generate` endpoint
- `pipeline.py` - sequential orchestrator wiring the 3 agents together
- `agents/researcher.py` - Agent 1, Browserbase/Stagehand (currently stubbed)
- `agents/storyteller.py` - Agent 2, Claude-powered chapter + image-prompt writer
- `agents/quiz_master.py` - Agent 3, Claude-powered quiz writer
- `agents/images.py` - turns image prompts into URLs (currently stubbed, no Midjourney API wired yet)
- `cache.py` - Redis get/set keyed by `storystream:{topic}:{age_group}`
- `models.py` - shared Pydantic schemas (also the source of truth for the frontend's `StoryPayload` shape)
- `sentry_init.py` - no-op unless `SENTRY_DSN` is set

## Known stubs / TODOs

- **Agent 1**: returns hardcoded research facts. Swap in real Stagehand calls once Browserbase keys are available — see the docstring in `agents/researcher.py`.
- **Images**: returns placeholder image URLs. Midjourney has no official API; wire in whatever proxy/alternative the team picks — see `agents/images.py`.
- **BAND platform**: not yet integrated. The pipeline is plain async Python for now; if BAND (band.ai) turns out to require routing agent calls through its own SDK/API, that swap happens inside `pipeline.py` without changing the function signature other code depends on.
