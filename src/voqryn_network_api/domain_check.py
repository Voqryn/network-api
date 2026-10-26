"""Conservative domain registration indication based on restricted RDAP lookups."""
from fastapi import APIRouter, HTTPException, Query
from voqryn_network_api.dns import validate_domain
from voqryn_network_api.rdap import domain_lookup

router = APIRouter(prefix="/v1/domain", tags=["domain"])


@router.get("/check")
def check_domain(domain: str = Query(min_length=1, max_length=254)) -> dict[str, str]:
    name = validate_domain(domain)
    try:
        domain_lookup(name)
    except HTTPException as exc:
        if exc.status_code == 404:
            return {"domain": name, "status": "possibly_available", "source": "rdap", "disclaimer": "RDAP absence does not guarantee registrability or purchase availability."}
        if exc.status_code in (422, 502, 503):
            return {"domain": name, "status": "unknown", "source": "rdap", "disclaimer": "Registration status could not be determined."}
        raise
    return {"domain": name, "status": "registered", "source": "rdap", "disclaimer": "RDAP registration information is not a registrar availability quote."}
