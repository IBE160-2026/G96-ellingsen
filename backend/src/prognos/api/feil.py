"""Norske feilsvar på formen `{detail}` (AD-9)."""

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

NORSKE_MELDINGER: dict[int, str] = {
    400: "Ugyldig forespørsel.",
    404: "Fant ikke ressursen.",
    405: "Metoden er ikke tillatt for denne ressursen.",
    500: "Det oppstod en intern feil.",
}

GENERISK_MELDING = "Forespørselen kunne ikke behandles."


def norsk_melding(statuskode: int) -> str:
    return NORSKE_MELDINGER.get(statuskode, GENERISK_MELDING)


def _standardfrase(statuskode: int) -> str | None:
    try:
        return HTTPStatus(statuskode).phrase
    except ValueError:
        return None


async def http_feil(request: Request, feil: StarletteHTTPException) -> JSONResponse:
    # Egen tekst fra en rute beholdes; Starlettes engelske standardfrase byttes ut.
    if feil.detail and feil.detail != _standardfrase(feil.status_code):
        detail = feil.detail
    else:
        detail = norsk_melding(feil.status_code)
    return JSONResponse(
        status_code=feil.status_code,
        content={"detail": detail},
        headers=getattr(feil, "headers", None),
    )


def registrer_feilhaandterere(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_feil)
