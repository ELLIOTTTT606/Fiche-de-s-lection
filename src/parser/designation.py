"""Décodage de la chaîne de désignation GALLETTI.

Exemple de chaîne :  ``VLS254HS0B  A000C00020G010I 00000000000000000000``

Structure du préfixe :
  - modèle      : ex. ``VLS`` (le plus long match du catalogue)
  - taille      : ex. ``254``
  - type        : ``H`` = PAC, ``C`` = GEG
  - acoustique  : ``S`` = standard, ``L`` = silencieux
  - variante    : ex. ``0B``

Le reste de la chaîne (``A000C00020G010I...``) encode les options position par
position. Le décodage des options NE SE FAIT PAS en dur : il s'appuie sur la
table Baserow ``DECODAGE_DESIGNATION`` (voir designation_repo). Ce module se
contente d'extraire la chaîne et son préfixe.
"""

from __future__ import annotations

import re

from src.models.schemas import Machine
from src.parser.catalogue import MODELES_PAR_LONGUEUR, info_modele, normaliser_taille

# Une désignation candidate : un modèle connu suivi de chiffres puis lettres/chiffres.
_MODELE_ALTERNATION = "|".join(MODELES_PAR_LONGUEUR)
_DESIGNATION_RE = re.compile(
    rf"\b(?P<modele>{_MODELE_ALTERNATION})"
    r"(?P<taille>\d{2,4})"
    r"(?P<type>[HC])?"
    r"(?P<acoustique>[SL])?"
    r"(?P<reste>[0-9A-Z ]*)",
    re.IGNORECASE,
)


def trouver_designation(texte: str) -> str:
    """Retrouve la chaîne de désignation à l'intérieur d'un texte.

    On cherche le premier motif "modèle connu + taille". On renvoie une chaîne
    nettoyée (espaces multiples compactés) ou une chaîne vide si rien trouvé.
    """
    if not texte:
        return ""

    candidates: list[tuple[int, str]] = []
    for m in _DESIGNATION_RE.finditer(texte):
        modele = m.group("modele").upper()
        if info_modele(modele) is None:
            continue
        # On prend une fenêtre raisonnable après le préfixe pour les options.
        start = m.start()
        window = texte[start : start + 60]
        # Compacte les espaces.
        window = re.sub(r"\s+", " ", window).strip()
        candidates.append((start, window))

    if not candidates:
        return ""
    # La première occurrence dans le document est la plus fiable.
    candidates.sort(key=lambda c: c[0])
    return candidates[0][1]


def decoder_prefixe(designation: str) -> Machine:
    """Décode le préfixe d'une désignation en une Machine.

    Le décodage des options se fait ailleurs (via Baserow).
    """
    machine = Machine(designation=designation)
    if not designation:
        return machine

    m = _DESIGNATION_RE.match(designation.strip())
    if not m:
        # tente sur la chaîne entière
        m = _DESIGNATION_RE.search(designation)
    if not m:
        return machine

    modele = m.group("modele").upper()
    info = info_modele(modele)
    if info is None:
        return machine

    machine.modele = modele
    machine.taille = normaliser_taille(m.group("taille"), modele)
    machine.fluide = info.fluide
    machine.medium = info.medium

    type_code = (m.group("type") or "").upper()
    if type_code == "H":
        machine.type_machine = "PAC"
    elif type_code == "C":
        machine.type_machine = "GEG"

    acou = (m.group("acoustique") or "").upper()
    if acou == "S":
        machine.acoustique = "Standard"
    elif acou == "L":
        machine.acoustique = "Silencieux"

    return machine


def extraire_segment_options(designation: str) -> str:
    """Renvoie la partie 'options' de la désignation (après le préfixe).

    Utilisée par le décodage Baserow position par position.
    """
    if not designation:
        return ""
    m = _DESIGNATION_RE.match(designation.strip()) or _DESIGNATION_RE.search(designation)
    if not m:
        return ""
    return (m.group("reste") or "").strip()
