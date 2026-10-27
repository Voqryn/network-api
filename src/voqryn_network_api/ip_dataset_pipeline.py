"""Operator-controlled staged dataset installation with SHA-256 integrity verification."""
import argparse
import hashlib
import json
from pathlib import Path
from voqryn_network_api.ip_dataset_update import install, validate


def verify_and_install(source: Path, destination: Path, expected_sha256: str, *, dry_run: bool = False) -> dict:
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in expected_sha256):
        raise ValueError("expected SHA-256 must be 64 hexadecimal characters")
    if source.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("source file too large")
    raw = source.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual.lower() != expected_sha256.lower():
        raise ValueError("SHA-256 mismatch; existing dataset unchanged")
    records = validate(json.loads(raw.decode("utf-8")))
    if not dry_run:
        install(source, destination)
    return {"records": len(records), "sha256": actual, "installed": not dry_run}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify and install operator-staged IP data")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify_and_install(args.source, args.destination, args.sha256, dry_run=args.dry_run)))


if __name__ == "__main__":
    main()
