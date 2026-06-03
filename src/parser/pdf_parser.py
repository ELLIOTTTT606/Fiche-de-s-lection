"""Extraction des données d'une fiche technique GALLETTI au format PDF."""

from __future__ import annotations

import pdfplumber

from src.models.schemas import ParseResult
from src.parser.designation import decoder_prefixe, trouver_designation
from src.parser.performances import extraire_performances_depuis_texte


def _texte_complet(path: str) -> tuple[str, int]:
    """Renvoie (texte concaténé, nombre d'images repérées)."""
    parts: list[str] = []
    images = 0
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            if txt:
                parts.append(txt)
            try:
                images += len(page.images or [])
            except Exception:
                pass
    return "\n".join(parts), images


def parse_pdf(path: str) -> ParseResult:
    """Parse une fiche GALLETTI PDF en ParseResult."""
    result = ParseResult()

    try:
        texte, images = _texte_complet(path)
    except Exception as exc:  # pragma: no cover - dépend du fichier
        result.warnings.append(f"Impossible d'ouvrir le PDF : {exc}")
        return result

    designation = trouver_designation(texte)
    result.raw_designation = designation
    if not designation:
        result.warnings.append(
            "Aucune chaîne de désignation reconnue dans le document."
        )
    else:
        result.machine = decoder_prefixe(designation)

    result.performances = extraire_performances_depuis_texte(texte)
    result.plans_count = images

    return result


def parse_file(path: str, filename: str) -> ParseResult:
    """Dispatch DOCX/PDF selon l'extension du fichier."""
    from src.parser.docx_parser import parse_docx

    lower = (filename or path).lower()
    if lower.endswith(".docx"):
        return parse_docx(path)
    if lower.endswith(".pdf"):
        return parse_pdf(path)

    result = ParseResult()
    result.warnings.append(
        "Format non pris en charge. Déposez un fichier .docx ou .pdf GALLETTI."
    )
    return result
