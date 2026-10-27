#!/usr/bin/env python3
"""Run scenarios from evals/scenarios.json against a coding agent and grade their assertions.

Each selected scenario gets a fresh workspace under a temporary run directory:
the fixture listed for it in evals/scenario-fixtures.json (if any) and only the
scenario's ``available_skills`` that exist in skills/, copied into
``.claude/skills/``. Grader material listed for the scenario (files under
evals/graders/) is copied beside the workspace, never into it, and only the
judge sees it. A coding agent receives the scenario prompt plus the
context as the situation. A judge model then grades each assertion PASS or
FAIL from the agent's final answer, the files it wrote and the skills it
loaded, quoting its evidence. Scenarios whose context describes fixtures that
do not exist are reported as ``fixture-missing`` and never run against nothing.

Subcommands::

    list                      which scenarios are runnable, need a repo fixture, or lack one
    prepare --ids a,b         build the run directory and workspaces only
    agent   --run-dir D       run the coding agent in each prepared workspace (claude-cli)
    judge   --run-dir D       grade assertions (claude-cli or files)
    run     --ids a,b         prepare, agent and judge in one go

With ``--backend files`` the agent step is left to a person or another agent:
work in ``D/<id>/workspace`` from ``D/<id>/task.md`` and save the final answer
as ``D/<id>/final.md``. With ``judge --backend files`` the judge prompts are
written to ``D/<id>/judge-prompt.md`` and the verdict JSON is read from
``D/<id>/judge-answer.json`` on the next ``judge`` call.

Exit status: 0 on success, 2 on bad input.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_backends import (DEFAULT_MODEL, BackendError, call_model, canonical_json,  # noqa: E402
                            extract_json, git_commit, sha256_bytes)

ROOT = Path(__file__).resolve().parents[1]
GRADER_ROOT = "evals/graders/"
SCHEMA = "scenario-results/1"
STATUSES = ("runnable", "repo-fixture", "fixture-missing")
AGENT_TOOLS = "Read,Write,Edit,Glob,Grep,Skill"
EVIDENCE_LIMIT = 150_000
FILE_LIMIT = 30_000

RUN_CONDITIONS = """\
---
Situation (from the person asking): {context}

Run conditions: this is a non-interactive session and nobody will answer questions. \
Where you would ask the user something, write the question down, state the assumption \
you proceed on, and carry on. Work only inside the current directory; do not install \
packages, make network requests or touch cloud resources. End with a short summary of \
what you did and what you left undone."""

JUDGE_SYSTEM = """\
You grade a coding agent's work against pre-registered assertions. Use only the \
evidence supplied: the agent's final answer, the files it wrote and the skills it \
loaded. For each assertion return PASS only when the evidence shows it; otherwise \
FAIL, including when the evidence is silent. Quote the evidence verbatim (a short \
exact excerpt from the final answer or a file) for every verdict; use an empty quote \
when nothing relevant exists. Do not reward intentions the work does not carry out.

