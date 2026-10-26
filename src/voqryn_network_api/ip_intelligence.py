"""Optional offline IP enrichment; no outbound lookup or third-party requests."""
import json
import os
from functools import lru_cache
from ipaddress import ip_address, ip_network
from pathlib import Path


@lru_cache(maxsize=1)
def _dataset() -> tuple[tuple[object, dict], ...]:
    path = os.getenv("VOQRYN_IP_DATASET")
    if not path:
        return ()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) > 100000:
        raise ValueError("IP dataset must be a bounded JSON list")
    records = []
    for entry in data:
        if not isinstance(entry, dict):
            raise ValueError("invalid IP dataset entry")
        network = ip_network(entry["network"], strict=True)
        country = entry.get("country")
        asn = entry.get("asn")
        provider = entry.get("provider")
        if country is not None and (not isinstance(country, str) or len(country) != 2 or not country.isalpha()):
            raise ValueError("country must be ISO 3166-1 alpha-2")
        if asn is not None and (not isinstance(asn, int) or isinstance(asn, bool) or asn < 0):
            raise ValueError("invalid ASN")
        if provider is not None and (not isinstance(provider, str) or len(provider) > 200):
            raise ValueError("invalid provider")
        records.append((network, {"country": country.upper() if country else None, "asn": asn, "provider": provider}))
    return tuple(records)


def lookup(ip: str) -> dict:
    """Return only dataset-backed fields; never infer country or VPN status."""
    address = ip_address(ip)
    if not address.is_global:
        return {"available": False, "country": None, "asn": None, "provider": None}
    matches = [(net.prefixlen, details) for net, details in _dataset() if address in net]
    if not matches:
        return {"available": False, "country": None, "asn": None, "provider": None}
    details = max(matches, key=lambda item: item[0])[1]
    return {"available": True, **details}
