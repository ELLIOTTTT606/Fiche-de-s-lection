"""Accès à la table LIBELLES_UI — les textes de l'interface, éditables sans coder.

L'application lit ses libellés depuis Baserow au démarrage. Si la table n'est pas
configurée, on renvoie un dictionnaire vide et le frontend utilise ses valeurs par
défaut. La commerciale peut ainsi changer les mots de l'interface depuis la page
Maintenance, sans toucher au code.
"""

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


def lister_libelles() -> list[dict[str, Any]]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_libelles, size=500)
    return [
        {
            "id": r.get("id"),
            "cle": _pick(r, "cle", "Clé", "key"),
            "valeur": _pick(r, "valeur", "Valeur", "value"),
            "page": _pick(r, "page", "Page"),
        }
        for r in rows
    ]


def libelles_dict() -> dict[str, str]:
    """Renvoie {cle: valeur} pour injection facile dans le frontend."""
    return {item["cle"]: item["valeur"] for item in lister_libelles() if item["cle"]}


def enregistrer_libelle(cle: str, valeur: str, page: str = "") -> dict[str, Any]:
    settings = get_settings()
    client = get_client()
    table = settings.baserow_table_libelles
    rows = lister_libelles()
    fields = {"cle": cle, "valeur": valeur, "page": page}
    for row in rows:
        if row["cle"] == cle:
            return client.update_row(table, row["id"], fields)
    return client.create_row(table, fields)


def supprimer_libelle(row_id: int) -> None:
    settings = get_settings()
    get_client().delete_row(settings.baserow_table_libelles, row_id)
