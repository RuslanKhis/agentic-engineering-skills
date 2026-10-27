"""Deterministic checks the review stage applies before the model review (pipeline/stages.py)."""
from __future__ import annotations

import re

# The applicant's own documents.
APPLICATION_PROSE = {"APP-FORM", "DAS", "AGT"}

# Words that show a policy is engaged by the application.
POLICY_TRIGGERS = {
    "LP-H4": ["extension", "rear", "side window"],
    "LP-T2": ["parking", "crossover", "garage"],
    "LP-T2-1": ["parking", "bedrooms"],
    "LP-ENV3": ["root protection area"],
}


def documents_cited(draft: dict) -> set[str]:
    ids = {c["span_id"] for c in draft["citations"]}
    for reason in draft["reasons"]:
        ids.update(reason["citations"])
    return {span_id.split("@", 1)[0] for span_id in ids}


def coverage_findings(draft: dict, case: dict) -> list[str]:
    """Every application document must be cited; once all are, the draft has nothing left open."""
    findings = []
    missing = {d["doc_id"] for d in case["documents"]} - documents_cited(draft)
    for doc_id in sorted(missing):
        findings.append(f"source {doc_id} is not accounted for")
    if not missing and draft["gaps"]:
        findings.append("gaps listed although every source is accounted for; remove them")
    return findings


def applicable_policies(case: dict) -> set[str]:
    prose = " ".join(page["text"] for doc in case["documents"] if doc["doc_id"] in APPLICATION_PROSE
                     for page in doc["pages"]).lower()
    return {policy for policy, words in POLICY_TRIGGERS.items()
            if any(re.search(r"\b" + re.escape(w) + r"\b", prose) for w in words)}


def policy_findings(draft: dict, case: dict) -> list[str]:
    applicable = applicable_policies(case)
    return [f"{doc} is cited but not applicable to this application"
            for doc in sorted(documents_cited(draft)) if doc in POLICY_TRIGGERS and doc not in applicable]


def review_findings(draft: dict, case: dict) -> list[str]:
    return coverage_findings(draft, case) + policy_findings(draft, case)