Answer with JSON only, one entry per assertion, in this shape:
{"verdicts": [{"assertion": "A1", "verdict": "PASS", "quote": "<exact excerpt>", "reason": "<one sentence>"}]}"""


class InputError(Exception):
    pass


# ---------------------------------------------------------------- inputs

def load_scenarios(root: Path) -> tuple[list[dict], str]:
    raw = (root / "evals" / "scenarios.json").read_bytes()
    return json.loads(raw)["cases"], sha256_bytes(raw)


def load_fixtures(root: Path) -> dict:
    path = root / "evals" / "scenario-fixtures.json"
    return json.loads(path.read_text(encoding="utf-8"))["scenarios"] if path.exists() else {}


def classify(case: dict, fixtures: dict, root: Path) -> dict:
    entry = dict(fixtures.get(case["id"]) or {"status": "fixture-missing"})
    if entry.get("status") not in STATUSES:
        raise InputError(f"{case['id']}: unknown fixture status {entry.get('status')!r}")
    for item in entry.get("grader", []):
        if not item["from"].startswith(GRADER_ROOT):
            raise InputError(f"{case['id']}: grader material must live under {GRADER_ROOT}: {item['from']}")
    if entry["status"] == "repo-fixture":
        absent = [c["from"] for c in entry.get("copy", []) if not (root / c["from"]).exists()]
        if absent or not entry.get("copy"):
            entry = {"status": "fixture-missing", "partial": "listed fixture paths are absent: "
                     + ", ".join(absent or ["(none listed)"])}
    absent = [g["from"] for g in entry.get("grader", []) if not (root / g["from"]).is_file()]
    if absent and entry["status"] != "fixture-missing":
        entry = {"status": "fixture-missing", "partial": "listed grader material is absent: "
                 + ", ".join(absent)}
    if entry["status"] == "fixture-missing" and "partial" not in entry:
        entry["needs"] = first_sentence(case["context"])
    installed = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    entry["skills_missing"] = [s for s in case["available_skills"] if s not in installed]
    return entry


def first_sentence(text: str) -> str:
    match = re.match(r"(.+?[.;])(\s|$)", text.strip())
    return (match.group(1) if match else text.strip())[:200]


def select(cases: list[dict], ids: list[str] | None, skill: str | None) -> list[dict]:
    if ids:
        by_id = {case["id"]: case for case in cases}
        unknown = [i for i in ids if i not in by_id]
        if unknown:
            raise InputError(f"unknown scenario ids: {', '.join(unknown)}")
        return [by_id[i] for i in ids]
    if skill:
        return [case for case in cases if case["expected_primary"] == skill]
    raise InputError("choose scenarios with --ids or --skill")


def format_list(cases: list[dict], fixtures: dict, root: Path) -> str:
    groups: dict[str, list[str]] = {status: [] for status in STATUSES}
    for case in cases:
        entry = classify(case, fixtures, root)
        detail = entry.get("note") or entry.get("partial") or entry.get("needs") or ""
        if entry["skills_missing"]:
            detail += f" [external skills absent: {', '.join(entry['skills_missing'])}]"
        groups[entry["status"]].append(
            f"- {case['id']} ({case['expected_primary'] or 'no primary'}){': ' + detail if detail else ''}")
    lines = []
    for status in STATUSES:
        lines += [f"## {status} ({len(groups[status])})", *groups[status], ""]
    return "\n".join(lines).rstrip()


# ---------------------------------------------------------------- prepare

def task_text(case: dict) -> str:
    return case["prompt"].rstrip() + "\n\n" + RUN_CONDITIONS.format(context=case["context"].strip())


def tree_digest(directory: Path) -> dict[str, str]:
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*")) if p.is_file()}


def prepare(root: Path, cases: list[dict], fixtures: dict, tmp_root: Path | None,
            run_dir: Path | None = None) -> tuple[Path, dict]:
    if run_dir is None:
        base = tmp_root or Path(tempfile.gettempdir())
        base.mkdir(parents=True, exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix="aes-scenarios-", dir=base))
    else:
        run_dir.mkdir(parents=True, exist_ok=False)
    entries = []
    for case in cases:
        entry = {"id": case["id"], **classify(case, fixtures, root)}
        if entry["status"] != "fixture-missing":
            case_dir = run_dir / case["id"]
            workspace = case_dir / "workspace"
            workspace.mkdir(parents=True)
            (case_dir / "home").mkdir()
            for item in fixtures.get(case["id"], {}).get("copy", []):
                source, target = root / item["from"], (workspace / item["to"]).resolve()
                if workspace.resolve() not in (target, *target.parents):
                    raise InputError(f"{case['id']}: fixture target escapes the workspace")
                if source.is_dir():
                    shutil.copytree(source, target, dirs_exist_ok=True,
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
            fixture_files = tree_digest(workspace)
            grader = []
            for item in fixtures.get(case["id"], {}).get("grader", []):
                target = case_dir / "grader" / Path(item["from"]).name
                target.parent.mkdir(exist_ok=True)
                shutil.copy2(root / item["from"], target)
                grader.append(target.name)
            installed = []
            for name in case["available_skills"]:
                if (root / "skills" / name / "SKILL.md").exists():
                    shutil.copytree(root / "skills" / name, workspace / ".claude" / "skills" / name,
                                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tests"))
                    installed.append(name)
            (case_dir / "task.md").write_text(task_text(case), encoding="utf-8")
            (case_dir / "fixture-digest.json").write_text(json.dumps(fixture_files, indent=1) + "\n",
                                                         encoding="utf-8")
            entry["skills_installed"] = installed
            entry["grader_files"] = grader
        entries.append(entry)
    manifest = {"created": now(), "root": str(root), "commit": git_commit(root),
                "scenarios": entries}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return run_dir, manifest


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- agent

def agent_command(model: str, max_turns: int, tools: str, budget: float | None) -> list[str]:
    command = ["claude", "-p", "--model", model, "--output-format", "stream-json", "--verbose",
               "--setting-sources", "project", "--strict-mcp-config", "--no-session-persistence",
               "--max-turns", str(max_turns), "--permission-mode", "acceptEdits", "--tools", tools]
    if budget:
        command += ["--max-budget-usd", str(budget)]
    return command


def parse_transcript(lines: list[str]) -> dict:
    """Summarise a stream-json transcript: final text, tool calls, skills loaded, usage."""
    summary = {"final": "", "texts": [], "tool_calls": [], "skills_loaded": [], "skill_files_read": [],
               "result": None, "catalogue": None}
    for line in lines:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            summary["catalogue"] = event.get("skills")
        elif kind == "assistant":
            for block in (event.get("message") or {}).get("content", []):
                if block.get("type") == "text" and block.get("text", "").strip():
                    summary["texts"].append(block["text"])
                elif block.get("type") == "tool_use":
                    tool_input = block.get("input") or {}
                    summary["tool_calls"].append({"tool": block.get("name"),
                                                  "input": json.dumps(tool_input)[:300]})
                    if block.get("name") == "Skill" and tool_input.get("skill"):
                        summary["skills_loaded"].append(str(tool_input["skill"]))
                    path = str(tool_input.get("file_path") or tool_input.get("path") or "")
                    match = re.search(r"\.claude/skills/([^/]+)/(.*)$", path)
                    if match and block.get("name") in ("Read", "Grep", "Glob"):
                        if block.get("name") == "Read" and match.group(2) == "SKILL.md":
                            summary["skills_loaded"].append(match.group(1))
                        summary["skill_files_read"].append(f"{match.group(1)}/{match.group(2)}")
        elif kind == "result":
            summary["result"] = {key: event.get(key) for key in
                                 ("subtype", "is_error", "num_turns", "total_cost_usd", "duration_ms",
                                  "terminal_reason")}
            summary["final"] = event.get("result") or ""
    if not summary["final"] and summary["texts"]:
        summary["final"] = summary["texts"][-1]
    summary["skills_loaded"] = list(dict.fromkeys(summary["skills_loaded"]))
    summary["skill_files_read"] = list(dict.fromkeys(summary["skill_files_read"]))
    return summary


def run_agent(run_dir: Path, entry: dict, model: str, max_turns: int, timeout: float,
              tools: str, budget: float | None, runner=subprocess.run) -> dict:
    case_dir = run_dir / entry["id"]
    workspace = case_dir / "workspace"
    env = os.environ.copy()
    env.update(AGENTIC_ENGINEERING_HOME=str(case_dir / "home"), AES_FIELD_NOTES="off")
    started, timed_out = time.monotonic(), False
    try:
        proc = runner(agent_command(model, max_turns, tools, budget), input=(case_dir / "task.md").read_text(),
                      cwd=workspace, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        code, timed_out = None, True
    (case_dir / "transcript.jsonl").write_text(stdout, encoding="utf-8")
    summary = parse_transcript(stdout.splitlines())
    (case_dir / "final.md").write_text(summary["final"], encoding="utf-8")
    record = {"exit": code, "timed_out": timed_out, "seconds": round(time.monotonic() - started, 1),
              "model": model, "max_turns": max_turns, "tools": tools, **(summary["result"] or {}),
              "skills_loaded": summary["skills_loaded"], "skill_files_read": summary["skill_files_read"],
              "tool_calls": len(summary["tool_calls"]),
              "catalogue": summary["catalogue"]}
    (case_dir / "agent.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


# ---------------------------------------------------------------- judge

def changed_files(case_dir: Path) -> dict[str, str]:
    workspace = case_dir / "workspace"
    before = json.loads((case_dir / "fixture-digest.json").read_text(encoding="utf-8"))
    files = {}
    for path in sorted(workspace.rglob("*")):
        rel = str(path.relative_to(workspace))
        if not path.is_file() or rel.startswith(".claude/"):
            continue
        if before.get(rel) == hashlib.sha256(path.read_bytes()).hexdigest():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = f"(binary file, {path.stat().st_size} bytes)"
        files[rel] = text if len(text) <= FILE_LIMIT else text[:FILE_LIMIT] + "\n[truncated]"
    return files


def evidence_text(case_dir: Path) -> tuple[str, dict]:
    final = (case_dir / "final.md").read_text(encoding="utf-8") if (case_dir / "final.md").exists() else ""
    agent = json.loads((case_dir / "agent.json").read_text()) if (case_dir / "agent.json").exists() else {}
    transcript = case_dir / "transcript.jsonl"
    if transcript.exists():
        parsed = parse_transcript(transcript.read_text(encoding="utf-8").splitlines())
        agent = {**agent, "skills_loaded": parsed["skills_loaded"],
                 "skill_files_read": parsed["skill_files_read"]}
    files = changed_files(case_dir)
    parts = ["### Final answer\n\n" + (final or "(empty)"),
             "### Skills loaded\n\n" + (", ".join(agent.get("skills_loaded") or []) or "(none recorded)"),
             "### Skill files read\n\n" + (", ".join(agent.get("skill_files_read") or []) or "(none recorded)"),
             "### Files written or changed\n\n" + ("\n".join(files) or "(none)")]
    for name, text in files.items():
        parts.append(f"### File: {name}\n\n{text}")
    evidence = "\n\n".join(parts)
    if len(evidence) > EVIDENCE_LIMIT:
        evidence = evidence[:EVIDENCE_LIMIT] + "\n[evidence truncated]"
    return evidence, {"final_chars": len(final), "files": list(files), "agent": agent}


def grader_text(case_dir: Path) -> str:
    """Grader-side files for the judge only; the agent's workspace never holds them."""
    folder = case_dir / "grader"
    parts = []
    for path in sorted(folder.glob("*")) if folder.is_dir() else []:
        text = path.read_text(encoding="utf-8", errors="replace")
        text = text if len(text) <= FILE_LIMIT else text[:FILE_LIMIT] + "\n[truncated]"
        parts.append(f"### {path.name}\n\n```\n{text}\n```")
    return "\n\n".join(parts)


