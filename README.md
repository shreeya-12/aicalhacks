# AI Hackathon @ UC Berkeley 2026

## StoryLearn Ai

Turns any topic into an age-appropriate illustrated story (3 chapters for elementary, scaling up
to 8-10 for college) with 2 quiz questions per chapter, via a per-chapter agent pipeline: a
planner splits the topic into chapters, then each chapter gets its own Researcher (Browserbase/
Stagehand) -> Storyteller (Claude) -> Quiz Master (Claude) pass, followed by AI-generated images
(OpenAI `gpt-image-1`).

- [`server/`](server/) - FastAPI backend, agent pipeline, Redis cache (see [server/README.md](server/README.md))
- [`frontend/`](frontend/) - React + Vite app: topic form -> story -> quiz, with a history sidebar (see [frontend/README.md](frontend/README.md))
