"""Site tools. No google.adk imports so the unit tests run without the SDK."""
from __future__ import annotations

from datetime import date

SITES = {
    "NW-0417": {"name": "Hollins Farm mast", "equipment": ["3 sector antennas", "BBU rack", "48V battery bank"],
                "access": "Farm gate code from the landowner; call 30 minutes ahead.", "hazards": ["livestock", "working at height"]},
    "NW-0522": {"name": "Canal Street rooftop", "equipment": ["2 small cells", "fibre splice box"],
                "access": "Building security desk; keys in the plant room safe.", "hazards": ["fragile roof lights"]},
}

VISITS: list[dict] = []


def get_site(site_id: str) -> dict:
    """Get a site's equipment, access arrangements and hazards.

    Args:
        site_id: Fieldline site ID such as "NW-0417".
    """
    site = SITES.get(site_id.strip().upper())
    if site is None:
        return {"status": "not_found", "message": f"No site {site_id}."}
    return {"status": "ok", "site_id": site_id.strip().upper(), **site}


def log_visit(site_id: str, work_done: str, tool_context) -> dict:
    """Log a completed visit for the engineer who is signed in.

    Args:
        site_id: The site visited.
        work_done: One or two sentences on what was done and anything left open.
    """
    if site_id.strip().upper() not in SITES:
        return {"status": "error", "message": f"No site {site_id}."}
    entry = {"site_id": site_id.strip().upper(), "engineer_id": tool_context.user_id,
             "work_done": work_done, "date": date.today().isoformat()}
    VISITS.append(entry)
    return {"status": "logged", **entry}
