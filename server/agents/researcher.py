"""Agent 1: The Live Researcher.

Owned by Member 3. Spins up a Browserbase cloud browser via the Stagehand SDK,
searches a reference/news source for the topic, and extracts factual text.

STUBBED: returns mock facts so Agent 2/3 and the pipeline can be built and
tested without live Browserbase credentials. Swap research() for the real
Stagehand calls once BROWSERBASE_API_KEY / BROWSERBASE_PROJECT_ID are set.

Real implementation sketch (Stagehand Python SDK):

    from stagehand import Stagehand

    async def research(topic: str) -> ResearchFacts:
        stagehand = Stagehand(
            api_key=settings.browserbase_api_key,
            project_id=settings.browserbase_project_id,
        )
        await stagehand.init()
        page = stagehand.page
        await page.goto(f"https://en.wikipedia.org/wiki/{topic}")
        facts = await page.extract(
            "Extract the key factual summary of this topic as plain text, "
            "along with the page's source URL."
        )
        await stagehand.close()
        return ResearchFacts(topic=topic, source_urls=[page.url], raw_text=facts)
"""

from models import ResearchFacts

_MOCK_FACTS = (
    "Photosynthesis is the process by which plants, algae, and some bacteria "
    "convert light energy, water, and carbon dioxide into glucose and oxygen. "
    "It occurs primarily in chloroplasts, using the pigment chlorophyll to "
    "capture light energy. The process has two stages: the light-dependent "
    "reactions, which occur in the thylakoid membranes, and the light-independent "
    "reactions (Calvin cycle), which occur in the stroma."
)


async def research(topic: str) -> ResearchFacts:
    # TODO(Member 3): replace with real Stagehand browser automation.
    return ResearchFacts(
        topic=topic,
        source_urls=["https://example.com/mock-source"],
        raw_text=_MOCK_FACTS,
    )
