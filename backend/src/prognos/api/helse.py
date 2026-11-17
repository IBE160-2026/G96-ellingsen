"""Helsesjekk."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

ruter = APIRouter()


class HelseSvar(BaseModel):
    status: Literal["ok"]


@ruter.get("/api/health", response_model=HelseSvar)
async def helse() -> HelseSvar:
    return HelseSvar(status="ok")
