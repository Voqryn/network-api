import json
from voqryn_network_api.ip_intelligence import _dataset, lookup


def test_ipv4_ipv6_longest_prefix_and_no_cross_family(monkeypatch, tmp_path):
    source = tmp_path / "prefixes.json"
    source.write_text(json.dumps([
        {"network": "8.0.0.0/8", "asn": 1},
        {"network": "8.8.8.0/24", "asn": 2},
        {"network": "2001:4860::/32", "asn": 3},
        {"network": "2001:4860:4860::/48", "asn": 4},
    ]))
    monkeypatch.setenv("VOQRYN_IP_DATASET", str(source))
    _dataset.cache_clear()
    try:
        assert lookup("8.8.8.8")["asn"] == 2
        assert lookup("8.9.0.1")["asn"] == 1
        assert lookup("2001:4860:4860::8888")["asn"] == 4
        assert lookup("2001:4860:1234::1")["asn"] == 3
        assert lookup("192.168.1.1")["available"] is False
    finally:
        _dataset.cache_clear()
