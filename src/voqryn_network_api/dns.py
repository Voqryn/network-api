"""Bounded DNS record lookups using the system-configured resolver."""
import re

import dns.exception
import dns.resolver
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/v1/dns", tags=["dns"])
ALLOWED_TYPES = ("A", "AAAA", "CAA", "CNAME", "MX", "NS", "SOA", "TXT")
LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def validate_domain(value: str) -> str:
    """Accept ASCII DNS hostnames only; no URLs, IP literals or underscores."""
    domain = value.rstrip(".").lower()
    if not 1 <= len(domain) <= 253 or not all(LABEL.fullmatch(p) for p in domain.split(".")):
        raise HTTPException(status_code=422, detail="Invalid DNS domain name")
    if "." not in domain or domain.split(".")[-1].isdigit():
        raise HTTPException(status_code=422, detail="A fully qualified domain name is required")
    return domain


@router.get("/lookup")
def lookup(
    domain: str = Query(min_length=1, max_length=254),
    record_type: str = Query(default="A", pattern="^(A|AAAA|CAA|CNAME|MX|NS|SOA|TXT)$"),
) -> dict:
    name = validate_domain(domain)
    resolver = dns.resolver.Resolver(configure=True)
    resolver.timeout = 2.0
    resolver.lifetime = 4.0
    try:
        answers = resolver.resolve(name, record_type, search=False, raise_on_no_answer=False)
        records = sorted(str(r) for r in answers) if answers.rrset is not None else []
        return {"domain": name, "record_type": record_type, "records": records}
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return {"domain": name, "record_type": record_type, "records": []}
    except (dns.exception.Timeout, dns.resolver.NoNameservers) as exc:
        raise HTTPException(status_code=503, detail="DNS lookup unavailable") from exc
    except dns.exception.DNSException as exc:
        raise HTTPException(status_code=502, detail="DNS lookup failed") from exc
