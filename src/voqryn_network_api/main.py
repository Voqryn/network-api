"""HTTP entry point for the Voqryn Network API."""
from fastapi import FastAPI
from voqryn_network_api.dns import router as dns_router
from voqryn_network_api.domain_check import router as domain_router
from voqryn_network_api.rdap import router as rdap_router

app = FastAPI(title="Voqryn Network API", version="0.1.0", docs_url="/docs")
app.include_router(dns_router)
app.include_router(domain_router)
app.include_router(rdap_router)


@app.get("/healthz", tags=["operations"])
def healthz() -> dict[str, str]:
    """Liveness only; no dependencies or outbound network calls."""
    return {"status": "ok"}


@app.get("/v1", tags=["meta"])
def api_version() -> dict[str, str]:
    return {"name": "voqryn-network-api", "version": "v1", "status": "development"}
