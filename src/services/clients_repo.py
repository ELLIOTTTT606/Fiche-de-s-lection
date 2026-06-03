"""Accès à la table CLIENTS (recherche, ajout, modification)."""

from __future__ import annotations

from typing import Any

from src.config import get_settings
from src.models.schemas import Client
from src.services.baserow_client import get_client


def _pick(row: dict[str, Any], *keys: str) -> str:
    for k in keys:
        val = row.get(k)
        if val:
            if isinstance(val, dict):
                return str(val.get("value", "")).strip()
            return str(val).strip()
    return ""


def _to_client(row: dict[str, Any]) -> Client:
    cp = _pick(row, "code_postal", "Code postal", "CP", "code postal")
    dep = _pick(row, "departement", "Département")
    if not dep and len(cp) >= 2:
        dep = cp[:2]
    return Client(
        id=row.get("id"),
        code_tiers=_pick(row, "code_tiers", "Code tiers", "code tiers", "ATC"),
        nom=_pick(row, "nom", "Nom", "raison_sociale", "Raison sociale"),
        code_postal=cp,
        departement=dep,
    )


def rechercher_clients(query: str, limit: int = 20) -> list[Client]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_clients, search=query or None, size=limit)
    return [_to_client(r) for r in rows][:limit]


def lister_clients(limit: int = 200) -> list[Client]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_clients, size=limit)
    return [_to_client(r) for r in rows]


def creer_client(data: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return get_client().create_row(settings.baserow_table_clients, data)


def modifier_client(row_id: int, data: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return get_client().update_row(settings.baserow_table_clients, row_id, data)
