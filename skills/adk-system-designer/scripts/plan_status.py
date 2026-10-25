#!/usr/bin/env python3
"""Roll ticket evidence up into the plan while the build runs. Standard library only; reads Markdown, never runs project code.

``check_schedule.py`` checks a plan before work starts; this script reads what
each ticket session wrote afterwards (status, Evidence contract lines,
``actual:`` hours, ``Rulings:``, resources, a ``Progress:`` block and
``contract_deltas``) and reports:

- each contract and security rule: evidenced (with tier), planned (an
  unfinished goal still cites it), settled in the design (``gap:``,
  ``deferred:`` or ``n/a:``) or orphaned (nothing left will prove it);
- design Evidence cells still ``planned:`` for a contract a ticket evidenced;
- contract deltas the design has not taken in (the contract's row does not yet
  name the goal that revised it) and rulings nobody has settled;
- the ready frontier from actual statuses, interrupted tickets with a
  Progress block, and which ready tickets can run in parallel;
- hours spent and remaining against the phase capacity, and overruns;
- the prompt to paste next: the designer's checkpoint when something above
  needs a decision, otherwise the next ticket.

``--gate`` turns the report into a phase-exit check. ``--weekly`` prints a
status update and RAID log for stakeholders instead.
Exit status: 0 healthy (or gate passed), 1 checkpoint needed (or gate failed),
2 when the input cannot be read.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys

from check_schedule import InputError, fmt as fmt_range
from plan_files import (CONTRACT_ID, FINISHED, RULE_ID, design_contracts, design_rules, read_plan_goals,
                        read_tickets, touches_overlap)

def fmt(pair) -> str:
    return f"{pair[0]:g}" if pair[0] == pair[1] else fmt_range(pair)


SETTLED_CELL = re.compile(r"^\s*(?:gap|deferred|n/?a)\s*:", re.IGNORECASE)
OVERRUN_FACTOR = 1.5


def merge(plan_goals: list[dict], tickets: list[dict]) -> list[dict]:
    """One record per goal; a ticket, when present, is the goal's home for status and evidence."""
    by_ticket = {t["goal"]: t for t in tickets}
    goals = []
    for goal in plan_goals:
        ticket = by_ticket.pop(goal["goal"], None)
        record = {"goal": goal["goal"], "phase": goal["phase"], "type": goal["type"], "status": goal["status"],
                  "total": goal["total"], "owner": goal["owner"], "blocked_by": goal["blocked_by"],
                  "contracts": goal["contracts"], "security": goal["security"], "touches": [], "deltas": [],
                  "evidence": goal["evidence"], "acceptance": goal["acceptance"], "file": None}
        if ticket:
            record.update({k: ticket[k] or record[k] for k in ("type", "status", "phase", "owner", "total")})
            record.update(blocked_by=ticket["blocked_by"] or record["blocked_by"],
                          contracts=sorted(set(record["contracts"]) | set(ticket["contracts"])),
                          security=sorted(set(record["security"]) | set(ticket["security"])),
                          touches=ticket["touches"], deltas=ticket["deltas"], evidence=ticket["evidence"],
                          acceptance=ticket["acceptance"], file=ticket["file"])
        goals.append(record)
    for ticket in by_ticket.values():
        goals.append({k: ticket[k] for k in ("goal", "phase", "type", "status", "total", "owner", "blocked_by",
                                            "contracts", "security", "touches", "deltas", "evidence",
                                            "acceptance", "file")})
    return goals


def in_phase(goal: dict, phase: str) -> bool:
    return not phase or goal["phase"] in (phase, f"phase {phase}")


