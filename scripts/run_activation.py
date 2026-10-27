#!/usr/bin/env python3
"""Measure skill selection from descriptions over evals/activation.json.

A selector model sees only the catalogue (every skills/*/SKILL.md name and
description) and a seeded, shuffled batch of prompts under neutral item labels.
It never sees case ids, target skills, labels or rationales. For each prompt it
names a primary skill (or ``none``), up to two supporting skills and a
one-sentence reason. Answers are graded with the rules of the 8 October 2026
trial (docs/testing/activation-trial-2026-10-08.md):

* positive case: PASS when the target is primary, PARTIAL when it is only
  supporting, FAIL otherwise;
* near-miss case: PASS when the target is neither primary nor supporting,
  PARTIAL when it is supporting behind another primary, FAIL when it is primary.

A batch whose answer cannot be read grades its cases ERROR, which is neither a
pass nor a fail. Backends: ``claude-cli`` (headless ``claude -p`` on the local
Claude Code login; no API key) and ``files`` (export prompt files for a person
or another agent to answer, then import the answers).

Examples::

    python scripts/run_activation.py --backend claude-cli --repeat 2 --out results.json
    python scripts/run_activation.py --backend files --export /tmp/act
    python scripts/run_activation.py --backend files --import /tmp/act --model claude-opus-5-5 --out results.json
    python scripts/run_activation.py --compare old.json new.json

Exit status: 0 on success, 1 when --compare finds a new FAIL, 2 on bad input or
a run that could not be completed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import json
from pathlib import Path
import random
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_backends import (DEFAULT_MODEL, KNOWN_MODELS, BackendError, call_model,  # noqa: E402
                            canonical_json, extract_json, git_commit, sha256_bytes)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "activation-results/1"
GRADES = ("PASS", "PARTIAL", "FAIL", "ERROR")
DEFAULT_SEED = 20261027
DEFAULT_BATCH = 14
KEY_LINE = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]+(.*))?$")

SELECTOR_SYSTEM = """\
You are the skill selector of a coding agent. Before the agent starts work on a \
user's request, you decide which of its installed skills, if any, it should load. \
You see only the skill catalogue (each skill's name and description) and the requests.

For each request choose:
- primary: the one skill whose description best fits the request as a whole, or \
"none" when no skill in the catalogue fits;
- supporting: zero, one or two further skills the agent should also load because \
the request clearly needs them (an empty list when none are needed);
- reason: one sentence explaining the choice.

Read each description in full, including what it says the skill is not for. Judge \
each request on its own. Use only names that appear in the catalogue.

Answer with JSON only, no other text, in exactly this shape, one entry per request:
{"answers": [{"item": "R01", "primary": "<skill name or none>", "supporting": ["<skill name>"], "reason": "<one sentence>"}]}"""


class InputError(Exception):
    pass


# ---------------------------------------------------------------- catalogue

def _fold(lines: list[str]) -> str:
    """YAML line folding: single breaks become spaces, blank lines become newlines."""
    out, pending_blank = "", 0
    for raw in lines:
        line = raw.strip()
        if not line:
            pending_blank += 1
            continue
        if out:
            out += "\n" * pending_blank if pending_blank else " "
        out += line
        pending_blank = 0
    return out


def _scalar(rest: str, continuation: list[str]):
    if not rest and any(line.strip() for line in continuation):
        return None  # nested mapping or sequence; not needed for the catalogue
    if rest[:1] in (">", "|"):
        body = continuation
        while body and not body[-1].strip():
            body = body[:-1]
        indent = min((len(line) - len(line.lstrip()) for line in body if line.strip()), default=0)
        body = [line[indent:] for line in body]
        text = "\n".join(body) if rest[0] == "|" else _fold(body)
        return text if rest.endswith("-") else text + "\n"
    if rest.startswith('"'):
        inner = _fold([rest] + continuation)
        if not inner.endswith('"') or len(inner) < 2:
            raise ValueError("unterminated double-quoted scalar")
        try:
            return json.loads(inner)
        except ValueError:
            return inner[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if rest.startswith("'"):
        inner = _fold([rest] + continuation)
        if not inner.endswith("'") or len(inner) < 2:
            raise ValueError("unterminated single-quoted scalar")
        return inner[1:-1].replace("''", "'")
    return _fold([rest] + continuation)


def parse_frontmatter(text: str) -> dict:
    """Top-level scalar keys of a SKILL.md frontmatter block (stdlib-only subset of YAML)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("unterminated frontmatter") from exc
    block, fields, i = lines[1:end], {}, 0
    while i < len(block):
        match = KEY_LINE.match(block[i])
        i += 1
        if not match:
            continue
        continuation = []
        while i < len(block) and (block[i][:1] in (" ", "\t") or not block[i].strip()):
            continuation.append(block[i])
            i += 1
        fields[match.group(1)] = _scalar((match.group(2) or "").rstrip(), continuation)
    return fields


