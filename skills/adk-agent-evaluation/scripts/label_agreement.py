#!/usr/bin/env python3
"""Check expert labels for agreement and an LLM judge against adjudicated labels. Standard library only.

Reads one or more label files, CSV or JSON Lines, one row per verdict with the
fields ``case_id``, ``criterion``, ``rater`` and ``label`` (``pass`` or
``fail``). Optional fields: ``critique``, ``labeller`` (the person or role
behind an ``adjudicated`` verdict), ``criteria_version``, ``labelled_at``
(ISO date) and ``split`` (``train``, ``dev`` or ``test``).
The gold-set schema is ``assets/gold-set-schema.md``.

Agreement mode (always): for every criterion and every pair of expert raters
(all raters except the judge and the reference), the cases both labelled,
percent agreement, Cohen's kappa and the fail share; every disagreement is
listed for adjudication. A kappa below ``--min-kappa`` or undefined (both
raters gave one label to every case) needs attention.

Judge mode (``--judge NAME``): the judge's labels against the reference
rater's (``--reference``, default ``adjudicated``), per criterion, with
``fail`` as the positive class: TPR is the share of reference failures the
judge fails, TNR the share of reference passes the judge passes. Raw
agreement is printed for context only. With a ``split`` column the held-out
``test`` split is used unless ``--split`` says otherwise; without one the
report says the cases may have been used to tune the judge. Rates are
refused (NOT REPORTED) when either class has fewer than ``--min-per-class``
cases, and flagged when either rate falls below its threshold.

With ``--reference consensus`` (before any adjudication) the reference is
the cases every expert labelled alike; it leaves out the hard cases, so the
rates are reported as indicative. ``--criteria-version`` restricts every
computation to labels given under one version, to compare agreement before
and after a criteria change.

A human rater's labels recorded under more than one ``criteria_version`` for
a criterion are reported as criteria drift: the labels under the older
versions need re-review before they count. Reference labels without
``labeller``, ``criteria_version`` or ``labelled_at`` are reported as missing
provenance, field by field; judge rows without a ``criteria_version``, or at a
version other than the reference's latest, are reported too.
Versions are compared as text, so name them so that they sort (v01, v02 or
dates).

Critiques can hold customer text; they are printed only with
``--show-critiques``. Exit status: 0 nothing needs attention, 1 at least one
finding (low or undefined kappa, a judge rate below threshold, judge metrics
refused for too few cases, criteria drift), 2 unreadable or invalid input.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
import io
import itertools
import json
from pathlib import Path
import sys

REQUIRED = ("case_id", "criterion", "rater", "label")
LABELS = ("pass", "fail")
SPLITS = ("train", "dev", "test")
CONSENSUS = "consensus"
MAX_BYTES = 20 * 1024 * 1024


class InputError(Exception):
    pass


def read_rows(path: Path) -> list[dict]:
    try:
        if path.stat().st_size > MAX_BYTES:
            raise InputError(f"{path}: larger than {MAX_BYTES // (1024 * 1024)} MB")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"{path}: cannot read: {exc}") from exc
    rows = []
    if path.suffix.lower() in (".jsonl", ".ndjson") or text.lstrip().startswith("{"):
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except ValueError as exc:
                raise InputError(f"{path}:{number}: not JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise InputError(f"{path}:{number}: each line must be a JSON object")
            rows.append((number, record))
    else:
        reader = csv.DictReader(io.StringIO(text))
        if reader.fieldnames is None:
            raise InputError(f"{path}: empty CSV")
        missing = [field for field in REQUIRED if field not in reader.fieldnames]
        if missing:
            raise InputError(f"{path}: CSV header lacks {', '.join(missing)}")
        rows = [(number, record) for number, record in enumerate(reader, start=2)]
    checked = []
    for number, record in rows:
        where = f"{path}:{number}"
        values = {key: str(record.get(key) or "").strip() for key in
                  REQUIRED + ("critique", "labeller", "criteria_version", "labelled_at", "split")}
        for key in REQUIRED:
            if not values[key]:
                raise InputError(f"{where}: missing {key}")
        values["label"] = values["label"].lower()
        if values["label"] not in LABELS:
            raise InputError(f"{where}: label must be pass or fail, got {values['label']!r}")
        values["split"] = values["split"].lower()
        if values["split"] and values["split"] not in SPLITS:
            raise InputError(f"{where}: split must be one of {', '.join(SPLITS)}, got {values['split']!r}")
        if values["labelled_at"]:
            try:
                date.fromisoformat(values["labelled_at"][:10])
            except ValueError as exc:
                raise InputError(f"{where}: labelled_at is not an ISO date: {values['labelled_at']!r}") from exc
        values["where"] = where
        checked.append(values)
    return checked


def index_labels(rows: list[dict]) -> dict:
    """{criterion: {rater: {case_id: row}}}, refusing a second verdict for the same cell."""
    table: dict = {}
    for row in rows:
        cell = table.setdefault(row["criterion"], {}).setdefault(row["rater"], {})
        if row["case_id"] in cell:
            raise InputError(f"{row['where']}: second label from {row['rater']} for case {row['case_id']} "
                             f"on {row['criterion']} (first at {cell[row['case_id']]['where']}); keep one")
        cell[row["case_id"]] = row
    return table


def cohen_kappa(first: list[str], second: list[str]) -> float | None:
    """Cohen's kappa for two raters on the same cases; None when expected agreement is 1."""
    total = len(first)
    observed = sum(a == b for a, b in zip(first, second)) / total
    expected = sum((first.count(label) / total) * (second.count(label) / total) for label in LABELS)
    if expected >= 1.0:
        return None
    return (observed - expected) / (1.0 - expected)


