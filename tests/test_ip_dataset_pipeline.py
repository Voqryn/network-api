import hashlib
import json
import pytest
from voqryn_network_api.ip_dataset_pipeline import verify_and_install


def test_verify_dry_run_then_install(tmp_path):
    source = tmp_path / "staged.json"
    dest = tmp_path / "live.json"
    source.write_text(json.dumps([{"network": "8.8.8.0/24", "country": "US", "asn": 15169}]))
    checksum = hashlib.sha256(source.read_bytes()).hexdigest()
    assert verify_and_install(source, dest, checksum, dry_run=True)["installed"] is False
    assert not dest.exists()
    assert verify_and_install(source, dest, checksum)["records"] == 1
    assert dest.exists()


def test_bad_checksum_preserves_existing_dataset(tmp_path):
    source = tmp_path / "staged.json"
    dest = tmp_path / "live.json"
    source.write_text("[]")
    dest.write_text("previous")
    with pytest.raises(ValueError, match="mismatch"):
        verify_and_install(source, dest, "0" * 64)
    assert dest.read_text() == "previous"