def judge_prompt(case: dict, evidence: str, grader: str = "") -> str:
    assertions = "\n".join(f"A{i}: {text}" for i, text in enumerate(case["assertions"], 1))
    material = ("## Grader material (withheld from the agent; use it to check the agent's work, "
                f"never quote it as evidence)\n\n{grader}\n\n" if grader else "")
    return (f"## Request given to the agent\n\n{case['prompt']}\n\n## Situation\n\n{case['context']}\n\n"
            f"## Assertions\n\n{assertions}\n\n{material}## Evidence\n\n{evidence}\n\n"
            f"Return one verdict for each of the {len(case['assertions'])} assertions as JSON.")


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def parse_verdicts(text: str, case: dict, evidence: str) -> list[dict]:
    data = extract_json(text)
    verdicts = data.get("verdicts") if isinstance(data, dict) else data
    if not isinstance(verdicts, list):
        raise BackendError("judge reply has no verdicts list")
    by_label = {str(v.get("assertion", "")).strip(): v for v in verdicts if isinstance(v, dict)}
    haystack, rows = normalise(evidence), []
    for i, assertion in enumerate(case["assertions"], 1):
        verdict = by_label.get(f"A{i}") or {}
        value = str(verdict.get("verdict", "")).upper()
        quote = str(verdict.get("quote") or "")
        rows.append({"n": i, "assertion": assertion,
                     "verdict": value if value in ("PASS", "FAIL") else "UNGRADED",
                     "quote": quote, "quote_found": bool(quote) and normalise(quote) in haystack,
                     "reason": str(verdict.get("reason") or "")})
    return rows


