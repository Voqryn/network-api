from fastapi.testclient import TestClient
from voqryn_network_api.main import app


def test_ip_response():
    client = TestClient(app, client=("198.51.100.7", 4321))
    response = client.get("/v1/ip/me", headers={"X-Forwarded-For": "203.0.113.99"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "ip": "198.51.100.7", "version": "IPv4"}
