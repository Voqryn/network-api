from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient
from voqryn_network_api.main import app

client = TestClient(app)


def test_registered() -> None:
    with patch("voqryn_network_api.domain_check.domain_lookup", return_value={"rdap": {}}):
        response = client.get("/v1/domain/check?domain=Example.COM")
    assert response.status_code == 200
    assert response.json()["status"] == "registered"


def test_rdap_404_is_only_possibly_available() -> None:
    with patch("voqryn_network_api.domain_check.domain_lookup", side_effect=HTTPException(404)):
        response = client.get("/v1/domain/check?domain=example.com")
    assert response.json()["status"] == "possibly_available"


def test_rdap_error_is_unknown() -> None:
    with patch("voqryn_network_api.domain_check.domain_lookup", side_effect=HTTPException(502)):
        response = client.get("/v1/domain/check?domain=example.com")
    assert response.json()["status"] == "unknown"


def test_invalid_domain() -> None:
    assert client.get("/v1/domain/check?domain=http://example.com").status_code == 422
