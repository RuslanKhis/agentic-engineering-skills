"""Monthly golden-question report.

Two steps, so the cloud part and the analysis part can be run apart:
  fetch   (needs the SDK and BigQuery) writes the SDK's drift result to JSON
  render  (offline) joins that JSON with the golden CSV and an optional pass
          history, and writes a Markdown report

A section whose input is missing says "not available"; it is never reported
as zero findings.
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date

ORDER_ID = re.compile(r"\bHO-\d+\b", re.IGNORECASE)


def normalise(question):
    """Case-fold, mask order ids and punctuation so template twins compare equal."""
    text = ORDER_ID.sub("<order>", question.lower())
    return " ".join(re.sub(r"[^\w<> ]", " ", text).split())


def load_golden(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def template_groups(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[normalise(row["question"])].append(row["question_id"])
    return dict(groups)


def stale_questions(rows, today, max_age_days):
    return sorted(r["question_id"] for r in rows
                  if (today - date.fromisoformat(r["reviewed_on"])).days > max_age_days)


def saturated(pass_history, min_runs):
    """Questions that passed every one of at least `min_runs` recorded runs."""
    return sorted(q for q, runs in pass_history.items() if len(runs) >= min_runs and all(runs))


def fetch_drift(project_id, dataset_id, golden_table, agent_id, start_time):
    """Run the SDK's drift detection (import is lazy; not exercised offline)."""
    from bigquery_agent_analytics import Client, TraceFilter  # noqa: PLC0415
    client = Client(project_id=project_id, dataset_id=dataset_id)
    rep = client.drift_detection(golden_dataset=golden_table,
                                 filters=TraceFilter(agent_id=agent_id, start_time=start_time))
    return {"coverage_percentage": rep.coverage_percentage,
            "uncovered_questions": list(rep.uncovered_questions),
            "details": rep.details}


def render(rows, today, drift=None, pass_history=None, max_age_days=90, min_runs=10):
    groups = template_groups(rows)
    dupes = {k: v for k, v in groups.items() if len(v) > 1}
    stale = stale_questions(rows, today, max_age_days)
    out = [f"# Golden question report, {today.isoformat()}", "",
           f"- Questions: {len(rows)}; distinct after masking order ids: {len(groups)}",
           f"- Topics: {len({r['topic'] for r in rows})}", "",
           "## Coverage of real traffic", ""]
    if drift is None:
        out.append("Not available: no drift result supplied (run `fetch` against BigQuery first).")
    else:
        out.append(f"Coverage reported by the SDK: {drift['coverage_percentage']:.1f}%. "
                   f"Its details: `{json.dumps(drift.get('details'), sort_keys=True)}`.")
        out.append(f"Golden questions matching no production question: "
                   f"{len(drift['uncovered_questions'])}.")
        out += [f"- {q}" for q in drift["uncovered_questions"]]
        out.append("")
        out.append(f"Read the percentage against {len(groups)} distinct questions, not {len(rows)}.")
    out += ["", "## Questions that tell us nothing new", "",
            f"### Template duplicates ({sum(len(v) - 1 for v in dupes.values())} redundant)", ""]
    out += [f"- `{k}`: {', '.join(v)}" for k, v in sorted(dupes.items())] or ["None."]
    out += ["", "### Saturated (passed every recent run)", ""]
    if pass_history is None:
        out.append("Not available: no pass history is recorded for golden questions yet.")
    else:
        sat = saturated(pass_history, min_runs)
        out += [f"- {q}" for q in sat] or [f"None with at least {min_runs} recorded runs."]
    out += ["", f"### Review older than {max_age_days} days", ""]
    out += [", ".join(stale)] if stale else ["None."]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    for name in ("project-id", "dataset-id", "golden-table", "start-time", "out"):
        f.add_argument(f"--{name}", required=True)
    f.add_argument("--agent-id")
    r = sub.add_parser("render")
    r.add_argument("--golden", default="bq/golden_questions.csv")
    r.add_argument("--drift")
    r.add_argument("--pass-history")
    r.add_argument("--today", default=date.today().isoformat())
    r.add_argument("--max-age-days", type=int, default=90)
    r.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "fetch":
        try:
            data = fetch_drift(args.project_id, args.dataset_id, args.golden_table,
                               args.agent_id, args.start_time)
        except Exception as exc:  # BigQuery, auth or SDK problems: no report, non-zero exit
            print(f"fetch failed: {type(exc).__name__}", file=sys.stderr)
            return 2
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        return 0
    load = lambda p: json.load(open(p, encoding="utf-8")) if p else None  # noqa: E731
    text = render(load_golden(args.golden), date.fromisoformat(args.today), load(args.drift),
                  load(args.pass_history), args.max_age_days)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
