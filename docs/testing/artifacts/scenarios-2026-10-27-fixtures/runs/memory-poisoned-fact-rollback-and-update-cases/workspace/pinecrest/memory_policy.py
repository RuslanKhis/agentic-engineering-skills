"""Write-side and audit rules for Memory Bank; no google.adk or vertexai imports."""
from __future__ import annotations

import re

# Memory never grants authority: offers, discounts and loyalty status belong to checkout/account
# systems, so no memory topic may hold them and a fact that claims one is treated as suspect.
ENTITLEMENT_RE = re.compile(
    r"\b(vip|discount|loyalty|coupon|promo(?:tion|code)?|free delivery|complimentary|waive[sd]?)\b|\d+\s*%",
    re.I)
# Text that addresses the assistant rather than describing the customer.
INJECTION_RE = re.compile(
    r"system note|note for (the )?assistant|ignore (all |any )?(previous|prior|above)|"
    r"remember this|instructions? (for|to) (the )?(assistant|ai|model)", re.I)


def is_entitlement_claim(fact: str) -> bool:
    return bool(ENTITLEMENT_RE.search(fact))


def looks_injected(text: str) -> bool:
    return bool(INJECTION_RE.search(text))


def generation_config(session_name: str, run_date: str) -> dict:
    """Generate config for one session. Revisions stay on and are labelled with their source,
    so a bad session can be found with revisions.list(filter=labels.session="...") and rolled back."""
    return {
        "wait_for_completion": False,
        "disable_memory_revisions": False,
        "revision_labels": {
            "source": "nightly_generate",
            "session": session_name.rsplit("/", 1)[-1],
            "run_date": run_date,
        },
    }


def newest_first(memories: list[dict]) -> list[dict]:
    """Order recalled memories by update_time (ISO strings) newest first, for the 'newest wins' rule."""
    return sorted(memories, key=lambda m: m.get("update_time", ""), reverse=True)
