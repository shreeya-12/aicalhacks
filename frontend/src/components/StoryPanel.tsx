import type { Chapter } from "../types";

interface StoryPanelProps {
  chapters: Chapter[];
  activeIndex: number;
  onSelectChapter: (index: number) => void;
}

export function StoryPanel({ chapters, activeIndex, onSelectChapter }: StoryPanelProps) {
  const active = chapters[activeIndex];

  return (
    <div className="story-panel">
      <div className="chapter-tabs">
        {chapters.map((chapter, i) => (
          <button
            key={chapter.title}
            className={i === activeIndex ? "chapter-tab active" : "chapter-tab"}
            onClick={() => onSelectChapter(i)}
          >
            {i + 1}
          </button>
        ))}
      </div>
      <h2>{active.title}</h2>
      <p>{active.text}</p>
    </div>
  );
}
