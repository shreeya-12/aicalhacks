# StoryLearn AI frontend

A 3-view app: pick a topic (`home`) -> read the generated chapters (`lesson`) -> take the quiz
(`quiz`), plus a collapsible history sidebar.

## Setup

```
cd frontend
npm install
cp .env.example .env   # only needed if backend isn't on localhost:8000
npm run dev
```

## Layout

- `src/types.ts` - shared shapes (`StoryPayload`, `Chapter`, `QuizQuestion`, `HistoryItem`) matching the backend's `models.py`
- `src/api.ts` - `generateStory()` (`POST /api/generate`) and `fetchHistory()` (`GET /api/history`)
- `src/data/mockPhotosynthesis.ts` - hardcoded demo payload (6 questions, 2/chapter, with explanations) wired to the "Use Demo" button so the UI works without a live backend
- `src/App.tsx` - top-level view state (`home` / `lesson` / `quiz`) and data flow
- `src/components/Sidebar.tsx` - collapsible history list, click to re-run a past topic/age group
- `src/components/TopicForm.tsx` - topic input + age group dropdown (`elementary | middle_school | high_school | college`)
- `src/components/StoryPanel.tsx` - paginated chapter view (prev/next, progress dots), advances to the quiz view after the last chapter
- `src/components/ImageFrame.tsx` - the active chapter's image, with a loading skeleton
- `src/components/Quiz.tsx` - multiple-choice quiz grouped by chapter, shows an explanation on wrong answers, scores the attempt, supports retry/restart