def judge_case(run_dir: Path, case: dict, backend: str, model: str, timeout: float) -> dict:
    case_dir = run_dir / case["id"]
    evidence, facts = evidence_text(case_dir)
    prompt = judge_prompt(case, evidence, grader_text(case_dir))
    record = {"judge_backend": backend, "judge_model": model}
    if backend == "files":
        answer = case_dir / "judge-answer.json"
        if not answer.exists():
            (case_dir / "judge-prompt.md").write_text(JUDGE_SYSTEM + "\n\n" + prompt, encoding="utf-8")
            return {**record, "status": "awaiting-judge", **facts}
        text = answer.read_text(encoding="utf-8")
    else:
        try:
            text = call_model(backend, prompt, JUDGE_SYSTEM, model, timeout).text
        except BackendError as exc:
            return {**record, "status": "judge-error", "error": str(exc), **facts}
    (case_dir / "judge-reply.txt").write_text(text, encoding="utf-8")
    try:
        rows = parse_verdicts(text, case, evidence)
    except BackendError as exc:
        return {**record, "status": "judge-error", "error": str(exc), **facts}
    return {**record, "status": "graded", "assertions": rows,
            "passed": sum(r["verdict"] == "PASS" for r in rows), "total": len(rows), **facts}


# ---------------------------------------------------------------- results

