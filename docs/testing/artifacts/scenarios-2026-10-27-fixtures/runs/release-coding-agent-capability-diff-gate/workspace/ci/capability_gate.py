"""Decides whether a pull request changed what the production agent can do.

Reads the JSON that `inspect_security_surface.py --compare base.json` wrote and
the inspector's exit status. Prints a verdict line and exits:

  0  no capability change, nothing unread that this pull request touched
  1  a human must approve (capability changed, or a changed file is one the
     inspector could not read, such as the Workflow graph in app/reporting.py)
  2  NOT RUN: the inspector failed or its output is unusable; never a pass

Standard library only, and no google.adk import.
"""
from __future__ import annotations

import argparse
import json
import sys

NEEDS_REVIEW = 1
NOT_RUN = 2


def decide(status: int, report: dict, changed_files: list[str]) -> tuple[int, str]:
    if status == 1:
        changes = report.get("capability_changes") or []
        return NEEDS_REVIEW, f"capability changed ({len(changes)} listed change(s))"
    if status == 3:
        touched = sorted(set(report.get("unread_paths") or []) & set(changed_files))
        if touched:
            return NEEDS_REVIEW, "changed file(s) the inspector cannot read: " + ", ".join(touched)
        return 0, "partial scan, but no changed file is in unread_paths"
    if status == 0:
        return 0, "no capability change"
    return NOT_RUN, f"inspector exited {status}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="head.json from --compare")
    parser.add_argument("--status", type=int, required=True, help="inspector exit status")
    parser.add_argument("--changed-files", required=True, help="file with one changed path per line")
    args = parser.parse_args(argv)
    try:
        with open(args.report, encoding="utf-8") as fh:
            report = json.load(fh)
        with open(args.changed_files, encoding="utf-8") as fh:
            changed = [line.strip() for line in fh if line.strip()]
    except (OSError, ValueError) as exc:
        print(f"NOT RUN: {exc}")
        return NOT_RUN
    code, reason = decide(args.status, report, changed)
    print({0: "PASS", NEEDS_REVIEW: "NEEDS HUMAN APPROVAL", NOT_RUN: "NOT RUN"}[code] + ": " + reason)
    return code


if __name__ == "__main__":
    sys.exit(main())
