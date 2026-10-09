#!/usr/bin/env python3
"""Check a plan's effort estimates and schedule. Standard library only; reads Markdown, never runs project code.

Reads goals from the plan's fenced ``yaml`` schedule block (a list of
``- goal:`` entries) and, optionally, the front matter of ticket files. Reports
the phase total against capacity, ticket and plan mismatches, the longest
dependent chain, each person's load and a finish estimate in working days that
respects dependencies, one person doing one goal at a time, and calendar waits.

Estimates are ranges of human hours (``1-2``, ``1.5 to 3``, ``2 h``). Exit
status: 0 when consistent and within capacity and calendar, 1 when something
does not fit or disagrees, 2 when the input cannot be read.
"""

import argparse
import json
from pathlib import Path
import re
import sys

RANGE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(?:(?:-|–|—|to)\s*(\d+(?:\.\d+)?))?\s*(?:h|hours?|person-hours?)?\s*$",
                   re.IGNORECASE)
FENCE = re.compile(r"^```(?:yaml|yml)\s*$(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
ESTIMATE_KEYS = {"hands_on", "review", "review_and_verify", "total", "calendar_waits", "wait_days"}


class InputError(Exception):
    pass


def parse_range(value, where):
    if value is None or str(value).strip() == "":
        return None
    match = RANGE.match(str(value))
    if not match:
        raise InputError(f"{where}: cannot read hours range {value!r}; write e.g. 1-2 or 3")
    low = float(match.group(1))
    high = float(match.group(2)) if match.group(2) else low
    if high < low:
        raise InputError(f"{where}: range {value!r} has its high end below its low end")
    return (low, high)


def parse_scalar(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        return [item.strip().strip("'\"") for item in text[1:-1].split(",") if item.strip()]
    if " #" in text:
        text = text.split(" #", 1)[0].rstrip()
    return text


def parse_mapping(lines, where):
    """Parse flat `key: value` lines, with one level of nesting (as under `estimate:`)."""
    result, parent = {}, None
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        if ":" not in raw:
            raise InputError(f"{where}: cannot read line {raw.strip()!r}")
        key, value = raw.strip().split(":", 1)
        key = key.strip()
        if indent and parent is not None:
            result[parent][key] = parse_scalar(value)
            continue
        if value.strip() == "" or value.strip().startswith("#"):
            result[key], parent = {}, key
        else:
            result[key], parent = parse_scalar(value), None
    return result


def flatten(entry):
    estimate = entry.pop("estimate", None)
    if isinstance(estimate, dict):
        for key, value in estimate.items():
            entry.setdefault(key, value)
    elif estimate not in (None, ""):
        entry.setdefault("total", estimate)
    if "review_and_verify" in entry:
        entry.setdefault("review", entry.pop("review_and_verify"))
    return entry


def normalise(entry, where):
    goal = str(entry.get("goal", "")).strip()
    if not goal:
        raise InputError(f"{where}: entry without a goal ID")
    blocked = entry.get("blocked_by", entry.get("depends_on", []))
    if isinstance(blocked, str):
        blocked = [] if blocked.strip().lower() in ("", "none", "-") else [b.strip() for b in blocked.split(",")]
    waits = entry.get("calendar_waits", "")
    wait_days = parse_range(entry.get("wait_days"), f"{where} {goal} wait_days") or (0.0, 0.0)
    total = parse_range(entry.get("total"), f"{where} {goal} total")
    hands_on = parse_range(entry.get("hands_on"), f"{where} {goal} hands_on")
    review = parse_range(entry.get("review"), f"{where} {goal} review")
    if total is None and hands_on and review:
        total = (hands_on[0] + review[0], hands_on[1] + review[1])
    if total is None:
        raise InputError(f"{where} {goal}: no total estimate")
    return {"goal": goal, "phase": str(entry.get("phase", "")).strip(), "total": total,
            "hands_on": hands_on, "review": review, "owner": str(entry.get("owner", "")).strip(),
            "blocked_by": [b for b in blocked if b], "waits": str(waits).strip(), "wait_days": wait_days}


def read_plan(path):
    text = path.read_text(encoding="utf-8")
    for block in FENCE.findall(text):
        if re.search(r"^\s*-\s*goal\s*:", block, re.MULTILINE):
            entries, current = [], None
            for line in block.splitlines():
                item = re.match(r"^(\s*)-\s+(.*)$", line)
                if item and re.match(r"goal\s*:", item.group(2)):
                    current = [" " * (len(item.group(1)) + 2) + item.group(2)]
                    entries.append(current)
                elif current is not None:
                    current.append(line)
            goals = []
            for lines in entries:
                base = len(lines[0]) - len(lines[0].lstrip())
                trimmed = [l[base:] if l[:base].strip() == "" else l for l in lines]
                goals.append(normalise(flatten(parse_mapping(trimmed, str(path))), str(path)))
            return goals
    raise InputError(f"{path}: no fenced yaml block with '- goal:' entries")


def read_tickets(directory):
    goals = []
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            raise InputError(f"{path}: front matter is not closed")
        data = flatten(parse_mapping(text[3:end].splitlines(), str(path)))
        if "goal" in data:
            goals.append(dict(normalise(data, str(path)), file=path.name))
    return goals


def hours_per_day(people, default):
    table = {}
    for item in people or []:
        if "=" not in item:
            raise InputError(f"--person {item!r}: write NAME=HOURS_PER_DAY")
        name, value = item.rsplit("=", 1)
        table[name.strip()] = float(value)
    return table, default


def analyse(goals, phase, capacity, days, people, default_hpd, reserve=0.0):
    by_id = {}
    for goal in goals:
        if goal["goal"] in by_id:
            raise InputError(f"goal {goal['goal']} appears twice")
        by_id[goal["goal"]] = goal
    selected = [g for g in goals if not phase or g["phase"] in (phase, f"phase {phase}")]
    chosen = {g["goal"] for g in selected}
    problems, external = [], set()
    for goal in selected:
        external.update(d for d in goal["blocked_by"] if d not in by_id)
        if goal["hands_on"] and goal["review"]:
            parts = (goal["hands_on"][0] + goal["review"][0], goal["hands_on"][1] + goal["review"][1])
            if any(abs(a - b) > 0.01 for a, b in zip(parts, goal["total"])):
                problems.append(f"{goal['goal']}: hands_on + review = {fmt(parts)} but total is {fmt(goal['total'])}")
    ratios = [g["review"][1] / g["hands_on"][1] for g in selected
              if g["hands_on"] and g["review"] and g["hands_on"][1] > 0]
    if len(ratios) >= 5 and max(ratios) - min(ratios) < 0.15:
        problems.append(f"review is {min(ratios):.2f}-{max(ratios):.2f} of hands-on on every goal; size review "
                        "to the change (heavier for authorization, money and security, lighter for templates)")
    total = (sum(g["total"][0] for g in selected), sum(g["total"][1] for g in selected))
    table, _ = hours_per_day(people, default_hpd)

    def rate(owner):
        return table.get(owner, default_hpd) * (1.0 - reserve)

    deps = {g["goal"]: [d for d in g["blocked_by"] if d in chosen] for g in selected}
    order, state = [], {}

    def visit(node, trail):
        if state.get(node) == "done":
            return
        if state.get(node) == "open":
            raise InputError("dependency cycle: " + " -> ".join(trail + [node]))
        state[node] = "open"
        for dep in deps[node]:
            visit(dep, trail + [node])
        state[node] = "done"
        order.append(node)

    for goal in selected:
        visit(goal["goal"], [])

    result = {"phase": phase or "all", "goals": len(selected), "total_hours": total, "reserve": reserve,
              "problems": problems,
              "outside_dependencies": sorted(external)}
    if capacity is None and days is not None:
        owners = {g["owner"] for g in selected if g["owner"]}
        capacity = round(sum(rate(o) for o in owners) * days, 2) if owners else None
    if capacity is not None:
        result["capacity_hours"] = capacity
        result["fits_capacity"] = "yes" if total[1] <= capacity else ("low end only" if total[0] <= capacity else "no")
    loads = {}
    for goal in selected:
        owner = goal["owner"] or "(unassigned)"
        low, high = loads.get(owner, (0.0, 0.0))
        loads[owner] = (low + goal["total"][0], high + goal["total"][1])
    result["load_by_person"] = loads
    for end, label in ((0, "low"), (1, "high")):
        duration = {g["goal"]: g["total"][end] / rate(g["owner"]) + g["wait_days"][end] for g in selected}
        longest, previous = {}, {}
        for node in order:
            best = max(deps[node], key=lambda d: longest[d], default=None)
            longest[node] = duration[node] + (longest[best] if best else 0.0)
            previous[node] = best
        tail = max(longest, key=longest.get) if longest else None
        chain = []
        while tail:
            chain.append(tail)
            tail = previous[tail]
        remaining = {}
        for node in reversed(order):
            after = [n for n in order if node in deps[n]]
            remaining[node] = duration[node] + max((remaining[n] for n in after), default=0.0)
        finish, free, pending = {}, {}, list(order)
        while pending:
            ready = [n for n in pending if all(d in finish for d in deps[n])]
            node = max(ready, key=lambda n: remaining[n])
            pending.remove(node)
            owner = by_id[node]["owner"]
            start = max([finish[d] for d in deps[node]] + ([free.get(owner, 0.0)] if owner else [0.0]))
            work = by_id[node]["total"][end] / rate(owner)
            if owner:
                free[owner] = start + work
            finish[node] = start + work + by_id[node]["wait_days"][end]
        result[f"chain_{label}"] = {"goals": list(reversed(chain)), "days": round(longest[chain[0]], 2) if chain else 0.0}
        result[f"finish_days_{label}"] = round(max(finish.values(), default=0.0), 2)
    if days is not None:
        result["calendar_days"] = days
        low, high = result["finish_days_low"], result["finish_days_high"]
        result["fits_calendar"] = "yes" if high <= days else ("low end only" if low <= days else "no")
        result["person_capacity"] = {owner: round(rate(owner if owner != "(unassigned)" else "") * days, 2)
                                     for owner in loads}
    return result


def compare(plan_goals, ticket_goals):
    problems = []
    plan = {g["goal"]: g for g in plan_goals}
    for ticket in ticket_goals:
        source = plan.get(ticket["goal"])
        if source is None:
            problems.append(f"{ticket['file']}: goal {ticket['goal']} is not in the plan's schedule block")
            continue
        for field in ("total", "hands_on", "review", "owner", "waits"):
            if ticket[field] and source[field] and ticket[field] != source[field]:
                problems.append(f"{ticket['file']}: {field} {show(ticket[field])} differs from plan {show(source[field])}")
        if set(ticket["blocked_by"]) != set(source["blocked_by"]):
            problems.append(f"{ticket['file']}: blocked_by {sorted(ticket['blocked_by'])} differs from plan "
                            f"{sorted(source['blocked_by'])}")
    return problems


def fmt(pair):
    return f"{pair[0]:g}-{pair[1]:g}"


def show(value):
    return fmt(value) if isinstance(value, tuple) else repr(value)


def report(result):
    lines = [f"Phase {result['phase']}: {result['goals']} goals, {fmt(result['total_hours'])} human hours"]
    if "capacity_hours" in result:
        lines.append(f"Capacity after reserve: {result['capacity_hours']:g} h; fits: {result['fits_capacity']}")
    for owner, load in sorted(result["load_by_person"].items()):
        cap = result.get("person_capacity", {}).get(owner)
        lines.append(f"  {owner}: {fmt(load)} h" + (f" of {cap:g} h available" if cap is not None else ""))
    for label in ("low", "high"):
        chain = result[f"chain_{label}"]
        lines.append(f"Longest dependent chain ({label}): {' -> '.join(chain['goals'])}, {chain['days']:g} working days")
    lines.append(f"Finish with these people and dependencies, {result['reserve']:.0%} of each day held in "
                 f"reserve: {result['finish_days_low']:g}-{result['finish_days_high']:g} working days")
    if "calendar_days" in result:
        lines.append(f"Calendar: {result['calendar_days']:g} working days; fits: {result['fits_calendar']}")
    if result["outside_dependencies"]:
        lines.append("Not scheduled here (decisions, other phases, other teams): "
                     + ", ".join(result["outside_dependencies"]))
    for problem in result["problems"]:
        lines.append(f"PROBLEM: {problem}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plan", type=Path, help="plan Markdown with a fenced yaml schedule block")
    parser.add_argument("--tickets", type=Path, help="directory of ticket files with front matter")
    parser.add_argument("--phase", default="1", help="phase to check; empty for all goals")
    parser.add_argument("--capacity", type=float,
                        help="phase hours available after the reserve; computed from --days and owners if omitted")
    parser.add_argument("--days", type=float, help="working days available on the calendar")
    parser.add_argument("--person", action="append", help="NAME=HOURS_PER_DAY, repeat for each owner")
    parser.add_argument("--reserve", type=float, default=0.25,
                        help="share of each person's hours held back, applied to the calendar too (default 0.25)")
    parser.add_argument("--hours-per-day", type=float, default=6.0,
                        help="focused hours per day for owners not given with --person (default 6)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.plan and not args.tickets:
            raise InputError("give --plan, --tickets or both")
        plan_goals = read_plan(args.plan) if args.plan else []
        ticket_goals = read_tickets(args.tickets) if args.tickets else []
        if args.tickets and not ticket_goals:
            raise InputError(f"{args.tickets}: no ticket files with a goal in their front matter")
        goals = plan_goals or ticket_goals
        if not 0.0 <= args.reserve < 1.0:
            raise InputError("--reserve is a share between 0 and 1, e.g. 0.25")
        result = analyse(goals, args.phase, args.capacity, args.days, args.person, args.hours_per_day,
                         args.reserve)
        if plan_goals and ticket_goals:
            result["problems"] += compare(plan_goals, ticket_goals)
    except (InputError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=1) if args.json else report(result))
    bad = result["problems"] or result.get("fits_capacity", "yes") != "yes" or result.get("fits_calendar", "yes") != "yes"
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
