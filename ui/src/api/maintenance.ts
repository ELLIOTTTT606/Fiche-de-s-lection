// API de la page Maintenance. Le mot de passe est envoyé dans un header.
const BASE = import.meta.env.VITE_API_URL || "";

let motDePasse = "";
export function setMotDePasse(mdp: string) {
  motDePasse = mdp;
  sessionStorage.setItem("invenio-maint", mdp);
}
export function getMotDePasse(): string {
  if (!motDePasse) motDePasse = sessionStorage.getItem("invenio-maint") || "";
  return motDePasse;
}

async function mreq<T>(path: string, options: RequestInit = {}): Promise<T> {
  const resp = await fetch(`${BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      "X-Maintenance-Password": getMotDePasse(),
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!resp.ok) {
    const j = await resp.json().catch(() => ({}));
    throw new Error(j.detail || `Erreur ${resp.status}`);
  }
  // 204 ou réponses sans corps
  const txt = await resp.text();
  return (txt ? JSON.parse(txt) : {}) as T;
}

export async function login(password: string): Promise<boolean> {
  const resp = await fetch(`${BASE}/api/maintenance/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
  if (resp.ok) {
    setMotDePasse(password);
    return true;
  }
  return false;
}

// ── Contacts ──
export const getContactsMaint = (dep = "") =>
  mreq<{ force_de_vente: any[]; solution: any[] }>(`/api/maintenance/contacts?departement=${dep}`);

// ── Options ──
export const getOptionsMaint = (modele = "") =>
  mreq<any[]>(`/api/maintenance/options?modele=${encodeURIComponent(modele)}`);
export const createOption = (data: any) =>
  mreq(`/api/maintenance/options`, { method: "POST", body: JSON.stringify(data) });
export const updateOption = (id: number, data: any) =>
  mreq(`/api/maintenance/options/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteOption = (id: number) =>
  mreq(`/api/maintenance/options/${id}`, { method: "DELETE" });

// ── Prescriptions ──
export const getPrescriptions = () => mreq<any[]>(`/api/maintenance/prescriptions`);
export const savePrescription = (modele: string, texte: string) =>
  mreq(`/api/maintenance/prescriptions`, {
    method: "POST",
    body: JSON.stringify({ modele, texte_prescription: texte }),
  });

// ── Décodage désignation ──
export const getDesignation = (modele = "") =>
  mreq<any[]>(`/api/maintenance/designation?modele=${encodeURIComponent(modele)}`);
export const createDesignation = (data: any) =>
  mreq(`/api/maintenance/designation`, { method: "POST", body: JSON.stringify(data) });
export const updateDesignation = (id: number, data: any) =>
  mreq(`/api/maintenance/designation/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteDesignation = (id: number) =>
  mreq(`/api/maintenance/designation/${id}`, { method: "DELETE" });

// ── Clients ──
export const getClientsMaint = (q = "") =>
  mreq<any[]>(`/api/maintenance/clients?q=${encodeURIComponent(q)}`);
export const createClient = (data: any) =>
  mreq(`/api/maintenance/clients`, { method: "POST", body: JSON.stringify(data) });
export const updateClient = (id: number, data: any) =>
  mreq(`/api/maintenance/clients/${id}`, { method: "PUT", body: JSON.stringify(data) });

// ── Libellés UI ──
export const getLibellesMaint = () => mreq<any[]>(`/api/maintenance/libelles`);
export const saveLibelle = (cle: string, valeur: string, page = "") =>
  mreq(`/api/maintenance/libelles`, {
    method: "POST",
    body: JSON.stringify({ cle, valeur, page }),
  });
export const deleteLibelle = (id: number) =>
  mreq(`/api/maintenance/libelles/${id}`, { method: "DELETE" });
