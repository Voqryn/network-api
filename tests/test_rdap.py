from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from voqryn_network_api.main import app

client = TestClient(app)


def test_unsupported_tld_does_not_access_network() -> None:
    with patch("voqryn_network_api.rdap.httpx.Client") as factory:
        result = client.get("/v1/rdap/domain", params={"domain": "example.org"})
        assert result.status_code == 422
        factory.assert_not_called()


def test_invalid_domain() -> None:
    assert client.get("/v1/rdap/domain", params={"domain": "http://example.com"}).status_code == 422


def test_success_with_mock_transport() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://rdap.verisign.com/com/v1/domain/example.com"
        return httpx.Response(200, json={"objectClassName": "domain", "ldhName": "EXAMPLE.COM"})

    transport = httpx.MockTransport(handler)
    real_client = httpx.Client
    with patch("voqryn_network_api.rdap.httpx.Client", side_effect=lambda **kwargs: real_client(transport=transport, **kwargs)):
        result = client.get("/v1/rdap/domain", params={"domain": "Example.COM"})
    assert result.status_code == 200
    assert result.json()["rdap"]["objectClassName"] == "domain"


def test_redirect_is_rejected() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(302, headers={"Location": "http://127.0.0.1/"}))
    real_client = httpx.Client
    with patch("voqryn_network_api.rdap.httpx.Client", side_effect=lambda **kwargs: real_client(transport=transport, **kwargs)):
        result = client.get("/v1/rdap/domain", params={"domain": "example.net"})
    assert result.status_code == 502
