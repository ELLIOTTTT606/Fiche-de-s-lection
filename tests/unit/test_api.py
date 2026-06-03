"""Tests d'intégration légers de l'API (sans Baserow configuré)."""

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_libelles_tolerant_sans_baserow():
    # Sans token Baserow, renvoie {} sans planter.
    resp = client.get("/api/libelles")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)


def test_decode_designation_endpoint():
    resp = client.post("/api/designation/decode", json={"designation": "VLS254HS0B A000C00020G010I"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["machine"]["modele"] == "VLS"
    assert data["machine"]["taille"] == "254"


def test_maintenance_protegee():
    # Sans mot de passe -> 401
    resp = client.get("/api/maintenance/options")
    assert resp.status_code == 401


def test_maintenance_login_mauvais_mdp():
    resp = client.post("/api/maintenance/login", json={"password": "faux"})
    assert resp.status_code == 401
