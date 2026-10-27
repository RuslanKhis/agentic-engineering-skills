#!/usr/bin/env python3
"""Fail when a shadcn theme file still carries shadcn's default tokens or fonts.

Reads one CSS file: the `tailwind.css` path from the project's components.json
(--project), or --css PATH. Reports every custom property in :root, .dark or
@theme whose normalised value equals the shadcn 4.22.1 default for that variable
(commit 3d98900, base colour "neutral", both the `init` output and the docs'
default chart palette), plus the Geist font import or stack and the default
`outline-ring/50` focus treatment.

Python 3.11+; standard library only. Read-only: no writes, network, shell or
project code; never reads .env files; inputs are size-bounded.
Exit codes: 0 no defaults remain; 1 defaults remain; 2 invalid input.
--dry-run is a deprecated no-op kept for old commands.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    print("error: check_theme.py requires Python 3.11 or newer.", file=sys.stderr)
    raise SystemExit(2)

import argparse
import json
import os
from pathlib import Path
import re
import stat

SHADCN_REFERENCE = {
    "package": "shadcn",
    "version": "4.22.1",
    "commit": "3d98900e9b73c45f035f8109e9d41ba6a51685e7",
    "style": "base-nova",
    "base_color": "neutral",
    "sources": [
        "npx shadcn@4.22.1 init --base base --preset nova --template vite (src/index.css)",
        "apps/v4/content/docs/(root)/theming.mdx at the commit (default chart palette)",
    ],
}

_GREY_CHARTS = ("oklch(0.87 0 0)", "oklch(0.556 0 0)", "oklch(0.439 0 0)", "oklch(0.371 0 0)", "oklch(0.269 0 0)")
_DOCS_CHARTS_LIGHT = ("oklch(0.646 0.222 41.116)", "oklch(0.6 0.118 184.704)", "oklch(0.398 0.07 227.392)",
                      "oklch(0.828 0.189 84.429)", "oklch(0.769 0.188 70.08)")
_DOCS_CHARTS_DARK = ("oklch(0.488 0.243 264.376)", "oklch(0.696 0.17 162.48)", "oklch(0.769 0.188 70.08)",
                     "oklch(0.627 0.265 303.9)", "oklch(0.645 0.246 16.439)")

# Variable -> default values in that scope (several where init and the docs differ).
DEFAULTS: dict[str, dict[str, tuple[str, ...]]] = {
    ":root": {
        "--radius": ("0.625rem",),
        "--background": ("oklch(1 0 0)",),
        "--foreground": ("oklch(0.145 0 0)",),
        "--card": ("oklch(1 0 0)",),
        "--card-foreground": ("oklch(0.145 0 0)",),
        "--popover": ("oklch(1 0 0)",),
        "--popover-foreground": ("oklch(0.145 0 0)",),
        "--primary": ("oklch(0.205 0 0)",),
        "--primary-foreground": ("oklch(0.985 0 0)",),
        "--secondary": ("oklch(0.97 0 0)",),
        "--secondary-foreground": ("oklch(0.205 0 0)",),
        "--muted": ("oklch(0.97 0 0)",),
        "--muted-foreground": ("oklch(0.556 0 0)",),
        "--accent": ("oklch(0.97 0 0)",),
        "--accent-foreground": ("oklch(0.205 0 0)",),
        "--destructive": ("oklch(0.577 0.245 27.325)",),
        "--border": ("oklch(0.922 0 0)",),
        "--input": ("oklch(0.922 0 0)",),
        "--ring": ("oklch(0.708 0 0)",),
        **{f"--chart-{i + 1}": (_GREY_CHARTS[i], _DOCS_CHARTS_LIGHT[i]) for i in range(5)},
        "--sidebar": ("oklch(0.985 0 0)",),
        "--sidebar-foreground": ("oklch(0.145 0 0)",),
        "--sidebar-primary": ("oklch(0.205 0 0)",),
        "--sidebar-primary-foreground": ("oklch(0.985 0 0)",),
        "--sidebar-accent": ("oklch(0.97 0 0)",),
        "--sidebar-accent-foreground": ("oklch(0.205 0 0)",),
        "--sidebar-border": ("oklch(0.922 0 0)",),
        "--sidebar-ring": ("oklch(0.708 0 0)",),
    },
    ".dark": {
        "--background": ("oklch(0.145 0 0)",),
        "--foreground": ("oklch(0.985 0 0)",),
        "--card": ("oklch(0.205 0 0)",),
        "--card-foreground": ("oklch(0.985 0 0)",),
        "--popover": ("oklch(0.205 0 0)",),
        "--popover-foreground": ("oklch(0.985 0 0)",),
        "--primary": ("oklch(0.922 0 0)",),
        "--primary-foreground": ("oklch(0.205 0 0)",),
        "--secondary": ("oklch(0.269 0 0)",),
        "--secondary-foreground": ("oklch(0.985 0 0)",),
        "--muted": ("oklch(0.269 0 0)",),
        "--muted-foreground": ("oklch(0.708 0 0)",),
        "--accent": ("oklch(0.269 0 0)",),
        "--accent-foreground": ("oklch(0.985 0 0)",),
        "--destructive": ("oklch(0.704 0.191 22.216)",),
        "--border": ("oklch(1 0 0 / 10%)",),
        "--input": ("oklch(1 0 0 / 15%)",),
        "--ring": ("oklch(0.556 0 0)",),
        **{f"--chart-{i + 1}": (_GREY_CHARTS[i], _DOCS_CHARTS_DARK[i]) for i in range(5)},
        "--sidebar": ("oklch(0.205 0 0)",),
        "--sidebar-foreground": ("oklch(0.985 0 0)",),
        "--sidebar-primary": ("oklch(0.488 0.243 264.376)",),
        "--sidebar-primary-foreground": ("oklch(0.985 0 0)",),
        "--sidebar-accent": ("oklch(0.269 0 0)",),
        "--sidebar-accent-foreground": ("oklch(0.985 0 0)",),
        "--sidebar-border": ("oklch(1 0 0 / 10%)",),
        "--sidebar-ring": ("oklch(0.556 0 0)",),
    },
}
DEFAULT_FONT = "Geist"  # init writes --font-sans: 'Geist Variable', sans-serif and imports @fontsource-variable/geist
FONT_VARIABLES = ("--font-sans", "--font-heading", "--font-serif", "--font-mono")
DEFAULT_FOCUS_CLASS = "outline-ring/50"
MAX_CSS_BYTES = 1_048_576
MAX_CONFIG_BYTES = 262_144


class InputError(Exception):
    """Invalid input; the code is a stable, non-sensitive identifier."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def normalise(value: str) -> str:
    """Lower-case, collapse whitespace and canonicalise plain numbers (0.50 -> 0.5)."""
    value = re.sub(r"\s*!important\s*$", "", value.strip(), flags=re.I).lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s*([(),/])\s*", r"\1", value)
    value = re.sub(r"(?<![\w.#-])(\d*\.\d+|\d+)(?![\w.])", lambda m: format(float(m[1]), "g"), value)
    value = re.sub(r"(?<![\w.#-])(\d*\.\d+|\d+)(?=[a-z%])", lambda m: format(float(m[1]), "g"), value)
    return value


