from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from voqryn_network_api.dns import validate_domain
from voqryn_network_api.main import app

client = TestClient(app)


@pytest.mark.parametrize("name", ["http://example.com", "example.com/path", "localhost", "127.0.0.1", "a..com", "-bad.com", "bad_.com"])
def test_rejects_invalid_names(name: str) -> None:
    assert client.get("/v1/dns/lookup", params={"domain": name}).status_code == 422


def test_normalizes_domain() -> None:
    assert validate_domain("Example.COM.") == "example.com"


def test_rejects_unknown_record_type() -> None:
    assert client.get("/v1/dns/lookup", params={"domain": "example.com", "record_type": "ANY"}).status_code == 422


def test_lookup_uses_bounded_resolver() -> None:
    with patch("voqryn_network_api.dns.dns.resolver.Resolver") as resolver_cls:
        resolver = resolver_cls.return_value
        resolver.resolve.return_value.rrset = [object()]
        response = client.get("/v1/dns/lookup", params={"domain": "Example.COM", "record_type": "A"})
        assert response.status_code == 200
        assert response.json()["domain"] == "example.com"
        assert resolver.timeout == 2.0
        assert resolver.lifetime == 4.0
        resolver.resolve.assert_called_once_with("example.com", "A", search=False, raise_on_no_answer=False)
