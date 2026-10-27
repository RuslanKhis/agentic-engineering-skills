#!/usr/bin/env python3
"""Run scenarios from evals/scenarios.json against a coding agent and grade their assertions.

Each selected scenario gets a fresh workspace under a temporary run directory
(never inside this repository): the fixture listed for it in
evals/scenario-fixtures.json (if any: shared base projects from
evals/fixtures/base/, explicit copies, then the scenario's own overlay from
evals/fixtures/<id>/, minus any listed removals) and only the scenario's
``available_skills`` that exist in skills/, copied (never symlinked, tests/
left out) as Claude Code project skills in ``<workspace>/.claude/skills/``.
With ``--skill-install add-dir`` they are copied to a sibling directory that
the agent receives through ``--add-dir`` instead, so a glob of the workspace
does not list them. Grader material listed for the scenario (files under
evals/graders/) is copied beside the workspace, never into it, and only the
judge sees it.

The ``claude-cli`` agent runs headless with project and local settings only
(no user-level skills, settings or CLAUDE.md), no MCP servers, auto-memory off
and ``--permission-mode dontAsk --permission-prompts none``: only the allow rules
the runner passes (reads, edits and writes under the workspace, and the Skill
tool) are granted, and every other tool call, including any read outside the
workspace, is refused without asking. A coding agent receives the scenario
prompt plus the context as the situation. A judge model then grades each
assertion PASS or FAIL from the agent's final answer, the files it wrote and
the skills it loaded, quoting its evidence; it judges ``--judge-repeats``
times (default 3) and each assertion takes the majority verdict, with
disagreements flagged ``unstable``. Scenarios whose context describes
fixtures that do not exist are reported as ``fixture-missing``, and those
marked ``not-representable`` (with a reason) cannot be built offline; neither
is ever run against nothing.

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
``D/<id>/judge-answer.json`` on the next ``judge`` call (one repeat).

Exit status: 0 on success, 2 on bad input.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
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
FIXTURE_ROOT = "evals/fixtures"
SCHEMA = "scenario-results/2"
STATUSES = ("runnable", "repo-fixture", "fixture-missing", "not-representable")
NOT_RUN = ("fixture-missing", "not-representable")
SKILL_INSTALLS = ("project", "add-dir")
AGENT_TOOLS = "Read,Write,Edit,Glob,Grep,Skill"
# Path-scoped allow rules. Glob and Grep are governed by the Read rules, so they
# are never allowed bare: a bare "Glob" would let the agent list ~/.claude.
SCOPED_RULES = {"Read": "Read(./**)", "Glob": "Read(./**)", "Grep": "Read(./**)",
                "Edit": "Edit(./**)", "Write": "Write(./**)", "Skill": "Skill"}
SETTING_SOURCES = "project,local"
# Auto-memory names a per-workspace directory under ~/.claude/projects/ that Claude Code
# lets the agent read despite dontAsk; switch it off so nothing outside the workspace is read.
AGENT_ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}
EVIDENCE_LIMIT = 150_000
FILE_LIMIT = 30_000
SKILL_PATH = re.compile(r"\.claude/skills/([^/]+)/(.*)$")

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
loaded. Grader material, when supplied, is reference the agent never saw (for \
example an answer key); use it to check the agent's claims, never as evidence of \
what the agent did. For each assertion return PASS only when the evidence shows it; \
otherwise FAIL, including when the evidence is silent. Quote the evidence verbatim \
(a short exact excerpt from the final answer or a file) for every verdict; use an \
empty quote when nothing relevant exists. Do not reward intentions the work does \
not carry out.

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


def fixture_copies(case_id: str, entry: dict) -> list[dict]:
    """The copies that build a workspace, in order: each shared base, explicit copies, the overlay.

    ``base`` names directories under evals/fixtures/base/; ``overlay: true`` copies
    evals/fixtures/<case id>/ last, so it adds or replaces files of the bases.
    """
    copies = [{"from": f"{FIXTURE_ROOT}/base/{name}", "to": "."} for name in entry.get("base", [])]
    copies += list(entry.get("copy", []))
    if entry.get("overlay"):
        copies.append({"from": f"{FIXTURE_ROOT}/{case_id}", "to": "."})
    return copies


def classify(case: dict, fixtures: dict, root: Path) -> dict:
    entry = dict(fixtures.get(case["id"]) or {"status": "fixture-missing"})
    if entry.get("status") not in STATUSES:
        raise InputError(f"{case['id']}: unknown fixture status {entry.get('status')!r}")
    if entry["status"] == "not-representable" and not entry.get("reason"):
        raise InputError(f"{case['id']}: a not-representable scenario needs a reason")
    for item in entry.get("grader", []):
        if not item["from"].startswith(GRADER_ROOT):
            raise InputError(f"{case['id']}: grader material must live under {GRADER_ROOT}: {item['from']}")
    if entry["status"] == "repo-fixture":
        copies = fixture_copies(case["id"], entry)
        absent = [c["from"] for c in copies if not (root / c["from"]).exists()]
        if absent or not copies:
            entry = {"status": "fixture-missing", "partial": "listed fixture paths are absent: "
                     + ", ".join(absent or ["(none listed)"])}
    absent = [g["from"] for g in entry.get("grader", []) if not (root / g["from"]).is_file()]
    if absent and entry["status"] not in NOT_RUN:
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
        detail = entry.get("note") or entry.get("reason") or entry.get("partial") or entry.get("needs") or ""
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


def skills_parent(case_dir: Path, skill_install: str) -> Path:
    """The directory whose .claude/skills/ holds the installed skills."""
    return case_dir / "workspace" if skill_install == "project" else case_dir / "skills-host"


def install_skills(root: Path, names: list[str], parent: Path) -> list[str]:
    """Copy each skill's files (symlinks resolved, tests/ left out) as a Claude Code skill."""
    installed = []
    for name in names:
        if (root / "skills" / name / "SKILL.md").exists():
            shutil.copytree(root / "skills" / name, parent / ".claude" / "skills" / name, symlinks=False,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tests"))
            installed.append(name)
    return installed


def build_workspace(root: Path, case_id: str, fixture: dict, workspace: Path) -> None:
    """Copy a scenario's bases, explicit copies and overlay into the workspace, then apply removals."""
    for item in fixture_copies(case_id, fixture):
        source, target = root / item["from"], (workspace / item["to"]).resolve()
        if workspace.resolve() not in (target, *target.parents):
            raise InputError(f"{case_id}: fixture target escapes the workspace")
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    for rel in fixture.get("remove", []):
        target = (workspace / rel).resolve()
        if workspace.resolve() not in target.parents:
            raise InputError(f"{case_id}: fixture removal escapes the workspace")
        if not target.exists():
            raise InputError(f"{case_id}: fixture removes {rel}, which no base or overlay supplies")
        shutil.rmtree(target) if target.is_dir() else target.unlink()


def prepare(root: Path, cases: list[dict], fixtures: dict, tmp_root: Path | None,
            run_dir: Path | None = None, skill_install: str = "project") -> tuple[Path, dict]:
    if skill_install not in SKILL_INSTALLS:
        raise InputError(f"unknown skill install {skill_install!r}")
    if run_dir is None:
        base = tmp_root or Path(tempfile.gettempdir())
        if root.resolve() in (base.resolve(), *base.resolve().parents):
            # Claude Code reads CLAUDE.md and .claude/ settings from parent directories.
            raise InputError("the run directory must not be inside the repository")
        base.mkdir(parents=True, exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix="aes-scenarios-", dir=base))
    else:
        run_dir.mkdir(parents=True, exist_ok=False)
    entries = []
    for case in cases:
        entry = {"id": case["id"], **classify(case, fixtures, root)}
        if entry["status"] not in NOT_RUN:
            case_dir = run_dir / case["id"]
            workspace = case_dir / "workspace"
            workspace.mkdir(parents=True)
            (case_dir / "home").mkdir()
            build_workspace(root, case["id"], fixtures.get(case["id"], {}), workspace)
            fixture_files = tree_digest(workspace)
            grader = []
            for item in fixtures.get(case["id"], {}).get("grader", []):
                target = case_dir / "grader" / Path(item["from"]).name
                target.parent.mkdir(exist_ok=True)
                shutil.copy2(root / item["from"], target)
                grader.append(target.name)
            installed = install_skills(root, case["available_skills"], skills_parent(case_dir, skill_install))
            (case_dir / "task.md").write_text(task_text(case), encoding="utf-8")
            (case_dir / "fixture-digest.json").write_text(json.dumps(fixture_files, indent=1) + "\n",
                                                         encoding="utf-8")
            entry["skills_installed"] = installed
            entry["grader_files"] = grader
        entries.append(entry)
    manifest = {"created": now(), "root": str(root), "commit": git_commit(root),
                "skill_install": skill_install, "scenarios": entries}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return run_dir, manifest


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- agent

