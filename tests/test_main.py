from fastapi.testclient import TestClient
from voqryn_network_api.main import app

client = TestClient(app)


def test_healthz() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version() -> None:
    response = client.get("/v1")
    assert response.status_code == 200
    assert response.json()["status"] == "development"


def test_openapi() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/healthz" in response.json()["paths"]
