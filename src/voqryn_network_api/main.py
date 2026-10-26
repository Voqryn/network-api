"""HTTP entry point for the Voqryn Network API."""
from fastapi import FastAPI

app = FastAPI(title="Voqryn Network API", version="0.1.0", docs_url="/docs")


@app.get("/healthz", tags=["operations"])
def healthz() -> dict[str, str]:
    """Liveness only; no dependencies or outbound network calls."""
    return {"status": "ok"}


@app.get("/v1", tags=["meta"])
def api_version() -> dict[str, str]:
    return {"name": "voqryn-network-api", "version": "v1", "status": "development"}