def agreement(table: dict, excluded: set[str], min_kappa: float) -> tuple[list[dict], list[str]]:
    results, findings = [], []
    for criterion in sorted(table):
        raters = sorted(rater for rater in table[criterion] if rater not in excluded)
        if len(raters) < 2:
            continue
        for first, second in itertools.combinations(raters, 2):
            shared = sorted(set(table[criterion][first]) & set(table[criterion][second]))
            if not shared:
                continue
            a = [table[criterion][first][case]["label"] for case in shared]
            b = [table[criterion][second][case]["label"] for case in shared]
            kappa = cohen_kappa(a, b)
            agree = sum(x == y for x, y in zip(a, b)) / len(shared)
            fail_share = (a.count("fail") + b.count("fail")) / (2 * len(shared))
            disagreements = [{"case_id": case, first: table[criterion][first][case]["label"],
                              second: table[criterion][second][case]["label"],
                              "critiques": {first: table[criterion][first][case]["critique"],
                                            second: table[criterion][second][case]["critique"]}}
                             for case, x, y in zip(shared, a, b) if x != y]
            result = {"criterion": criterion, "raters": [first, second], "cases": len(shared),
                      "percent_agreement": round(100 * agree, 1),
                      "kappa": None if kappa is None else round(kappa, 3),
                      "fail_share": round(fail_share, 3), "disagreements": disagreements}
            results.append(result)
            label = f"{criterion}, {first} and {second}"
            if kappa is None:
                findings.append(f"{label}: kappa undefined on {len(shared)} cases (each rater gave one label "
                                f"to every case); add cases of the other class before judging agreement")
            elif kappa < min_kappa:
                hint = (" with high raw agreement: the classes are imbalanced, so add cases of the rarer class"
                        if agree >= 0.8 else "; adjudicate the disagreements and sharpen the criterion's definition")
                findings.append(f"{label}: kappa {kappa:.2f} below {min_kappa:.2f} on {len(shared)} cases{hint}")
    return results, findings


def add_consensus(table: dict, excluded: set[str]) -> None:
    """A provisional reference: cases every expert labelled, with one label from all of them."""
    for criterion, raters in table.items():
        experts = [rater for rater in raters if rater not in excluded]
        if len(experts) < 2:
            continue
        shared = set.intersection(*(set(raters[rater]) for rater in experts))
        consensus = {}
        for case in shared:
            labels = {raters[rater][case]["label"] for rater in experts}
            if len(labels) == 1:
                first = raters[experts[0]][case]
                consensus[case] = dict(first, rater=CONSENSUS, split="", critique="")
        raters[CONSENSUS] = consensus


