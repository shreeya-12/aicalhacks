import { useState } from "react";
import type { AgeGroup } from "../types";

interface TopicFormProps {
  onGenerate: (topic: string, ageGroup: AgeGroup) => void;
  isLoading: boolean;
}

export function TopicForm({ onGenerate, isLoading }: TopicFormProps) {
  const [topic, setTopic] = useState("");
  const [ageGroup, setAgeGroup] = useState<AgeGroup>("elementary");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!topic.trim()) return;
    onGenerate(topic.trim(), ageGroup);
  }

  return (
    <form className="topic-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter a complex topic (e.g. The Roman Empire)"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />
      <select value={ageGroup} onChange={(e) => setAgeGroup(e.target.value as AgeGroup)}>
        <option value="elementary">Elementary</option>
        <option value="high_school">High School</option>
        <option value="adult">Adult</option>
      </select>
      <button type="submit" disabled={isLoading}>
        {isLoading ? "Generating..." : "Generate"}
      </button>
    </form>
  );
}
