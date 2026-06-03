"""Accès aux contacts commerciaux (Force de Vente + Solution).

Les noms de champs Baserow réels peuvent varier. On lit de façon tolérante en
testant plusieurs clés possibles, pour que la commerciale n'ait pas à renommer
ses colonnes.
"""

from __future__ import annotations

from typing import Any

from src.config import get_settings
from src.models.schemas import Contact
from src.services.baserow_client import get_client


def _pick(row: dict[str, Any], *keys: str) -> str:
    for k in keys:
        val = row.get(k)
        if val:
            if isinstance(val, dict):  # select Baserow -> {"value": ...}
                return str(val.get("value", "")).strip()
            if isinstance(val, list) and val:
                first = val[0]
                return str(first.get("value", first) if isinstance(first, dict) else first)
            return str(val).strip()
    return ""


def _normaliser_departement(cp_ou_dep: str) -> str:
    """Renvoie un numéro de département à 2 (ou 3) chiffres."""
    s = (cp_ou_dep or "").strip()
    if not s:
        return ""
    if len(s) >= 4 and s.isdigit():  # code postal -> département
        return s[:2]
    return s.zfill(2) if s.isdigit() and len(s) == 1 else s


def contacts_force_de_vente(departement: str) -> list[Contact]:
    settings = get_settings()
    client = get_client()
    dep = _normaliser_departement(departement)
    rows = client.list_rows(settings.baserow_table_contacts_fv, search=dep or None)

    contacts: list[Contact] = []
    for row in rows:
        row_dep = _normaliser_departement(
            _pick(row, "departement", "Département", "Departement", "dept", "code_postal")
        )
        if dep and row_dep and row_dep != dep:
            continue
        # Une ligne peut contenir un TCI et/ou un TCS.
        tci_nom = _pick(row, "TCI", "TCI nom", "tci_nom", "nom_tci")
        if tci_nom:
            contacts.append(
                Contact(
                    role="TCI",
                    nom=tci_nom,
                    email=_pick(row, "TCI email", "tci_email", "email_tci"),
                    telephone=_pick(row, "TCI tel", "tci_tel", "tel_tci", "TCI téléphone"),
                    departement=row_dep,
                )
            )
        tcs_nom = _pick(row, "TCS", "TCS nom", "tcs_nom", "nom_tcs")
        if tcs_nom:
            contacts.append(
                Contact(
                    role="TCS",
                    nom=tcs_nom,
                    email=_pick(row, "TCS email", "tcs_email", "email_tcs"),
                    telephone=_pick(row, "TCS tel", "tcs_tel", "tel_tcs", "TCS téléphone"),
                    departement=row_dep,
                )
            )
    return contacts


def contacts_solution() -> list[Contact]:
    settings = get_settings()
    client = get_client()
    rows = client.list_rows(settings.baserow_table_contacts_solution)
    contacts: list[Contact] = []
    for row in rows:
        nom = _pick(row, "nom", "Nom", "contact", "Contact")
        if not nom:
            continue
        contacts.append(
            Contact(
                role="Solution",
                nom=nom,
                email=_pick(row, "email", "Email", "mail"),
                telephone=_pick(row, "telephone", "Téléphone", "tel", "Tel"),
                departement=_pick(row, "departement", "Département", "zone"),
            )
        )
    return contacts
