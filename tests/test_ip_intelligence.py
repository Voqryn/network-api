import json
from voqryn_network_api.ip_intelligence import _dataset, lookup


def test_no_dataset_returns_unavailable(monkeypatch):
    monkeypatch.delenv("VOQRYN_IP_DATASET", raising=False)
    _dataset.cache_clear()
    assert lookup("8.8.8.8")["available"] is False


def test_offline_longest_prefix(monkeypatch, tmp_path):
    path = tmp_path / "ip.json"
    path.write_text(json.dumps([
        {"network": "8.0.0.0/8", "country": "US", "asn": 10, "provider": "Broad network"},
        {"network": "8.8.8.0/24", "country": "US", "asn": 20, "provider": "Specific network"},
    ]))
    monkeypatch.setenv("VOQRYN_IP_DATASET", str(path))
    _dataset.cache_clear()
    assert lookup("8.8.8.8")["asn"] == 20
    assert lookup("192.168.1.1")["available"] is False
    _dataset.cache_clear()
