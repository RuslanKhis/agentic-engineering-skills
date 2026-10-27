"""HTTP routes for the customer's own profile. Mounted by app/server.py."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import services
from app.auth import Principal
from app.profiles import ProfileNotFound, profile_view, rename

router = APIRouter(prefix="/api/profile")


def _principal() -> Principal:  # replaced by server.current_principal when mounted
    raise HTTPException(status_code=401)


class RenameIn(BaseModel):
    display_name: str


@router.get("")
def get_profile(principal: Principal = Depends(_principal)):
    try:
        return profile_view(services.get().store, principal)
    except ProfileNotFound:
        raise HTTPException(status_code=404, detail="not found")


@router.put("")
def put_profile(body: RenameIn, principal: Principal = Depends(_principal)):
    try:
        return rename(services.get().store, principal, body.display_name)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
