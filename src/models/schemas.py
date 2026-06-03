"""Modèles Pydantic partagés entre le parser, l'API et le générateur PDF."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# Machine
# ─────────────────────────────────────────────────────────────
class Machine(BaseModel):
    """Identité d'une machine GALLETTI déduite de la désignation."""

    modele: str = ""
    taille: str = ""
    type_machine: str = ""  # "PAC" ou "GEG"
    acoustique: str = ""  # "Standard" ou "Silencieux"
    fluide: str = ""
    medium: str = ""  # "air/eau", "eau/eau"
    designation: str = ""


# ─────────────────────────────────────────────────────────────
# Performances
# ─────────────────────────────────────────────────────────────
class Performance(BaseModel):
    """Une ligne de performance (froid ou chaud)."""

    mode: str = ""  # "Froid" / "Chaud"
    puissance_kw: float | None = None
    puissance_absorbee_kw: float | None = None
    cop: float | None = None
    eer: float | None = None
    scop: float | None = None
    seer: float | None = None
    classe_energetique: str = ""


# ─────────────────────────────────────────────────────────────
# Option / accessoire
# ─────────────────────────────────────────────────────────────
class Option(BaseModel):
    code: str = ""
    libelle: str = ""
    categorie: str = ""
    description: str = ""
    conseil: str = ""
    prix: float | None = None
    modele: str = ""
    selected: bool = False


# ─────────────────────────────────────────────────────────────
# Contacts
# ─────────────────────────────────────────────────────────────
class Contact(BaseModel):
    role: str = ""  # "TCI" / "TCS" / "Solution"
    nom: str = ""
    email: str = ""
    telephone: str = ""
    departement: str = ""


# ─────────────────────────────────────────────────────────────
# Client
# ─────────────────────────────────────────────────────────────
class Client(BaseModel):
    id: int | None = None
    code_tiers: str = ""
    nom: str = ""
    code_postal: str = ""
    departement: str = ""


# ─────────────────────────────────────────────────────────────
# Résultat de parsing d'une fiche GALLETTI
# ─────────────────────────────────────────────────────────────
class ParseResult(BaseModel):
    machine: Machine = Field(default_factory=Machine)
    performances: list[Performance] = Field(default_factory=list)
    options: list[Option] = Field(default_factory=list)
    raw_designation: str = ""
    plans_count: int = 0
    warnings: list[str] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Projet (saisi par le commercial)
# ─────────────────────────────────────────────────────────────
class Projet(BaseModel):
    numero: str = ""
    nom: str = ""
    client: Client | None = None
    contact_solution: Contact | None = None


# ─────────────────────────────────────────────────────────────
# Requête de génération PDF
# ─────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    machine: Machine
    projet: Projet
    performances: list[Performance] = Field(default_factory=list)
    options: list[Option] = Field(default_factory=list)
    contacts: list[Contact] = Field(default_factory=list)
    texte_prescription: str = ""
    plans_images: list[str] = Field(default_factory=list)  # PNG base64 data URLs
