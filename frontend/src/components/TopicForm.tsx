import { useState } from "react";
import type { AgeGroup } from "../types";

const AGE_GROUPS: { value: AgeGroup; label: string }[] = [
  { value: "elementary", label: "Elementary School" },
  { value: "middle_school", label: "Middle School" },
  { value: "high_school", label: "High School" },
  { value: "college", label: "College" },
];

interface TopicFormProps {
  onGenerate: (topic: string, ageGroup: AgeGroup) => void;
  isLoading: boolean;
}

export function TopicForm({ onGenerate, isLoading }: TopicFormProps) {
  const [topic, setTopic] = useState("");
  const [ageGroup, setAgeGroup] = useState<AgeGroup>("elementary");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!topic.trim() || isLoading) return;
    onGenerate(topic.trim(), ageGroup);
  }

  return (
    <form className="topic-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter a topic, e.g. The Roman Empire"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        disabled={isLoading}
        autoFocus
      />
      <div className="select-wrapper">
        <select
          value={ageGroup}
          onChange={(e) => setAgeGroup(e.target.value as AgeGroup)}
          disabled={isLoading}
        >
          {AGE_GROUPS.map((g) => (
            <option key={g.value} value={g.value}>
              {g.label}
            </option>
          ))}
        </select>
        <span className="select-arrow">▾</span>
      </div>
      <button className="generate-btn" type="submit" disabled={isLoading || !topic.trim()}>
        {isLoading ? (
          <span className="generating-row">
            <span className="spinner" />
            Generating your lesson…
          </span>
        ) : (
          "Generate Lesson"
        )}
      </button>
    </form>
  );
}
