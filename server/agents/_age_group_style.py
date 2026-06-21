"""Shared age-group tone/style guidance, used by chapter_planner.py and storyteller.py."""

from models import AgeGroup

AUDIENCE_STYLE = {
    AgeGroup.ELEMENTARY: "a curious 8-year-old. Use simple words, short sentences, and fun analogies.",
    AgeGroup.MIDDLE_SCHOOL: "a middle schooler (12-13 years old). Use clear language, introduce "
    "technical terms with a brief explanation, and keep an engaging, relatable tone.",
    AgeGroup.HIGH_SCHOOL: "a high school student. Use clear, engaging language with accurate terminology.",
    AgeGroup.COLLEGE: "a college student. Use precise, nuanced academic language and don't oversimplify.",
}

IMAGE_PROMPT_STYLE = {
    AgeGroup.ELEMENTARY: "Pixar-style 3D render, bright, friendly, whimsical",
    AgeGroup.MIDDLE_SCHOOL: "vibrant educational illustration, engaging and slightly more detailed than a children's style",
    AgeGroup.HIGH_SCHOOL: "clean educational diagram or realistic illustration, labeled if relevant",
    AgeGroup.COLLEGE: "hyper-realistic, detailed, documentary-style",
}
