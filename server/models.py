from enum import Enum

from pydantic import BaseModel, Field


class AgeGroup(str, Enum):
    ELEMENTARY = "elementary"
    HIGH_SCHOOL = "high_school"
    ADULT = "adult"


class GenerateRequest(BaseModel):
    topic: str = Field(min_length=1)
    age_group: AgeGroup


class ResearchFacts(BaseModel):
    """Output of Agent 1 (Researcher). Plain extracted text, no formatting yet."""

    topic: str
    source_urls: list[str]
    raw_text: str


class ChapterDraft(BaseModel):
    """A chapter as Agent 2 produces it — no image_url yet, since that field
    is filled in later by the image step and shouldn't be something Agent 2
    could hallucinate a value for."""

    title: str
    text: str
    image_prompt: str


class Chapter(BaseModel):
    title: str
    text: str
    image_prompt: str
    image_url: str = ""  # populated by the image generation step, empty until then


class StoryDraft(BaseModel):
    """Output of Agent 2 (Storyteller), before images are attached."""

    topic: str
    age_group: AgeGroup
    chapters: list[ChapterDraft]


class QuizQuestion(BaseModel):
    question: str
    choices: list[str] = Field(min_length=4, max_length=4)
    correct_index: int = Field(ge=0, le=3)


class QuizPayload(BaseModel):
    """Output of Agent 3 (Quiz Master)."""

    quiz: list[QuizQuestion] = Field(min_length=3, max_length=3)


class StoryPayload(BaseModel):
    """Final combined payload sent to the frontend and cached in Redis."""

    topic: str
    age_group: AgeGroup
    chapters: list[Chapter]
    quiz: list[QuizQuestion]