def build_results(root: Path, run_dir: Path, manifest: dict, cases_by_id: dict, graded: dict,
                  scenarios_hash: str, settings: dict) -> dict:
    rows = []
    for entry in manifest["scenarios"]:
        case = cases_by_id[entry["id"]]
        row = {"id": entry["id"], "expected_primary": case["expected_primary"],
               "fixture_status": entry["status"], **{k: entry[k] for k in
               ("note", "partial", "needs", "skills_missing", "skills_installed") if k in entry}}
        if entry["status"] == "fixture-missing":
            row["status"] = "fixture-missing"
        else:
            row.update(graded.get(entry["id"]) or {"status": "not-run"})
            agent = row.get("agent") or {}
            loaded = agent.get("skills_loaded") or []
            consulted = {path.split("/", 1)[0] for path in agent.get("skill_files_read") or []}
            primary = case["expected_primary"]
            row["primary_loaded"] = primary in loaded if primary else None
            row["primary_consulted"] = primary in consulted | set(loaded) if primary else None
        rows.append(row)
    catalogue = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
    return {"schema": SCHEMA, "created": now(), "run_dir": str(run_dir),
            "commit": manifest.get("commit"), "scenarios_sha256": scenarios_hash,
            "skills_sha256": sha256_bytes(canonical_json(catalogue)), **settings, "cases": rows}


def format_results(results: dict) -> str:
    lines = ["| Scenario | Status | Assertions passed | Primary SKILL.md loaded | Primary files read |",
             "| --- | --- | --- | --- | --- |"]
    words = {True: "yes", False: "no", None: "n/a"}
    for row in results["cases"]:
        passed = f"{row['passed']}/{row['total']}" if "total" in row else "-"
        loaded = words.get(row.get("primary_loaded"), "-")
        consulted = words.get(row.get("primary_consulted"), "-")
        lines.append(f"| {row['id']} | {row['status']} | {passed} | {loaded} | {consulted} |")
    return "\n".join(lines)