def allow_rules(tools: str) -> tuple[list[str], list[str]]:
    """Allow rules for --allowedTools, and the tools that cannot be confined by path."""
    rules, unconfined = [], []
    for tool in (t.strip() for t in tools.split(",") if t.strip()):
        if tool in SCOPED_RULES:
            rules.append(SCOPED_RULES[tool])
        else:
            rules.append(tool)
            unconfined.append(tool)
    return list(dict.fromkeys(rules)), unconfined


def agent_command(model: str, max_turns: int, tools: str, budget: float | None,
                  add_dir: Path | None = None) -> list[str]:
    rules, _ = allow_rules(tools)
    command = ["claude", "-p", "--model", model, "--output-format", "stream-json", "--verbose",
               "--setting-sources", SETTING_SOURCES, "--strict-mcp-config", "--no-session-persistence",
               "--max-turns", str(max_turns), "--tools", tools,
               "--permission-mode", "dontAsk", "--permission-prompts", "none",
               "--allowedTools", ",".join(rules)]
    if add_dir is not None:
        command += ["--add-dir", str(add_dir)]
    if budget:
        command += ["--max-budget-usd", str(budget)]
    return command


def confinement(tools: str, skill_install: str) -> dict:
    rules, unconfined = allow_rules(tools)
    return {"setting_sources": SETTING_SOURCES, "permission_mode": "dontAsk", "permission_prompts": "none",
            "allowed": rules, "unconfined_tools": unconfined, "skill_install": skill_install,
            "environment": dict(AGENT_ENV),
            "confined_to_workspace": not unconfined}


