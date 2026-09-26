"""Synthetic review service used for an offline skill execution trial."""

import json


def check(draft, issues, review):
    errors = []
    claim_ids = {claim["id"] for claim in draft["claims"]}
    seen = set()
    covered = set()
    for row in review["claims"]:
        if row["claim_id"] not in claim_ids or row["claim_id"] in seen:
            errors.append("claim identity")
        seen.add(row["claim_id"])
        if row["support"] != "supported":
            errors.append("unsupported claim")
        if not row["evidence"]:
            errors.append("missing claim evidence")
        for issue_id in row["issue_ids"]:
            if issue_id not in issues:
                errors.append("unknown issue")
            covered.add(issue_id)
    for row in review["gaps"]:
        issue = issues.get(row["issue_id"])
        if issue is None or issue["resolved"]:
            errors.append("not an unresolved gap")
        covered.add(row["issue_id"])
    if seen != claim_ids:
        errors.append("claim coverage")
    if covered != set(issues):
        errors.append("issue coverage")
    return errors


def serve(payload):
    """JSON boundary, deliberately no ADK dependency or model inference."""
    request = json.loads(payload)
    errors = check(request["draft"], request["issues"], request["review"])
    return json.dumps({"accepted": not errors, "errors": errors})