# ---------------------------------------------------------------- command line

def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("list", "prepare", "agent", "judge", "run"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ids", type=lambda s: [x.strip() for x in s.split(",") if x.strip()])
    parser.add_argument("--skill", help="select scenarios by expected_primary")
    parser.add_argument("--tmp-root", type=Path, help="parent for the run directory (default: system temp)")
    parser.add_argument("--run-dir", type=Path, help="existing run directory (agent, judge)")
    parser.add_argument("--backend", choices=("claude-cli", "files"), default="claude-cli",
                        help="coding agent backend")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="coding agent model")
    parser.add_argument("--judge-backend", choices=("claude-cli", "files"))
    parser.add_argument("--judge-model", default=DEFAULT_MODEL)
    parser.add_argument("--max-turns", type=int, default=40)
    parser.add_argument("--timeout", type=float, default=900, help="seconds per agent run")
    parser.add_argument("--max-budget-usd", type=float, help="cost cap per agent run")
    parser.add_argument("--agent-tools", default=AGENT_TOOLS,
                        help="Claude Code tools for the agent; Bash is left out by default")
    parser.add_argument("--out", type=Path, help="results JSON (default: <run dir>/results.json)")
    args = parser.parse_args(argv)
    if args.command in ("agent", "judge") and not args.run_dir:
        parser.error(f"{args.command} needs --run-dir")
    if args.judge_backend is None:
        args.judge_backend = "files" if args.backend == "files" else "claude-cli"
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    try:
        cases, scenarios_hash = load_scenarios(root)
        fixtures = load_fixtures(root)
        cases_by_id = {case["id"]: case for case in cases}
        if args.command == "list":
            print(format_list(cases, fixtures, root))
            return 0
        if args.command in ("prepare", "run"):
            run_dir, manifest = prepare(root, select(cases, args.ids, args.skill), fixtures, args.tmp_root)
            print(f"Prepared {run_dir}", file=sys.stderr)
        else:
            run_dir = args.run_dir.resolve()
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        prepared = [e for e in manifest["scenarios"] if e["status"] != "fixture-missing"]
        for entry in manifest["scenarios"]:
            if entry["status"] == "fixture-missing":
                print(f"{entry['id']}: fixture-missing, not run", file=sys.stderr)
        if args.command == "prepare" or (args.command == "run" and args.backend == "files"):
            print(f"Run directory: {run_dir}\nFor each prepared scenario, work in <id>/workspace from "
                  "<id>/task.md and save the final answer as <id>/final.md; then run the judge step.")
            return 0
        if args.command in ("agent", "run"):
            if args.backend == "files":
                raise InputError("the files backend has no agent step; see prepare")
            for entry in prepared:
                print(f"{entry['id']}: agent running", file=sys.stderr, flush=True)
                record = run_agent(run_dir, entry, args.model, args.max_turns, args.timeout,
                                   args.agent_tools, args.max_budget_usd)
                print(f"{entry['id']}: agent finished in {record['seconds']}s "
                      f"(turns {record.get('num_turns')}, timed out {record['timed_out']})",
                      file=sys.stderr, flush=True)
            if args.command == "agent":
                return 0
        graded = {}
        for entry in prepared:
            graded[entry["id"]] = judge_case(run_dir, cases_by_id[entry["id"]], args.judge_backend,
                                             args.judge_model, args.timeout)
            print(f"{entry['id']}: {graded[entry['id']]['status']}", file=sys.stderr, flush=True)
        settings = {"agent_backend": args.backend, "agent_model": args.model,
                    "agent_tools": args.agent_tools, "max_turns": args.max_turns,
                    "timeout_s": args.timeout, "judge_backend": args.judge_backend,
                    "judge_model": args.judge_model}
        results = build_results(root, run_dir, manifest, cases_by_id, graded, scenarios_hash, settings)
    except (InputError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    out = args.out or run_dir / "results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(format_results(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
