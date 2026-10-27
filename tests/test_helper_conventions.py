"""Hold every skill helper to docs/helper-conventions.md, statically and fast.

The helpers are read with ``ast`` (never imported or run), so this suite needs
no optional packages and finishes in well under a second. Justified exceptions
live in tests/helper_conventions_allowlist.json; an entry nothing uses fails too.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import shlex
import unittest

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = Path(__file__).resolve().with_name("helper_conventions_allowlist.json")
# Spellings of "the directory to work on" that --project replaces.
DIRECTORY_FLAGS = {"--root", "--project-root", "--project-dir", "--repo", "--dir", "--directory"}
GCP_ID = re.compile(r"\bGCP\b|project[ _-]?id", re.IGNORECASE)
NO_OP_HELP = re.compile(r"\b(same|synonym|equivalent)\b", re.IGNORECASE)
EXIT_CODES = {0, 1, 2, 3}
# A documented command: an interpreter, then a path ending in scripts/<helper>.py.
COMMAND = re.compile(r"""(?:^|[\s`(])(?:"\$\{?PYTHON[^"]*"|\$\{?PYTHON\}?|python3?(?:\.\d+)?)(?:\s+-[A-Za-z]+)*\s+"""
                     r"""(?P<path>"[^"]*scripts/(?P<q>[a-z_]+)\.py"|[^\s"`]*scripts/(?P<u>[a-z_]+)\.py)(?P<rest>[^`]*)""")
SHELL_STOP = {">", ">>", "|", "||", "&&", ";", "2>", "2>&1"}
# Dated records of past runs keep the flags that were current then.
RECORD_FILES = {"validation-results.md", "skill-validation.md", "verification-record.md"}


@dataclass
class Option:
    strings: tuple[str, ...]
    help: str | None
    hidden: bool
    deprecated: bool
    line: int


@dataclass
class Helper:
    path: Path
    options: list[Option] = field(default_factory=list)
    exit_codes: set[int] = field(default_factory=set)
    dynamic: bool = False  # some option names are built at run time, so unknown flags are not reported

    @property
    def relative(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    def visible_flags(self) -> set[str]:
        return {s for o in self.options if not o.deprecated and not o.hidden for s in o.strings if s.startswith("--")}

    def all_flags(self) -> dict[str, Option]:
        return {s: o for o in self.options for s in o.strings if s.startswith("-")}


def _string(node) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):  # f-string help: keep the literal parts
        return "".join(v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _string(node.left), _string(node.right)
        return (left or "") + (right or "") if left is not None or right is not None else None
    return None


def _is_suppress(node) -> bool:
    return isinstance(node, ast.Attribute) and node.attr == "SUPPRESS"


def _int_constants(tree: ast.Module) -> dict[str, int]:
    """Module-level NAME = 0 and A, B = 0, 1 assignments, for exit constants."""
    names: dict[str, int] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, value = node.targets[0], node.value
        pairs = (zip(target.elts, value.elts) if isinstance(target, ast.Tuple) and isinstance(value, ast.Tuple)
                 else [(target, value)])
        for name, constant in pairs:
            if (isinstance(name, ast.Name) and isinstance(constant, ast.Constant)
                    and type(constant.value) is int):
                names[name.id] = constant.value
    return names


def _exit_values(node, constants: dict[str, int]) -> set[int]:
    values = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and type(child.value) is int:
            values.add(child.value)
        elif isinstance(child, ast.Name) and child.id in constants:
            values.add(constants[child.id])
    return values


def read_helper(path: Path) -> Helper | None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    helper = Helper(path)
    constants = _int_constants(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
            literal = [a for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            helper.dynamic |= len(literal) != len(node.args)
            strings = tuple(a.value for a in literal)
            keywords = {k.arg: k.value for k in node.keywords if k.arg}
            action = keywords.get("action")
            deprecated = isinstance(action, ast.Name) and action.id == "Deprecated"
            hidden = deprecated or _is_suppress(keywords.get("help"))
            help_text = None if "help" not in keywords else _string(keywords["help"])
            helper.options.append(Option(strings, help_text, hidden, deprecated, node.lineno))
        elif isinstance(node, ast.FunctionDef) and (node.name == "main" or node.name.startswith("cmd_")):
            for child in ast.walk(node):
                if isinstance(child, ast.Return) and child.value is not None:
                    if isinstance(child.value, (ast.Constant, ast.IfExp, ast.Name)):
                        helper.exit_codes |= _exit_values(child.value, constants)
        elif (isinstance(node, ast.Call) and node.args
              and ((isinstance(node.func, ast.Name) and node.func.id == "SystemExit")
                   or (isinstance(node.func, ast.Attribute) and node.func.attr == "exit"))):
            if isinstance(node.args[0], (ast.Constant, ast.Name)):
                helper.exit_codes |= _exit_values(node.args[0], constants)
    return helper if helper.options else None  # no argparse CLI: an importable module


def helpers() -> list[Helper]:
    found = [read_helper(path) for path in sorted(ROOT.glob("skills/*/scripts/*.py"))]
    return [helper for helper in found if helper is not None]


def exception_sites(found: list[Helper]) -> set[tuple[str, str, str]]:
    """Every place that breaks a rule unless the allowlist excuses it."""
    sites = set()
    for helper in found:
        for option in helper.options:
            sites |= {(helper.relative, "directory-flag", name) for name in option.strings
                      if name in DIRECTORY_FLAGS and not option.deprecated}
            if option.strings and not option.strings[0].startswith("-") and not option.hidden:
                sites.add((helper.relative, "positional", option.strings[0]))
        extra = sorted(helper.exit_codes - EXIT_CODES)
        if extra:
            sites.add((helper.relative, "exit-codes", f"{min(extra)}-{max(extra)}"))
    return sites


def documented_commands(text: str):
    """Yield (line number, helper name, quoted path?, path, flags) for commands in Markdown or YAML."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        start, line = index + 1, lines[index]
        while line.rstrip().endswith("\\") and index + 1 < len(lines):
            index += 1
            line = line.rstrip()[:-1] + " " + lines[index].strip()
        index += 1
        for match in COMMAND.finditer(line):
            rest = match.group("rest")
            try:
                tokens = shlex.split(rest, comments=False)
            except ValueError:
                tokens = rest.split()
            flags = []
            for token in tokens:
                if token in SHELL_STOP or token.startswith(">"):
                    break
                if token.startswith("--"):
                    flags.append(token.split("=", 1)[0])
            yield start, match.group("q") or match.group("u"), match.group("path"), flags


class HelperConventionTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.helpers = helpers()
        cls.allowed = {(e["script"], e["rule"], e["name"]): e["why"]
                       for e in json.loads(ALLOWLIST.read_text(encoding="utf-8"))["exceptions"]}

    def allowed_exception(self, helper: Helper, rule: str, name: str) -> bool:
        return (helper.relative, rule, name) in self.allowed

    def test_found_the_helper_command_lines(self):
        self.assertGreaterEqual(len(self.helpers), 40)

    def test_target_directories_use_project_and_old_spellings_are_hidden_aliases(self):
        problems = []
        for helper in self.helpers:
            flags = helper.all_flags()
            for option in helper.options:
                for name in option.strings:
                    if name in DIRECTORY_FLAGS and not option.deprecated and not self.allowed_exception(
                            helper, "directory-flag", name):
                        problems.append(f"{helper.relative}:{option.line} {name} names a directory; use --project")
                if option.strings and not option.strings[0].startswith("-"):
                    if not option.hidden and not self.allowed_exception(helper, "positional", option.strings[0]):
                        problems.append(f"{helper.relative}:{option.line} positional {option.strings[0]!r}: "
                                        "pass a target directory with --project")
            legacy = [o for o in helper.options if o.hidden and o.strings and (
                not o.strings[0].startswith("-") or set(o.strings) & DIRECTORY_FLAGS)]
            needs_project = legacy or helper.path.name.startswith("inspect_")
            if needs_project and "--project" not in flags:
                problems.append(f"{helper.relative} inspects a directory but has no --project")
        self.assertEqual([], problems)

    def test_project_never_means_a_gcp_project_id(self):
        problems = []
        for helper in self.helpers:
            for option in helper.options:
                text = option.help or ""
                if "--project" in option.strings and GCP_ID.search(text):
                    problems.append(f"{helper.relative}:{option.line} --project help mentions a GCP project ID")
                if re.search(r"GCP project ID", text) and "--gcp-project" not in option.strings:
                    problems.append(f"{helper.relative}:{option.line} a GCP project ID belongs in --gcp-project")
        self.assertEqual([], problems)

    def test_visible_dry_run_changes_behaviour(self):
        problems = [f"{h.relative}:{o.line} --dry-run is documented as a no-op; hide it as a deprecated alias"
                    for h in self.helpers for o in h.options
                    if "--dry-run" in o.strings and not o.hidden and NO_OP_HELP.search(o.help or "")]
        self.assertEqual([], problems)

    def test_exit_codes_stay_within_the_convention(self):
        problems = []
        for helper in self.helpers:
            extra = sorted(helper.exit_codes - EXIT_CODES)
            if extra and not self.allowed_exception(helper, "exit-codes", f"{min(extra)}-{max(extra)}"):
                problems.append(f"{helper.relative} returns exit codes {extra}; use 0, 1, 2 or 3")
        self.assertEqual([], problems)

    def test_skill_md_commands_use_skill_dir_and_current_flags(self):
        by_skill = {(h.path.parents[1].name, h.path.stem): h for h in self.helpers}
        by_name: dict[str, list[Helper]] = {}
        for helper in self.helpers:
            by_name.setdefault(helper.path.stem, []).append(helper)
        problems = []
        documents = sorted(ROOT.glob("skills/*/SKILL.md")) + sorted(ROOT.glob("skills/*/references/*.md")) \
            + sorted(ROOT.glob("skills/*/assets/**/*.yml"))
        for document in documents:
            if document.name in RECORD_FILES:
                continue
            skill = document.relative_to(ROOT).parts[1]
            where = document.relative_to(ROOT).as_posix()
            for line, name, path, flags in documented_commands(document.read_text(encoding="utf-8")):
                helper = by_skill.get((skill, name)) or (by_name[name][0] if len(by_name.get(name, ())) == 1 else None)
                if document.name == "SKILL.md" and "SKILL_DIR" not in path:
                    problems.append(f"{where}:{line} run {name}.py as python \"$SKILL_DIR/scripts/{name}.py\"")
                if helper is None:
                    continue
                visible, every = helper.visible_flags() | {"--help"}, helper.all_flags()
                for flag in flags:
                    if flag in visible:
                        continue
                    if flag not in every and helper.dynamic:
                        continue
                    state = "a deprecated alias" if flag in every else "not an option"
                    problems.append(f"{where}:{line} {name}.py {flag} is {state}")
        self.assertEqual([], problems)

    def test_every_allowlist_entry_excuses_something(self):
        self.assertTrue(all(why.strip() for why in self.allowed.values()), "every exception needs a reason")
        unused = sorted(set(self.allowed) - exception_sites(self.helpers))
        self.assertEqual([], unused, "remove stale entries from helper_conventions_allowlist.json")


class DocumentedCommandParsingTests(unittest.TestCase):
    def test_parses_quoted_paths_continuations_and_stops_at_redirection(self):
        text = ('python "$SKILL_DIR/scripts/inspect_project.py" --project . \\\n'
                '  --mode auto > "${RUNNER_TEMP}/out.json" --ignored\n'
                "Run `python3 -I scripts/check_deck.py --deck d.md` here.\n")
        found = list(documented_commands(text))
        self.assertEqual(found[0][1:], ("inspect_project", '"$SKILL_DIR/scripts/inspect_project.py"',
                                        ["--project", "--mode"]))
        self.assertEqual(found[1][1:], ("check_deck", "scripts/check_deck.py", ["--deck"]))

    def test_quoted_values_are_not_read_as_flags(self):
        text = 'python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --command "npx -y server --flag" --out m.json\n'
        self.assertEqual(list(documented_commands(text))[0][3], ["--command", "--out"])


if __name__ == "__main__":
    unittest.main()
