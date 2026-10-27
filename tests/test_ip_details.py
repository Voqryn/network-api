from fastapi.testclient import TestClient
from voqryn_network_api.main import app


def test_details_falls_back_when_dataset_unreadable(monkeypatch):
    from voqryn_network_api import my_ip as module

    def broken_lookup(_ip):
        raise ValueError("corrupt local dataset")

    monkeypatch.setattr(module, "lookup", broken_lookup)
    with TestClient(app, client=("8.8.8.8", 1234)) as client:
        response = client.get("/v1/ip/me/details")
    assert response.status_code == 200
    body = response.json()
    assert body["ip"] == "8.8.8.8"
    assert body["version"] == "IPv4"
    assert body["intelligence"] == {"available": False, "country": None, "asn": None, "provider": None}


def test_details_ignores_client_supplied_ip_headers(monkeypatch):
    from voqryn_network_api import my_ip as module
    monkeypatch.setattr(module, "lookup", lambda ip: {"available": True, "country": "US", "asn": 1, "provider": ip})
    with TestClient(app, client=("8.8.4.4", 1234)) as client:
        response = client.get("/v1/ip/me/details", headers={"X-Forwarded-For": "9.9.9.9"})
    assert response.json()["intelligence"]["provider"] == "8.8.4.4"
