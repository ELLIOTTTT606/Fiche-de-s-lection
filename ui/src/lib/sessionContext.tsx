import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { fetchLibelles } from "../api/client";

// ── Types partagés entre les étapes du workflow ──
export interface Machine {
  modele: string;
  taille: string;
  type_machine: string;
  acoustique: string;
  fluide: string;
  medium: string;
  designation: string;
}

export interface Performance {
  mode: string;
  puissance_kw: number | null;
  puissance_absorbee_kw: number | null;
  cop: number | null;
  eer: number | null;
  scop: number | null;
  seer: number | null;
  classe_energetique: string;
}

export interface Option {
  code: string;
  libelle: string;
  categorie: string;
  description: string;
  conseil: string;
  prix: number | null;
  modele: string;
  selected: boolean;
}

export interface Contact {
  role: string;
  nom: string;
  email: string;
  telephone: string;
  departement: string;
}

export interface Client {
  id: number | null;
  code_tiers: string;
  nom: string;
  code_postal: string;
  departement: string;
}

export interface SessionState {
  machine: Machine;
  performances: Performance[];
  options: Option[];
  contacts: Contact[];
  texte_prescription: string;
  projet: {
    numero: string;
    nom: string;
    client: Client | null;
    contact_solution: Contact | null;
  };
  plans_images: string[];
  warnings: string[];
}

const emptyMachine: Machine = {
  modele: "",
  taille: "",
  type_machine: "",
  acoustique: "",
  fluide: "",
  medium: "",
  designation: "",
};

const initialState: SessionState = {
  machine: emptyMachine,
  performances: [],
  options: [],
  contacts: [],
  texte_prescription: "",
  projet: { numero: "", nom: "", client: null, contact_solution: null },
  plans_images: [],
  warnings: [],
};

interface Ctx {
  state: SessionState;
  update: (patch: Partial<SessionState>) => void;
  reset: () => void;
  libelles: Record<string, string>;
  t: (cle: string, defaut: string) => string;
}

const SessionContext = createContext<Ctx>({
  state: initialState,
  update: () => {},
  reset: () => {},
  libelles: {},
  t: (_c, d) => d,
});

export function SessionProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<SessionState>(initialState);
  const [libelles, setLibelles] = useState<Record<string, string>>({});

  // Chargement des libellés UI depuis Baserow (sans coder : la commerciale les édite).
  useEffect(() => {
    fetchLibelles()
      .then(setLibelles)
      .catch(() => setLibelles({}));
  }, []);

  const update = (patch: Partial<SessionState>) => setState((s) => ({ ...s, ...patch }));
  const reset = () => setState(initialState);
  const t = (cle: string, defaut: string) => libelles[cle] || defaut;

  return (
    <SessionContext.Provider value={{ state, update, reset, libelles, t }}>
      {children}
    </SessionContext.Provider>
  );
}

export const useSession = () => useContext(SessionContext);
