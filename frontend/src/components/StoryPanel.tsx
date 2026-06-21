import katex from "katex";
import type { Chapter, KeyTerm } from "../types";

const CHAPTER_COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#a855f7"];

function renderMath(tex: string, display: boolean, key: number) {
  const html = katex.renderToString(tex, { throwOnError: false, displayMode: display });
  return <span key={key} dangerouslySetInnerHTML={{ __html: html }} />;
}

// Render markdown emphasis (**bold** / *italic*) Claude emits, so it shows as
// highlighted/emphasized text instead of literal asterisks. Bolded terms with
// a matching definition get a hover tooltip.
function renderEmphasis(text: string, defs: Map<string, string>, offset: number) {
  return text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g).map((part, i) => {
    const key = offset + i;
    if (part.startsWith("**") && part.endsWith("**")) {
      const term = part.slice(2, -2);
      const def = defs.get(term.trim().toLowerCase());
      if (def) {
        return (
          <strong key={key} className="term" tabIndex={0}>
            {term}
            <span className="term-tip" role="tooltip">
              {def}
            </span>
          </strong>
        );
      }
      return <strong key={key}>{term}</strong>;
    }
    if (part.startsWith("*") && part.endsWith("*")) {
      return <em key={key}>{part.slice(1, -1)}</em>;
    }
    return part;
  });
}

// Split out LaTeX math ($$display$$ / $inline$) and render it with KaTeX;
// run emphasis/tooltip rendering on the remaining text.
function renderInline(text: string, defs: Map<string, string> = new Map()) {
  return text.split(/(\$\$[^$]+\$\$|\$[^$]+\$)/g).flatMap((part, i) => {
    if (part.startsWith("$$") && part.endsWith("$$")) {
      return [renderMath(part.slice(2, -2), true, i * 1000)];
    }
    if (part.startsWith("$") && part.endsWith("$") && part.length > 2) {
      return [renderMath(part.slice(1, -1), false, i * 1000)];
    }
    return renderEmphasis(part, defs, i * 1000);
  });
}

function buildDefs(keyTerms?: KeyTerm[]): Map<string, string> {
  const map = new Map<string, string>();
  for (const kt of keyTerms ?? []) {
    map.set(kt.term.trim().toLowerCase(), kt.definition);
  }
  return map;
}

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
  const defs = buildDefs(active.key_terms);

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
              {renderInline(para, defs)}
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
