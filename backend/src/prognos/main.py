"""App-fabrikk (AD-14)."""

import logging
from pathlib import Path

from fastapi import FastAPI

from prognos.api.feil import registrer_feilhaandterere
from prognos.api.helse import ruter as helse_ruter
from prognos.konstanter import STANDARD_DB_STI
from prognos.oppstart import lag_lifespan

logging.basicConfig(level=logging.INFO)


def lag_app(db_sti: Path) -> FastAPI:
    db_sti = Path(db_sti)
    app = FastAPI(title="PROGNOS", lifespan=lag_lifespan(db_sti))
    app.state.db_sti = db_sti
    registrer_feilhaandterere(app)
    app.include_router(helse_ruter)
    return app


app = lag_app(STANDARD_DB_STI)
