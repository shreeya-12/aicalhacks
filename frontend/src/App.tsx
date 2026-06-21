import { useState, useEffect } from "react";
import { TopicForm } from "./components/TopicForm";
import { StoryPanel } from "./components/StoryPanel";
import { ImageFrame } from "./components/ImageFrame";
import { Quiz } from "./components/Quiz";
import { Sidebar } from "./components/Sidebar";
import { GenerationProgress } from "./components/GenerationProgress";
import { mockPhotosynthesis } from "./data/mockPhotosynthesis";
import { generateStory, fetchHistory } from "./api";
import type { AgeGroup, HistoryItem, StoryPayload } from "./types";
import "./App.css";

type View = "home" | "lesson" | "quiz";

function App() {
  const [view, setView] = useState<View>("home");
  const [story, setStory] = useState<StoryPayload | null>(null);
  const [activeChapter, setActiveChapter] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    fetchHistory().then(setHistory);
  }, []);

  async function handleGenerate(topic: string, ageGroup: AgeGroup) {
    setIsLoading(true);
    setError(null);
    try {
      const payload = await generateStory({ topic, age_group: ageGroup });
      setStory(payload);
      setActiveChapter(0);
      setView("lesson");
      // Refresh history — new entry may have been cached
      fetchHistory().then(setHistory);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate story");
    } finally {
      setIsLoading(false);
    }
  }

  function loadDemo() {
    setStory(mockPhotosynthesis);
    setActiveChapter(0);
    setError(null);
    setView("lesson");
  }

  function goHome() {
    setView("home");
    setStory(null);
    setActiveChapter(0);
    setError(null);
  }

  return (
    <div className="app-shell">
      <Sidebar history={history} onSelect={handleGenerate} isLoading={isLoading} />

      <div className="app-main">
        {view === "home" && (
          <div className="home-view">
            <div className="home-content">
              <div className="home-brand">
                <div className="home-logo">✦</div>
                <h1 className="home-title">Story Learn Ai</h1>
                <p className="home-tagline">
                  Turn any topic into an illustrated story and quiz — powered by AI.
                </p>
              </div>

              <div className="home-card">
                <TopicForm onGenerate={handleGenerate} isLoading={isLoading} />
                {isLoading && <GenerationProgress />}
                {error && <p className="error-msg">{error}</p>}
                <div className="home-divider">
                  <span>or</span>
                </div>
                <button className="demo-btn" onClick={loadDemo}>
                  Use Demo: Photosynthesis
                </button>
              </div>
            </div>
          </div>
        )}

        {view === "lesson" && story && (
          <div className="lesson-view">
            <header className="lesson-header">
              <div className="lesson-header-left">
                <span className="lesson-brand">✦ Story Learn Ai</span>
                <span className="lesson-topic">{story.topic}</span>
              </div>
              <button className="header-btn" onClick={goHome}>
                ← New Lesson
              </button>
            </header>

            <main className="lesson-main">
              <section className="lesson-story">
                <StoryPanel
                  chapters={story.chapters}
                  activeIndex={activeChapter}
                  onSelectChapter={setActiveChapter}
                  onComplete={() => setView("quiz")}
                />
              </section>
              <section className="lesson-image">
                <ImageFrame chapter={story.chapters[activeChapter]} />
              </section>
            </main>
          </div>
        )}

        {view === "quiz" && story && (
          <div className="quiz-view">
            <header className="lesson-header">
              <div className="lesson-header-left">
                <span className="lesson-brand">✦ Story Learn Ai</span>
                <span className="lesson-topic">{story.topic}</span>
              </div>
              <button className="header-btn" onClick={() => setView("lesson")}>
                ← Back to Story
              </button>
            </header>

            <main className="quiz-main">
              <div className="quiz-header">
                <h2 className="quiz-title">Quiz Time</h2>
                <p className="quiz-subtitle">
                  Let's see how much you remember from the story.
                </p>
              </div>
              <Quiz questions={story.quiz} onRestart={goHome} />
            </main>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
