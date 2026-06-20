# StoryStream frontend

Single-page dashboard: topic input + age group selector, split-screen story/image view, and an
interactive quiz below.

## Setup

```
cd frontend
npm install
cp .env.example .env   # only needed if backend isn't on localhost:8000
npm run dev
```

## Layout

- `src/types.ts` - shared shapes (`StoryPayload`, `Chapter`, `QuizQuestion`) matching the backend's `models.py`
- `src/api.ts` - `generateStory()`, calls `POST /api/generate` on the FastAPI backend
- `src/data/mockPhotosynthesis.ts` - hardcoded demo payload, wired to the "Use demo data" button so the UI works without a live backend
- `src/components/TopicForm.tsx` - topic input + age group dropdown
- `src/components/StoryPanel.tsx` - left panel, chapter text + tab navigation
- `src/components/ImageFrame.tsx` - right panel, the active chapter's image
- `src/components/Quiz.tsx` - multiple-choice quiz, buttons turn green/red on click and lock after answering
