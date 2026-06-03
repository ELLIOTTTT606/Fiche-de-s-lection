"""Catalogue des 13 modèles GALLETTI (Solution Habitat).

Source de vérité côté backend. Le frontend possède une copie dans
`ui/src/lib/machines.ts`. Le catalogue sert à :
  - valider le modèle/taille extrait d'une désignation,
  - normaliser la taille (retirer les zéros de tête),
  - retrouver fluide et medium.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModeleInfo:
    modele: str
    fluide: str
    medium: str
    tailles: tuple[str, ...]


CATALOGUE: dict[str, ModeleInfo] = {
    "PLP": ModeleInfo("PLP", "R290", "air/eau", ("37", "45", "52", "57", "62")),
    "PLN": ModeleInfo("PLN", "R290", "air/eau", ("52", "72", "82", "104", "114", "134", "154")),
    "MLI": ModeleInfo("MLI", "R32", "air/eau", ("06", "08", "10", "12", "16", "18", "26", "30")),
    "PLE": ModeleInfo(
        "PLE", "R454B", "air/eau",
        ("52", "62", "72", "82", "92", "102", "122", "132", "142", "152"),
    ),
    "PLI": ModeleInfo("PLI", "R454B", "air/eau", ("35", "40", "45", "50")),
    "GLE": ModeleInfo("GLE", "R454B", "air/eau", ("658", "748", "818", "900", "942", "1072")),
    "VLS": ModeleInfo(
        "VLS", "R454B", "air/eau",
        ("162", "202", "234", "254", "274", "314", "344", "374", "414", "456", "576"),
    ),
    "VRS": ModeleInfo(
        "VRS", "R410A", "air/eau",
        ("162", "202", "234", "254", "274", "314", "344", "374", "414", "456", "546", "576"),
    ),
    "MPE": ModeleInfo(
        "MPE", "R410A", "air/eau",
        ("04", "05", "08", "09", "10", "13", "14", "15", "18", "21", "24", "27", "28", "30",
         "35", "40", "42", "54", "61", "66", "69", "76"),
    ),
    "MPED": ModeleInfo(
        "MPED", "R410A", "air/eau",
        ("07", "08", "10", "13", "15", "18", "20", "24", "27", "28", "30", "32", "34", "35",
         "40", "45", "54", "61", "66", "69", "76"),
    ),
    "LCC": ModeleInfo(
        "LCC", "R410A", "eau/eau",
        ("52", "62", "72", "82", "92", "102", "112", "132", "142", "162", "182", "204"),
    ),
    "LCX": ModeleInfo(
        "LCX", "R410A", "eau/eau",
        ("92", "102", "122", "124", "142", "144", "162", "164", "174", "194", "214", "244",
         "274", "294", "324", "364"),
    ),
    "EVITECH": ModeleInfo(
        "EVITECH", "R410A", "air/eau",
        ("52", "62", "72", "82", "92", "104", "124", "154", "174", "184"),
    ),
}

# Modèles triés par longueur décroissante : MPED avant MPE, EVITECH avant tout.
MODELES_PAR_LONGUEUR = sorted(CATALOGUE.keys(), key=len, reverse=True)


def normaliser_taille(taille: str, modele: str | None = None) -> str:
    """Retire les zéros de tête (052 -> 52) en respectant le catalogue.

    Si le modèle est connu, on essaie de retrouver une taille valide :
    on teste d'abord la taille telle quelle, puis sans les zéros de tête.
    """
    taille = (taille or "").strip()
    if not taille:
        return ""

    if modele and modele in CATALOGUE:
        valides = CATALOGUE[modele].tailles
        if taille in valides:
            return taille
        sans_zero = taille.lstrip("0") or "0"
        if sans_zero in valides:
            return sans_zero
        # Certains modèles ont des tailles à 2 chiffres avec zéro (06, 08...).
        # On garde alors la forme paddée si elle existe au catalogue.
        return sans_zero

    return taille.lstrip("0") or taille


def info_modele(modele: str) -> ModeleInfo | None:
    return CATALOGUE.get((modele or "").upper())
