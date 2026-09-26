"""Synthetic review service used for an offline skill execution trial."""

import json


def check(draft, issues, review):
    """Return publication blockers for a review of the supplied trusted draft.

    A resolved, nonmaterial issue may be assessed independently of the decision
    claims. Material issues still require a supported claim and full registered
    evidence. Source IDs establish coverage, not semantic truth of a judgment.
    """
    errors = []
    claims = {claim["id"]: claim for claim in draft["claims"]}
    claim_ids = set(claims)
    seen = set()
    covered = set()
    issue_evidence = {issue_id: set() for issue_id in issues}
    for row in review["claims"]:
        if row["claim_id"] not in claim_ids or row["claim_id"] in seen:
            errors.append("claim identity")
        seen.add(row["claim_id"])
        claim = claims.get(row["claim_id"])
        if claim is not None:
            if (set(row["issue_ids"]) != set(claim["issue_ids"])
                    or len(row["issue_ids"]) != len(set(row["issue_ids"]))):
                errors.append("claim issue association")
            if (set(row["evidence"]) != set(claim["source_ids"])
                    or len(row["evidence"]) != len(set(row["evidence"]))):
                errors.append("claim evidence identity")
        if row["support"] != "supported":
            errors.append("unsupported claim")
        if not row["evidence"]:
            errors.append("missing claim evidence")
        for issue_id in row["issue_ids"]:
            if issue_id not in issues:
                errors.append("unknown issue")
            else:
                issue_evidence[issue_id].update(row["evidence"])
            covered.add(issue_id)
    for row in review.get("issue_dispositions", []):
        issue_id = row["issue_id"]
        issue = issues.get(issue_id)
        if issue is None:
            errors.append("unknown issue")
        else:
            if issue_id in covered:
                errors.append("duplicate issue disposition")
            if not issue["resolved"] or row["disposition"] != "nondecisive":
                errors.append("invalid issue disposition")
            if issue["material"]:
                errors.append("material issue requires claim")
            if row["support"] != "supported":
                errors.append("unsupported issue disposition")
            if (not row["evidence"]
                    or set(row["evidence"]) != set(issue["source_ids"])
                    or len(row["evidence"]) != len(set(row["evidence"]))):
                errors.append("issue evidence identity")
            issue_evidence[issue_id].update(row["evidence"])
        covered.add(issue_id)
    for row in review["gaps"]:
        issue = issues.get(row["issue_id"])
        if issue is None or issue["resolved"]:
            errors.append("not an unresolved gap")
        if row["issue_id"] in covered:
            errors.append("duplicate issue disposition")
        covered.add(row["issue_id"])
    for issue_id, issue in issues.items():
        if issue["material"] and not issue["resolved"]:
            errors.append("unresolved material issue")
        if (issue["resolved"] and issue_id in covered
                and (not issue["source_ids"]
                     or not set(issue["source_ids"]) <= issue_evidence[issue_id])):
            errors.append("missing required issue evidence")
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
