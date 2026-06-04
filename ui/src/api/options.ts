import { api } from "./client";
import type { Option } from "../lib/sessionContext";

export async function getOptions(modele: string): Promise<Option[]> {
  return api<Option[]>(`/api/options?modele=${encodeURIComponent(modele)}`);
}

export async function getPrescription(modele: string): Promise<string> {
  const r = await api<{ texte_prescription: string }>(
    `/api/prescription?modele=${encodeURIComponent(modele)}`,
  );
  return r.texte_prescription;
}
