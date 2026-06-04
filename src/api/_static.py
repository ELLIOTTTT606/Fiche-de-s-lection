"""Sert le frontend React buildé (ui/dist) en fichiers statiques.

En production (Vercel / Oracle), FastAPI sert à la fois l'API et le frontend.
Si ui/dist n'existe pas encore (dev backend seul), on n'attache rien.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

DIST_DIR = Path(__file__).resolve().parents[2] / "ui" / "dist"
# Les pages de garde restent dans ui/public/covers (volontairement non copiées
# dans dist pour ne pas dupliquer ~73 Mo). On les sert directement de là.
COVERS_DIR = Path(__file__).resolve().parents[2] / "ui" / "public" / "covers"


def mount_frontend(app: FastAPI) -> None:
    # Sert les pages de garde même si dist n'est pas encore buildé.
    if COVERS_DIR.exists():
        app.mount("/covers", StaticFiles(directory=str(COVERS_DIR)), name="covers")

    if not DIST_DIR.exists():
        return

    assets = DIST_DIR / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=str(assets)), name="assets")

    index_file = DIST_DIR / "index.html"

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        # Fichier statique réel (favicon, etc.) ?
        candidate = DIST_DIR / full_path
        if full_path and candidate.is_file():
            return FileResponse(str(candidate))
        # Sinon, on renvoie l'app React (routing côté client).
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"detail": "Frontend non buildé. Lancez `cd ui && npm run build`."}