def coverage(goals: list[dict], table: dict[str, dict], key: str, pattern: re.Pattern) -> dict:
    """State of each design ID: evidenced, planned, settled in the design or orphaned."""
    evidenced, cited_open = {}, {}
    for goal in goals:
        for ident, lines in goal["evidence"]["lines"].items():
            if pattern.fullmatch(ident):
                for line in lines:
                    if line["state"] == "evidenced":
                        evidenced.setdefault(ident, []).append(f"{goal['goal']} {line['tier']}".strip())
        if goal["status"] not in FINISHED:
            for ident in goal[key]:
                cited_open.setdefault(ident, []).append(goal["goal"])
    report = {"evidenced": {}, "planned": {}, "settled": {}, "orphaned": [], "stale_design_cells": [],
              "unknown": sorted(set(evidenced) - set(table)) if table else []}
    for ident, row in sorted(table.items(), key=lambda kv: int(re.sub(r"\D", "", kv[0]))):
        cell = row["last"]
        depth = next((v for h, v in row["cells"].items() if h.startswith("depth")), "")
        if ident in evidenced:
            report["evidenced"][ident] = evidenced[ident]
            if re.match(r"^\s*planned\b", cell, re.IGNORECASE):
                report["stale_design_cells"].append(ident)
        elif SETTLED_CELL.match(cell):
            report["settled"][ident] = cell
        elif ident in cited_open:
            report["planned"][ident] = cited_open[ident]
        elif re.match(r"\s*(?:defer|n/?a)", depth, re.IGNORECASE):
            report["settled"][ident] = f"depth {depth}"
        else:
            report["orphaned"].append(ident)
    return report


def pending_deltas(goals: list[dict], contracts: dict[str, dict]) -> list[str]:
    """A contract delta is taken in when the design's row for that contract names the goal that revised it."""
    found = []
    for goal in goals:
        for delta in goal["deltas"]:
            ids = CONTRACT_ID.findall(delta) or ["(no contract ID)"]
            for ident in ids:
                row = contracts.get(ident, {}).get("row", "")
                if not re.search(rf"(?<![\w-]){re.escape(goal['goal'])}(?![\w-])", row):
                    found.append(f"{goal['goal']}: {delta}")
                    break
    return found


def frontier(goals: list[dict], phase: str) -> tuple[list[dict], list[dict], dict[str, list[str]]]:
    """Ready goals (all in-plan blockers finished), interrupted goals, and what each waiting goal waits for."""
    by_id = {g["goal"]: g for g in goals}
    ready, interrupted, waiting = [], [], {}
    for goal in goals:
        if not in_phase(goal, phase) or goal["status"] in FINISHED:
            continue
        if goal["evidence"]["progress"]:
            interrupted.append(goal)
        open_blockers = [b for b in goal["blocked_by"] if b in by_id and by_id[b]["status"] not in FINISHED]
        outside = [b for b in goal["blocked_by"] if b not in by_id]
        if goal["status"] == "blocked" or open_blockers or outside:
            waiting[goal["goal"]] = open_blockers + outside + (["status blocked"] if goal["status"] == "blocked"
                                                               else [])
        else:
            ready.append(goal)
    return ready, interrupted, waiting


def parallel_groups(ready: list[dict]) -> tuple[list[list[str]], list[str]]:
    """Greedy groups of ready goals whose touches do not overlap, plus the overlaps found."""
    groups, overlaps = [], []
    for goal in ready:
        if not goal["touches"]:
            continue
        for other in ready:
            if other["goal"] > goal["goal"] and other["touches"]:
                shared = touches_overlap(goal["touches"], other["touches"])
                if shared:
                    overlaps.append(f"{goal['goal']} and {other['goal']} both write {', '.join(shared)}")
        for group in groups:
            if all(not touches_overlap(goal["touches"], g["touches"]) for g in group):
                group.append(goal)
                break
        else:
            groups.append([goal])
    return [[g["goal"] for g in group] for group in groups if len(group) > 1], overlaps


def effort(goals: list[dict], phase: str, capacity: float | None) -> dict:
    spent, spent_estimated, remaining, overruns, notes = [0.0, 0.0], [], [0.0, 0.0], [], []
    for goal in goals:
        if not in_phase(goal, phase) or goal["total"] is None:
            continue
        actual = goal["evidence"]["actual"]
        if goal["status"] in FINISHED:
            if actual:
                spent = [spent[0] + actual[0], spent[1] + actual[1]]
                # A finished overrun is history; its consequence is the phase fit below, which stays a
                # trigger until the cut line moves. Flagging it again would make every checkpoint recur.
                if actual[1] > goal["total"][1] * OVERRUN_FACTOR:
                    notes.append(f"{goal['goal']}: {fmt(actual)} h against an estimate of {fmt(goal['total'])} h; "
                                 "re-estimate similar tickets")
                elif actual[1] > goal["total"][1]:
                    notes.append(f"{goal['goal']}: {fmt(actual)} h, above its {fmt(goal['total'])} h estimate")
            else:
                spent = [spent[0] + goal["total"][0], spent[1] + goal["total"][1]]
                spent_estimated.append(goal["goal"])
        else:
            if actual and actual[1] > goal["total"][1]:
                overruns.append(f"{goal['goal']}: already {fmt(actual)} h against {fmt(goal['total'])} h, unfinished; "
                                "split the remainder into its own ticket")
            remaining = [remaining[0] + goal["total"][0], remaining[1] + goal["total"][1]]
    projected = (spent[0] + remaining[0], spent[1] + remaining[1])
    result = {"spent": tuple(spent), "spent_from_estimates": spent_estimated, "remaining": tuple(remaining),
              "projected": projected, "overruns": overruns, "above_estimate": notes}
    if capacity is not None:
        result["capacity"] = capacity
        result["fits"] = "yes" if projected[1] <= capacity else ("low end only" if projected[0] <= capacity else "no")
    return result


