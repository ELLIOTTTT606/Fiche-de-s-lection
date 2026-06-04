// Catalogue des 13 modèles GALLETTI (Solution Habitat).
// Copie frontend du catalogue backend (src/parser/catalogue.py).

export interface ModeleInfo {
  modele: string;
  fluide: string;
  medium: string; // "air/eau" | "eau/eau"
  tailles: string[];
}

export const MACHINES: ModeleInfo[] = [
  { modele: "PLP", fluide: "R290", medium: "air/eau", tailles: ["37", "45", "52", "57", "62"] },
  { modele: "PLN", fluide: "R290", medium: "air/eau", tailles: ["52", "72", "82", "104", "114", "134", "154"] },
  { modele: "MLI", fluide: "R32", medium: "air/eau", tailles: ["06", "08", "10", "12", "16", "18", "22", "26", "30"] },
  { modele: "PLE", fluide: "R454B", medium: "air/eau", tailles: ["52", "62", "72", "82", "92", "102", "122", "132", "142", "152"] },
  { modele: "PLI", fluide: "R454B", medium: "air/eau", tailles: ["35", "40", "45", "50"] },
  { modele: "GLE", fluide: "R454B", medium: "air/eau", tailles: ["658", "748", "818", "900", "942", "1072"] },
  { modele: "VLS", fluide: "R454B", medium: "air/eau", tailles: ["162", "202", "234", "254", "274", "314", "344", "374", "414", "456", "546", "576"] },
  { modele: "VRS", fluide: "R410A", medium: "air/eau", tailles: ["162", "202", "234", "254", "274", "314", "344", "374", "414", "456", "546", "576"] },
  { modele: "MPE", fluide: "R410A", medium: "air/eau", tailles: ["04", "05", "07", "08", "09", "10", "13", "14", "15", "18", "20", "21", "24", "27", "28", "30", "32", "34", "35", "40", "42", "54", "61", "66", "69", "76"] },
  { modele: "MPED", fluide: "R410A", medium: "air/eau", tailles: ["07", "08", "10", "13", "15", "18", "20", "24", "27", "28", "30", "32", "34", "35", "40", "45", "54", "61", "66", "69", "76"] },
  { modele: "LCC", fluide: "R410A", medium: "eau/eau", tailles: ["52", "62", "72", "82", "92", "102", "112", "132", "142", "162", "182", "204"] },
  { modele: "LCX", fluide: "R410A", medium: "eau/eau", tailles: ["92", "102", "122", "124", "142", "144", "162", "164", "174", "194", "214", "244", "274", "294", "324", "364"] },
  { modele: "EVITECH", fluide: "R410A", medium: "air/eau", tailles: ["52", "62", "72", "82", "92", "104", "124", "154", "174", "184"] },
];

export const MODELES = MACHINES.map((m) => m.modele);

export function infoModele(modele: string): ModeleInfo | undefined {
  return MACHINES.find((m) => m.modele === modele?.toUpperCase());
}

export const TYPES_MACHINE = ["PAC", "GEG"] as const;
export const ACOUSTIQUES = ["Standard", "Silencieux"] as const;
