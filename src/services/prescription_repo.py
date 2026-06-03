"""Accès à la table TEXTES_PRESCRIPTION (un texte par modèle)."""

from __future__ import annotations

from typing import Any

from src.config import get_settings
from src.services.baserow_client import get_client


def _pick(row: dict[str, Any], *keys: str) -> str:
    for k in keys:
        val = row.get(k)
        if val:
            if isinstance(val, dict):
                return str(val.get("value", "")).strip()
            return str(val).strip()
    return ""


def texte_pour_modele(modele: str) -> str:
    if not modele:
        return ""
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_prescription, size=200)
    m = modele.upper()
    for row in rows:
        if _pick(row, "modele", "Modèle").upper() == m:
            return _pick(row, "texte_prescription", "Texte prescription", "texte", "Texte")
    return ""


def lister_prescriptions() -> list[dict[str, Any]]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_prescription, size=200)
    return [
        {
            "id": r.get("id"),
            "modele": _pick(r, "modele", "Modèle"),
            "texte_prescription": _pick(
                r, "texte_prescription", "Texte prescription", "texte", "Texte"
            ),
        }
        for r in rows
    ]


def enregistrer_prescription(modele: str, texte: str) -> dict[str, Any]:
    """Crée ou met à jour le texte de prescription d'un modèle."""
    settings = get_settings()
    client = get_client()
    table = settings.baserow_table_prescription
    rows = client.list_rows(table, size=200)
    m = modele.upper()
    fields = {"modele": modele, "texte_prescription": texte}
    for row in rows:
        if _pick(row, "modele", "Modèle").upper() == m:
            return client.update_row(table, row["id"], fields)
    return client.create_row(table, fields)
