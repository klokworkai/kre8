# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

import asyncio
import os
import signal
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="kiosk", version="0.1.0", description="kre8 developer UI")

_static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(_static_dir / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "component": "kiosk"}


@app.post("/shutdown")
async def shutdown():
    asyncio.get_running_loop().call_later(
        0.5, lambda: os.kill(os.getpid(), signal.SIGTERM)
    )
    return {"ok": True}
