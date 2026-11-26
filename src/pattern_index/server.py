"""HTTP server for patterns: /healthz, /readyz, /mcp."""

from __future__ import annotations

import hmac
import os
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from .mcp_server import build_server

PROBE_PATHS = frozenset({"/health", "/healthz", "/ready", "/readyz"})


def _check_ready(data_dir: Path) -> dict[str, object]:
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        probe = data_dir / ".readyz-probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return {"status": "ready", "data_dir": str(data_dir)}
    except Exception as exc:  # pragma: no cover
        return {"status": "not_ready", "data_dir": str(data_dir), "error": str(exc)}


def _build_http_app(mcp_instance: Any) -> FastAPI:
    data_dir = Path(os.environ.get("FLEET_DATA_DIR", "/data"))
    streamable_app = mcp_instance.streamable_http_app(streamable_http_path="/mcp", json_response=True)
    lifespan = getattr(streamable_app.router, "lifespan_context", None)
    app = FastAPI(title="patterns", version="0.1.0", lifespan=lifespan)

    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        path = request.url.path.rstrip("/") or "/"
        if path in PROBE_PATHS:
            return await call_next(request)
        fleet_key = os.environ.get("FLEET_API_KEY")
        if fleet_key:
            auth_header = request.headers.get("authorization", "")
            if not auth_header.startswith("Bearer "):
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)
            token = auth_header[len("Bearer "):].strip()
            if not hmac.compare_digest(token.encode(), fleet_key.encode()):
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)
        return await call_next(request)

    @app.get("/health")
    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready")
    @app.get("/readyz")
    def ready(response: Response) -> dict[str, object]:
        payload = _check_ready(data_dir)
        if payload["status"] != "ready":
            response.status_code = 503
        return payload

    app.mount("/", streamable_app)
    return app


def run(host: str = "0.0.0.0", port: int = 8080) -> None:
    uvicorn.run(_build_http_app(build_server()), host=host, port=port, log_level="info")
