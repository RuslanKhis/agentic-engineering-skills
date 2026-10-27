"""The customer's own profile, as the account page shows it."""
from __future__ import annotations

from app.auth import Principal
from app.store import Store


class ProfileNotFound(Exception):
    pass


def profile_view(store: Store, principal: Principal) -> dict:
    """The signed-in customer's profile. Only ever the caller's own row."""
    row = store.get_profile(principal.user_id)
    if row is None:
        raise ProfileNotFound(principal.user_id)
    return {"user_id": row["user_id"], "display_name": row["display_name"]}


def rename(store: Store, principal: Principal, display_name: str) -> dict:
    name = display_name.strip()
    if not 1 <= len(name) <= 60:
        raise ValueError("display name must be 1 to 60 characters")
    store.upsert_profile(principal.user_id, name)
    return profile_view(store, principal)
