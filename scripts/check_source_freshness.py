#!/usr/bin/env python3
"""Report whether the external repositories this toolkit cites are still maintained.

Reads docs/research/source-register.json, asks the GitHub REST API (read only)
about each repository, and reports its band (active, quiet or stale by days
since the last commit on the default branch), latest release, commits since the
commit the toolkit read, and anything that needs a maintainer: an archived,
renamed or missing repository, a changed licence, a stale band or a pinned
commit GitHub no longer has. It changes nothing.

Exit codes: 0 nothing needs attention; 1 at least one source needs attention;
2 the register or the arguments are invalid; 3 at least one source could not be
checked (network error or rate limit), so the result is incomplete.

The band thresholds are placeholders for a maintainer's judgement, not policy;
set them with --quiet-after-days and --stale-after-days. A token in GITHUB_TOKEN
or GH_TOKEN raises GitHub's rate limit and is sent only to api.github.com.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
import json
import os
from pathlib import Path
import re
import sys
from typing import Callable
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
FIELDS = {"id", "repo", "pinned", "read", "licence", "note", "used_by"}

Fetch = Callable[[str], tuple[int, object]]


class RateLimited(Exception):
    pass


def _iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def load_register(path: Path, root: Path) -> tuple[list[dict], list[str]]:
    """Return the sources and every structural error; never touches the network."""
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return [], [f"{path}: {exc}"]
    if (not isinstance(data, dict) or data.get("version") != 1
            or not isinstance(data.get("sources"), list) or not data["sources"]):
        return [], [f"{path}: expected version 1 and a nonempty sources list"]
    skills = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_repos: set[str] = set()
    for index, src in enumerate(data["sources"]):
        label = src.get("id", f"#{index}") if isinstance(src, dict) else f"#{index}"
        if not isinstance(src, dict) or set(src) != FIELDS:
            errors.append(f"{label}: expected exactly the fields {sorted(FIELDS)}")
            continue
        if not isinstance(src["id"], str) or not ID_RE.match(src["id"]) or src["id"] in seen_ids:
            errors.append(f"{label}: id must be unique lowercase-kebab text")
        seen_ids.add(src["id"])
        repo = src["repo"]
        if not isinstance(repo, str) or not REPO_RE.match(repo):
            errors.append(f"{label}: repo must be owner/name")
        elif repo.lower() in seen_repos:
            errors.append(f"{label}: repo {repo} is listed twice")
        else:
            seen_repos.add(repo.lower())
        if src["pinned"] is not None and (not isinstance(src["pinned"], str)
                                          or not SHA_RE.match(src["pinned"])):
            errors.append(f"{label}: pinned must be null or a 7-40 character commit")
        if not _iso_date(src["read"]):
            errors.append(f"{label}: read must be an ISO date")
        if not isinstance(src["licence"], str) or not src["licence"].strip():
            errors.append(f"{label}: licence must be the SPDX id GitHub reported, or none")
        note = src["note"]
        if (not isinstance(note, str) or not note.startswith("docs/")
                or not (root / note).is_file()):
            errors.append(f"{label}: note must be an existing file under docs/")
        used = src["used_by"]
        if not isinstance(used, list) or not all(isinstance(s, str) for s in used):
            errors.append(f"{label}: used_by must be a list of skill names")
        else:
            unknown = sorted(set(used) - skills)
            if unknown:
                errors.append(f"{label}: used_by names unknown skills {unknown}")
    return data["sources"], errors


def github_fetch(token: str | None) -> Fetch:
    def fetch(path: str) -> tuple[int, object]:
        request = urllib.request.Request(API + path, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "agentic-engineering-skills-freshness",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.status, json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 or (exc.code == 403 and
                                   exc.headers.get("x-ratelimit-remaining") == "0"):
                raise RateLimited(f"GitHub rate limit ({exc.code})") from None
            return exc.code, None
    return fetch


def band(days: int, quiet_after: int, stale_after: int) -> str:
    if days > stale_after:
        return "stale"
    if days > quiet_after:
        return "quiet"
    return "active"


def _day(stamp: object) -> date | None:
    if not isinstance(stamp, str):
        return None
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _blank(src: dict, error: str | None = None) -> dict:
    return {"id": src["id"], "repo": src["repo"], "band": "unchecked", "attention": [],
            "last_commit": None, "days": None, "release": None, "since_pin": None,
            "licence": None, "error": error}


def check_source(src: dict, fetch: Fetch, today: date,
                 quiet_after: int, stale_after: int) -> dict:
    result = _blank(src)
    repo = urllib.parse.quote(src["repo"], safe="/")
    status, meta = fetch(f"/repos/{repo}")
    if status == 404:
        result["attention"].append("repository not found")
        result["band"] = "missing"
        return result
    if status != 200 or not isinstance(meta, dict):
        result["error"] = f"repository lookup returned HTTP {status}"
        return result
    full_name = meta.get("full_name") or src["repo"]
    if full_name.lower() != src["repo"].lower():
        result["attention"].append(f"renamed to {full_name}")
    if meta.get("archived"):
        result["attention"].append("archived")
    licence = (meta.get("license") or {}).get("spdx_id") or "none"
    result["licence"] = licence
    if licence != src["licence"]:
        result["attention"].append(f"licence changed from {src['licence']} to {licence}")
    branch = urllib.parse.quote(meta.get("default_branch") or "main", safe="")
    status, commits = fetch(f"/repos/{repo}/commits?per_page=1&sha={branch}")
    last = None
    if status == 200 and isinstance(commits, list) and commits:
        last = _day(((commits[0].get("commit") or {}).get("committer") or {}).get("date"))
    if last is None:
        result["error"] = f"latest commit lookup returned HTTP {status}"
        return result
    result["last_commit"] = last.isoformat()
    result["days"] = (today - last).days
    result["band"] = band(result["days"], quiet_after, stale_after)
    if result["band"] == "stale":
        result["attention"].append(f"no commit for {result['days']} days")
    status, release = fetch(f"/repos/{repo}/releases/latest")
    if status == 200 and isinstance(release, dict):
        published = _day(release.get("published_at"))
        result["release"] = f"{release.get('tag_name')} ({published})" if published else release.get("tag_name")
    if src["pinned"]:
        status, compare = fetch(f"/repos/{repo}/compare/{src['pinned']}...{branch}")
        if status == 200 and isinstance(compare, dict):
            result["since_pin"] = compare.get("ahead_by")
        elif status == 404:
            result["attention"].append(f"pinned commit {src['pinned']} not found")
        else:
            result["error"] = f"comparison with the pinned commit returned HTTP {status}"
    return result


def render(result: dict) -> str:
    parts = [f"{result['id']:<28}", f"{result['band']:<9}"]
    if result["last_commit"]:
        parts.append(f"last commit {result['last_commit']} ({result['days']}d)")
    if result["release"]:
        parts.append(f"release {result['release']}")
    if result["since_pin"] is not None:
        parts.append(f"+{result['since_pin']} since read")
    if result["error"]:
        parts.append(f"UNCHECKED: {result['error']}")
    if result["attention"]:
        parts.append("ATTENTION: " + "; ".join(result["attention"]))
    return "  ".join(parts)


def main(argv: list[str] | None = None, fetch: Fetch | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    root_default = Path(__file__).resolve().parents[1]
    parser.add_argument("--root", type=Path, default=root_default)
    parser.add_argument("--register", type=Path,
                        help="default: <root>/docs/research/source-register.json")
    parser.add_argument("--only", action="append", default=[], metavar="ID",
                        help="check only this source id (repeatable)")
    parser.add_argument("--quiet-after-days", type=int, default=30)
    parser.add_argument("--stale-after-days", type=int, default=365)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(),
                        help=argparse.SUPPRESS)
    parser.add_argument("--validate-only", action="store_true",
                        help="check the register's structure without network calls")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    root = args.root.resolve()
    sources, errors = load_register(args.register or root / "docs/research/source-register.json", root)
    if not 0 < args.quiet_after_days < args.stale_after_days:
        errors.append("--quiet-after-days must be positive and below --stale-after-days")
    unknown = sorted(set(args.only) - {s.get("id") for s in sources if isinstance(s, dict)})
    if unknown:
        errors.append(f"--only names unknown ids {unknown}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    if args.validate_only:
        print(f"Register valid: {len(sources)} sources; nothing was fetched.")
        return 0
    if fetch is None:
        fetch = github_fetch(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    results = []
    limited = None
    for src in sources:
        if args.only and src["id"] not in args.only:
            continue
        if limited:
            result = _blank(src, limited)
        else:
            try:
                result = check_source(src, fetch, args.today,
                                      args.quiet_after_days, args.stale_after_days)
            except RateLimited as exc:
                limited = str(exc)
                result = _blank(src, limited)
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                result = _blank(src, f"{type(exc).__name__}: {exc}")
        results.append(result)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(render(result))
        print(f"\nChecked {len(results)} sources on {args.today}; bands use "
              f"{args.quiet_after_days} and {args.stale_after_days} days (placeholders).")
    if any(r["error"] for r in results):
        return 3
    if any(r["attention"] for r in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
