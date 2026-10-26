"""Explicit local IP dataset importer. Never downloads remote files automatically."""
import argparse
import json
import os
import tempfile
from ipaddress import ip_network
from pathlib import Path


def validate(payload: object) -> list[dict]:
    if not isinstance(payload, list) or len(payload) > 100000:
        raise ValueError("expected a list of up to 100000 records")
    result = []
    for item in payload:
        if not isinstance(item, dict) or not isinstance(item.get("network"), str):
            raise ValueError("each record requires a network string")
        network = ip_network(item["network"], strict=True)
        country, asn, provider = item.get("country"), item.get("asn"), item.get("provider")
        if country is not None and (not isinstance(country, str) or len(country) != 2 or not country.isascii() or not country.isalpha()):
            raise ValueError("invalid country code")
        if asn is not None and (type(asn) is not int or not 0 <= asn <= 4294967295):
            raise ValueError("invalid ASN")
        if provider is not None and (not isinstance(provider, str) or len(provider) > 200):
            raise ValueError("invalid provider")
        result.append({"network": str(network), "country": country.upper() if country else None, "asn": asn, "provider": provider})
    return result


def install(source: Path, destination: Path) -> int:
    """Validate and atomically replace an existing local dataset; no network access."""
    if source.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("source file too large")
    records = validate(json.loads(source.read_text(encoding="utf-8")))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent, prefix=".ipdata-", delete=False) as tmp:
            temp_name = tmp.name
            os.fchmod(tmp.fileno(), 0o600)
            json.dump(records, tmp, separators=(",", ":"))
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(temp_name, destination)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and install a local IP dataset")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    print(f"Installed {install(args.source, args.destination)} network records")


if __name__ == "__main__":
    main()
