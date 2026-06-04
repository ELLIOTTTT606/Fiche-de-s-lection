"""Tests du décodage de la chaîne de désignation GALLETTI."""

from src.parser.catalogue import normaliser_taille
from src.parser.designation import (
    decoder_prefixe,
    extraire_segment_options,
    trouver_designation,
)


def test_trouver_designation_dans_texte():
    texte = "Réf produit : VLS254HS0B  A000C00020G010I 00000000000000000000\nautre ligne"
    d = trouver_designation(texte)
    assert d.startswith("VLS254HS0B")
    assert "A000C00020G010I" in d
    # Pas de texte parasite en minuscules.
    assert "ligne" not in d


def test_decoder_prefixe_pac_standard():
    m = decoder_prefixe("VLS254HS0B A000C00020G010I")
    assert m.modele == "VLS"
    assert m.taille == "254"
    assert m.type_machine == "PAC"
    assert m.acoustique == "Standard"
    assert m.fluide == "R454B"
    assert m.medium == "air/eau"


def test_decoder_prefixe_geg_silencieux():
    m = decoder_prefixe("MPED076CL00 B100")
    assert m.modele == "MPED"  # MPED gagne sur MPE (match le plus long)
    assert m.taille == "76"
    assert m.type_machine == "GEG"
    assert m.acoustique == "Silencieux"


def test_modele_inconnu():
    m = decoder_prefixe("ZZZ999XS")
    assert m.modele == ""


def test_extraire_segment_options():
    seg = extraire_segment_options("VLS254HS0B A000C00020G010I 00000000000000000000")
    # Tokens après la tête, espaces retirés.
    assert seg == "A000C00020G010I00000000000000000000"


def test_extraire_segment_options_vide():
    assert extraire_segment_options("MLI06HS") == ""


def test_normaliser_taille_retire_zeros():
    # 052 -> 52 (le zéro de tête est retiré)
    assert normaliser_taille("052", "VLS") == "52"
    assert normaliser_taille("254", "VLS") == "254"


def test_normaliser_taille_conserve_taille_paddee_valide():
    # MLI a une taille "06" : on ne doit pas la transformer en "6".
    assert normaliser_taille("06", "MLI") == "06"