def load_catalogue(root: Path) -> list[dict]:
    catalogue = []
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        fields = parse_frontmatter(path.read_text(encoding="utf-8"))
        name, description = fields.get("name"), fields.get("description")
        if not isinstance(name, str) or not isinstance(description, str) or not description.strip():
            raise InputError(f"{path}: frontmatter needs name and description")
        catalogue.append({"name": name, "description": description.strip()})
    if not catalogue:
        raise InputError(f"no skills found under {root / 'skills'}")
    return catalogue


def catalogue_sha256(catalogue: list[dict]) -> str:
    return sha256_bytes(canonical_json(catalogue))


# ---------------------------------------------------------------- corpus

def load_cases(root: Path, only: list[str] | None = None) -> tuple[list[dict], str]:
    path = root / "evals" / "activation.json"
    raw = path.read_bytes()
    cases = json.loads(raw)["cases"]
    if only:
        unknown = set(only) - {case["skill"] for case in cases}
        if unknown:
            raise InputError(f"--only names skills with no activation cases: {', '.join(sorted(unknown))}")
        cases = [case for case in cases if case["skill"] in only]
    return cases, sha256_bytes(raw)


def make_batches(cases: list[dict], batch_size: int, seed) -> list[list[dict]]:
    """Seeded shuffle (independent of file order) cut into near-equal batches of at most batch_size."""
    if batch_size < 1:
        raise InputError("batch size must be at least 1")
    ordered = sorted(cases, key=lambda case: case["id"])
    random.Random(str(seed)).shuffle(ordered)
    count = -(-len(ordered) // batch_size)
    size, extra = divmod(len(ordered), count) if count else (0, 0)
    batches, start = [], 0
    for index in range(count):
        end = start + size + (1 if index < extra else 0)
        batches.append(ordered[start:end])
        start = end
    return batches


def item_label(index: int) -> str:
    return f"R{index + 1:02d}"


def build_prompt(catalogue: list[dict], batch: list[dict]) -> str:
    requests = [{"item": item_label(i), "request": case["prompt"]} for i, case in enumerate(batch)]
    return ("## Skill catalogue\n\n" + json.dumps(catalogue, indent=1, ensure_ascii=False)
            + "\n\n## Requests\n\n" + json.dumps(requests, indent=1, ensure_ascii=False)
            + f"\n\nReturn one answer for each of the {len(batch)} requests as JSON.")


# ---------------------------------------------------------------- grading

def grade(should_trigger: bool, target: str, primary: str, supporting: list[str]) -> str:
    if should_trigger:
        if primary == target:
            return "PASS"
        return "PARTIAL" if target in supporting else "FAIL"
    if primary == target:
        return "FAIL"
    return "PARTIAL" if target in supporting else "PASS"


def parse_answers(text: str, count: int, names: set[str]) -> dict[str, dict]:
    """Map item label to a normalised answer; raises BackendError when unusable."""
    data = extract_json(text)
    answers = data.get("answers") if isinstance(data, dict) else data
    if not isinstance(answers, list):
        raise BackendError("reply has no answers list")
    result = {}
    for answer in answers:
        if not isinstance(answer, dict) or not isinstance(answer.get("item"), str):
            continue
        primary = str(answer.get("primary") or "none").strip()
        supporting = answer.get("supporting") or []
        if isinstance(supporting, str):
            supporting = [supporting]
        supporting = [str(s).strip() for s in supporting if str(s).strip() not in ("", "none")]
        unknown = [n for n in [primary, *supporting] if n != "none" and n not in names]
        result[answer["item"].strip()] = {
            "primary": primary, "supporting": supporting[:2],
            "reason": str(answer.get("reason") or "").strip(),
            **({"unknown_names": unknown} if unknown else {}),
            **({"supporting_trimmed": supporting[2:]} if len(supporting) > 2 else {}),
        }
    expected = {item_label(i) for i in range(count)}
    if not expected & set(result):
        raise BackendError("reply answered none of the batch's items")
    return result


def grade_batch(batch: list[dict], answers: dict[str, dict] | None, repeat: int,
                error: str | None = None) -> list[dict]:
    rows = []
    for i, case in enumerate(batch):
        answer = (answers or {}).get(item_label(i))
        row = {"id": case["id"], "skill": case["skill"], "should_trigger": case["should_trigger"],
               "repeat": repeat}
        if "split" in case:
            row["split"] = case["split"]
        if answer is None:
            row.update(primary=None, supporting=[], reason="",
                       grade="ERROR", error=error or "no answer for this item")
        else:
            row.update(answer)
            row["grade"] = grade(case["should_trigger"], case["skill"],
                                 answer["primary"], answer["supporting"])
        rows.append(row)
    return rows


# ---------------------------------------------------------------- running

def plan(cases: list[dict], repeats: int, batch_size: int, seed) -> list[tuple[int, int, list[dict]]]:
    jobs = []
    for repeat in range(1, repeats + 1):
        for number, batch in enumerate(make_batches(cases, batch_size, f"{seed}:{repeat}"), 1):
            jobs.append((repeat, number, batch))
    return jobs


def run_model(backend: str, model: str, catalogue: list[dict], jobs, timeout: float,
              workers: int, log=print) -> tuple[list[dict], list[dict]]:
    names = {entry["name"] for entry in catalogue}

    def one(job):
        repeat, number, batch = job
        prompt, error = build_prompt(catalogue, batch), None
        for attempt in (1, 2):
            try:
                reply = call_model(backend, prompt, SELECTOR_SYSTEM, model, timeout)
                answers = parse_answers(reply.text, len(batch), names)
                log(f"repeat {repeat} batch {number}: {len(answers)}/{len(batch)} answers "
                    f"({reply.duration_s}s, {reply.model})")
                meta = {"repeat": repeat, "batch": number, "cases": [c["id"] for c in batch],
                        "model": reply.model, "usage": reply.usage, "cost_usd": reply.cost_usd,
                        "duration_s": reply.duration_s, "attempts": attempt}
                return grade_batch(batch, answers, repeat), meta
            except BackendError as exc:
                error = str(exc)
                log(f"repeat {repeat} batch {number}: attempt {attempt} failed: {error}")
        meta = {"repeat": repeat, "batch": number, "cases": [c["id"] for c in batch],
                "error": error, "attempts": 2}
        return grade_batch(batch, None, repeat, error), meta

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        outcomes = list(pool.map(one, jobs))
    rows = [row for batch_rows, _ in outcomes for row in batch_rows]
    return rows, [meta for _, meta in outcomes]


def export_files(directory: Path, catalogue: list[dict], jobs, header: dict) -> None:
    """Write prompts/ for the selector and a manifest the selector must not see."""
    prompts, answers = directory / "prompts", directory / "answers"
    prompts.mkdir(parents=True, exist_ok=True)
    answers.mkdir(parents=True, exist_ok=True)
    batches = []
    for repeat, number, batch in jobs:
        stem = f"r{repeat}-b{number:02d}"
        text = ("# Skill selection batch " + stem + "\n\n" + SELECTOR_SYSTEM + "\n\n"
                + build_prompt(catalogue, batch)
                + f"\n\nSave the JSON answer as answers/{stem}.json.\n")
        (prompts / f"{stem}.md").write_text(text, encoding="utf-8")
        batches.append({"stem": stem, "repeat": repeat, "batch": number,
                        "items": {item_label(i): case["id"] for i, case in enumerate(batch)}})
    manifest = {**header, "batches": batches}
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    (directory / "README.txt").write_text(
        "Give each selector only one file from prompts/ (a fresh session per file, no access to\n"
        "this directory or the repository). Save its JSON reply as answers/<same stem>.json.\n"
        "manifest.json maps item labels to case ids and must stay hidden from selectors.\n"
        "Then run: python scripts/run_activation.py --backend files --import <this directory>\n",
        encoding="utf-8")


def import_files(directory: Path, cases: list[dict], catalogue: list[dict],
                 header: dict) -> tuple[list[dict], list[dict], dict]:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    for key in ("catalogue_sha256", "corpus_sha256"):
        if manifest.get(key) != header[key]:
            raise InputError(f"{key} differs from the exported batches; re-export them")
    by_id = {case["id"]: case for case in cases}
    names = {entry["name"] for entry in catalogue}
    rows, metas = [], []
    for entry in manifest["batches"]:
        batch = [by_id[cid] for _, cid in sorted(entry["items"].items())]
        path = directory / "answers" / f"{entry['stem']}.json"
        meta = {"repeat": entry["repeat"], "batch": entry["batch"], "cases": [c["id"] for c in batch],
                "answer_file": f"answers/{path.name}"}
        try:
            answers = parse_answers(path.read_text(encoding="utf-8"), len(batch), names)
            rows += grade_batch(batch, answers, entry["repeat"])
        except (OSError, BackendError) as exc:
            meta["error"] = str(exc)
            rows += grade_batch(batch, None, entry["repeat"], str(exc))
        metas.append(meta)
    return rows, metas, manifest


# ---------------------------------------------------------------- reporting

def summarise(rows: list[dict]) -> dict:
    by_repeat: dict[int, Counter] = {}
    for row in rows:
        by_repeat.setdefault(row["repeat"], Counter())[row["grade"]] += 1
    total = Counter(row["grade"] for row in rows)
    per_case: dict[str, list[str]] = {}
    for row in sorted(rows, key=lambda r: r["repeat"]):
        per_case.setdefault(row["id"], []).append(row["grade"])
    return {
        "overall": {g: total.get(g, 0) for g in GRADES},
        "by_repeat": {str(r): {g: c.get(g, 0) for g in GRADES} for r, c in sorted(by_repeat.items())},
        "not_pass": {cid: grades for cid, grades in sorted(per_case.items())
                     if any(g != "PASS" for g in grades)},
    }


def format_summary(results: dict) -> str:
    summary = results["summary"]
    lines = [f"Activation run: backend {results['backend']}, model {results['model']}, "
             f"{results['case_count']} cases x {results['repeats']} repeat(s)",
             f"catalogue {results['catalogue_sha256'][:16]}  corpus {results['corpus_sha256'][:16]}", "",
             "| Run | PASS | PARTIAL | FAIL | ERROR |", "| --- | --- | --- | --- | --- |"]
    for repeat, counts in summary["by_repeat"].items():
        lines.append(f"| repeat {repeat} | " + " | ".join(str(counts[g]) for g in GRADES) + " |")
    lines.append("| all | " + " | ".join(str(summary["overall"][g]) for g in GRADES) + " |")
    if summary["not_pass"]:
        lines += ["", "Cases not passing in every repeat:"]
        rows = {}
        for row in results["cases"]:
            rows.setdefault(row["id"], []).append(row)
        for cid, grades in summary["not_pass"].items():
            first = next(r for r in rows[cid] if r["grade"] != "PASS")
            kind = "positive" if first["should_trigger"] else "near-miss"
            chosen = first.get("primary") or "-"
            support = ",".join(first.get("supporting") or []) or "-"
            lines.append(f"- {cid} [{first['skill']}, {kind}] {' '.join(grades)}: "
                         f"primary {chosen}; supporting {support}. {first.get('reason') or first.get('error', '')}")
    return "\n".join(lines)


def compare(old: dict, new: dict) -> tuple[list[str], int]:
    def grades(results):
        table = {}
        for row in sorted(results["cases"], key=lambda r: r["repeat"]):
            table.setdefault(row["id"], []).append(row["grade"])
        return table

    before, after = grades(old), grades(new)
    lines, new_fails = [], 0
    for key in ("catalogue_sha256", "corpus_sha256", "model"):
        if old.get(key) != new.get(key):
            lines.append(f"note: {key} differs ({str(old.get(key))[:16]} -> {str(new.get(key))[:16]})")
    for cid in sorted(set(before) | set(after)):
        a, b = before.get(cid), after.get(cid)
        if a is None or b is None:
            lines.append(f"{cid}: {'only in new' if a is None else 'only in old'}")
            continue
        if Counter(a) != Counter(b):
            fail = "FAIL" in b and "FAIL" not in a
            new_fails += fail
            lines.append(f"{cid}: {' '.join(a)} -> {' '.join(b)}" + ("  NEW FAIL" if fail else ""))
    if not any(not line.startswith("note:") for line in lines):
        lines.append("No case changed grade.")
    return lines, new_fails


# ---------------------------------------------------------------- command line

def build_results(args, catalogue, cases, corpus_hash, rows, metas, model, extra=None) -> dict:
    results = {
        "schema": SCHEMA,
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "backend": args.backend, "model": model, "seed": args.seed,
        "batch_size": args.batch_size, "repeats": args.repeat,
        "only": args.only or None, "commit": git_commit(args.root),
        "catalogue_sha256": catalogue_sha256(catalogue), "corpus_sha256": corpus_hash,
        "skill_count": len(catalogue), "case_count": len(cases),
        "grading": "8 October 2026 rules; see scripts/run_activation.py",
        "batches": metas, "cases": rows,
    }
    results.update(extra or {})
    results["summary"] = summarise(rows)
    return results


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--backend", choices=("claude-cli", "files"), default="claude-cli")
    parser.add_argument("--model", help=f"selector model (default {DEFAULT_MODEL}; "
                        f"also {', '.join(m for m in KNOWN_MODELS if m != DEFAULT_MODEL)})")
    parser.add_argument("--repeat", type=int, default=1, help="independent reshuffled runs")
    parser.add_argument("--only", type=lambda s: [x.strip() for x in s.split(",") if x.strip()],
                        help="comma-separated skills whose cases to run (the catalogue stays complete)")
    parser.add_argument("--seed", default=str(DEFAULT_SEED))
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH)
    parser.add_argument("--jobs", type=int, default=4, help="concurrent model calls")
    parser.add_argument("--timeout", type=float, default=600, help="seconds per model call")
    parser.add_argument("--out", type=Path, help="results JSON path")
    parser.add_argument("--export", type=Path, metavar="DIR", help="files backend: write batch prompts")
    parser.add_argument("--import", dest="import_dir", type=Path, metavar="DIR",
                        help="files backend: grade answers written into DIR/answers/")
    parser.add_argument("--compare", nargs=2, type=Path, metavar=("OLD", "NEW"),
                        help="list cases whose grades changed between two results files")
    args = parser.parse_args(argv)
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")
    if args.backend == "files" and not args.compare and bool(args.export) == bool(args.import_dir):
        parser.error("the files backend needs exactly one of --export DIR or --import DIR")
    if args.backend != "files" and (args.export or args.import_dir):
        parser.error("--export and --import belong to the files backend")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.compare:
            old, new = (json.loads(p.read_text(encoding="utf-8")) for p in args.compare)
            lines, new_fails = compare(old, new)
            print("\n".join(lines))
            print(f"\n{new_fails} new FAIL(s).")
            return 1 if new_fails else 0
        root = args.root.resolve()
        catalogue = load_catalogue(root)
        cases, corpus_hash = load_cases(root, args.only)
        jobs = plan(cases, args.repeat, args.batch_size, args.seed)
        header = {"catalogue_sha256": catalogue_sha256(catalogue), "corpus_sha256": corpus_hash,
                  "seed": args.seed, "batch_size": args.batch_size, "repeats": args.repeat,
                  "only": args.only or None}
        if args.backend == "files" and args.export:
            export_files(args.export, catalogue, jobs, header)
            print(f"Wrote {len(jobs)} batch prompt(s) to {args.export / 'prompts'}; "
                  "keep manifest.json away from the selectors.")
            return 0
        if args.backend == "files":
            rows, metas, manifest = import_files(args.import_dir, cases, catalogue, header)
            args.seed, args.batch_size, args.repeat = (manifest["seed"], manifest["batch_size"],
                                                       manifest["repeats"])
            results = build_results(args, catalogue, cases, corpus_hash, rows, metas,
                                    args.model or "external selector")
        else:
            model = args.model or DEFAULT_MODEL
            rows, metas = run_model(args.backend, model, catalogue, jobs, args.timeout, args.jobs,
                                    log=lambda m: print(m, file=sys.stderr, flush=True))
            results = build_results(args, catalogue, cases, corpus_hash, rows, metas, model)
    except (InputError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(format_summary(results))
    errors = results["summary"]["overall"]["ERROR"]
    return 2 if errors == len(rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
