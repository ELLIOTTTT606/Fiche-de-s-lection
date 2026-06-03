"""Test du décodage d'options à partir de règles (sans Baserow réel).

On monkeypatch `lister_regles` pour fournir des règles factices et on vérifie
que le segment d'options est correctement comparé position par position.
"""

from src.services import designation_repo


def test_decoder_options_avec_regles(monkeypatch):
    regles = [
        {"id": 1, "position_start": 0, "position_end": 1, "code_attendu": "A",
         "option_label": "Châssis standard", "categorie": "Châssis", "modele": ""},
        {"id": 2, "position_start": 4, "position_end": 5, "code_attendu": "C",
         "option_label": "Régulation avancée", "categorie": "Régulation", "modele": ""},
        {"id": 3, "position_start": 0, "position_end": 1, "code_attendu": "Z",
         "option_label": "Ne matche pas", "categorie": "X", "modele": ""},
    ]
    monkeypatch.setattr(designation_repo, "lister_regles", lambda modele=None: regles)

    # segment "A000C00020..." : pos0='A', pos4='C'
    options = designation_repo.decoder_options("A000C00020G010I", modele="VLS")
    labels = {o.libelle for o in options}
    assert "Châssis standard" in labels
    assert "Régulation avancée" in labels
    assert "Ne matche pas" not in labels
    assert all(o.selected for o in options)


def test_decoder_options_segment_vide(monkeypatch):
    monkeypatch.setattr(designation_repo, "lister_regles", lambda modele=None: [])
    assert designation_repo.decoder_options("", modele="VLS") == []
