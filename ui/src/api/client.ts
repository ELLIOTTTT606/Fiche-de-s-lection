// Client HTTP central. En production, VITE_API_URL est vide (même origine).
const BASE = import.meta.env.VITE_API_URL || "";

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const resp = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!resp.ok) {
    let detail = `Erreur ${resp.status}`;
    try {
      const j = await resp.json();
      detail = j.detail || detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return resp.json() as Promise<T>;
}

export async function fetchLibelles(): Promise<Record<string, string>> {
  return api<Record<string, string>>("/api/libelles");
}

export interface ParseResponse {
  machine: any;
  performances: any[];
  options: any[];
  options_detectees: any[];
  raw_designation: string;
  plans_count: number;
  warnings: string[];
}

export async function parseFichier(file: File): Promise<ParseResponse> {
  const form = new FormData();
  form.append("file", file);
  const resp = await fetch(`${BASE}/api/parse`, { method: "POST", body: form });
  if (!resp.ok) {
    const j = await resp.json().catch(() => ({}));
    throw new Error(j.detail || `Erreur ${resp.status}`);
  }
  return resp.json();
}

export async function genererPdf(payload: unknown): Promise<Blob> {
  const resp = await fetch(`${BASE}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!resp.ok) {
    const j = await resp.json().catch(() => ({}));
    throw new Error(j.detail || `Erreur ${resp.status}`);
  }
  return resp.blob();
}
