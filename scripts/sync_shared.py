#!/usr/bin/env python3
"""Copy the canonical shared snippets into the skill files that carry them.

Each skill package is installed on its own, so guidance several skills share
cannot be a link to another package. The single source of each snippet is
shared/<name>.md; every skill file that carries it holds a copy between
markers on their own lines:

    <!-- shared:<name> -->
    ...copied text...
    <!-- /shared:<name> -->

A canonical file may start with one HTML comment for maintainers. It is not
copied; a line in it reading `carriers: a, b, c` names the skill packages that
must carry the snippet. Everything after that comment, without surrounding
blank lines, is the snippet.

Run without arguments to rewrite drifted blocks in place; run with --check to
change nothing and fail on drift. Exit codes: 0 in sync (or rewritten);
1 drift found by --check, or a structural problem (unknown snippet, unclosed
or nested markers, a listed carrier without the block, a block in a package
that is not listed); 2 invalid arguments or a missing shared/ directory.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys

OPEN = re.compile(r"^<!-- shared:([a-z0-9]+(?:-[a-z0-9]+)*) -->$")
CLOSE = re.compile(r"^<!-- /shared:([a-z0-9]+(?:-[a-z0-9]+)*) -->$")
HEADER = re.compile(r"\A\s*<!--(.*?)-->", re.S)
CARRIERS = re.compile(r"^\s*carriers:\s*(.*)$", re.M)


@dataclass
class Snippet:
    name: str
    body: str
    carriers: tuple[str, ...]


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    drifted: list[Path] = field(default_factory=list)
    carried: dict[str, set[str]] = field(default_factory=dict)


def load_snippets(shared: Path, result: Result) -> dict[str, Snippet]:
    snippets: dict[str, Snippet] = {}
    for path in sorted(shared.glob("*.md")):
        name = path.stem
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            result.errors.append(f"{path}: snippet names use lowercase letters, digits and single hyphens")
            continue
        text = path.read_text(encoding="utf-8")
        carriers: tuple[str, ...] = ()
        header = HEADER.match(text)
        if header:
            found = CARRIERS.search(header.group(1))
            if found:
                carriers = tuple(c.strip() for c in found.group(1).split(",") if c.strip())
            text = text[header.end():]
        body = text.strip("\n")
        if not body.strip():
            result.errors.append(f"{path}: snippet is empty")
            continue
        if OPEN.search(body) or CLOSE.search(body) or "<!-- shared:" in body or "<!-- /shared:" in body:
            result.errors.append(f"{path}: a snippet cannot contain shared markers")
            continue
        snippets[name] = Snippet(name, body, carriers)
    return snippets


def sync_text(text: str, path: Path, snippets: dict[str, Snippet], result: Result) -> str:
    """Return the text with every marked block replaced by its canonical body."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        opened = OPEN.match(lines[i].strip())
        closed = CLOSE.match(lines[i].strip())
        if closed:
            result.errors.append(f"{path}:{i + 1}: closing marker for {closed.group(1)!r} without an opening one")
            out.append(lines[i])
            i += 1
            continue
        if not opened:
            out.append(lines[i])
            i += 1
            continue
        name = opened.group(1)
        end = None
        problem = f"{path}:{i + 1}: shared block {name!r} is never closed"
        for j in range(i + 1, len(lines)):
            stripped = lines[j].strip()
            if OPEN.match(stripped):
                problem = f"{path}:{j + 1}: shared block nested inside {name!r}"
                break
            inner = CLOSE.match(stripped)
            if inner:
                if inner.group(1) == name:
                    end = j
                else:
                    problem = f"{path}:{j + 1}: {name!r} closed as {inner.group(1)!r}"
                break
        if end is None:
            # Leave the rest of the file untouched; a malformed block is never rewritten.
            result.errors.append(problem)
            out.extend(lines[i:])
            break
        snippet = snippets.get(name)
        if snippet is None:
            result.errors.append(f"{path}:{i + 1}: no canonical shared/{name}.md")
            out.extend(lines[i:end + 1])
        else:
            out.append(lines[i])
            out.extend(snippet.body.split("\n"))
            out.append(lines[end])
            result.carried.setdefault(name, set()).add(package_of(path))
        i = end + 1
    return "\n".join(out)


def package_of(path: Path) -> str:
    parts = path.parts
    return parts[parts.index("skills") + 1] if "skills" in parts else str(path)


def run(root: Path, check: bool) -> Result:
    result = Result()
    snippets = load_snippets(root / "shared", result)
    skills = root / "skills"
    for path in sorted(skills.rglob("*.md")):
        if path.is_symlink() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "<!-- shared:" not in text and "<!-- /shared:" not in text:
            continue
        synced = sync_text(text, path.relative_to(root), snippets, result)
        if synced != text:
            result.drifted.append(path.relative_to(root))
            if not check:
                path.write_text(synced, encoding="utf-8")
    present = {p.name for p in skills.iterdir() if p.is_dir()} if skills.is_dir() else set()
    for name, snippet in sorted(snippets.items()):
        carried = result.carried.get(name, set())
        for carrier in snippet.carriers:
            if carrier in present and carrier not in carried:
                result.errors.append(f"skills/{carrier}: missing the shared:{name} block that shared/{name}.md lists it for")
        for package in sorted(carried - set(snippet.carriers)):
            result.errors.append(f"skills/{package}: carries shared:{name} but shared/{name}.md does not list it as a carrier")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="repository containing shared/ and skills/ (default: this script's repository)")
    parser.add_argument("--check", action="store_true", help="change nothing; fail when any copy has drifted")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not (root / "shared").is_dir():
        print(f"ERROR {root / 'shared'}: no shared/ directory", file=sys.stderr)
        return 2
    result = run(root, args.check)
    for error in result.errors:
        print(f"ERROR {error}")
    for path in result.drifted:
        print(f"{'DRIFT' if args.check else 'SYNCED'} {path}")
    total = sum(len(v) for v in result.carried.values())
    print(f"Shared snippets: {len(result.carried)} in use, carried by {total} snippet-package pairs; "
          f"{len(result.drifted)} {'drifted' if args.check else 'rewritten'}, {len(result.errors)} errors.")
    if result.errors or (args.check and result.drifted):
        if args.check and result.drifted:
            print("Run scripts/sync_shared.py to copy shared/*.md into the marked blocks.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