def judge_metrics(table: dict, judge: str, reference: str, split: str | None,
                  min_per_class: int, min_tpr: float, min_tnr: float) -> tuple[list[dict], list[str], list[str]]:
    results, findings, notes = [], [], []
    seen_judge = False
    for criterion in sorted(table):
        judged = table[criterion].get(judge, {})
        gold = table[criterion].get(reference, {})
        if not judged:
            continue
        seen_judge = True
        if not gold:
            findings.append(f"{criterion}: no {reference!r} labels to compare the judge with; adjudicate first")
            continue
        has_split = any(row["split"] for row in gold.values())
        chosen = split if split else ("test" if has_split else None)
        cases = sorted(case for case in set(judged) & set(gold)
                       if chosen is None or gold[case]["split"] == chosen)
        unmatched = len(set(judged) - set(gold))
        if reference == CONSENSUS:
            notes.append(f"{criterion}: reference is the cases all experts agreed on, which leaves out the hard "
                         f"ones; the rates are indicative, not a calibration")
        elif not has_split:
            notes.append(f"{criterion}: reference labels carry no split; these cases may have tuned the judge, "
                         f"so the rates are not a held-out result")
        elif chosen in ("train", "dev"):
            notes.append(f"{criterion}: rates on the {chosen} split measure fit, not held-out performance")
        positives = [case for case in cases if gold[case]["label"] == "fail"]
        negatives = [case for case in cases if gold[case]["label"] == "pass"]
        result = {"criterion": criterion, "split": chosen or "no", "cases": len(cases),
                  "reference_fails": len(positives), "reference_passes": len(negatives),
                  "judge_without_reference": unmatched}
        if len(positives) < min_per_class or len(negatives) < min_per_class:
            result["status"] = "NOT REPORTED"
            findings.append(f"{criterion}: judge rates NOT REPORTED: {len(positives)} reference fails and "
                            f"{len(negatives)} reference passes on the {chosen + ' split' if chosen else 'unsplit'} cases; "
                            f"need at least {min_per_class} of each")
            results.append(result)
            continue
        tp = sum(judged[case]["label"] == "fail" for case in positives)
        tn = sum(judged[case]["label"] == "pass" for case in negatives)
        tpr, tnr = tp / len(positives), tn / len(negatives)
        missed = [case for case in positives if judged[case]["label"] == "pass"]
        false_alarms = [case for case in negatives if judged[case]["label"] == "fail"]
        result.update(status="reported", tpr=round(tpr, 3), tnr=round(tnr, 3),
                      raw_agreement=round((tp + tn) / len(cases), 3),
                      missed_failures=missed, false_alarms=false_alarms)
        results.append(result)
        if tpr < min_tpr:
            findings.append(f"{criterion}: judge TPR {tpr:.2f} below {min_tpr:.2f}: it passes "
                            f"{len(missed)} of {len(positives)} reference failures")
        if tnr < min_tnr:
            findings.append(f"{criterion}: judge TNR {tnr:.2f} below {min_tnr:.2f}: it fails "
                            f"{len(false_alarms)} of {len(negatives)} reference passes")
    if not seen_judge:
        findings.append(f"no labels from the judge rater {judge!r}")
    return results, findings, notes


