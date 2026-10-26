import json
import pytest
from voqryn_network_api.ip_dataset_update import install, validate


def test_install_atomic(tmp_path):
    source = tmp_path / "source.json"
    destination = tmp_path / "data" / "ip.json"
    source.write_text(json.dumps([{"network": "8.8.8.0/24", "country": "us", "asn": 15169, "provider": "Example"}]))
    assert install(source, destination) == 1
    assert json.loads(destination.read_text())[0]["country"] == "US"


def test_invalid_source_keeps_old_data(tmp_path):
    source = tmp_path / "bad.json"
    destination = tmp_path / "installed.json"
    destination.write_text("previous")
    source.write_text(json.dumps([{"network": "invalid"}]))
    with pytest.raises(ValueError):
        install(source, destination)
    assert destination.read_text() == "previous"


def test_reject_bad_asn_and_country():
    with pytest.raises(ValueError):
        validate([{"network": "8.8.8.0/24", "asn": True}])
    with pytest.raises(ValueError):
        validate([{"network": "8.8.8.0/24", "country": "USA"}])
