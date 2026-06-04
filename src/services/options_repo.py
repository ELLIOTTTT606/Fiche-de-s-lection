"""Accès à la table OPTIONS et ACCESSOIRES."""

from __future__ import annotations

from typing import Any

from src.config import get_settings
from src.models.schemas import Option
from src.services.baserow_client import get_client


def _pick(row: dict[str, Any], *keys: str) -> str:
    for k in keys:
        val = row.get(k)
        if val:
            if isinstance(val, dict):
                return str(val.get("value", "")).strip()
            return str(val).strip()
    return ""


def _to_float(s: str) -> float | None:
    s = (s or "").replace("€", "").replace(",", ".").strip()
    try:
        return float(s) if s else None
    except ValueError:
        return None


def _to_option(row: dict[str, Any]) -> Option:
    return Option(
        code=_pick(row, "code", "Code", "code_option"),
        libelle=_pick(row, "libelle", "Libellé", "libelle_option", "designation", "Désignation"),
        categorie=_pick(row, "categorie", "Catégorie", "famille", "Famille"),
        description=_pick(row, "description", "Description"),
        conseil=_pick(row, "conseil", "Conseil", "conseil_vente"),
        prix=_to_float(_pick(row, "prix", "Prix", "prix_public", "tarif")),
        modele=_pick(row, "modele", "Modèle", "modeles", "Modèles"),
    )


def lister_options(modele: str | None = None) -> list[Option]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_options, size=500)
    options = [_to_option(r) for r in rows]
    if modele:
        m = modele.upper()
        options = [o for o in options if not o.modele or m in o.modele.upper()]
    return options


def creer_option(data: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return get_client().create_row(settings.baserow_table_options, data)


def modifier_option(row_id: int, data: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return get_client().update_row(settings.baserow_table_options, row_id, data)


def supprimer_option(row_id: int) -> None:
    settings = get_settings()
    get_client().delete_row(settings.baserow_table_options, row_id)
