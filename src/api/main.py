"""Point d'entrée FastAPI d'INVENIO — toutes les routes du workflow.

Workflow : Import (upload + parse) → Machine → Projet/Client → Contacts → Options
→ Génération PDF. La page Maintenance a ses propres routes (api/maintenance.py).
"""

from __future__ import annotations

import os
import tempfile
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from src.api._static import mount_frontend
from src.api.maintenance import router as maintenance_router
from src.config import get_settings
from src.models.schemas import GenerateRequest
from src.parser.designation import decoder_prefixe, extraire_segment_options, trouver_designation
from src.parser.pdf_parser import parse_file
from src.services import clients_repo, contacts_repo, designation_repo, options_repo
from src.services import prescription_repo
from src.services.baserow_client import BaserowError
from src.services.libelles_repo import libelles_dict

app = FastAPI(title="INVENIO", description="Générateur de fiches de sélection France Air")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, Any]:
    settings = get_settings()
    return {"status": "ok", "baserow_configured": settings.baserow_configured}


# ── Libellés UI (lus au démarrage du frontend) ─────────────────
@app.get("/api/libelles")
def get_libelles_publics() -> dict[str, str]:
    """Renvoie les libellés de l'interface. Tolérant : {} si Baserow indispo."""
    try:
        return libelles_dict()
    except BaserowError:
        return {}


# ── Étape 1 : Import + parsing d'une fiche GALLETTI ────────────
@app.post("/api/parse")
async def parse_upload(file: UploadFile = File(...)) -> dict[str, Any]:
    suffix = os.path.splitext(file.filename or "")[1] or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = parse_file(tmp_path, file.filename or "")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    # Décodage des options via Baserow (si configuré).
    options_detectees = []
    try:
        segment = extraire_segment_options(result.raw_designation)
        options_detectees = designation_repo.decoder_options(segment, result.machine.modele)
    except BaserowError as exc:
        result.warnings.append(f"Décodage options indisponible : {exc}")

    payload = result.model_dump()
    payload["options_detectees"] = [o.model_dump() for o in options_detectees]
    return payload


# ── Décodage d'une désignation saisie manuellement ─────────────
@app.post("/api/designation/decode")
def decode_designation(payload: dict[str, str]) -> dict[str, Any]:
    designation = trouver_designation(payload.get("designation", "")) or payload.get(
        "designation", ""
    )
    machine = decoder_prefixe(designation)
    options = []
    try:
        segment = extraire_segment_options(designation)
        options = designation_repo.decoder_options(segment, machine.modele)
    except BaserowError:
        pass
    return {"machine": machine.model_dump(), "options": [o.model_dump() for o in options]}


# ── Étape 3 : Recherche client ─────────────────────────────────
@app.get("/api/clients")
def search_clients(q: str = "") -> list[dict[str, Any]]:
    try:
        return [c.model_dump() for c in clients_repo.rechercher_clients(q)]
    except BaserowError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# ── Étape 4 : Contacts d'un département ─────────────────────────
@app.get("/api/contacts")
def get_contacts(departement: str = "") -> dict[str, Any]:
    try:
        fv = contacts_repo.contacts_force_de_vente(departement)
        sol = contacts_repo.contacts_solution()
    except BaserowError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {
        "force_de_vente": [c.model_dump() for c in fv],
        "solution": [c.model_dump() for c in sol],
    }


# ── Étape 5 : Catalogue d'options pour un modèle ───────────────
@app.get("/api/options")
def get_options(modele: str = "") -> list[dict[str, Any]]:
    try:
        return [o.model_dump() for o in options_repo.lister_options(modele or None)]
    except BaserowError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# ── Texte de prescription d'un modèle ──────────────────────────
@app.get("/api/prescription")
def get_prescription(modele: str = "") -> dict[str, str]:
    try:
        return {"texte_prescription": prescription_repo.texte_pour_modele(modele)}
    except BaserowError:
        return {"texte_prescription": ""}


# ── Étape 6 : Génération du PDF ────────────────────────────────
@app.post("/api/generate")
def generate(req: GenerateRequest) -> Response:
    from src.pdf.generator import generer_pdf

    try:
        pdf_bytes = generer_pdf(req)
    except Exception as exc:  # pragma: no cover - dépend de WeasyPrint
        raise HTTPException(status_code=500, detail=f"Erreur de génération PDF : {exc}") from exc

    nom = req.projet.nom or f"{req.machine.modele}_{req.machine.taille}"
    nom = "".join(c if c.isalnum() or c in "-_" else "_" for c in nom)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="INVENIO_{nom}.pdf"'},
    )


# Routes Maintenance
app.include_router(maintenance_router)

# Frontend (doit être attaché en dernier : route catch-all)
mount_frontend(app)
