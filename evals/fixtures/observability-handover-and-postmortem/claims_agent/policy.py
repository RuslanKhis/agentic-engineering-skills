"""Cover checks over the policy extract. No google.adk imports."""
from __future__ import annotations

POLICIES = {"KP-100231": {"holder": "synthetic holder", "cover": ["escape_of_water", "fire", "theft"], "excess_gbp": 250}}


def check_cover(policy_number: str, peril: str) -> dict:
    """Is the peril covered by the policy? Returns covered, excess and the policy's perils."""
    policy = POLICIES.get(policy_number)
    if policy is None:
        return {"status": "not_found", "message": f"No policy {policy_number}."}
    return {"status": "ok", "covered": peril in policy["cover"], "excess_gbp": policy["excess_gbp"]}
