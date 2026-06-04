"""Décodage des options depuis la table Baserow DECODAGE_DESIGNATION.

Principe : la commerciale remplit un tableau de correspondances
(position_start, position_end, code_attendu, option_label, categorie, modele).
Le parser compare chaque segment de la chaîne de désignation à ces règles et en
déduit les options. Si GALLETTI change son format, la commerciale modifie la
table — jamais le code.
"""

from __future__ import annotations

from typing import Any

from src.config import get_settings
from src.models.schemas import Option
from src.services.baserow_client import get_client


def _pick(row: dict[str, Any], *keys: str) -> str:
    for k in keys:
        val = row.get(k)
        if val is not None and val != "":
            if isinstance(val, dict):
                return str(val.get("value", "")).strip()
            return str(val).strip()
    return ""


def _to_int(s: str) -> int | None:
    try:
        return int(str(s).strip())
    except (ValueError, TypeError):
        return None


def lister_regles(modele: str | None = None) -> list[dict[str, Any]]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_designation, size=500)
    regles: list[dict[str, Any]] = []
    for row in rows:
        regle = {
            "id": row.get("id"),
            "position_start": _to_int(_pick(row, "position_start", "Position start", "debut")),
            "position_end": _to_int(_pick(row, "position_end", "Position end", "fin")),
            "code_attendu": _pick(row, "code_attendu", "Code attendu", "code"),
            "option_label": _pick(row, "option_label", "Option", "libelle", "Libellé"),
            "categorie": _pick(row, "categorie", "Catégorie"),
            "modele": _pick(row, "modele", "Modèle"),
        }
        regles.append(regle)
    if modele:
        m = modele.upper()
        regles = [r for r in regles if not r["modele"] or r["modele"].upper() == m]
    return regles


def decoder_options(segment_options: str, modele: str | None = None) -> list[Option]:
    """Compare le segment d'options aux règles Baserow et renvoie les options détectées.

    `segment_options` est la portion de désignation après le préfixe
    (ex. ``A000C00020G010I``). On retire les espaces pour indexer proprement.
    """
    if not segment_options:
        return []
    chaine = segment_options.replace(" ", "")

    detectees: list[Option] = []
    vues: set[str] = set()
    for regle in lister_regles(modele):
        start = regle["position_start"]
        end = regle["position_end"]
        code_attendu = regle["code_attendu"]
        if start is None or end is None or not code_attendu:
            continue
        if start < 0 or end > len(chaine) or start >= end:
            continue
        segment = chaine[start:end]
        if segment.upper() == code_attendu.upper():
            label = regle["option_label"] or f"{code_attendu}"
            if label in vues:
                continue
            vues.add(label)
            detectees.append(
                Option(
                    code=code_attendu,
                    libelle=label,
                    categorie=regle["categorie"],
                    modele=regle["modele"],
                    selected=True,
                )
            )
    return detectees


# ── CRUD pour la page Maintenance ──────────────────────────────
def creer_regle(data: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return get_client().create_row(settings.baserow_table_designation, data)


def modifier_regle(row_id: int, data: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return get_client().update_row(settings.baserow_table_designation, row_id, data)


def supprimer_regle(row_id: int) -> None:
    settings = get_settings()
    get_client().delete_row(settings.baserow_table_designation, row_id)
