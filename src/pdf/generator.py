"""Génération de la fiche de sélection PDF (7 parties) via WeasyPrint + Jinja2."""

from __future__ import annotations

import base64
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.models.schemas import GenerateRequest

TEMPLATES_DIR = Path(__file__).parent / "templates"
# Les PNG des pages de garde sont dans ui/public/covers
COVERS_DIR = Path(__file__).resolve().parents[2] / "ui" / "public" / "covers"

# Couleurs France Air
COULEURS = {
    "bleu_marine": "#2f4a6f",
    "rouge": "#d62828",
    "bleu_electrique": "#00a8e8",
    "teal": "#00b4a0",
    "encre": "#0a0e1a",
    "fond_cover": "#eef0f1",
}


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml", "j2"]),
    )


def _cover_data_uri(modele: str, taille: str) -> str | None:
    """Renvoie le PNG de la page de garde en data URI, ou None s'il manque."""
    if not modele or not taille:
        return None
    candidates = [
        COVERS_DIR / f"{modele}_{taille}.png",
        COVERS_DIR / f"{modele.upper()}_{taille}.png",
    ]
    for path in candidates:
        if path.exists():
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            return f"data:image/png;base64,{data}"
    return None


def _carte_france_svg(env: Environment, departement: str) -> str:
    """Charge la carte de France SVG et surligne le département du client.

    Le SVG est rendu via Jinja (pour insérer le numéro de département) puis,
    si le SVG départemental précis est fourni, le path id="dep-XX" est surligné.
    """
    svg_path = TEMPLATES_DIR / "carte_france.svg"
    if not svg_path.exists():
        return ""
    dep = (departement or "").strip()
    # Fallback Corse : un CP 20xxx est normalisé en "20" par le backend,
    # mais le SVG utilise les codes 2A / 2B. On mappe sur 2A par défaut.
    if dep == "20":
        dep = "2A"
    svg = env.get_template("carte_france.svg").render(departement=dep)
    if dep:
        # Les paths de département portent id="dep-XX". On ajoute une surbrillance.
        svg = svg.replace(
            f'id="dep-{dep}"',
            f'id="dep-{dep}" class="dep-actif" style="fill:{COULEURS["rouge"]};"',
        )
    return svg


def generer_pdf(req: GenerateRequest) -> bytes:
    """Construit le HTML complet puis le rend en PDF avec WeasyPrint."""
    from weasyprint import HTML  # import tardif (dépendances système lourdes)

    env = _env()
    template = env.get_template("fiche.html.j2")

    cover = _cover_data_uri(req.machine.modele, req.machine.taille)

    departement = ""
    if req.projet.client:
        departement = req.projet.client.departement
    if not departement:
        for c in req.contacts:
            if c.departement:
                departement = c.departement
                break

    contexte = {
        "machine": req.machine,
        "projet": req.projet,
        "performances": req.performances,
        "options": [o for o in req.options if o.selected] or req.options,
        "contacts": req.contacts,
        "texte_prescription": req.texte_prescription,
        "plans_images": req.plans_images,
        "cover_uri": cover,
        "couleurs": COULEURS,
        "carte_svg": _carte_france_svg(env, departement),
        "departement": departement,
        "tci": [c for c in req.contacts if c.role == "TCI"],
        "tcs": [c for c in req.contacts if c.role == "TCS"],
        "solution": [c for c in req.contacts if c.role == "Solution"],
    }

    html = template.render(**contexte)
    return HTML(string=html, base_url=str(TEMPLATES_DIR)).write_pdf()
