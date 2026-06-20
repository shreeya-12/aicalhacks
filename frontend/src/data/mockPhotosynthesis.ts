import type { StoryPayload } from "../types";

export const mockPhotosynthesis: StoryPayload = {
  topic: "Photosynthesis",
  age_group: "elementary",
  chapters: [
    {
      title: "Chapter 1: The Hungry Leaf",
      text: "Every leaf is like a tiny kitchen! Leaves use sunlight, water, and air to cook up their own food. This magic trick is called photosynthesis. Plants figured out how to eat sunlight long before humans even existed, making them the original solar-powered chefs of planet Earth.",
      image_prompt: "A Pixar-style 3D render of a cheerful talking leaf wearing a chef hat, cooking sunlight in a tiny kitchen, bright and colorful",
      image_url: "https://placehold.co/600x400/e9d5ff/7c3aed?text=Chapter+1%3A+The+Hungry+Leaf",
    },
    {
      title: "Chapter 2: Sunlight Power",
      text: "Sunlight beams down and the leaf catches it with a special green color called chlorophyll. This incredible pigment acts like a tiny solar panel, soaking up energy from the sun. The leaf uses that energy to turn water and carbon dioxide into sugar — its very own homemade fuel!",
      image_prompt: "A Pixar-style 3D render of glowing sunbeams being caught by a smiling green leaf, sparkly and magical",
      image_url: "https://placehold.co/600x400/dbeafe/1d4ed8?text=Chapter+2%3A+Sunlight+Power",
    },
    {
      title: "Chapter 3: Sharing the Air",
      text: "The oxygen the leaf makes floats into the air for us to breathe. Plants and people are best friends, helping each other every single day. We breathe in oxygen and breathe out carbon dioxide — exactly what plants need. It's the world's most perfect partnership.",
      image_prompt: "A Pixar-style 3D render of a happy plant releasing sparkly oxygen bubbles next to a smiling child breathing fresh air",
      image_url: "https://placehold.co/600x400/d1fae5/065f46?text=Chapter+3%3A+Sharing+the+Air",
    },
    {
      title: "Chapter 4: The Cycle Continues",
      text: "Photosynthesis never stops — day after day, leaves keep working to feed the plant and clean the air. Thanks to photosynthesis, nearly all life on Earth has food and oxygen. From the tallest rainforest tree to the tiniest blade of grass, plants are quietly powering life on our whole planet.",
      image_prompt: "A beautiful illustration of a lush green forest with sunbeams streaming through the canopy, showing the cycle of life",
      image_url: "https://placehold.co/600x400/fef3c7/92400e?text=Chapter+4%3A+The+Cycle+Continues",
    },
  ],
  quiz: [
    {
      question: "What does a leaf use to make its own food?",
      choices: ["Sunlight, water, and air", "Sand and rocks", "Plastic and metal", "Ice cream"],
      correct_index: 0,
      chapter_index: 0,
      explanation: "Chapter 1 explains that leaves are like tiny kitchens that use sunlight, water, and air — not rocks or other materials — to cook up their food through photosynthesis.",
    },
    {
      question: "What is the green pigment in leaves that captures sunlight?",
      choices: ["Melanin", "Chlorophyll", "Keratin", "Hemoglobin"],
      correct_index: 1,
      chapter_index: 1,
      explanation: "Chapter 2 describes chlorophyll as the special green pigment that acts like a solar panel, absorbing sunlight so the leaf can turn it into energy.",
    },
    {
      question: "What gas do plants release that we breathe?",
      choices: ["Carbon dioxide", "Nitrogen", "Oxygen", "Helium"],
      correct_index: 2,
      chapter_index: 2,
      explanation: "Chapter 3 explains that leaves release oxygen as a byproduct of photosynthesis — the same oxygen that floats into the air for us to breathe.",
    },
    {
      question: "What gas do humans breathe out that plants need for photosynthesis?",
      choices: ["Oxygen", "Nitrogen", "Hydrogen", "Carbon dioxide"],
      correct_index: 3,
      chapter_index: 2,
      explanation: "Chapter 3 describes the perfect partnership: we breathe in oxygen and breathe out carbon dioxide, which is exactly the raw material plants need to photosynthesize.",
    },
  ],
};
