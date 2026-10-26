"""Restricted RDAP lookups for supported domain registries."""

from urllib.parse import quote

import httpx
from fastapi import APIRouter, HTTPException, Query

from voqryn_network_api.dns import validate_domain

router = APIRouter(prefix="/v1/rdap", tags=["rdap"])

# Explicit registry allowlist; no caller-controlled URL or redirects.
REGISTRIES = {"com": "https://rdap.verisign.com/com/v1/domain/", "net": "https://rdap.verisign.com/net/v1/domain/"}
MAX_BYTES = 256_000


@router.get("/domain")
def domain_lookup(domain: str = Query(min_length=1, max_length=254)) -> dict:
    name = validate_domain(domain)
    tld = name.rsplit(".", 1)[-1]
    base = REGISTRIES.get(tld)
    if base is None:
        raise HTTPException(status_code=422, detail="TLD not yet supported")
    url = base + quote(name, safe="")
    try:
        with httpx.Client(timeout=httpx.Timeout(5.0, connect=2.0), follow_redirects=False, trust_env=False) as client:
            with client.stream("GET", url, headers={"Accept": "application/rdap+json"}) as response:
                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Domain not found in RDAP")
                if response.status_code != 200:
                    raise HTTPException(status_code=502, detail="Registry returned an unexpected response")
                data = bytearray()
                for chunk in response.iter_bytes():
                    data.extend(chunk)
                    if len(data) > MAX_BYTES:
                        raise HTTPException(status_code=502, detail="Registry response too large")
        payload = httpx.Response(200, content=bytes(data)).json()
        if not isinstance(payload, dict):
            raise ValueError("RDAP response must be an object")
        return {"domain": name, "rdap": payload}
    except (httpx.RequestError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="RDAP registry unavailable or returned invalid JSON") from exc
