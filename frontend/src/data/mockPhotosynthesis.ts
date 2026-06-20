import type { StoryPayload } from "../types";

// Hardcoded dummy payload matching the backend's StoryPayload contract.
// Lets the frontend be built/demoed before the live agent pipeline works.
export const mockPhotosynthesis: StoryPayload = {
  topic: "Photosynthesis",
  age_group: "elementary",
  chapters: [
    {
      title: "Chapter 1: The Hungry Leaf",
      text: "Every leaf is like a tiny kitchen! Leaves use sunlight, water, and air to cook up their own food. This magic trick is called photosynthesis.",
      image_prompt: "A Pixar-style 3D render of a cheerful talking leaf wearing a chef hat, cooking sunlight in a tiny kitchen, bright and colorful",
      image_url: "https://placehold.co/512x512?text=Chapter+1",
    },
    {
      title: "Chapter 2: Sunlight Power",
      text: "Sunlight beams down and the leaf catches it with a special green color called chlorophyll. The leaf turns sunlight, water, and air into sugar and oxygen!",
      image_prompt: "A Pixar-style 3D render of glowing sunbeams being caught by a smiling green leaf, sparkly and magical",
      image_url: "https://placehold.co/512x512?text=Chapter+2",
    },
    {
      title: "Chapter 3: Sharing the Air",
      text: "The oxygen the leaf makes floats into the air for us to breathe. Plants and people are best friends, helping each other every single day.",
      image_prompt: "A Pixar-style 3D render of a happy plant releasing sparkly oxygen bubbles next to a smiling child breathing fresh air",
      image_url: "https://placehold.co/512x512?text=Chapter+3",
    },
  ],
  quiz: [
    {
      question: "What does a leaf use to make its own food?",
      choices: ["Sunlight, water, and air", "Sand and rocks", "Plastic and metal", "Ice cream"],
      correct_index: 0,
    },
    {
      question: "What is the green color in leaves called?",
      choices: ["Melanin", "Chlorophyll", "Keratin", "Hemoglobin"],
      correct_index: 1,
    },
    {
      question: "What gas do plants release that we breathe?",
      choices: ["Carbon dioxide", "Nitrogen", "Oxygen", "Helium"],
      correct_index: 2,
    },
  ],
};
