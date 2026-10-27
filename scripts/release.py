#!/usr/bin/env python3
"""Stamp, prepare and tag a release of the skill collection. Standard library only.

A release is a date version (``YYYY.MM.DD``, or ``YYYY.MM.DD.N`` for a second
release on the same day) written into every ``skills/*/SKILL.md`` as
``metadata.version`` and into the plugin manifests that carry a version, a
``CHANGELOG.md`` section, an annotated tag ``v<version>`` and a local ``stable``
branch moved to that tag. Plugin users who add the marketplace at ``#stable``
receive releases rather than every commit to ``main``.

    release.py stamp 2026.10.25     write the version, nothing else
    release.py prepare              stamp today's version and add a CHANGELOG section
    release.py tag                  tag the stamped, committed version and move stable

``tag`` refuses a dirty worktree or a version that is not stamped everywhere. It
never pushes; it prints the push commands for the maintainer to run.
Exit status: 0 on success, 1 when a check fails, 2 on unusable input.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys

VERSION = re.compile(r"^\d{4}\.\d{2}\.\d{2}(?:\.\d+)?$")
# Manifests whose "version" field follows the collection. The Antigravity
# plugin.json at the root accepts only name and description, so it is not listed.
MANIFESTS = (".claude-plugin/plugin.json", "gemini-extension.json")
CHANGELOG_HEAD = "# Changelog\n\nOne section per tagged release, newest first. Pin a release with\n`npx skills@latest add RuslanKhis/agentic-engineering-skills#v<version> --skill '*'`.\n"


class ReleaseError(Exception):
    pass


def skill_files(root: Path) -> list[Path]:
    files = sorted(root.glob("skills/*/SKILL.md"))
    if not files:
        raise ReleaseError(f"{root}: no skills/*/SKILL.md files")
    return files


def frontmatter_bounds(lines: list[str], path: Path) -> int:
    if not lines or lines[0].strip() != "---":
        raise ReleaseError(f"{path}: no YAML frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index
    raise ReleaseError(f"{path}: frontmatter is not closed")


def stamp_skill(path: Path, version: str) -> bool:
    """Set metadata.version in block-style frontmatter; return whether the file changed."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    end = frontmatter_bounds(lines, path)
    meta = next((i for i in range(1, end) if re.match(r"^metadata:\s*$", lines[i])), None)
    line = f'  version: "{version}"\n'
    if meta is None:
        lines[end:end] = ["metadata:\n", line]
    else:
        stop = meta + 1
        while stop < end and lines[stop].startswith((" ", "\t")):
            stop += 1
        existing = next((i for i in range(meta + 1, stop) if re.match(r"^\s+version:", lines[i])), None)
        if existing is None:
            lines.insert(stop, line)
        else:
            lines[existing] = line
    updated = "".join(lines)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def read_skill_version(path: Path) -> str | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    end = frontmatter_bounds([l + "\n" for l in lines], path)
    inside = False
    for line in lines[1:end]:
        if re.match(r"^metadata:\s*$", line):
            inside = True
            continue
        if inside and not line.startswith((" ", "\t")):
            inside = False
        match = re.match(r"^\s+version:\s*['\"]?([^'\"\s]+)['\"]?\s*$", line) if inside else None
        if match:
            return match.group(1)
    return None


def stamp_manifest(path: Path, version: str) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") == version:
        return False
    data["version"] = version
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def stamp(root: Path, version: str) -> list[Path]:
    if not VERSION.match(version):
        raise ReleaseError(f"version {version!r} is not YYYY.MM.DD or YYYY.MM.DD.N")
    changed = [p for p in skill_files(root) if stamp_skill(p, version)]
    for name in MANIFESTS:
        path = root / name
        if path.exists() and stamp_manifest(path, version):
            changed.append(path)
    return changed


def versions(root: Path) -> dict[str, str | None]:
    found = {str(p.relative_to(root)): read_skill_version(p) for p in skill_files(root)}
    for name in MANIFESTS:
        path = root / name
        if path.exists():
            found[name] = json.loads(path.read_text(encoding="utf-8")).get("version")
    return found


def git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise ReleaseError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


