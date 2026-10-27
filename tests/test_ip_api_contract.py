"""Smoke contract for both public IP endpoints; no external network calls."""
from fastapi.testclient import TestClient
from voqryn_network_api.main import app


def test_ip_endpoints_share_basic_fields(monkeypatch):
    from voqryn_network_api import my_ip as module
    monkeypatch.setattr(module, "lookup", lambda ip: {"available": False, "country": None, "asn": None, "provider": None})
    with TestClient(app, client=("2001:4860:4860::8888", 1234)) as client:
        basic = client.get("/v1/ip/me")
        details = client.get("/v1/ip/me/details")
    assert basic.status_code == details.status_code == 200
    assert basic.json() == {"status": "ok", "ip": "2001:4860:4860::8888", "version": "IPv6"}
    assert all(details.json()[key] == value for key, value in basic.json().items())
    assert details.json()["intelligence"]["available"] is False