def strip_comments(text: str) -> str:
    out, i, quote = [], 0, ""
    while i < len(text):
        ch = text[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < len(text):
                out.append(text[i + 1])
                i += 1
            elif ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                raise InputError("css_unterminated_comment")
            i = end + 2
            continue
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def parse_blocks(text: str) -> list[tuple[tuple[str, ...], list[str]]]:
    """Return (prelude path, declarations) for every block, plus the top level as ()."""
    stack: list[tuple[str, list[str]]] = [("", [])]
    path: list[str] = []
    blocks: list[tuple[tuple[str, ...], list[str]]] = []
    buf: list[str] = []
    quote = ""
    for ch in strip_comments(text):
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == "{":
            prelude = " ".join("".join(buf).split())
            buf = []
            stack.append((prelude, []))
            path.append(prelude)
        elif ch == ";":
            stack[-1][1].append("".join(buf).strip())
            buf = []
        elif ch == "}":
            if len(stack) == 1:
                raise InputError("css_unbalanced_braces")
            if "".join(buf).strip():
                stack[-1][1].append("".join(buf).strip())
            buf = []
            _, decls = stack.pop()
            blocks.append((tuple(path), decls))
            path.pop()
        else:
            buf.append(ch)
    if len(stack) != 1 or quote:
        raise InputError("css_unbalanced_braces")
    blocks.append(((), stack[0][1]))
    return blocks


def scope_of(prelude: str) -> str | None:
    if prelude.startswith("@theme"):
        return "@theme"
    parts = [p.strip() for p in prelude.split(",")]
    if any(p == ":root" or p == "html" for p in parts):
        return ":root"
    if any(re.search(r"\.dark\b", p) for p in parts):
        return ".dark"
    return None


def find_leftovers(text: str) -> tuple[list[dict], dict]:
    blocks = parse_blocks(text)
    leftovers: list[dict] = []
    seen = {":root": 0, ".dark": 0, "@theme": 0}
    for path, decls in blocks:
        scope = scope_of(path[-1]) if path else None
        for decl in decls:
            if not path and decl.lower().startswith("@import") and re.search(r"@fontsource(-variable)?/geist", decl, re.I):
                leftovers.append({"variable": "@import", "scope": "top-level", "value": decl[len("@import"):].strip()})
                continue
            if decl.startswith("@apply") and DEFAULT_FOCUS_CLASS in decl.split():
                leftovers.append({"variable": DEFAULT_FOCUS_CLASS, "scope": " > ".join(path), "value": decl})
                continue
            if scope is None or ":" not in decl or not decl.startswith("--"):
                continue
            name, value = (part.strip() for part in decl.split(":", 1))
            seen[scope] += 1
            if name in FONT_VARIABLES and DEFAULT_FONT.lower() in value.lower():
                leftovers.append({"variable": name, "scope": scope, "value": value})
            elif scope in DEFAULTS and name in DEFAULTS[scope]:
                if normalise(value) in {normalise(v) for v in DEFAULTS[scope][name]}:
                    leftovers.append({"variable": name, "scope": scope, "value": value})
    if not seen[":root"] and not seen[".dark"]:
        raise InputError("no_root_or_dark_custom_properties")
    return leftovers, seen


def read_bounded(path: Path, limit: int) -> str:
    if path.name.startswith(".env"):
        raise InputError("refused_env_file")
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    except FileNotFoundError:
        raise InputError("file_not_found") from None
    except OSError:
        raise InputError("file_unreadable_or_symlink") from None
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise InputError("not_a_regular_file")
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise InputError("file_too_large")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InputError("file_not_utf8") from None


def css_from_project(project: Path) -> tuple[Path, str]:
    try:
        info = project.lstat()
    except OSError:
        raise InputError("project_not_found") from None
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise InputError("project_must_be_a_non_symlink_directory")
    try:
        config = json.loads(read_bounded(project / "components.json", MAX_CONFIG_BYTES))
    except InputError as exc:
        raise InputError("components_json_" + exc.code) from None
    except json.JSONDecodeError:
        raise InputError("components_json_invalid") from None
    tailwind = config.get("tailwind") if isinstance(config, dict) else None
    css = tailwind.get("css") if isinstance(tailwind, dict) else None
    if not isinstance(css, str) or not css.strip() or len(css) > 512:
        raise InputError("components_json_missing_tailwind_css")
    relative = Path(css)
    root = project.resolve()
    target = (root / relative).resolve()
    if relative.is_absolute() or ".." in relative.parts or not target.is_relative_to(root):
        raise InputError("tailwind_css_outside_project")
    return target, relative.as_posix()


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse normally quotes invalid argv, which may contain pasted secrets.
        self.exit(2, "error: invalid arguments; use --help for the accepted interface.\n")


class Deprecated(argparse.Action):
    """An old flag spelling that still works: hidden from --help, noted on stderr."""

    def __init__(self, option_strings, dest, note, nargs=None, const=None, default=argparse.SUPPRESS, **kwargs):
        self.note = note
        super().__init__(option_strings, dest, nargs=nargs, const=const, default=default,
                         help=argparse.SUPPRESS, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(f"{parser.prog}: {option_string} is deprecated; {self.note}", file=sys.stderr)
        setattr(namespace, self.dest, self.const if self.nargs == 0 else values)


def main(argv: list[str] | None = None) -> int:
    parser = SafeArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", type=Path, help="Project directory containing components.json (tailwind.css field).")
    parser.add_argument("--css", type=Path, help="Theme CSS file; relative paths resolve against --project when given.")
    parser.add_argument("--dry-run", action=Deprecated, nargs=0, const=True, default=False, note="this helper only reads, so it changes nothing")
    parser.add_argument("--json", action="store_true", help="Print a JSON report instead of text.")
    args = parser.parse_args(argv)

    def fail(code: str) -> int:
        if args.json:
            print(json.dumps({"schema_version": 1, "error": code}))
        else:
            print(f"error: {code}", file=sys.stderr)
        return 2

    if not args.project and not args.css:
        return fail("give_project_or_css")
    try:
        if args.css:
            css_path = args.project / args.css if args.project and not args.css.is_absolute() else args.css
            shown = args.css.as_posix()
        else:
            css_path, shown = css_from_project(args.project)
        leftovers, seen = find_leftovers(read_bounded(css_path, MAX_CSS_BYTES))
    except InputError as exc:
        return fail(exc.code)

    report = {
        "schema_version": 1,
        "read_only": True,
        "css": shown,
        "status": "defaults_remain" if leftovers else "clean",
        "leftovers": leftovers,
        "custom_properties_checked": seen,
        "reference": SHADCN_REFERENCE,
        "limitations": [
            "Only exact default values (after whitespace, case and number normalisation) are detected; near-defaults pass.",
            "Other shadcn base colours (stone, zinc, mauve, olive, mist, taupe) and other versions are not listed.",
            "Contrast, component classes such as ring-ring/50, and DESIGN.md conformance are not checked.",
        ],
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    elif leftovers:
        print(f"{shown}: {len(leftovers)} shadcn {SHADCN_REFERENCE['version']} default(s) remain:")
        for item in leftovers:
            print(f"  {item['scope']} {item['variable']}: {item['value']}")
    else:
        print(f"{shown}: no shadcn {SHADCN_REFERENCE['version']} default tokens or fonts found.")
    return 1 if leftovers else 0


if __name__ == "__main__":
    raise SystemExit(main())
