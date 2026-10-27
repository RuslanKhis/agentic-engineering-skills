"""Offline completeness controls for the local policy retriever.

Builds adapter-style observations from document-coverage.json (synthetic extracted
pages, no PDF bytes) and checks that the skill's scorer exposes each missing-evidence
state. Expected sections stay in the fixture's `questions` block, never in observations.

Usage: python3 -I coverage_controls.py SCORER_PATH [FIXTURE_PATH]
Exit 0: every control behaved as expected. Exit 1: a control was misjudged. Exit 2: bad input.
"""

import importlib.util
import json
import sys
from pathlib import Path

ALL_DOCS = ["main-policy", "supplement-s1", "notice-n1"]
MAIN_PAGES = ["route-rule", "table-first", "table-continuation"]


def load_scorer(path):
    spec = importlib.util.spec_from_file_location("score_document_coverage", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.score


def observation(fixture, hit_keys, queries, *, extracted=None, documents=None, hit_text=None):
    """Record what a trusted adapter would: extraction per segment plus returned passages."""
    texts = {key: seg["text"] for key, seg in fixture["segments"].items()}
    extracted = texts if extracted is None else extracted
    hit_text = hit_text or {}
    return {
        "available_documents": ALL_DOCS if documents is None else documents,
        "extracted_segments": extracted,
        "hits": [{"segment": k, "text": hit_text.get(k, texts[k])} for k in hit_keys],
        "query_origin": "manual_golden",
        "queries": queries,
    }


def controls(fixture):
    texts = {key: seg["text"] for key, seg in fixture["segments"].items()}
    cont = texts["table-continuation"]
    # name: (question, observation, pass, doc coverage, section coverage, {(segment, reason)})
    return {
        "complete_text_control": (
            "maintenance-route",
            observation(fixture, MAIN_PAGES + ["maintenance-exception"],
                        ["raised route maintenance exception width"]),
            True, (2, 2), (3, 3), set()),
        "main_policy_only": (
            "maintenance-route",
            observation(fixture, MAIN_PAGES, ["route width table 1"]),
            False, (1, 2), (2, 3), {("maintenance-exception", "query_miss")}),
        "contents_only": (
            "maintenance-route",
            observation(fixture, ["contents"], ["route requirements contents"]),
            False, (1, 2), (0, 3),
            {(k, "query_miss") for k in MAIN_PAGES + ["maintenance-exception"]}),
        "incomplete_table_not_returned": (
            "complete-table",
            observation(fixture, ["table-first"], ["Table 1 route widths"]),
            False, (1, 1), (0, 1), {("table-continuation", "query_miss")}),
        "incomplete_table_truncated_extraction": (
            "complete-table",
            observation(fixture, ["table-first", "table-continuation"], ["Table 1 route widths"],
                        extracted={**texts, "table-continuation": cont[: len(cont) // 2]},
                        hit_text={"table-continuation": cont[: len(cont) // 2]}),
            False, (1, 1), (0, 1), {("table-continuation", "section_truncation")}),
        "empty_text_extraction": (
            "maintenance-route",
            observation(fixture, MAIN_PAGES, ["maintenance exception"],
                        extracted={**texts, "maintenance-exception": ""}),
            False, (1, 2), (2, 3), {("maintenance-exception", "empty_extraction")}),
        "absent_supplement": (
            "maintenance-route",
            observation(fixture, MAIN_PAGES, ["maintenance exception"],
                        documents=["main-policy", "notice-n1"],
                        extracted={k: v for k, v in texts.items() if k != "maintenance-exception"}),
            False, (1, 2), (2, 3), {("maintenance-exception", "absent_content")}),
        "empty_image_page": (
            "closure-status",
            observation(fixture, [], ["Route Cedar closure Notice N1"],
                        extracted={**texts, "closure-notice": ""}),
            False, (0, 1), (0, 1),
            {("closure-notice", "empty_extraction"), ("closure-notice", "unviewed_visuals")}),
    }


def main(argv):
    if not 2 <= len(argv) <= 3:
        print(__doc__, file=sys.stderr)
        return 2
    here = Path(__file__).resolve().parent
    try:
        score = load_scorer(argv[1])
        fixture = json.loads(Path(argv[2] if len(argv) == 3 else here / "document-coverage.json")
                             .read_text(encoding="utf-8"))
        cases = controls(fixture)
    except (OSError, ValueError, KeyError, AttributeError, ImportError) as exc:
        print(f"invalid input: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    failures = 0
    for name, (question, obs, want_pass, docs, secs, want_diag) in cases.items():
        report = score(fixture, question, obs)
        got = {
            "pass": report["retrieval_pass"],
            "docs": (report["document_coverage"]["covered"], report["document_coverage"]["required"]),
            "sections": (report["operative_section_coverage"]["covered"],
                         report["operative_section_coverage"]["required"]),
            "diag": {(d["segment"], d["reason"]) for d in report["diagnoses"]},
        }
        want = {"pass": want_pass, "docs": docs, "sections": secs, "diag": want_diag}
        ok = got == want and not report["invalid_hit_segments"]
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: docs {got['docs']} sections {got['sections']} "
              f"diag {sorted(got['diag'])}")
        if not ok:
            print(f"     expected {want}")

    # A claimed review must not turn the text-only placeholder into evidence.
    claimed = observation(fixture, [], ["Route Cedar closure"])
    claimed["visual_review_claimed"] = True
    report = score(fixture, "closure-status", claimed)
    ok = (not report["retrieval_pass"]
          and any(d["reason"] == "unviewed_visuals" for d in report["diagnoses"]))
    failures += not ok
    print(f"{'ok  ' if ok else 'FAIL'} claimed_visual_review_still_unresolved")
    print(f"{failures} failing control(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
