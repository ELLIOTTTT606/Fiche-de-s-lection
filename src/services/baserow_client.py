"""Client minimal de l'API REST Baserow.

Toutes les données métier d'INVENIO vivent dans Baserow. Ce client est volontairement
fin : lister, créer, modifier, supprimer des lignes d'une table. Il gère l'absence de
configuration (token vide) en renvoyant des résultats vides plutôt qu'en plantant, pour
que l'application reste démarrable en local sans secret.
"""

from __future__ import annotations

from typing import Any

import httpx

from src.config import get_settings


class BaserowError(RuntimeError):
    pass


class BaserowClient:
    def __init__(self, api_url: str | None = None, token: str | None = None) -> None:
        settings = get_settings()
        self.api_url = (api_url or settings.baserow_api_url).rstrip("/")
        self.token = token if token is not None else settings.baserow_token

    @property
    def configured(self) -> bool:
        return bool(self.token)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Token {self.token}"}

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=30.0, headers=self._headers())

    # ── Lecture ────────────────────────────────────────────────
    def list_rows(
        self,
        table_id: str,
        *,
        search: str | None = None,
        size: int = 200,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        if not self.configured or not table_id:
            return []
        url = f"{self.api_url}/api/database/rows/table/{table_id}/"
        params: dict[str, Any] = {"user_field_names": "true", "size": size}
        if search:
            params["search"] = search
        if filters:
            params.update(filters)

        rows: list[dict[str, Any]] = []
        with self._client() as client:
            while url:
                resp = client.get(url, params=params)
                if resp.status_code >= 400:
                    raise BaserowError(f"Baserow {resp.status_code}: {resp.text}")
                data = resp.json()
                rows.extend(data.get("results", []))
                url = data.get("next")
                params = {}  # 'next' contient déjà les paramètres
        return rows

    # ── Écriture ───────────────────────────────────────────────
    def create_row(self, table_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        self._require()
        url = f"{self.api_url}/api/database/rows/table/{table_id}/"
        with self._client() as client:
            resp = client.post(url, params={"user_field_names": "true"}, json=fields)
            self._raise(resp)
            return resp.json()

    def update_row(self, table_id: str, row_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        self._require()
        url = f"{self.api_url}/api/database/rows/table/{table_id}/{row_id}/"
        with self._client() as client:
            resp = client.patch(url, params={"user_field_names": "true"}, json=fields)
            self._raise(resp)
            return resp.json()

    def delete_row(self, table_id: str, row_id: int) -> None:
        self._require()
        url = f"{self.api_url}/api/database/rows/table/{table_id}/{row_id}/"
        with self._client() as client:
            resp = client.delete(url)
            self._raise(resp)

    # ── Helpers ────────────────────────────────────────────────
    def _require(self) -> None:
        if not self.configured:
            raise BaserowError(
                "Baserow n'est pas configuré (BASEROW_TOKEN manquant). "
                "Renseignez le token dans les variables d'environnement."
            )

    @staticmethod
    def _raise(resp: httpx.Response) -> None:
        if resp.status_code >= 400:
            raise BaserowError(f"Baserow {resp.status_code}: {resp.text}")


_default_client: BaserowClient | None = None


def get_client() -> BaserowClient:
    global _default_client
    if _default_client is None:
        _default_client = BaserowClient()
    return _default_client
