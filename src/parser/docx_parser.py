"""Extraction des données d'une fiche technique GALLETTI au format DOCX.

Bug GALLETTI connu : les DOCX référencent dans les `.rels` des thumbnails JPEG
absents du ZIP, ce qui fait planter python-docx avec un KeyError. La fonction
`_open_docx_safe` reconstruit le ZIP en supprimant ces références mortes.
"""

from __future__ import annotations

import io
import re
import zipfile

from docx import Document

from src.models.schemas import ParseResult
from src.parser.designation import decoder_prefixe, trouver_designation
from src.parser.performances import extraire_performances_depuis_texte


def _open_docx_safe(path: str):
    """Ouvre un DOCX en nettoyant les médias manquants dans le ZIP."""
    with open(path, "rb") as f:
        raw = f.read()

    src_zip = zipfile.ZipFile(io.BytesIO(raw), "r")
    names = set(src_zip.namelist())

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as dst_zip:
        for item in src_zip.infolist():
            data = src_zip.read(item.filename)
            if item.filename.endswith(".rels"):
                try:
                    text = data.decode("utf-8")

                    def keep_rel(match, _item=item):
                        target = re.search(r'Target="([^"]+)"', match.group(0))
                        if not target:
                            return match.group(0)
                        t = target.group(1).lstrip("/")
                        base = "/".join(_item.filename.split("/")[:-2])
                        full = f"{base}/{t}".lstrip("/") if base else t
                        if full not in names and t not in names:
                            return ""
                        return match.group(0)

                    text = re.sub(r"<Relationship[^/]*/>", keep_rel, text)
                    data = text.encode("utf-8")
                except Exception:
                    pass
            dst_zip.writestr(item, data)

    src_zip.close()
    buf.seek(0)
    return Document(buf)


def _texte_complet(doc) -> str:
    """Concatène tout le texte du document (paragraphes + tableaux)."""
    parts: list[str] = []
    for para in doc.paragraphs:
        if para.text:
            parts.append(para.text)
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text for c in row.cells if c.text]
            if cells:
                parts.append("\t".join(cells))
    return "\n".join(parts)


def _compter_images(path: str) -> int:
    """Compte les images effectivement présentes dans le ZIP (pour les plans)."""
    try:
        with zipfile.ZipFile(path, "r") as z:
            return sum(
                1
                for n in z.namelist()
                if n.startswith("word/media/") and n.lower().endswith((".png", ".jpg", ".jpeg", ".emf"))
            )
    except Exception:
        return 0


def parse_docx(path: str) -> ParseResult:
    """Parse une fiche GALLETTI DOCX en ParseResult."""
    result = ParseResult()

    try:
        doc = _open_docx_safe(path)
    except Exception as exc:  # pragma: no cover - dépend du fichier
        result.warnings.append(f"Impossible d'ouvrir le DOCX : {exc}")
        return result

    texte = _texte_complet(doc)

    designation = trouver_designation(texte)
    result.raw_designation = designation
    if not designation:
        result.warnings.append(
            "Aucune chaîne de désignation reconnue dans le document."
        )
    else:
        result.machine = decoder_prefixe(designation)

    result.performances = extraire_performances_depuis_texte(texte)
    result.plans_count = _compter_images(path)

    return result
