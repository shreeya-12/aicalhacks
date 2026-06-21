"""Agent 1: The Live Researcher — "Mega-Crawler".

One continuous Browserbase/Stagehand browser session does the entire
data-gathering phase, visiting multiple pages in sequence and accumulating
text into a single raw_text block for Agent 2/3 to work from:

  1. Wikipedia: navigate to the topic's article, extract a factual summary.
     This is the one must-have source — if it fails, the whole research step
     falls back to mock data.
  2. Google: search the same topic, extract the top 2 YouTube video URLs and
     top 2 article URLs (excluding Wikipedia). Best-effort — if this fails,
     research continues with just the Wikipedia summary.
  3. Deep dive: visit each found article/YouTube URL in the same session,
     dismiss popups/expand transcripts via act(), and extract their text.
     Each URL is independently best-effort — a single failed source is
     skipped, not fatal to the whole crawl.

Falls back to mock facts when BROWSERBASE_API_KEY/BROWSERBASE_PROJECT_ID are
unset, so the rest of the pipeline keeps working without live credentials —
this is the expected dev-mode path, not an error condition.

Stagehand's Python SDK (package `stagehand-py`, module `stagehand`) is fully
async-native: Stagehand.init/page.goto/page.act/page.extract/close are all
coroutines, confirmed by inspecting the installed package directly. With no
explicit schema, page.extract(instruction) defaults to schema
{"extraction": "<string>"}, so the result is read off `result.extraction`.
For the Google link-extraction step, an explicit Pydantic schema
(_RelatedLinks) is passed instead, so the result's fields match that shape.
"""

import asyncio
import logging

from pydantic import BaseModel, Field
from stagehand import Stagehand, StagehandConfig
from stagehand.page import StagehandPage

from config import settings
from models import ResearchFacts

logger = logging.getLogger(__name__)

_PAGE_TIMEOUT_SECONDS = 20
_MAX_ARTICLES = 2
_MAX_YOUTUBE = 2

_MOCK_FACTS = (
    "Photosynthesis is the process by which plants, algae, and some bacteria "
    "convert light energy, water, and carbon dioxide into glucose and oxygen. "
    "It occurs primarily in chloroplasts, using the pigment chlorophyll to "
    "capture light energy. The process has two stages: the light-dependent "
    "reactions, which occur in the thylakoid membranes, and the light-independent "
    "reactions (Calvin cycle), which occur in the stroma."
)


class _RelatedLinks(BaseModel):
    youtube_urls: list[str] = Field(default_factory=list)
    article_urls: list[str] = Field(default_factory=list)


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


async def _extract_wikipedia_summary(page: StagehandPage, topic: str) -> str:
    await page.goto(_build_wikipedia_url(topic))
    result = await page.extract(
        "Extract a factual summary of this topic as plain text, 3-5 paragraphs, "
        "suitable as raw research notes."
    )
    return result.extraction


async def _search_google_for_links(page: StagehandPage, topic: str) -> _RelatedLinks:
    await page.goto("https://www.google.com")
    await page.act(f"type '{topic}' into the search box and press enter")
    result = await page.extract(
        "Identify and extract the URLs for the top two relevant YouTube videos, "
        "and the top two standard web articles relevant to this search. "
        "Explicitly ignore any URLs from wikipedia.org.",
        schema_definition=_RelatedLinks,
    )
    return _RelatedLinks(
        youtube_urls=getattr(result, "youtube_urls", None) or [],
        article_urls=getattr(result, "article_urls", None) or [],
    )


async def _extract_article_text(page: StagehandPage, url: str) -> str:
    await page.goto(url)
    await page.act("dismiss any popup, cookie consent banner, or newsletter signup dialog if present")
    result = await page.extract(
        "Extract the core educational article text as plain text, ignoring ads, "
        "navigation, and sidebars."
    )
    return result.extraction


async def _extract_youtube_transcript(page: StagehandPage, url: str) -> str:
    await page.goto(url)
    await page.act("expand the video description and open the transcript panel if one is available")
    result = await page.extract("Extract the visible video description and transcript text as plain text.")
    return result.extraction


async def _crawl(topic: str) -> ResearchFacts:
    config = StagehandConfig(
        env="BROWSERBASE",
        api_key=settings.browserbase_api_key,
        project_id=settings.browserbase_project_id,
        model_name="claude-3-7-sonnet-latest",
    )
    stagehand = Stagehand(config=config, model_api_key=settings.stagehand_model_api_key)
    chunks: list[str] = []
    source_urls: list[str] = []

    try:
        await stagehand.init()
        page = stagehand.page

        # Step 1: Wikipedia — the one must-have source. Let failures here
        # propagate up to research()'s except block, which falls back to mock.
        wiki_summary = await asyncio.wait_for(
            _extract_wikipedia_summary(page, topic), timeout=_PAGE_TIMEOUT_SECONDS
        )
        chunks.append(f"From Wikipedia:\n{wiki_summary}")
        source_urls.append(_build_wikipedia_url(topic))

        # Step 2: Google search & link extraction — best-effort.
        links = _RelatedLinks()
        try:
            links = await asyncio.wait_for(
                _search_google_for_links(page, topic), timeout=_PAGE_TIMEOUT_SECONDS
            )
        except Exception:
            logger.warning("Google link extraction failed for topic=%r, continuing with Wikipedia only", topic)

        # Step 3: deep dive on whatever links were found. Each URL is
        # independently best-effort — a single failure is skipped, not fatal.
        for url in links.article_urls[:_MAX_ARTICLES]:
            try:
                text = await asyncio.wait_for(_extract_article_text(page, url), timeout=_PAGE_TIMEOUT_SECONDS)
                chunks.append(f"From article {url}:\n{text}")
                source_urls.append(url)
            except Exception:
                logger.warning("Article extraction failed for url=%r, skipping", url)

        for url in links.youtube_urls[:_MAX_YOUTUBE]:
            try:
                text = await asyncio.wait_for(_extract_youtube_transcript(page, url), timeout=_PAGE_TIMEOUT_SECONDS)
                chunks.append(f"From YouTube video {url}:\n{text}")
                source_urls.append(url)
            except Exception:
                logger.warning("YouTube extraction failed for url=%r, skipping", url)
    finally:
        await stagehand.close()

    return ResearchFacts(topic=topic, source_urls=source_urls, raw_text="\n\n".join(chunks))


async def research(topic: str) -> ResearchFacts:
    if not settings.browserbase_api_key or not settings.browserbase_project_id:
        return _mock_research(topic)

    try:
        return await _crawl(topic)
    except Exception:
        logger.exception("Stagehand research failed for topic=%r, falling back to mock", topic)
        return _mock_research(topic)
