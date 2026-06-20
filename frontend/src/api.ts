import type { GenerateRequest, StoryPayload } from "./types";

// Assumption: backend runs on :8000 in dev; override with VITE_API_BASE_URL for deployed builds.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function generateStory(req: GenerateRequest): Promise<StoryPayload> {
  const res = await fetch(`${API_BASE_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    throw new Error(`Generate request failed: ${res.status} ${res.statusText}`);
  }

  return res.json();
}
