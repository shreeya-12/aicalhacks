import { useState } from "react";
import { TopicForm } from "./components/TopicForm";
import { StoryPanel } from "./components/StoryPanel";
import { ImageFrame } from "./components/ImageFrame";
import { Quiz } from "./components/Quiz";
import { mockPhotosynthesis } from "./data/mockPhotosynthesis";
import { generateStory } from "./api";
import type { AgeGroup, StoryPayload } from "./types";
import "./App.css";

// Assumption: until the live pipeline is wired up, "Use demo data" lets the
// frontend be developed/demoed independently (per Member 2's mock requirement).
function App() {
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
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>StoryStream</h1>
        <TopicForm onGenerate={handleGenerate} isLoading={isLoading} />
        <button className="demo-button" onClick={loadDemo}>
          Use demo data (Photosynthesis)
        </button>
      </header>

      {error && <p className="error">{error}</p>}

      {story && (
        <main className="dashboard">
          <section className="dashboard-left">
            <StoryPanel
              chapters={story.chapters}
              activeIndex={activeChapter}
              onSelectChapter={setActiveChapter}
            />
          </section>
          <section className="dashboard-right">
            <ImageFrame chapter={story.chapters[activeChapter]} />
          </section>
        </main>
      )}

      {story && (
        <footer className="quiz-section">
          <h2>Quiz Time</h2>
          <Quiz questions={story.quiz} />
        </footer>
      )}
    </div>
  );
}

export default App;
