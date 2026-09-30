import type { AnalysisSummary } from "../types";

// Use the browser's current origin by default. Next.js proxies these requests
// to the FastAPI service, which also works when the UI is opened through a
// forwarded Codespaces/remote port.
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

function apiUrl(path: string) {
  return `${API_URL.replace(/\/$/, "")}${path}`;
}

export async function analyzeIncidentFile(file: File): Promise<AnalysisSummary> {
  const form = new FormData();
  form.append("file", file);
  const response = await fetch(apiUrl("/api/incidents/analyze"), {
    method: "POST",
    body: form,
  });
  const payload = (await response.json().catch(() => ({}))) as {
    detail?: string;
  } & Partial<AnalysisSummary>;
  if (!response.ok) {
    throw new Error(payload.detail ?? "The incident file could not be analyzed.");
  }
  return payload as AnalysisSummary;
}

export function resultsExportUrl() {
  return apiUrl("/api/incidents/results/export");
}
