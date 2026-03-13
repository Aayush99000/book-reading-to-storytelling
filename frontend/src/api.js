const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function generateComic(chapterText, style = "western_comic") {
  const res = await fetch(`${BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chapter_text: chapterText, style }),
  });
  if (!res.ok) throw new Error("Failed to start generation");
  return res.json(); // { job_id, status, progress }
}

export async function pollStatus(jobId) {
  const res = await fetch(`${BASE}/status/${jobId}`);
  if (!res.ok) throw new Error("Failed to fetch status");
  return res.json(); // { job_id, status, progress, result_url, scenes }
}

export function getComicUrl(resultUrl) {
  return `${BASE}${resultUrl}`;
}
