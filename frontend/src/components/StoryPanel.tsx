import type { Chapter } from "../types";

const CHAPTER_COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#a855f7"];

interface StoryPanelProps {
  chapters: Chapter[];
  activeIndex: number;
  onSelectChapter: (index: number) => void;
  onComplete: () => void;
}

export function StoryPanel({
  chapters,
  activeIndex,
  onSelectChapter,
  onComplete,
}: StoryPanelProps) {
  const active = chapters[activeIndex];
  const isFirst = activeIndex === 0;
  const isLast = activeIndex === chapters.length - 1;

  function goNext() {
    if (isLast) {
      onComplete();
    } else {
      onSelectChapter(activeIndex + 1);
    }
  }

  function goPrev() {
    if (!isFirst) onSelectChapter(activeIndex - 1);
  }

  return (
    <div className="story-panel">
      <div className="chapter-progress">
        {chapters.map((ch, i) => (
          <button
            key={ch.title}
            className={
              "chapter-dot" +
              (i === activeIndex ? " active" : i < activeIndex ? " visited" : "")
            }
            onClick={() => onSelectChapter(i)}
            aria-label={`Go to chapter ${i + 1}`}
          />
        ))}
        <span className="chapter-counter">
          {activeIndex + 1} / {chapters.length}
        </span>
      </div>

      {/* key forces remount → triggers CSS animation on chapter change */}
      <div className="chapter-content" key={activeIndex}>
        <h2
          className="chapter-title"
          style={{ borderLeftColor: CHAPTER_COLORS[activeIndex % CHAPTER_COLORS.length] }}
        >
          {active.title}
        </h2>
        {active.text
          .split(/\n\s*\n/)
          .map((para) => para.trim())
          .filter(Boolean)
          .map((para, i) => (
            <p className="chapter-text" key={i}>
              {para}
            </p>
          ))}
      </div>

      <div className="chapter-nav">
        <button className="nav-btn" onClick={goPrev} disabled={isFirst}>
          ← Previous
        </button>
        <button className={`nav-btn${isLast ? " primary" : ""}`} onClick={goNext}>
          {isLast ? "Take the Quiz →" : "Next →"}
        </button>
      </div>
    </div>
  );
}
