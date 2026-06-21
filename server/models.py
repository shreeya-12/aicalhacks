from enum import Enum

from pydantic import BaseModel, Field


class AgeGroup(str, Enum):
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"


class GenerateRequest(BaseModel):
    topic: str = Field(min_length=1)
    age_group: AgeGroup


class ChapterOutline(BaseModel):
    """One chapter's plan, produced before any research happens. title is
    for display; research_query is a separate plain search-friendly phrase
    (stylized titles like "The Hungry Leaf" make poor search queries)."""

    title: str
    research_query: str


class ResearchFacts(BaseModel):
    """Output of Agent 1 (Researcher), scoped to a single chapter's research_query."""

    topic: str
    source_urls: list[str]
    raw_text: str


class ChapterContent(BaseModel):
    """What Agent 2 (Storyteller) actually produces per chapter — title is
    not re-generated, it's carried over verbatim from the ChapterOutline."""

    text: str
    image_prompt: str


class ChapterDraft(BaseModel):
    """A chapter's title (from planning) + content (from Agent 2) — no
    image_url yet, since that field is filled in later by the image step."""

    title: str
    text: str
    image_prompt: str


class Chapter(BaseModel):
    title: str
    text: str
    image_prompt: str
    image_url: str = ""  # populated by the image generation step, empty until then


class QuizQuestionContent(BaseModel):
    """What the Quiz Master actually produces per question — chapter_index is
    not generated, it's assigned afterward by pipeline.py based on which
    chapter's quiz call produced it."""

    question: str
    choices: list[str] = Field(min_length=4, max_length=4)
    correct_index: int = Field(ge=0, le=3)
    explanation: str


class QuizQuestion(BaseModel):
    question: str
    choices: list[str] = Field(min_length=4, max_length=4)
    correct_index: int = Field(ge=0, le=3)
    explanation: str
    chapter_index: int


class QuizPayload(BaseModel):
    """Output of Agent 3 (Quiz Master) for a single chapter — 2 questions per
    chapter, 3 chapters, assembled into 6 total by pipeline.py."""

    quiz: list[QuizQuestionContent] = Field(min_length=2, max_length=2)


class StoryPayload(BaseModel):
    """Final combined payload sent to the frontend and cached in Redis."""

    topic: str
    age_group: AgeGroup
    chapters: list[Chapter]
    quiz: list[QuizQuestion]


class HistoryItem(BaseModel):
    topic: str
    age_group: AgeGroup
