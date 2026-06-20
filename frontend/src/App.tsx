import { useState } from "react";
import { TopicForm } from "./components/TopicForm";
import { StoryPanel } from "./components/StoryPanel";
import { ImageFrame } from "./components/ImageFrame";
import { Quiz } from "./components/Quiz";
import { mockPhotosynthesis } from "./data/mockPhotosynthesis";
import { generateStory } from "./api";
import type { AgeGroup, StoryPayload } from "./types";
import "./App.css";

type View = "home" | "lesson" | "quiz";

function App() {
  const [view, setView] = useState<View>("home");
  const [story, setStory] = useState<StoryPayload | null>(null);
  const [activeChapter, setActiveChapter] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate(topic: string, ageGroup: AgeGroup) {
    setIsLoading(true);
    setError(null);
    try {
      const payload = await generateStory({ topic, age_group: ageGroup });
      setStory(payload);
      setActiveChapter(0);
      setView("lesson");
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

  if (view === "home") {
    return (
      <div className="home-view">
        <div className="home-content">
          <div className="home-brand">
            <div className="home-logo">✦</div>
            <h1 className="home-title">StoryStream</h1>
            <p className="home-tagline">
              Turn any topic into an illustrated story and quiz — powered by AI.
            </p>
          </div>

          <div className="home-card">
            <TopicForm onGenerate={handleGenerate} isLoading={isLoading} />
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
    );
  }

  if (view === "lesson" && story) {
    return (
      <div className="lesson-view">
        <header className="lesson-header">
          <div className="lesson-header-left">
            <span className="lesson-brand">✦ StoryStream</span>
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
    );
  }

  if (view === "quiz" && story) {
    return (
      <div className="quiz-view">
        <header className="lesson-header">
          <div className="lesson-header-left">
            <span className="lesson-brand">✦ StoryStream</span>
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
    );
  }

  return null;
}

export default App;
