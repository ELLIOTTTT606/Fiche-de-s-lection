"""Décodage de la chaîne de désignation GALLETTI.

Exemple de chaîne :  ``VLS254HS0B  A000C00020G010I 00000000000000000000``

Structure :
  - token de tête : modèle + taille + type + acoustique + variante
      - modèle     : ex. ``VLS`` (le plus long match du catalogue)
      - taille     : ex. ``254``
      - type       : ``H`` = PAC, ``C`` = GEG
      - acoustique : ``S`` = standard, ``L`` = silencieux
      - variante   : ex. ``0B``
  - tokens suivants : ``A000C00020G010I 00000000000000000000`` encodent les
    options/accessoires position par position.

Le décodage des options NE SE FAIT PAS en dur : il s'appuie sur la table Baserow
``DECODAGE_DESIGNATION`` (voir designation_repo). Le « segment d'options » exposé
ici est la concaténation (sans espaces) des tokens qui suivent le token de tête.
C'est sur cette chaîne que la commerciale définit ses positions.
"""

from __future__ import annotations

import re

from src.models.schemas import Machine
from src.parser.catalogue import MODELES_PAR_LONGUEUR, info_modele, normaliser_taille

_MODELE_ALTERNATION = "|".join(MODELES_PAR_LONGUEUR)

# Token de tête : modèle connu + taille + (type) + (acoustique) + (variante).
_TETE_RE = re.compile(
    rf"(?P<modele>{_MODELE_ALTERNATION})"
    r"(?P<taille>\d{2,4})"
    r"(?P<type>[HC])?"
    r"(?P<acoustique>[SL])?"
    r"(?P<variante>[0-9A-Z]{0,3})",
)

# Repère une occurrence de désignation dans un texte libre, suivie de ses tokens
# d'options (tokens en MAJUSCULES/chiffres séparés par des espaces).
_DESIGNATION_RE = re.compile(
    rf"(?P<modele>{_MODELE_ALTERNATION})"
    r"\d{2,4}[HC]?[SL]?[0-9A-Z]*"
    r"(?:\s+[0-9A-Z]{3,})*",
)


def trouver_designation(texte: str) -> str:
    """Retrouve la chaîne de désignation à l'intérieur d'un texte.

    On cherche le premier motif « modèle connu + taille (+ tokens d'options) ».
    Renvoie la chaîne avec espaces compactés, ou "" si rien trouvé.
    """
    if not texte:
        return ""
    for m in _DESIGNATION_RE.finditer(texte):
        if info_modele(m.group("modele")) is None:
            continue
        return re.sub(r"\s+", " ", m.group(0)).strip()
    return ""


def decoder_prefixe(designation: str) -> Machine:
    """Décode le token de tête d'une désignation en une Machine."""
    machine = Machine(designation=designation)
    if not designation:
        return machine

    tete = designation.strip().split()[0] if designation.strip() else ""
    m = _TETE_RE.match(tete)
    if not m:
        m = _TETE_RE.search(designation)
    if not m or info_modele(m.group("modele")) is None:
        return machine

    modele = m.group("modele").upper()
    info = info_modele(modele)
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
    """Renvoie la partie 'options' de la désignation (tokens après le token de tête).

    Les espaces sont retirés : c'est la chaîne sur laquelle les positions de la
    table DECODAGE_DESIGNATION sont comptées.
    """
    if not designation:
        return ""
    tokens = designation.strip().split()
    if len(tokens) <= 1:
        return ""
    return "".join(tokens[1:])
