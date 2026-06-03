"""Configuration centrale d'INVENIO — lit les variables d'environnement.

Aucune donnée métier ici : uniquement la connexion à Baserow et le mot de passe
de la page Maintenance. Tout le reste vit dans Baserow.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Baserow ---
    baserow_api_url: str = "https://api.baserow.io"
    baserow_token: str = ""

    baserow_table_clients: str = "939119"
    baserow_table_contacts_fv: str = "939355"
    baserow_table_contacts_solution: str = "939361"
    baserow_table_options: str = "941070"
    baserow_table_prix: str = "939101"

    # Tables à créer (vides tant qu'elles n'existent pas dans Baserow)
    baserow_table_designation: str = ""
    baserow_table_prescription: str = ""
    baserow_table_libelles: str = ""

    # --- Maintenance ---
    maintenance_password: str = "changez_moi"

    @property
    def baserow_configured(self) -> bool:
        return bool(self.baserow_token)


@lru_cache
def get_settings() -> Settings:
    return Settings()