def analyse(goals, contracts, rules, phase, capacity):
    phase_goals = [g for g in goals if in_phase(g, phase)]
    # Coverage spans every goal: a contract a later phase still cites is planned, not orphaned.
    contract_cov = coverage(goals, contracts, "contracts", CONTRACT_ID) if contracts else {}
    rule_cov = coverage(goals, rules, "security", RULE_ID) if rules else {}
    for cov, key in ((contract_cov, "contracts"), (rule_cov, "security")):
        if cov:
            cov["phase_cited"] = sorted({i for g in phase_goals for i in g[key]})
    ready, interrupted, waiting = frontier(goals, phase)
    groups, overlaps = parallel_groups(ready)
    rulings = [f"{g['goal']}: {r}" for g in phase_goals for r in g["evidence"]["open_rulings"]
               if g["status"] in FINISHED or g["status"] == "in_progress"]
    deltas = pending_deltas(phase_goals, contracts) if contracts else [
        f"{g['goal']}: {d}" for g in phase_goals for d in g["deltas"]]
    unknown_resources = [f"{g['goal']}: {r['name']}" for g in phase_goals for r in g["evidence"]["resources"]
                         if r["state"] == "unknown"]
    work = effort(goals, phase, capacity)
    triggers = []
    triggers += [f"contract delta not yet in the design: {d}" for d in deltas]
    triggers += [f"open ruling: {r}" for r in rulings]
    triggers += [f"overrun: {o}" for o in work["overruns"]]
    triggers += [f"blocked: {g['goal']}" for g in phase_goals if g["status"] == "blocked"]
    if work.get("fits") in ("no", "low end only"):
        triggers.append(f"phase no longer fits: {fmt(work['projected'])} h projected against "
                        f"{work['capacity']:g} h available")
    for label, cov in (("contract", contract_cov), ("security rule", rule_cov)):
        triggers += [f"orphaned {label} {i}: no finished goal evidenced it and no open goal cites it"
                     for i in cov.get("orphaned", [])]
    return {"phase": phase or "all", "goals": len(phase_goals),
            "status_counts": {s: sum(1 for g in phase_goals if (g["status"] or "unset") == s)
                              for s in sorted({g["status"] or "unset" for g in phase_goals})},
            "contracts": contract_cov, "security": rule_cov, "ready": [g["goal"] for g in ready],
            "ready_files": {g["goal"]: str(g["file"]) for g in ready if g["file"]},
            "interrupted": {g["goal"]: g["evidence"]["progress"] for g in interrupted},
            "interrupted_files": {g["goal"]: str(g["file"]) for g in interrupted if g["file"]},
            "waiting": waiting, "parallel_groups": groups, "touch_overlaps": overlaps,
            "open_rulings": rulings, "pending_deltas": deltas, "unknown_resources": unknown_resources,
            "effort": work, "checkpoint": triggers}


def gate(result: dict, goals: list[dict], phase: str) -> list[str]:
    """Reasons the phase cannot be called complete."""
    reasons = []
    phase_goals = [g for g in goals if in_phase(g, phase)]
    for goal in phase_goals:
        if goal["status"] not in FINISHED:
            reasons.append(f"{goal['goal']} is {goal['status'] or 'without a status'}")
    types = {g["type"] for g in phase_goals}
    if "implementation" in types and "journey" not in types:
        reasons.append("the phase has implementation goals but no journey goal")
    for label, cov in (("contract", result["contracts"]), ("security rule", result["security"])):
        for ident in cov.get("phase_cited", []):
            if ident not in cov["evidenced"] and ident not in cov["settled"]:
                reasons.append(f"{label} {ident} is neither evidenced nor recorded as gap, deferred or n/a")
    reasons += [f"open ruling: {r}" for r in result["open_rulings"]]
    reasons += [f"contract delta not in the design: {d}" for d in result["pending_deltas"]]
    reasons += [f"resource state unknown: {r}" for r in result["unknown_resources"]]
    return reasons


