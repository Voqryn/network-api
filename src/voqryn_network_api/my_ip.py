"""Return the directly connected peer IP, without trusting spoofable forwarding headers."""
from ipaddress import ip_address
from fastapi import APIRouter, Request
from voqryn_network_api.ip_intelligence import lookup

router = APIRouter(prefix="/v1/ip", tags=["ip"])


@router.get("/me")
def my_ip(request: Request) -> dict[str, str]:
    """Only accurate for a direct connection or correctly configured trusted proxy."""
    peer = request.client.host if request.client else None
    if peer is None:
        return {"status": "unavailable", "ip": "", "version": ""}
    try:
        address = ip_address(peer)
    except ValueError:
        return {"status": "unavailable", "ip": "", "version": ""}
    return {"status": "ok", "ip": str(address), "version": f"IPv{address.version}"}


@router.get("/me/details")
def my_ip_details(request: Request) -> dict:
    """Optional local enrichment of the request peer; never accepts arbitrary IP input."""
    basic = my_ip(request)
    if basic["status"] != "ok":
        return {**basic, "intelligence": {"available": False, "country": None, "asn": None, "provider": None}}
    return {**basic, "intelligence": lookup(basic["ip"])}
