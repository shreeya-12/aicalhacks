import { useState } from "react";
import type { QuizQuestion } from "../types";

interface QuizProps {
  questions: QuizQuestion[];
  onRestart: () => void;
}

interface QuestionGroup {
  chapterIndex: number | null;
  items: { question: QuizQuestion; globalIndex: number }[];
}

const Q_COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#a855f7", "#ec4899", "#14b8a6"];

function groupByChapter(questions: QuizQuestion[]): QuestionGroup[] {
  const groups: QuestionGroup[] = [];
  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    const ci = q.chapter_index ?? null;
    const last = groups[groups.length - 1];
    if (!last || last.chapterIndex !== ci) {
      groups.push({ chapterIndex: ci, items: [{ question: q, globalIndex: i }] });
    } else {
      last.items.push({ question: q, globalIndex: i });
    }
  }
  return groups;
}

function scoreEmoji(score: number, total: number): string {
  const pct = score / total;
  if (pct === 1) return "🏆";
  if (pct >= 0.75) return "🎉";
  if (pct >= 0.5) return "👍";
  return "📚";
}

function scoreMessage(score: number, total: number): string {
  const pct = score / total;
  if (pct === 1) return "Perfect score! You nailed it.";
  if (pct >= 0.75) return "Great job! Almost there.";
  if (pct >= 0.5) return "Good effort — keep going!";
  return "Keep learning — you'll get it next time!";
}

export function Quiz({ questions, onRestart }: QuizProps) {
  const [selections, setSelections] = useState<Record<number, number>>({});

  function selectChoice(qIndex: number, cIndex: number) {
    if (selections[qIndex] !== undefined) return;
    setSelections((prev) => ({ ...prev, [qIndex]: cIndex }));
  }

  function practiceAgain() {
    setSelections({});
  }

  const allAnswered = Object.keys(selections).length === questions.length;
  const score = questions.filter((q, i) => selections[i] === q.correct_index).length;
  const groups = groupByChapter(questions);
  const hasChapterGroups = groups.some((g) => g.chapterIndex !== null);

  return (
    <div>
      <div className="quiz-questions">
        {groups.map((group, groupIdx) => (
          <div className="quiz-chapter-group" key={groupIdx}>
            {hasChapterGroups && group.chapterIndex !== null && (
              <div className="quiz-chapter-heading">
                <span
                  className="quiz-chapter-dot"
                  style={{ background: Q_COLORS[group.chapterIndex % Q_COLORS.length] }}
                />
                Chapter {group.chapterIndex + 1}
              </div>
            )}

            {group.items.map(({ question: q, globalIndex: qIndex }) => {
              const selected = selections[qIndex];
              const isWrong = selected !== undefined && selected !== q.correct_index;
              const color = Q_COLORS[qIndex % Q_COLORS.length];

              return (
                <div className="quiz-question" key={q.question}>
                  <span
                    className="quiz-question-label"
                    style={{ background: color + "18", color, borderColor: color + "40" }}
                  >
                    Question {qIndex + 1}
                  </span>
                  <p className="quiz-question-text">{q.question}</p>
                  <div className="quiz-choices">
                    {q.choices.map((choice, cIndex) => {
                      let cls = "quiz-choice";
                      if (selected !== undefined) {
                        if (cIndex === q.correct_index) cls += " correct";
                        else if (cIndex === selected) cls += " incorrect";
                      }
                      return (
                        <button
                          key={choice}
                          className={cls}
                          onClick={() => selectChoice(qIndex, cIndex)}
                          disabled={selected !== undefined}
                        >
                          {selected !== undefined && cIndex === q.correct_index && (
                            <span className="choice-icon">✓</span>
                          )}
                          {selected !== undefined && cIndex === selected && cIndex !== q.correct_index && (
                            <span className="choice-icon">✗</span>
                          )}
                          {choice}
                        </button>
                      );
                    })}
                  </div>

                  {isWrong && (q.explanation || q.chapter_index !== undefined) && (
                    <div className="quiz-hint">
                      <span className="quiz-hint-icon">📖</span>
                      <div className="quiz-hint-body">
                        {q.chapter_index !== null && q.chapter_index !== undefined && (
                          <span className="quiz-hint-chapter">
                            Review Chapter {q.chapter_index + 1}
                          </span>
                        )}
                        {q.explanation && (
                          <p className="quiz-hint-text">{q.explanation}</p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {allAnswered && (
        <div className="quiz-score">
          <span className="quiz-score-emoji">{scoreEmoji(score, questions.length)}</span>
          <p className="quiz-score-text">{scoreMessage(score, questions.length)}</p>
          <p className="quiz-score-fraction">
            You got <strong>{score}</strong> out of <strong>{questions.length}</strong> correct.
          </p>
          <div className="quiz-score-actions">
            <button className="quiz-practice-btn" onClick={practiceAgain}>
              ↺ Practice Again
            </button>
            <button className="quiz-restart-btn" onClick={onRestart}>
              New Lesson
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