def next_prompt(result: dict, plan: Path | None, tickets: Path | None) -> str:
    source = plan or tickets
    if result["checkpoint"]:
        return f"/adk-system-designer Checkpoint {source}: {len(result['checkpoint'])} item(s) need a decision."
    if result["interrupted"]:
        goal = next(iter(result["interrupted"]))
        where = result["interrupted_files"].get(goal) or f"{goal} from {source}"
        return f"/adk-engineer Resume {where} from its Progress block."
    if result["ready"]:
        goal = result["ready"][0]
        where = result["ready_files"].get(goal)
        return f"/adk-engineer Carry out {where}." if where else f"/adk-engineer Carry out {goal} from {source}."
    if not result["waiting"]:
        return f"Every goal of phase {result['phase']} is finished; run this script with --gate before its review."
    return "Nothing is ready; the waiting goals and what they wait for are listed above."


def changed_since(paths: list[Path], since: str) -> list[str]:
    """Files under the given paths that git records as changed since a date or commit; empty without git."""
    args = ["git", "log", "--name-only", "--format="]
    args += [f"--since={since}"] if re.match(r"^\d{4}-\d{2}-\d{2}$", since) else [f"{since}..HEAD"]
    args += ["--"] + [str(p) for p in paths]
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=30,
                             cwd=paths[0].parent if paths[0].is_file() else paths[0])
    except (OSError, subprocess.TimeoutExpired):
        return []
    return sorted({Path(l).name for l in out.stdout.splitlines() if l.strip()}) if out.returncode == 0 else []


def weekly(result: dict, goals: list[dict], plan: Path | None, tickets: Path | None, since: str | None) -> str:
    today = dt.date.today()
    lines = [f"# Status update · {today.day} {today:%B %Y}", ""]
    finished = [g for g in goals if g["status"] in FINISHED and in_phase(g, result["phase"] if result["phase"] != "all" else "")]
    changed = changed_since([p for p in (plan, tickets) if p], since) if since else []
    if changed:
        moved = [g for g in finished if g["file"] and Path(g["file"]).name in changed]
        lines.append(f"**Finished since {since}:** " + (", ".join(g["goal"] for g in moved) or "none"))
    lines.append(f"**Finished in the phase:** {len(finished)} of {result['goals']} goals")
    work = result["effort"]
    hours = f"{fmt(work['spent'])} h spent, {fmt(work['remaining'])} h remaining"
    if "capacity" in work:
        hours += f", {fmt(work['projected'])} h projected against {work['capacity']:g} h (fits: {work['fits']})"
    lines += [f"**Effort:** {hours}", ""]
    contracts = result["contracts"]
    if contracts:
        lines.append(f"**Promises proven:** {len(contracts['evidenced'])} of "
                     f"{sum(len(contracts[k]) for k in ('evidenced', 'planned', 'settled')) + len(contracts['orphaned'])}"
                     " contracts evidenced")
    lines += ["", "## Next", ""]
    lines += [f"- {g}" for g in result["ready"][:5]] or ["- Nothing ready"]
    lines += ["", "## RAID", "", "| Type | Item | Owner or next step |", "| --- | --- | --- |"]
    for item in result["checkpoint"]:
        kind = "Issue" if item.startswith(("overrun", "blocked", "phase")) else "Risk"
        lines.append(f"| {kind} | {item} | Designer checkpoint |")
    for note in result["effort"]["above_estimate"]:
        lines.append(f"| Issue | above estimate: {note} | Designer checkpoint |")
    ids = {g["goal"] for g in goals}
    for goal, waits in result["waiting"].items():
        outside = [w for w in waits if w not in ids and w != "status blocked"]
        if outside:
            lines.append(f"| Dependency | {goal} waits for {', '.join(outside)} | Named owner of each |")
    for ident in result["unknown_resources"]:
        lines.append(f"| Issue | Resource state unknown: {ident} | Teardown owner |")
    if len(lines) and lines[-1].startswith("| ---"):
        lines.append("| — | Nothing open | — |")
    lines += ["", "Figures come from the plan and tickets as recorded; assumptions stay labelled where they "
              "are written."]
    return "\n".join(lines)


