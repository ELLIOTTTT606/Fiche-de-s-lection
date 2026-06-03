"""Routes de la page Maintenance.

Toutes ces routes écrivent dans Baserow. Elles sont protégées par un mot de passe
simple (header ``X-Maintenance-Password``) comparé à MAINTENANCE_PASSWORD.
Aucun jargon technique n'est exposé : le frontend traduit ces appels en
formulaires et tableaux pour la commerciale.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Header, HTTPException

from src.config import get_settings
from src.services import (
    clients_repo,
    contacts_repo,
    designation_repo,
    libelles_repo,
    options_repo,
    prescription_repo,
)
from src.services.baserow_client import BaserowError

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


def _verifier_mdp(mdp: str | None) -> None:
    settings = get_settings()
    if not mdp or mdp != settings.maintenance_password:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect.")


def _guard(x_maintenance_password: str | None) -> None:
    _verifier_mdp(x_maintenance_password)


@router.post("/login")
def login(payload: dict[str, str]) -> dict[str, bool]:
    """Vérifie le mot de passe (le frontend l'envoie au déverrouillage)."""
    _verifier_mdp(payload.get("password"))
    return {"ok": True}


def _safe(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except BaserowError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# ── Onglet 1 — Contacts ────────────────────────────────────────
@router.get("/contacts")
def get_contacts(
    departement: str = "", x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    fv = _safe(contacts_repo.contacts_force_de_vente, departement)
    sol = _safe(contacts_repo.contacts_solution)
    return {"force_de_vente": [c.model_dump() for c in fv], "solution": [c.model_dump() for c in sol]}


# ── Onglet 2 — Options ─────────────────────────────────────────
@router.get("/options")
def get_options(
    modele: str = "", x_maintenance_password: str | None = Header(default=None)
) -> list[dict[str, Any]]:
    _guard(x_maintenance_password)
    return [o.model_dump() for o in _safe(options_repo.lister_options, modele or None)]


@router.post("/options")
def post_option(
    data: dict[str, Any], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(options_repo.creer_option, data)


@router.put("/options/{row_id}")
def put_option(
    row_id: int, data: dict[str, Any], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(options_repo.modifier_option, row_id, data)


@router.delete("/options/{row_id}")
def delete_option(
    row_id: int, x_maintenance_password: str | None = Header(default=None)
) -> dict[str, bool]:
    _guard(x_maintenance_password)
    _safe(options_repo.supprimer_option, row_id)
    return {"ok": True}


# ── Onglet 3 — Textes de prescription ──────────────────────────
@router.get("/prescriptions")
def get_prescriptions(x_maintenance_password: str | None = Header(default=None)) -> list[dict[str, Any]]:
    _guard(x_maintenance_password)
    return _safe(prescription_repo.lister_prescriptions)


@router.post("/prescriptions")
def post_prescription(
    data: dict[str, str], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(
        prescription_repo.enregistrer_prescription,
        data.get("modele", ""),
        data.get("texte_prescription", ""),
    )


# ── Onglet 4 — Décodage désignation ────────────────────────────
@router.get("/designation")
def get_designation(
    modele: str = "", x_maintenance_password: str | None = Header(default=None)
) -> list[dict[str, Any]]:
    _guard(x_maintenance_password)
    return _safe(designation_repo.lister_regles, modele or None)


@router.post("/designation")
def post_designation(
    data: dict[str, Any], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(designation_repo.creer_regle, data)


@router.put("/designation/{row_id}")
def put_designation(
    row_id: int, data: dict[str, Any], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(designation_repo.modifier_regle, row_id, data)


@router.delete("/designation/{row_id}")
def delete_designation(
    row_id: int, x_maintenance_password: str | None = Header(default=None)
) -> dict[str, bool]:
    _guard(x_maintenance_password)
    _safe(designation_repo.supprimer_regle, row_id)
    return {"ok": True}


# ── Onglet 5 — Clients ─────────────────────────────────────────
@router.get("/clients")
def get_clients(
    q: str = "", x_maintenance_password: str | None = Header(default=None)
) -> list[dict[str, Any]]:
    _guard(x_maintenance_password)
    if q:
        return [c.model_dump() for c in _safe(clients_repo.rechercher_clients, q)]
    return [c.model_dump() for c in _safe(clients_repo.lister_clients)]


@router.post("/clients")
def post_client(
    data: dict[str, Any], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(clients_repo.creer_client, data)


@router.put("/clients/{row_id}")
def put_client(
    row_id: int, data: dict[str, Any], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(clients_repo.modifier_client, row_id, data)


# ── Onglet 6 — Libellés de l'interface ─────────────────────────
@router.get("/libelles")
def get_libelles(x_maintenance_password: str | None = Header(default=None)) -> list[dict[str, Any]]:
    _guard(x_maintenance_password)
    return _safe(libelles_repo.lister_libelles)


@router.post("/libelles")
def post_libelle(
    data: dict[str, str], x_maintenance_password: str | None = Header(default=None)
) -> dict[str, Any]:
    _guard(x_maintenance_password)
    return _safe(
        libelles_repo.enregistrer_libelle,
        data.get("cle", ""),
        data.get("valeur", ""),
        data.get("page", ""),
    )


@router.delete("/libelles/{row_id}")
def delete_libelle(
    row_id: int, x_maintenance_password: str | None = Header(default=None)
) -> dict[str, bool]:
    _guard(x_maintenance_password)
    _safe(libelles_repo.supprimer_libelle, row_id)
    return {"ok": True}