def parse_transcript(lines: list[str]) -> dict:
    """Summarise a stream-json transcript: final text, tool calls, skills loaded, refusals, usage."""
    summary = {"final": "", "texts": [], "tool_calls": [], "skills_loaded": [], "skill_tool_calls": [],
               "skill_md_reads": [], "skill_files_read": [], "result": None, "catalogue": None,
               "permission_denials": []}
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
                        summary["skill_tool_calls"].append(str(tool_input["skill"]))
                    path = str(tool_input.get("file_path") or tool_input.get("path") or "")
                    match = SKILL_PATH.search(path)
                    if match and block.get("name") in ("Read", "Grep", "Glob"):
                        if block.get("name") == "Read" and match.group(2) == "SKILL.md":
                            summary["skills_loaded"].append(match.group(1))
                            summary["skill_md_reads"].append(match.group(1))
                        summary["skill_files_read"].append(f"{match.group(1)}/{match.group(2)}")
        elif kind == "result":
            summary["result"] = {key: event.get(key) for key in
                                 ("subtype", "is_error", "num_turns", "total_cost_usd", "duration_ms",
                                  "terminal_reason")}
            summary["final"] = event.get("result") or ""
            summary["permission_denials"] = [
                {"tool": d.get("tool_name"), "input": json.dumps(d.get("tool_input") or {})[:300]}
                for d in event.get("permission_denials") or []]
    if not summary["final"] and summary["texts"]:
        summary["final"] = summary["texts"][-1]
    for key in ("skills_loaded", "skill_tool_calls", "skill_md_reads", "skill_files_read"):
        summary[key] = list(dict.fromkeys(summary[key]))
    return summary


