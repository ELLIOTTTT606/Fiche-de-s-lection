import { api } from "./client";
import type { Client, Contact } from "../lib/sessionContext";

export async function rechercherClients(q: string): Promise<Client[]> {
  return api<Client[]>(`/api/clients?q=${encodeURIComponent(q)}`);
}

export interface ContactsResponse {
  force_de_vente: Contact[];
  solution: Contact[];
}

export async function getContacts(departement: string): Promise<ContactsResponse> {
  return api<ContactsResponse>(`/api/contacts?departement=${encodeURIComponent(departement)}`);
}
