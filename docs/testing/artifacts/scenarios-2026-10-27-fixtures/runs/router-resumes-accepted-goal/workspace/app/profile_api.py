"""HTTP routes for the customer's own profile. Mounted by app/server.py."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import preferences, services
from app.auth import Principal
from app.profiles import ProfileNotFound, profile_view, rename

router = APIRouter(prefix="/api/profile")


def _principal() -> Principal:  # replaced by server.current_principal when mounted
    raise HTTPException(status_code=401)


class RenameIn(BaseModel):
    display_name: str


class LanguageIn(BaseModel):
    language: str


@router.get("/language")
def get_language_route(principal: Principal = Depends(_principal)):
    try:
        return preferences.get_language(services.get().store, principal)
    except preferences.PreferenceNotFound:
        raise HTTPException(status_code=404, detail="not found")


@router.put("/language")
def put_language_route(body: LanguageIn, principal: Principal = Depends(_principal)):
    try:
        return preferences.save_language(services.get().store, principal, body.language)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.delete("/language", status_code=204)
def delete_language_route(principal: Principal = Depends(_principal)):
    try:
        preferences.forget_language(services.get().store, principal)
    except preferences.PreferenceNotFound:
        raise HTTPException(status_code=404, detail="not found")


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