def drift(table: dict, reference: str, judge: str | None) -> list[str]:
    """Criteria drift per human rater, and gold-set provenance on the reference labels."""
    findings = []
    for criterion in sorted(table):
        for rater in sorted(table[criterion]):
            if rater in (judge, CONSENSUS):
                continue
            labelled = list(table[criterion][rater].values())
            versions = sorted({row["criteria_version"] for row in labelled if row["criteria_version"]})
            if len(versions) > 1:
                latest = versions[-1]
                older = sum(1 for row in labelled if row["criteria_version"] and row["criteria_version"] != latest)
                findings.append(f"{criterion}: {rater} labels span criteria versions {', '.join(versions)}; "
                                f"re-review the {older} labelled under an older version against {latest}")
        rows = list(table[criterion].get(reference, {}).values())
        for field in ("labeller", "criteria_version", "labelled_at"):
            missing = 0 if reference == CONSENSUS else sum(1 for row in rows if not row[field])
            if missing:
                findings.append(f"{criterion}: {missing} {reference} labels lack {field}; gold rows need labeller, "
                                f"criteria_version and labelled_at for provenance")
        if judge:
            judged = table[criterion].get(judge, {}).values()
            judge_versions = {row["criteria_version"] for row in judged if row["criteria_version"]}
            gold_versions = sorted({row["criteria_version"] for row in rows if row["criteria_version"]})
            if judged and not judge_versions:
                findings.append(f"{criterion}: {judge} rows carry no criteria_version; record which criteria "
                                f"its prompt implements")
            elif gold_versions and judge_versions - {gold_versions[-1]}:
                findings.append(f"{criterion}: {judge} implements criteria {', '.join(sorted(judge_versions))} but "
                                f"the reference is at {gold_versions[-1]}; rewrite the judge prompt before scoring")
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--labels", type=Path, nargs="+", required=True, help="CSV or JSONL label files")
    parser.add_argument("--judge", help="rater name of the LLM judge; enables judge mode")
    parser.add_argument("--reference", default="adjudicated",
                        help="rater name of the adjudicated labels, or 'consensus' for the cases all experts agreed "
                             "on (indicative only, before adjudication)")
    parser.add_argument("--criteria-version", help="use only labels given under this criteria version")
    parser.add_argument("--split", choices=SPLITS, help="split to score the judge on (default: test when present)")
    parser.add_argument("--min-kappa", type=float, default=0.6, help="kappa below this needs attention")
    parser.add_argument("--min-per-class", type=int, default=30,
                        help="reference fails and passes each needed before judge rates are reported")
    parser.add_argument("--min-tpr", type=float, default=0.8)
    parser.add_argument("--min-tnr", type=float, default=0.8)
    parser.add_argument("--show-critiques", action="store_true", help="print critiques beside disagreements")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)
    try:
        rows = [row for path in args.labels for row in read_rows(path)]
        if not rows:
            raise InputError("no label rows found")
        table = index_labels(rows)
    except InputError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    if args.criteria_version:
        table = {criterion: {rater: {case: row for case, row in cases.items()
                                     if row["criteria_version"] == args.criteria_version}
                             for rater, cases in raters.items()}
                 for criterion, raters in table.items()}
    excluded = {args.reference} | ({args.judge} if args.judge else set())
    pairs, findings = agreement(table, excluded, args.min_kappa)
    if args.reference == CONSENSUS:
        add_consensus(table, excluded)
    report = {"agreement": pairs, "judge": [], "notes": [], "findings": findings}
    if args.judge:
        judged, judge_findings, notes = judge_metrics(table, args.judge, args.reference, args.split,
                                                      args.min_per_class, args.min_tpr, args.min_tnr)
        report["judge"], report["notes"] = judged, notes
        findings.extend(judge_findings)
    findings.extend(drift(table, args.reference, args.judge))
    if not pairs:
        message = ("no criterion has two expert raters on shared cases, after excluding the judge and "
                   f"the reference {args.reference!r}")
        (report["notes"].append if args.judge else findings.append)(message)
    if not args.show_critiques:
        for pair in pairs:
            for item in pair["disagreements"]:
                item.pop("critiques")
    if args.json:
        print(json.dumps(report, indent=2))
        return 1 if findings else 0
    for pair in pairs:
        first, second = pair["raters"]
        kappa = "undefined" if pair["kappa"] is None else f"{pair['kappa']:.2f}"
        print(f"{pair['criterion']}: {first} vs {second} on {pair['cases']} cases: agreement "
              f"{pair['percent_agreement']}%, kappa {kappa}, fail share {pair['fail_share']:.2f}, "
              f"{len(pair['disagreements'])} to adjudicate")
        for item in pair["disagreements"]:
            line = f"  adjudicate {item['case_id']}: {first}={item[first]} {second}={item[second]}"
            print(line)
            for rater, text in item.get("critiques", {}).items():
                if text:
                    print(f"    {rater}: {text}")
    for result in report["judge"]:
        head = (f"judge on {result['criterion']} ({result['split']} split, {result['cases']} cases: "
                f"{result['reference_fails']} fail, {result['reference_passes']} pass)")
        if result["status"] == "NOT REPORTED":
            print(f"{head}: NOT REPORTED")
            continue
        print(f"{head}: TPR {result['tpr']:.2f}, TNR {result['tnr']:.2f} "
              f"(raw agreement {result['raw_agreement']:.2f}, context only)")
        for case in result["missed_failures"]:
            print(f"  missed failure {case}")
        for case in result["false_alarms"]:
            print(f"  false alarm {case}")
    for note in report["notes"]:
        print(f"NOTE {note}")
    for finding in findings:
        print(f"ATTENTION {finding}")
    if not findings:
        print("Nothing needs attention at the thresholds given.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
