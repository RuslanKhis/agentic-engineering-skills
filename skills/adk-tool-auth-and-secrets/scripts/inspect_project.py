#!/usr/bin/env python3
"""Bounded, read-only static observations; never a security certification.

Uses only Python 3.11's standard library. Project code is parsed, never imported.
No environment files, payload files, symlinks, network, subprocesses or plugins
are used. Output intentionally omits source, arbitrary literals and raw errors.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import re
import stat
import sys

if sys.version_info < (3, 11):
    print('{"complete": false, "diagnostics": [{"code": "PYTHON_3_11_REQUIRED"}]}')
    raise SystemExit(2)

import tomllib


PACKAGES = frozenset({
    "google-adk", "google-genai", "google-auth", "google-cloud-secret-manager",
    "firebase-admin", "fastapi", "pydantic", "httpx", "python",
})
SKIP_DIRS = frozenset({
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
    "site-packages", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", "dist", "build", "vendor", "vendors", "third_party", ".next",
    "secrets", "credentials", "logs", "log", "data", "databases",
})
MANIFESTS = frozenset({"pyproject.toml", "uv.lock", "poetry.lock"})
IDENTITY_PARAMETERS = frozenset({
    "user_id", "uid", "tenant_id", "customer_id", "account_id", "principal_id",
})
CREDENTIAL_PARAMETERS = frozenset({
    "api_key", "access_token", "refresh_token", "client_secret", "secret_name",
    "secret_id", "secret_version", "credential", "credentials", "authorization",
})
EVENT_NAMES = frozenset({"event", "events", "adk_event", "adk_events", "raw_event"})
VERSION = r"\d+(?:\.\d+){0,3}(?:\.\*)?"
CONSTRAINT = re.compile(rf"(?:===|==|!=|~=|<=|>=|<|>|\^|~)?\s*{VERSION}\Z")
PIN = re.compile(r"(?:===|==)?\s*(\d+(?:\.\d+){0,3})\Z")
EXPECT_VERSION = re.compile(r"\d+\.\d+\.\d+\Z")
REQUIREMENT = re.compile(r"([A-Za-z0-9_.-]+)(?:\[[A-Za-z0-9_., -]+\])?\s*(.*)\Z")


def package_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = re.sub(r"[-_.]+", "-", value).lower()
    return normalized if normalized in PACKAGES else None


def numeric_constraint(value: object) -> tuple[str, list[str]]:
    """Only a complete numeric constraint can contribute output text."""
    if not isinstance(value, str) or len(value) > 128:
        return "unknown", []
    value = value.strip()
    pieces = [piece.strip() for piece in value.split(",")]
    if not pieces or any(not CONSTRAINT.fullmatch(piece) for piece in pieces):
        return "unknown", []
    pin = PIN.fullmatch(value)
    versions = re.findall(r"\d+(?:\.\d+){0,3}(?:\.\*)?", value)
    return ("pinned" if pin else "ranged"), versions


def qualified_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def is_event(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id in EVENT_NAMES


class Inspector:
    def __init__(self, root: Path, max_files: int, max_file_bytes: int,
                 max_total_bytes: int):
        self.root = root
        self.max_files = max_files
        self.max_file_bytes = max_file_bytes
        self.max_total_bytes = max_total_bytes
        self.max_entries = min(100_000, max(1000, max_files * 20))
        self.entries = self.files = self.bytes = self.skipped_symlinks = 0
        self.observations: list[dict] = []
        self.dependencies: list[dict] = []
        self.diagnostics: list[dict] = []
        self._seen: set[tuple] = set()
        self._stop = False

    def diagnostic(self, code: str, location: str = ".") -> None:
        item = {"code": code, "path": location}
        if item not in self.diagnostics:
            self.diagnostics.append(item)

    def observe(self, code: str, location: str, line: int) -> None:
        key = (code, location, line)
        if key not in self._seen:
            self._seen.add(key)
            self.observations.append({"code": code, "path": location, "line": line})

    @staticmethod
    def candidate(name: str) -> bool:
        lower = name.lower()
        if lower.startswith(".env"):
            return False
        return (lower.endswith(".py") or lower in MANIFESTS
                or bool(re.fullmatch(r"requirements(?:[-_.][a-z0-9_-]+)?\.(txt|in)", lower)))

    def walk(self, directory: Path, depth: int = 0) -> None:
        relative = directory.relative_to(self.root).as_posix()
        if depth > 32:
            self.diagnostic("TRAVERSAL_DEPTH_LIMIT", relative)
            return
        entries = []
        try:
            with os.scandir(directory) as iterator:
                for entry in iterator:
                    self.entries += 1
                    if self.entries > self.max_entries:
                        self.diagnostic("TRAVERSAL_ENTRY_LIMIT")
                        self._stop = True
                        break
                    entries.append(entry)
        except OSError:
            self.diagnostic("DIRECTORY_UNREADABLE", relative)
            return
        # The list is bounded above, and sorting makes repeated runs stable.
        for entry in sorted(entries, key=lambda item: item.name):
            if self._stop:
                return
            name = entry.name
            if name.lower().startswith(".env"):
                continue
            try:
                if entry.is_symlink():
                    self.skipped_symlinks += 1
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if name.lower() not in SKIP_DIRS and not name.startswith("."):
                        self.walk(Path(entry.path), depth + 1)
                elif entry.is_file(follow_symlinks=False) and self.candidate(name):
                    self.inspect_file(Path(entry.path))
            except OSError:
                self.diagnostic("ENTRY_UNREADABLE", str(Path(entry.path).relative_to(self.root)))

    def inspect_file(self, path: Path) -> None:
        relative = path.relative_to(self.root).as_posix()
        if self.files >= self.max_files:
            self.diagnostic("FILE_COUNT_LIMIT")
            self._stop = True
            return
        self.files += 1
        try:
            # Reject an escaped path and a final-component symlink. Symlink
            # directories are also rejected during traversal; this is not a
            # sandbox against a hostile concurrent filesystem mutator.
            if not path.resolve().is_relative_to(self.root):
                self.diagnostic("PATH_OUTSIDE_ROOT", relative)
                return
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            fd = os.open(path, flags)
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode):
                    self.diagnostic("NON_REGULAR_FILE", relative)
                    return
                if info.st_size > self.max_file_bytes:
                    self.diagnostic("FILE_SIZE_LIMIT", relative)
                    return
                remaining = self.max_total_bytes - self.bytes
                if info.st_size > remaining:
                    self.diagnostic("TOTAL_BYTES_LIMIT")
                    self._stop = True
                    return
                payload = stream.read(min(self.max_file_bytes, remaining) + 1)
            if len(payload) > self.max_file_bytes or len(payload) > remaining:
                self.diagnostic("READ_SIZE_LIMIT", relative)
                self._stop = True
                return
            self.bytes += len(payload)
            text = payload.decode("utf-8")
            if path.suffix.lower() == ".py":
                self.inspect_python(text, relative)
            elif path.name.lower() in MANIFESTS:
                self.inspect_toml(text, relative, path.name.lower())
            else:
                for line, value in enumerate(text.splitlines(), 1):
                    self.requirement(value, relative, line)
        except (OSError, UnicodeError, ValueError, RecursionError, MemoryError):
            self.diagnostic("FILE_UNREADABLE_OR_INVALID", relative)

    def add_dependency(self, name: object, value: object, relative: str,
                       line: int, origin: str) -> None:
        name = package_name(name)
        if name is None:
            return
        kind, versions = numeric_constraint(value)
        self.dependencies.append({
            "code": "DEPENDENCY_CONSTRAINT", "path": relative, "line": line,
            "dependency": name, "constraint_kind": kind,
            "numeric_versions": versions, "origin": origin,
        })

    def requirement(self, value: object, relative: str, line: int) -> None:
        if not isinstance(value, str):
            return
        value = value.strip()
        if not value or value.startswith("#"):
            return
        # Includes/indexes/direct URLs are not followed, parsed for credentials,
        # or reproduced. Named URL requirements remain unknown constraints.
        if value.startswith(("-", "http:", "https:", "git+", "file:")):
            self.observe("UNRESOLVED_REQUIREMENT_DIRECTIVE", relative, line)
            return
        match = REQUIREMENT.fullmatch(value)
        if match:
            constraint = match.group(2).split(";", 1)[0].split(" #", 1)[0].strip()
            self.add_dependency(match.group(1), constraint, relative, line, "declaration")
        else:
            self.observe("UNRECOGNIZED_REQUIREMENT", relative, line)

    def inspect_toml(self, text: str, relative: str, name: str) -> None:
        try:
            document = tomllib.loads(text)
        except (tomllib.TOMLDecodeError, RecursionError):
            self.diagnostic("TOML_PARSE_ERROR", relative)
            return
        if name in {"uv.lock", "poetry.lock"}:
            packages = document.get("package", [])
            if not isinstance(packages, list):
                self.diagnostic("MANIFEST_SHAPE_UNKNOWN", relative)
                return
            for package in packages:
                if isinstance(package, dict):
                    self.add_dependency(package.get("name"), package.get("version"),
                                        relative, 1, "lockfile")
            return
        project = document.get("project", {})
        if isinstance(project, dict):
            if "requires-python" in project:
                self.add_dependency("python", project["requires-python"], relative, 1, "declaration")
            deps = project.get("dependencies", [])
            if isinstance(deps, list):
                for value in deps:
                    self.requirement(value, relative, 1)
            optional = project.get("optional-dependencies", {})
            if isinstance(optional, dict):
                for values in optional.values():
                    if isinstance(values, list):
                        for value in values:
                            self.requirement(value, relative, 1)
        tool = document.get("tool", {})
        poetry = tool.get("poetry", {}) if isinstance(tool, dict) else {}
        deps = poetry.get("dependencies", {}) if isinstance(poetry, dict) else {}
        if isinstance(deps, dict):
            for dependency, value in deps.items():
                if isinstance(value, dict):
                    value = value.get("version")
                self.add_dependency(dependency, value, relative, 1, "declaration")

    def inspect_python(self, text: str, relative: str) -> None:
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError, MemoryError):
            self.diagnostic("PYTHON_PARSE_ERROR", relative)
            return
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                arguments = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
                context = any(qualified_name(arg.annotation) == "ToolContext" for arg in arguments)
                decorated = any(qualified_name(item.func if isinstance(item, ast.Call) else item)
                                in {"tool", "function_tool"} for item in node.decorator_list)
                if context:
                    self.observe("TOOL_CONTEXT_PARAMETER", relative, node.lineno)
                if context or decorated:
                    for arg in arguments:
                        if arg.arg in IDENTITY_PARAMETERS:
                            self.observe("TOOL_IDENTITY_PARAMETER_CANDIDATE", relative, arg.lineno)
                        if arg.arg in CREDENTIAL_PARAMETERS:
                            self.observe("TOOL_CREDENTIAL_PARAMETER_CANDIDATE", relative, arg.lineno)
            if isinstance(node, ast.Call):
                function = node.func
                if (isinstance(function, ast.Attribute) and is_event(function.value)
                        and function.attr in {"model_dump", "model_dump_json", "dict", "json", "to_json"}):
                    self.observe("RAW_EVENT_SERIALIZATION_CANDIDATE", relative, node.lineno)
                elif (qualified_name(function) in {"dumps", "dump", "jsonable_encoder"}
                      and any(is_event(arg) for arg in node.args)):
                    self.observe("RAW_EVENT_SERIALIZATION_CANDIDATE", relative, node.lineno)
                if qualified_name(function) in {"get_session", "create_session"}:
                    self.observe("SESSION_INTERFACE_CANDIDATE", relative, node.lineno)
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value == "latest" or "/versions/latest" in node.value:
                    self.observe("LATEST_SECRET_REFERENCE_CANDIDATE", relative, node.lineno)
                if node.value == "ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS":
                    self.observe("CONTENT_CAPTURE_SETTING_REFERENCE", relative, node.lineno)

    def result(self, expected: str | None) -> tuple[dict, int]:
        expectation = {"requested": expected is not None, "result": "not_requested"}
        exit_code = 2 if self.diagnostics else 0
        if expected is not None:
            adk = [item for item in self.dependencies if item["dependency"] == "google-adk"]
            unresolved = any(item["code"] in {"UNRESOLVED_REQUIREMENT_DIRECTIVE",
                                              "UNRECOGNIZED_REQUIREMENT"}
                             for item in self.observations)
            matches = bool(adk) and not unresolved and all(item["constraint_kind"] == "pinned"
                                       and item["numeric_versions"] == [expected] for item in adk)
            expectation["result"] = "static_pins_match" if matches else "missing_different_or_unproven"
            if not matches and exit_code == 0:
                exit_code = 3
        report = {
            "schema_version": 1,
            "inspection": "read_only_static_inventory",
            "complete": not self.diagnostics,
            "security_verdict": "not_assessed",
            "runtime_compatibility": "not_verified",
            "limits": {"max_files": self.max_files, "max_file_bytes": self.max_file_bytes,
                       "max_total_bytes": self.max_total_bytes, "max_traversal_entries": self.max_entries},
            "counts": {"candidate_files": self.files, "bytes_read": self.bytes,
                       "traversal_entries": self.entries, "symlinks_skipped": self.skipped_symlinks},
            "observations": sorted(self.observations, key=lambda item: (item["path"], item["line"], item["code"])),
            "dependencies": sorted(self.dependencies, key=lambda item: (item["path"], item["line"], item["dependency"])),
            "diagnostics": sorted(self.diagnostics, key=lambda item: (item["path"], item["code"])),
            "adk_expectation": expectation,
            "limitations": ["No target code executed or imported.",
                            "Skipped paths and unresolved dependency directives are not inspected.",
                            "Candidate observations require human review; absence is not proof of safety.",
                            "Manifest pins do not verify the installed environment.",
                            "TOML locations use line 1 because the stdlib parser supplies no line map."],
        }
        return report, exit_code


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({"schema_version": 1, "complete": False,
                          "diagnostics": [{"code": "INVALID_ARGUMENTS"}]}))
        raise SystemExit(2)


def positive_integer(value: str) -> int:
    result = int(value)
    if result <= 0 or result > 268_435_456:
        raise argparse.ArgumentTypeError("out of range")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_root", help="Project directory; target code is never executed.")
    parser.add_argument("--dry-run", action="store_true", help="Equivalent to normal read-only inspection.")
    parser.add_argument("--max-files", type=positive_integer, default=250)
    parser.add_argument("--max-file-bytes", type=positive_integer, default=262_144)
    parser.add_argument("--max-total-bytes", type=positive_integer, default=4_194_304)
    parser.add_argument("--expect-adk", metavar="X.Y.Z", help="Require every observed ADK constraint to pin this version; exit 3 if missing, different or unproven.")
    args = parser.parse_args(argv)
    if args.max_files > 10_000 or (args.expect_adk is not None and not EXPECT_VERSION.fullmatch(args.expect_adk)):
        parser.error("invalid bounds or version")
    root = Path(args.project_root)
    try:
        valid = not root.is_symlink() and root.is_dir()
        root = root.resolve()
    except (OSError, ValueError):
        valid = False
    if not valid:
        print(json.dumps({"schema_version": 1, "complete": False,
                          "diagnostics": [{"code": "INVALID_PROJECT_ROOT"}]}))
        return 2
    inspector = Inspector(root, args.max_files, args.max_file_bytes, args.max_total_bytes)
    inspector.walk(root)
    report, exit_code = inspector.result(args.expect_adk)
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