def report(result: dict, prompt: str) -> str:
    lines = [f"Phase {result['phase']}: {result['goals']} goals; "
             + ", ".join(f"{n} {s}" for s, n in result["status_counts"].items())]
    work = result["effort"]
    line = f"Hours: {fmt(work['spent'])} spent, {fmt(work['remaining'])} remaining, {fmt(work['projected'])} projected"
    if "capacity" in work:
        line += f" against {work['capacity']:g} available; fits: {work['fits']}"
    lines.append(line)
    if work["spent_from_estimates"]:
        lines.append("  Finished without an actual: line (estimate counted): " + ", ".join(work["spent_from_estimates"]))
    lines += [f"  Above estimate (finished): {n}" for n in work["above_estimate"]]
    for label, cov in (("Contracts", result["contracts"]), ("Security rules", result["security"])):
        if not cov:
            continue
        lines.append(f"{label}: {len(cov['evidenced'])} evidenced, {len(cov['planned'])} planned, "
                     f"{len(cov['settled'])} settled in the design, {len(cov['orphaned'])} orphaned")
        lines += [f"  {i} evidenced: {', '.join(v)}" for i, v in cov["evidenced"].items()]
        if cov["stale_design_cells"]:
            lines.append("  Design Evidence cell still says planned (update it to the evidence): "
                         + ", ".join(cov["stale_design_cells"]))
        if cov["unknown"]:
            lines.append("  Evidence names IDs the design does not have: " + ", ".join(cov["unknown"]))
    if result["ready"]:
        lines.append("Ready: " + ", ".join(result["ready"]))
    for goal, progress in result["interrupted"].items():
        lines.append(f"Interrupted: {goal} has a Progress block ({'; '.join(progress)[:160]})")
    for goal, waits in result["waiting"].items():
        lines.append(f"Waiting: {goal} on {', '.join(waits)}")
    for group in result["parallel_groups"]:
        lines.append("Can run in parallel (no shared touches): " + ", ".join(group))
    lines += [f"Not parallel: {o}" for o in result["touch_overlaps"]]
    for item in result["checkpoint"]:
        lines.append(f"CHECKPOINT: {item}")
    lines.append(f"Next: {prompt}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plan", type=Path, help="plan Markdown with a fenced yaml schedule block")
    parser.add_argument("--tickets", type=Path, help="directory of ticket files")
    parser.add_argument("--design", type=Path, help="design Markdown with the contracts and security tables")
    parser.add_argument("--phase", default="1", help="phase to report; empty for every goal")
    parser.add_argument("--capacity", type=float, help="hours available for the phase after the reserve")
    parser.add_argument("--gate", action="store_true", help="exit 0 only when the phase can be called complete")
    parser.add_argument("--weekly", action="store_true", help="print a stakeholder status update and RAID log")
    parser.add_argument("--since", help="with --weekly: a date (YYYY-MM-DD) or commit for 'finished since'")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.plan and not args.tickets:
            raise InputError("give --plan, --tickets or both")
        plan_goals = read_plan_goals(args.plan) if args.plan else []
        tickets = read_tickets(args.tickets) if args.tickets else []
        if args.tickets and not tickets:
            raise InputError(f"{args.tickets}: no ticket files with a goal in their front matter")
        goals = merge(plan_goals, tickets)
        contracts = design_contracts(args.design) if args.design else {}
        rules = design_rules(args.design) if args.design else {}
        result = analyse(goals, contracts, rules, args.phase, args.capacity)
    except (InputError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    prompt = next_prompt(result, args.plan, args.tickets)
    result["next"] = prompt
    if args.gate:
        reasons = gate(result, goals, args.phase)
        result["gate"] = {"passed": not reasons, "reasons": reasons}
        if args.json:
            print(json.dumps(result, indent=1, default=str))
        else:
            print(f"Phase {result['phase']} exit gate: {'passed' if not reasons else 'not passed'}")
            for reason in reasons:
                print(f"  {reason}")
        return 0 if not reasons else 1
    if args.weekly:
        print(weekly(result, goals, args.plan, args.tickets, args.since))
        return 0
    print(json.dumps(result, indent=1, default=str) if args.json else report(result, prompt))
    return 1 if result["checkpoint"] else 0


if __name__ == "__main__":
    sys.exit(main())
