"""Extraction des performances (froid/chaud, COP, EER, SCOP, SEER, classes).

GALLETTI présente ces données dans des tableaux dont la mise en forme varie.
On adopte une approche tolérante par expressions régulières sur le texte
aplati : on cherche des libellés connus suivis d'une valeur numérique. Si rien
n'est trouvé, on renvoie deux lignes vides (Froid / Chaud) que le commercial
pourra compléter manuellement à l'écran.
"""

from __future__ import annotations

import re

from src.models.schemas import Performance


def _num(texte: str) -> float | None:
    m = re.search(r"-?\d+(?:[.,]\d+)?", texte)
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", "."))
    except ValueError:
        return None


def _chercher(texte: str, *patterns: str) -> str | None:
    for p in patterns:
        m = re.search(p, texte, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def extraire_performances_depuis_texte(texte: str) -> list[Performance]:
    """Renvoie une liste [Froid, Chaud] remplie au mieux depuis le texte."""
    froid = Performance(mode="Froid")
    chaud = Performance(mode="Chaud")

    # Indicateurs saisonniers : EER/SEER pour le froid, COP/SCOP pour le chaud.
    if (v := _chercher(texte, r"\bEER\b[^\d\-]{0,12}(-?\d+(?:[.,]\d+)?)")):
        froid.eer = _num(v)
    if (v := _chercher(texte, r"\bSEER\b[^\d\-]{0,12}(-?\d+(?:[.,]\d+)?)")):
        froid.seer = _num(v)
    if (v := _chercher(texte, r"\bCOP\b[^\d\-]{0,12}(-?\d+(?:[.,]\d+)?)")):
        chaud.cop = _num(v)
    if (v := _chercher(texte, r"\bSCOP\b[^\d\-]{0,12}(-?\d+(?:[.,]\d+)?)")):
        chaud.scop = _num(v)

    # Classes énergétiques (A+++ ... G), repérées proches des libellés saisonniers.
    classes = re.findall(r"\b([A-G]\+{0,3})\b", texte)
    if classes:
        froid.classe_energetique = classes[0]
        if len(classes) > 1:
            chaud.classe_energetique = classes[1]

    return [froid, chaud]