def tags(root: Path) -> list[str]:
    return [t for t in git(root, "tag", "--list", "v*", "--sort=-creatordate").splitlines() if t]


def next_version(root: Path, today: dt.date) -> str:
    base = today.strftime("%Y.%m.%d")
    existing = set(tags(root))
    if f"v{base}" not in existing:
        return base
    n = 1
    while f"v{base}.{n}" in existing:
        n += 1
    return f"{base}.{n}"


def changelog_section(root: Path, version: str, today: dt.date) -> str:
    previous = tags(root)
    if previous:
        subjects = git(root, "log", "--no-merges", "--format=%s", f"{previous[0]}..HEAD").splitlines()
        body = "\n".join(f"- {s}" for s in subjects if s) or "- No commits since the previous release."
        since = f"Changes since {previous[0]}:\n\n"
    else:
        body = ("- First tagged release. Earlier changes are recorded in the testing log, "
                "docs/testing/index.md.")
        since = ""
    when = f"{today.day} {today:%B %Y}"
    return f"## {version} · {when}\n\n{since}{body}\n"


def add_changelog(root: Path, section: str, version: str) -> None:
    path = root / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8") if path.exists() else CHANGELOG_HEAD
    if re.search(rf"^## {re.escape(version)} ", text, re.MULTILINE):
        raise ReleaseError(f"CHANGELOG.md already has a section for {version}")
    marker = re.search(r"^## ", text, re.MULTILINE)
    position = marker.start() if marker else len(text)
    head = text[:position].rstrip("\n") + "\n\n"
    path.write_text(head + section + ("\n" + text[position:] if marker else ""), encoding="utf-8")


def tag(root: Path) -> tuple[str, list[str]]:
    found = versions(root)
    values = set(found.values())
    if len(values) != 1 or None in values:
        detail = ", ".join(f"{k}={v or 'missing'}" for k, v in sorted(found.items()))
        raise ReleaseError(f"versions differ or are missing; run release.py stamp first ({detail})")
    version = values.pop()
    if git(root, "status", "--porcelain"):
        raise ReleaseError("worktree has uncommitted changes; commit the stamped release first")
    if f"v{version}" in tags(root):
        raise ReleaseError(f"tag v{version} already exists")
    if not re.search(rf"^## {re.escape(version)} ", (root / "CHANGELOG.md").read_text(encoding="utf-8")
                     if (root / "CHANGELOG.md").exists() else "", re.MULTILINE):
        raise ReleaseError(f"CHANGELOG.md has no section for {version}; run release.py prepare")
    git(root, "tag", "-a", f"v{version}", "-m", f"Release {version}")
    git(root, "branch", "-f", "stable", f"v{version}")
    return version, [f"git push origin v{version}", "git push --force-with-lease origin stable"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    stamp_cmd = sub.add_parser("stamp", help="write a version into every SKILL.md and manifest")
    stamp_cmd.add_argument("version")
    prepare_cmd = sub.add_parser("prepare", help="stamp the next date version and add a CHANGELOG section")
    prepare_cmd.add_argument("--version", help="override the computed date version")
    prepare_cmd.add_argument("--date", help="release date as YYYY-MM-DD (default today)")
    sub.add_parser("tag", help="tag the stamped, committed version and move the local stable branch")
    sub.add_parser("show", help="print the version each file carries")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "stamp":
            changed = stamp(root, args.version)
            print(f"Stamped {args.version}; {len(changed)} files changed.")
        elif args.command == "prepare":
            today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
            version = args.version or next_version(root, today)
            changed = stamp(root, version)
            add_changelog(root, changelog_section(root, version, today), version)
            print(f"Prepared {version}: {len(changed)} files stamped and a CHANGELOG.md section added.")
            print("Edit the CHANGELOG section into readable notes, run scripts/check_repo.py, commit, then "
                  "run release.py tag.")
        elif args.command == "tag":
            version, commands = tag(root)
            print(f"Tagged v{version} and moved the local stable branch to it. Nothing was pushed.")
            print("To publish:\n  " + "\n  ".join(commands))
        else:
            for name, version in sorted(versions(root).items()):
                print(f"{version or 'MISSING'}  {name}")
    except (ReleaseError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1 if isinstance(exc, ReleaseError) else 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
