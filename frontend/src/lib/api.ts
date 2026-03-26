import type {
  AnalyzeRequest,
  AnalyzeResponse,
  RunAlgorithmRequest,
  RunAlgorithmResponse,
  FeedbackRequest,
  FeedbackItem,
  UserSettings,
  SettingsStatus,
} from "./types";

const BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `Request failed: ${res.status}`);
  }

  return res.json();
}

export async function analyze(data: AnalyzeRequest): Promise<AnalyzeResponse> {
  return request("/analyze", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function runAlgorithm(data: RunAlgorithmRequest): Promise<RunAlgorithmResponse> {
  return request("/run-algorithm", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function submitFeedback(data: FeedbackRequest): Promise<{ status: string; id: string }> {
  return request("/feedback", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getFeedback(limit = 100): Promise<FeedbackItem[]> {
  return request(`/feedback?limit=${limit}`);
}

export async function saveSettings(data: UserSettings): Promise<{ status: string }> {
  return request("/settings", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getSettings(userName: string): Promise<SettingsStatus> {
  return request(`/settings/${encodeURIComponent(userName)}`);
}
