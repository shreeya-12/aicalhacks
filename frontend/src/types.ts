export type AgeGroup = "elementary" | "middle_school" | "high_school" | "college";

export interface Chapter {
  title: string;
  text: string;
  image_prompt: string;
  image_url: string;
}

export interface QuizQuestion {
  question: string;
  choices: string[];
  correct_index: number;
  explanation?: string;
  chapter_index?: number;
}

export interface StoryPayload {
  topic: string;
  age_group: AgeGroup;
  chapters: Chapter[];
  quiz: QuizQuestion[];
}

export interface GenerateRequest {
  topic: string;
  age_group: AgeGroup;
}
