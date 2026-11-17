from pathlib import Path

import httpx
from fastapi import HTTPException

from prognos.main import lag_app


async def test_helse_gir_ok(klient: httpx.AsyncClient) -> None:
    svar = await klient.get("/api/health")
    assert svar.status_code == 200
    assert svar.json() == {"status": "ok"}


async def test_ukjent_sti_gir_norsk_404(klient: httpx.AsyncClient) -> None:
    svar = await klient.get("/api/finnes-ikke")
    assert svar.status_code == 404
    assert svar.json() == {"detail": "Fant ikke ressursen."}


async def test_feil_metode_gir_norsk_detail(klient: httpx.AsyncClient) -> None:
    svar = await klient.post("/api/health")
    assert svar.status_code == 405
    assert svar.json() == {"detail": "Metoden er ikke tillatt for denne ressursen."}
    assert "GET" in svar.headers["allow"]


async def test_egen_detail_fra_rute_beholdes(db_sti: Path) -> None:
    app = lag_app(db_sti)

    @app.get("/api/test-feil")
    async def test_feil() -> None:
        raise HTTPException(status_code=404, detail="Fant ikke datasettet.")

    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as k:
            svar = await k.get("/api/test-feil")
    assert svar.status_code == 404
    assert svar.json() == {"detail": "Fant ikke datasettet."}
