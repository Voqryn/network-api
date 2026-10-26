from fastapi.testclient import TestClient
from voqryn_network_api.main import app


def test_ip_response_ignores_untrusted_forwarding_headers():
    with TestClient(app, client=("198.51.100.7", 4321)) as client:
        response = client.get("/v1/ip/me", headers={
            "X-Forwarded-For": "203.0.113.99",
            "Forwarded": "for=203.0.113.100",
            "X-Real-IP": "203.0.113.101",
        })
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "ip": "198.51.100.7", "version": "IPv4"}


def test_ipv6_address():
    with TestClient(app, client=("2001:db8::7", 4321)) as client:
        response = client.get("/v1/ip/me")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "ip": "2001:db8::7", "version": "IPv6"}
