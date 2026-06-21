"""Shared age-group tone/style guidance, used by chapter_planner.py and storyteller.py."""

from models import AgeGroup

AUDIENCE_STYLE = {
    AgeGroup.ELEMENTARY: "a curious 8-year-old. Use simple words, short sentences, and fun analogies.",
    AgeGroup.HIGH_SCHOOL: "a high school student. Use clear, engaging language with accurate terminology.",
    AgeGroup.ADULT: "an informed adult. Use precise, nuanced language and don't oversimplify.",
}

IMAGE_PROMPT_STYLE = {
    AgeGroup.ELEMENTARY: "Pixar-style 3D render, bright, friendly, whimsical",
    AgeGroup.HIGH_SCHOOL: "clean educational diagram or realistic illustration, labeled if relevant",
    AgeGroup.ADULT: "hyper-realistic, detailed, documentary-style",
}