def skill_md_loaded(summary: dict, installed: list[str]) -> dict[str, dict]:
    """Per installed skill: was its SKILL.md loaded (through the Skill tool or a Read), and how."""
    report = {}
    for name in installed:
        via_tool = name in summary["skill_tool_calls"]
        via_read = name in summary["skill_md_reads"]
        files = [path for path in summary["skill_files_read"] if path.split("/", 1)[0] == name]
        report[name] = {"loaded": via_tool or via_read,
                        "how": "skill-tool" if via_tool else "read" if via_read else None,
                        "other_files_read": len([f for f in files if f != f"{name}/SKILL.md"])}
    return report


def catalogue_check(catalogue: list | None, installed: list[str], root: Path) -> dict:
    """Repository skills in the session catalogue that were not installed reached it from elsewhere."""
    repo = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    names = set(catalogue or [])
    return {"missing": sorted(set(installed) - names) if catalogue is not None else None,
            "leaked": sorted((names & repo) - set(installed))}


def run_agent(run_dir: Path, entry: dict, model: str, max_turns: int, timeout: float,
              tools: str, budget: float | None, runner=subprocess.run, skill_install: str = "project",
              root: Path = ROOT) -> dict:
    case_dir = run_dir / entry["id"]
    workspace = case_dir / "workspace"
    add_dir = skills_parent(case_dir, skill_install) if skill_install == "add-dir" else None
    command = agent_command(model, max_turns, tools, budget, add_dir)
    env = os.environ.copy()
    env.update(AGENTIC_ENGINEERING_HOME=str(case_dir / "home"), AES_FIELD_NOTES="off", **AGENT_ENV)
    started, timed_out = time.monotonic(), False
    try:
        proc = runner(command, input=(case_dir / "task.md").read_text(),
                      cwd=workspace, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        code, timed_out = None, True
    (case_dir / "transcript.jsonl").write_text(stdout, encoding="utf-8")
    summary = parse_transcript(stdout.splitlines())
    (case_dir / "final.md").write_text(summary["final"], encoding="utf-8")
    installed = entry.get("skills_installed") or []
    record = {"exit": code, "timed_out": timed_out, "seconds": round(time.monotonic() - started, 1),
              "model": model, "max_turns": max_turns, "tools": tools, **(summary["result"] or {}),
              "command": command,
              "confinement": confinement(tools, skill_install),
              "skills_loaded": summary["skills_loaded"], "skill_files_read": summary["skill_files_read"],
              "skill_md_loaded": skill_md_loaded(summary, installed),
              "permission_denials": summary["permission_denials"],
              "tool_calls": len(summary["tool_calls"]),
              "catalogue": summary["catalogue"],
              "catalogue_check": catalogue_check(summary["catalogue"], installed, root)}
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


def majority(repeats: list[list[dict]]) -> list[dict]:
    """Per assertion: PASS or UNGRADED only on a strict majority, otherwise FAIL; record agreement."""
    combined = []
    for rows in zip(*repeats):
        votes = [row["verdict"] for row in rows]
        counts = Counter(votes)
        verdict = next((v for v in ("PASS", "UNGRADED") if counts[v] * 2 > len(votes)), "FAIL")
        chosen = next(row for row in rows if row["verdict"] == verdict) if verdict in votes else rows[0]
        combined.append({**chosen, "verdict": verdict, "votes": votes,
                         "agreement": round(counts[verdict] / len(votes), 2),
                         "unstable": len(counts) > 1})
    return combined


def judge_case(run_dir: Path, case: dict, backend: str, model: str, timeout: float,
               repeats: int = 3, caller=call_model) -> dict:
    case_dir = run_dir / case["id"]
    evidence, facts = evidence_text(case_dir)
    prompt = judge_prompt(case, evidence, grader_text(case_dir))
    record = {"judge_backend": backend, "judge_model": model}
    if backend == "files":
        answer = case_dir / "judge-answer.json"
        if not answer.exists():
            (case_dir / "judge-prompt.md").write_text(JUDGE_SYSTEM + "\n\n" + prompt, encoding="utf-8")
            return {**record, "status": "awaiting-judge", "judge_repeats": 1, **facts}
        text = answer.read_text(encoding="utf-8")
        (case_dir / "judge-reply-1.txt").write_text(text, encoding="utf-8")
        try:
            parsed, errors = [parse_verdicts(text, case, evidence)], []
        except BackendError as exc:
            parsed, errors = [], [f"reply 1: {exc}"]
    else:
        costs: list = []

        def one(k):
            """One repeat; a reply that cannot be read is asked for once more."""
            problems = []
            for attempt in (1, 2):
                try:
                    reply = caller(backend, prompt, JUDGE_SYSTEM, model, timeout)
                except BackendError as exc:
                    problems.append(f"repeat {k} attempt {attempt}: {exc}")
                    continue
                text = reply.text
                costs.append(getattr(reply, "cost_usd", None))
                suffix = "" if attempt == 1 else "-retry"
                (case_dir / f"judge-reply-{k}{suffix}.txt").write_text(text, encoding="utf-8")
                try:
                    return parse_verdicts(text, case, evidence), problems
                except BackendError as exc:
                    problems.append(f"repeat {k} attempt {attempt}: {exc}")
            return None, problems
        with ThreadPoolExecutor(max_workers=repeats) as pool:
            outcomes = list(pool.map(one, range(1, repeats + 1)))
        parsed = [rows for rows, _ in outcomes if rows is not None]
        errors = [problem for _, problems in outcomes for problem in problems]
        known = [c for c in costs if isinstance(c, (int, float))]
        record["judge_cost_usd"] = round(sum(known), 4) if known else None
    if not parsed:
        return {**record, "status": "judge-error", "error": "; ".join(errors), **facts}
    rows = majority(parsed)
    return {**record, "status": "graded", "assertions": rows,
            "passed": sum(r["verdict"] == "PASS" for r in rows), "total": len(rows),
            "judge_repeats": len(parsed), "judge_errors": errors,
            "agreement": round(sum(r["agreement"] for r in rows) / len(rows), 2),
            "unstable": [r["n"] for r in rows if r["unstable"]], **facts}


# ---------------------------------------------------------------- results

def build_results(root: Path, run_dir: Path, manifest: dict, cases_by_id: dict, graded: dict,
                  scenarios_hash: str, settings: dict) -> dict:
    rows = []
    for entry in manifest["scenarios"]:
        case = cases_by_id[entry["id"]]
        row = {"id": entry["id"], "expected_primary": case["expected_primary"],
               "fixture_status": entry["status"], **{k: entry[k] for k in
               ("note", "reason", "partial", "needs", "skills_missing", "skills_installed", "grader_files")
               if k in entry}}
        if entry["status"] in NOT_RUN:
            row["status"] = entry["status"]
        else:
            row.update(graded.get(entry["id"]) or {"status": "not-run"})
            agent = row.get("agent") or {}
            loaded = agent.get("skills_loaded") or []
            consulted = {path.split("/", 1)[0] for path in agent.get("skill_files_read") or []}
            primary = case["expected_primary"]
            row["primary_loaded"] = primary in loaded if primary else None
            row["primary_consulted"] = primary in consulted | set(loaded) if primary else None
            row["skill_md_loaded"] = {name: name in loaded for name in entry.get("skills_installed") or []}
        rows.append(row)
    catalogue = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
    return {"schema": SCHEMA, "created": now(), "run_dir": str(run_dir),
            "commit": manifest.get("commit"), "scenarios_sha256": scenarios_hash,
            "skills_sha256": sha256_bytes(canonical_json(catalogue)), **settings, "cases": rows}


def format_results(results: dict) -> str:
    lines = ["| Scenario | Status | Assertions passed | Unstable | Judge agreement "
             "| Primary SKILL.md loaded | Primary files read |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    words = {True: "yes", False: "no", None: "n/a"}
    for row in results["cases"]:
        passed = f"{row['passed']}/{row['total']}" if "total" in row else "-"
        unstable = ", ".join(f"A{n}" for n in row.get("unstable") or []) or ("none" if "total" in row else "-")
        agreement = f"{row['agreement']:.2f}" if "agreement" in row else "-"
        loaded = words.get(row.get("primary_loaded"), "-")
        consulted = words.get(row.get("primary_consulted"), "-")
        lines.append(f"| {row['id']} | {row['status']} | {passed} | {unstable} | {agreement} "
                     f"| {loaded} | {consulted} |")
    agent_cost = sum((row.get("agent") or {}).get("total_cost_usd") or 0 for row in results["cases"])
    judge_cost = sum(row.get("judge_cost_usd") or 0 for row in results["cases"])
    if agent_cost or judge_cost:
        lines.append(f"\nCost: agent ${agent_cost:.2f}, judge ${judge_cost:.2f}")
    return "\n".join(lines)


# ---------------------------------------------------------------- command line

def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("list", "prepare", "agent", "judge", "run"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ids", type=lambda s: [x.strip() for x in s.split(",") if x.strip()])
    parser.add_argument("--skill", help="select scenarios by expected_primary")
    parser.add_argument("--tmp-root", type=Path,
                        help="parent for the run directory (default: system temp; never inside the repository)")
    parser.add_argument("--run-dir", type=Path, help="existing run directory (agent, judge)")
    parser.add_argument("--backend", choices=("claude-cli", "files"), default="claude-cli",
                        help="coding agent backend")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="coding agent model")
    parser.add_argument("--skill-install", choices=SKILL_INSTALLS, default="project",
                        help="project: <workspace>/.claude/skills/ (default); add-dir: a sibling "
                             "directory passed with --add-dir, so the workspace does not list them")
    parser.add_argument("--judge-backend", choices=("claude-cli", "files"))
    parser.add_argument("--judge-model", default=DEFAULT_MODEL)
    parser.add_argument("--judge-repeats", type=int, default=3,
                        help="independent judge calls per scenario; majority verdict per assertion")
    parser.add_argument("--max-turns", type=int, default=40)
    parser.add_argument("--timeout", type=float, default=900, help="seconds per agent run")
    parser.add_argument("--max-budget-usd", type=float, help="cost cap per agent run")
    parser.add_argument("--agent-tools", default=AGENT_TOOLS,
                        help="Claude Code tools for the agent; Bash is left out by default and "
                             "cannot be confined to the workspace by path rules")
    parser.add_argument("--out", type=Path, help="results JSON (default: <run dir>/results.json)")
    args = parser.parse_args(argv)
    if args.command in ("agent", "judge") and not args.run_dir:
        parser.error(f"{args.command} needs --run-dir")
    if args.judge_repeats < 1:
        parser.error("--judge-repeats must be at least 1")
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
            run_dir, manifest = prepare(root, select(cases, args.ids, args.skill), fixtures, args.tmp_root,
                                        skill_install=args.skill_install)
            print(f"Prepared {run_dir}", file=sys.stderr)
        else:
            run_dir = args.run_dir.resolve()
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        skill_install = manifest.get("skill_install", "project")
        prepared = [e for e in manifest["scenarios"] if e["status"] not in NOT_RUN]
        for entry in manifest["scenarios"]:
            if entry["status"] in NOT_RUN:
                print(f"{entry['id']}: {entry['status']}, not run", file=sys.stderr)
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
                                   args.agent_tools, args.max_budget_usd, skill_install=skill_install,
                                   root=root)
                print(f"{entry['id']}: agent finished in {record['seconds']}s "
                      f"(turns {record.get('num_turns')}, timed out {record['timed_out']})",
                      file=sys.stderr, flush=True)
            if args.command == "agent":
                return 0
        repeats = 1 if args.judge_backend == "files" else args.judge_repeats
        graded = {}
        for entry in prepared:
            graded[entry["id"]] = judge_case(run_dir, cases_by_id[entry["id"]], args.judge_backend,
                                             args.judge_model, args.timeout, repeats)
            print(f"{entry['id']}: {graded[entry['id']]['status']}", file=sys.stderr, flush=True)
        settings = {"agent_backend": args.backend, "agent_model": args.model,
                    "agent_tools": args.agent_tools, "max_turns": args.max_turns,
                    "timeout_s": args.timeout, "max_budget_usd": args.max_budget_usd,
                    "confinement": confinement(args.agent_tools, skill_install),
                    "judge_backend": args.judge_backend, "judge_model": args.judge_model,
                    "judge_repeats": repeats}
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
