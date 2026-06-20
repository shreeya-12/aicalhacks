"""Agent 1: The Live Researcher.

Spins up a Browserbase cloud browser via the Stagehand SDK, navigates to the
topic's Wikipedia article, and extracts a factual text summary.

Falls back to mock facts when BROWSERBASE_API_KEY/BROWSERBASE_PROJECT_ID are
unset, so the rest of the pipeline keeps working without live credentials —
this is the expected dev-mode path, not an error condition.

Stagehand's Python SDK (package `stagehand-py`, module `stagehand`) is fully
async-native: Stagehand.init/page.goto/page.act/page.extract/close are all
coroutines, confirmed by inspecting the installed package directly. With no
explicit schema, page.extract(instruction) defaults to schema
{"extraction": "<string>"}, so the result is read off `result.extraction`.
"""

import logging

from stagehand import Stagehand, StagehandConfig

from config import settings
from models import ResearchFacts

logger = logging.getLogger(__name__)

_MOCK_FACTS = (
    "Photosynthesis is the process by which plants, algae, and some bacteria "
    "convert light energy, water, and carbon dioxide into glucose and oxygen. "
    "It occurs primarily in chloroplasts, using the pigment chlorophyll to "
    "capture light energy. The process has two stages: the light-dependent "
    "reactions, which occur in the thylakoid membranes, and the light-independent "
    "reactions (Calvin cycle), which occur in the stroma."
)


def _mock_research(topic: str) -> ResearchFacts:
    return ResearchFacts(
        topic=topic,
        source_urls=["https://example.com/mock-source"],
        raw_text=_MOCK_FACTS,
    )


def _build_wikipedia_url(topic: str) -> str:
    # Naive slug — doesn't handle disambiguation pages or missing articles,
    # acceptable for hackathon scope.
    return f"https://en.wikipedia.org/wiki/{topic.strip().replace(' ', '_')}"


async def _extract_from_wikipedia(topic: str) -> tuple[str, str]:
    url = _build_wikipedia_url(topic)
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=settings.browserbase_api_key,
        project_id=settings.browserbase_project_id,
        model_name="claude-3-7-sonnet-latest",
    )
    stagehand = Stagehand(config=config, model_api_key=settings.stagehand_model_api_key)
    try:
        await stagehand.init()
        await stagehand.page.goto(url)
        result = await stagehand.page.extract(
            "Extract a factual summary of this topic as plain text, "
            "3-5 paragraphs, suitable as raw research notes."
        )
        return result.extraction, url
    finally:
        await stagehand.close()


async def research(topic: str) -> ResearchFacts:
    if not settings.browserbase_api_key or not settings.browserbase_project_id:
        return _mock_research(topic)

    try:
        raw_text, url = await _extract_from_wikipedia(topic)
    except Exception:
        logger.exception("Stagehand research failed for topic=%r, falling back to mock", topic)
        return _mock_research(topic)

    return ResearchFacts(topic=topic, source_urls=[url], raw_text=raw_text)
