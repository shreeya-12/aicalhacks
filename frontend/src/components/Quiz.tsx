import { useState } from "react";
import type { QuizQuestion } from "../types";

interface QuizProps {
  questions: QuizQuestion[];
}

export function Quiz({ questions }: QuizProps) {
  // Tracks the selected choice index per question so each question's
  // button styling is independent and persists once answered.
  const [selections, setSelections] = useState<Record<number, number>>({});

  function selectChoice(questionIndex: number, choiceIndex: number) {
    if (selections[questionIndex] !== undefined) return; // lock after first answer
    setSelections((prev) => ({ ...prev, [questionIndex]: choiceIndex }));
  }

  return (
    <div className="quiz">
      {questions.map((q, qIndex) => {
        const selected = selections[qIndex];
        return (
          <div className="quiz-question" key={q.question}>
            <p className="quiz-question-text">{q.question}</p>
            <div className="quiz-choices">
              {q.choices.map((choice, cIndex) => {
                let className = "quiz-choice";
                if (selected !== undefined) {
                  if (cIndex === q.correct_index) {
                    className += " correct";
                  } else if (cIndex === selected) {
                    className += " incorrect";
                  }
                }
                return (
                  <button
                    key={choice}
                    className={className}
                    onClick={() => selectChoice(qIndex, cIndex)}
                    disabled={selected !== undefined}
                  >
                    {choice}
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}
