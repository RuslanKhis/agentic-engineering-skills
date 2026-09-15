#!/usr/bin/env python3
"""Read-only, bounded Python/ADK project inventory (Python 3.11+).

This script imports no project modules and runs no project commands. Interpreter
metadata is a separate observation, not proof of the target's environment.
Directory scanning requires file-descriptor support (POSIX); unsupported
platforms fail clearly so the agent can perform a manual read-only inventory.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import re
import stat
import sys
import tomllib


MAX_FILES = 3000
MAX_ENTRIES = 12000
MAX_DEPTH = 32
MAX_FILE_BYTES = 256 * 1024
MAX_TOTAL_BYTES = 16 * 1024 * 1024
PACKAGES = (
    "google-adk", "google-genai", "google-cloud-bigquery", "google-auth",
    "pydantic", "sqlglot", "pytest",
)
SKIP_DIRS = frozenset({
    "venv", "env", "node_modules", "__pycache__", "site-packages", "vendor",
    "private", "secrets", "credentials", "logs", "log", "output", "outputs",
    "artifacts", "audit", "dist", "build", "coverage", "htmlcov",
})
LOCKS = {
    "uv.lock": "uv", "poetry.lock": "poetry", "pdm.lock": "pdm",
    "Pipfile.lock": "pipenv", "package-lock.json": "npm",
    "npm-shrinkwrap.json": "npm", "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn", "bun.lock": "bun", "bun.lockb": "bun",
}
MANIFESTS = {
    "pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "package.json",
    "environment.yml", "environment.yaml", "tox.ini", "pytest.ini",
}
VERSION = r"[0-9]+(?:\.[0-9]+)*(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"
VERSION_RE = re.compile(rf"{VERSION}\Z")
SPEC_RE = re.compile(rf"(?:===|==|!=|~=|>=|<=|>|<){VERSION}(?:\.\*)?\Z")
NAME_RE = re.compile(r"([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\[[A-Za-z0-9_., -]+\])?(.*)\Z")
ENV_NAME_RE = re.compile(r"(?:export\s+)?([A-Z_][A-Z0-9_]{0,127})\s*=")


def emit(value: dict) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse's default errors may echo arbitrary argument values.
        emit({"error": "invalid_arguments"})
        raise SystemExit(2)


def safe_constraint(value: object, *, poetry: bool = False) -> str | None:
    """Return only a bounded numeric version expression, never arbitrary text."""
    if not isinstance(value, str) or len(value) > 200:
        return None
    compact = re.sub(r"\s+", "", value)
    if poetry and VERSION_RE.fullmatch(compact):
        return "==" + compact
    parts = compact.split(",")
    if parts and all(SPEC_RE.fullmatch(part) for part in parts):
        return ",".join(parts)
    return None


def exact_version(constraint: str | None) -> str | None:
    if constraint and constraint.startswith("==") and not constraint.startswith("==="):
        version = constraint[2:]
        if VERSION_RE.fullmatch(version):
            return version
    return None


def normal_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


class Inspector:
    def __init__(self, root: Path, *, dry_run: bool = False):
        self.root = root
        self.dry_run = dry_run
        self.files: list[str] = []
        self.manifests: list[str] = []
        self.locks: list[str] = []
        self.declarations: list[dict] = []
        self.python_declarations: list[dict] = []
        self.issues: list[dict] = []
        self.managers: set[str] = set()
        self.env_names: set[str] = set()
        self.dotenv_present = False
        self.bytes_read = 0
        self.files_seen = 0
        self.entries_seen = 0
        self.symlinks_skipped = 0
        self.directories_skipped = 0
        self.halted = False

    def issue(self, code: str, relative: str | None = None) -> None:
        item = {"code": code}
        if relative is not None:
            item["file"] = relative
        if item not in self.issues:
            self.issues.append(item)

    def declare(self, package: str, value: object, relative: str, *, poetry: bool = False,
                conditional: bool = False) -> None:
        constraint = safe_constraint(value, poetry=poetry)
        self.declarations.append({
            "package": package, "file": relative, "constraint": constraint,
            "exact_version": exact_version(constraint), "conditional": conditional,
        })
        if constraint is None or conditional:
            self.issue("unsupported_dependency_constraint", relative)

    def requirement(self, value: object, relative: str) -> None:
        if not isinstance(value, str) or len(value) > MAX_FILE_BYTES:
            self.issue("unsupported_requirement", relative)
            return
        line = value.strip()
        if not line or line.startswith("#"):
            return
        if line.startswith("-") or "\\" in line:
            self.issue("unsupported_requirements_directive", relative)
            return
        match = NAME_RE.fullmatch(line)
        if not match:
            self.issue("unsupported_requirement", relative)
            return
        package, tail = normal_name(match[1]), match[2]
        if package not in PACKAGES:
            return
        # Preserve that markers are conditional, while suppressing their values.
        condition = ";" in tail
        tail = tail.split(";", 1)[0].split("#", 1)[0].strip()
        self.declare(package, tail, relative, conditional=condition)

    def python_constraint(self, value: object, relative: str, *, poetry: bool = False) -> None:
        constraint = safe_constraint(value, poetry=poetry)
        self.python_declarations.append({"file": relative, "constraint": constraint})
        if constraint is None:
            self.issue("unsupported_python_constraint", relative)

    def pyproject(self, content: str, relative: str) -> None:
        try:
            document = tomllib.loads(content)
        except (tomllib.TOMLDecodeError, ValueError):
            self.issue("malformed_manifest", relative)
            return
        project = document.get("project", {})
        if not isinstance(project, dict):
            self.issue("unsupported_manifest_structure", relative)
            project = {}
        if "requires-python" in project:
            self.python_constraint(project["requires-python"], relative)
        if project.get("dynamic"):
            self.issue("dynamic_project_metadata", relative)
        dependencies = project.get("dependencies", [])
        if isinstance(dependencies, list):
            for dependency in dependencies:
                self.requirement(dependency, relative)
        else:
            self.issue("unsupported_manifest_structure", relative)
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, dict):
            for group in optional.values():
                if isinstance(group, list):
                    for dependency in group:
                        self.requirement(dependency, relative)
                else:
                    self.issue("unsupported_manifest_structure", relative)
        else:
            self.issue("unsupported_manifest_structure", relative)
        tool = document.get("tool", {})
        if not isinstance(tool, dict):
            self.issue("unsupported_manifest_structure", relative)
            tool = {}
        for name in ("uv", "poetry", "pdm", "hatch", "rye"):
            if name in tool:
                self.managers.add(name)
        poetry = tool.get("poetry", {})
        if not isinstance(poetry, dict):
            self.issue("unsupported_manifest_structure", relative)
            return
        groups = [poetry.get("dependencies", {}), poetry.get("dev-dependencies", {})]
        extra_groups = poetry.get("group", {})
        if isinstance(extra_groups, dict):
            for group in extra_groups.values():
                if isinstance(group, dict):
                    groups.append(group.get("dependencies", {}))
                else:
                    self.issue("unsupported_manifest_structure", relative)
        else:
            self.issue("unsupported_manifest_structure", relative)
        for group in groups:
            if not isinstance(group, dict):
                self.issue("unsupported_manifest_structure", relative)
                continue
            for package, value in group.items():
                package = normal_name(package)
                if package == "python":
                    self.python_constraint(value, relative, poetry=True)
                elif package in PACKAGES:
                    conditional = False
                    if isinstance(value, dict):
                        conditional = any(key in value for key in ("markers", "python", "platform", "optional"))
                        # URLs, git/path dependencies and custom sources stay unresolved.
                        if set(value) - {"version", "markers", "python", "platform", "optional", "extras"}:
                            value = None
                        else:
                            value = value.get("version")
                    self.declare(package, value, relative, poetry=True, conditional=conditional)
        if "dependency-groups" in document:
            self.issue("dependency_groups_not_parsed", relative)

    def read_content(self, path: Path, relative: str) -> str | None:
        if self.dry_run:
            return None
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        try:
            descriptor = os.open(path, flags)
            with os.fdopen(descriptor, "rb") as source:
                info = os.fstat(source.fileno())
                if not stat.S_ISREG(info.st_mode):
                    self.issue("not_regular_file", relative)
                    return None
                if info.st_size > MAX_FILE_BYTES:
                    self.issue("file_byte_limit", relative)
                    return None
                remaining = MAX_TOTAL_BYTES - self.bytes_read
                if info.st_size > remaining:
                    self.issue("total_byte_limit")
                    return None
                payload = source.read(min(MAX_FILE_BYTES, remaining) + 1)
                self.bytes_read += len(payload)
                if len(payload) > MAX_FILE_BYTES:
                    self.issue("file_byte_limit", relative)
                    return None
                if self.bytes_read > MAX_TOTAL_BYTES:
                    self.issue("total_byte_limit")
                    return None
                return payload.decode("utf-8")
        except (OSError, UnicodeError):
            self.issue("unreadable_or_non_utf8_file", relative)
            return None

    def inspect_file(self, path: Path, relative: str) -> None:
        name = path.name
        lowered = name.lower()
        if name.startswith(".env") and name != ".env.example":
            self.dotenv_present = True
            return
        if name.startswith(".") and name != ".env.example":
            return
        if any(word in lowered for word in ("secret", "credential", "private_key")):
            return
        requirement_file = lowered.startswith("requirements") and lowered.endswith(".txt")
        if name in LOCKS:
            self.locks.append(relative)
            self.managers.add(LOCKS[name])
            # Lock presence is intentionally not treated as version resolution.
            self.issue("lock_contents_not_parsed", relative)
        if name in MANIFESTS or requirement_file:
            self.manifests.append(relative)
        if requirement_file:
            self.managers.add("pip")
        if name == "Pipfile":
            self.managers.add("pipenv")
        if name in {"environment.yml", "environment.yaml"}:
            self.managers.add("conda")
        relevant = (path.suffix in {".py", ".sql"} or name in MANIFESTS or
                    name in LOCKS or requirement_file or name == ".env.example")
        if not relevant:
            return
        self.files.append(relative)
        if self.dry_run:
            return
        if name == "pyproject.toml" or requirement_file or name == ".env.example":
            content = self.read_content(path, relative)
            if content is None:
                return
            if name == "pyproject.toml":
                self.pyproject(content, relative)
            elif requirement_file:
                for line in content.splitlines():
                    self.requirement(line, relative)
            else:
                for line in content.splitlines():
                    match = ENV_NAME_RE.match(line.strip())
                    if match:
                        self.env_names.add(match[1])
        elif name in {"setup.py", "setup.cfg", "Pipfile", "package.json", "environment.yml", "environment.yaml"}:
            self.issue("manifest_contents_not_parsed", relative)

    def walk(self, path: Path, relative: Path = Path(), depth: int = 0) -> None:
        if self.halted:
            return
        if depth > MAX_DEPTH:
            self.issue("depth_limit")
            return
        try:
            # Opening each directory with O_NOFOLLOW also rejects a symlink swapped
            # in after its parent's directory entry was inspected.
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(path, flags)
            try:
                with os.scandir(descriptor) as scan:
                    entries = []
                    for entry in scan:
                        self.entries_seen += 1
                        if self.entries_seen > MAX_ENTRIES:
                            self.issue("entry_limit")
                            self.halted = True
                            break
                        entries.append(entry)
                    for entry in sorted(entries, key=lambda item: item.name):
                        if self.halted:
                            break
                        next_relative = relative / entry.name
                        if entry.is_symlink():
                            self.symlinks_skipped += 1
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name.startswith(".") or entry.name.lower() in SKIP_DIRS:
                                self.directories_skipped += 1
                            else:
                                self.walk(path / entry.name, next_relative, depth + 1)
                        elif entry.is_file(follow_symlinks=False):
                            self.files_seen += 1
                            if self.files_seen > MAX_FILES:
                                self.issue("file_count_limit")
                                self.halted = True
                                break
                            self.inspect_file(path / entry.name, next_relative.as_posix())
            finally:
                os.close(descriptor)
        except OSError:
            self.issue("unreadable_directory", relative.as_posix() if relative.parts else None)

    def report(self) -> dict:
        self.walk(self.root)
        return {
            "schema_version": 1,
            "mode": "dry_run_inventory_only" if self.dry_run else "static_inventory",
            "read_only": True,
            "complete_within_supported_scope": not self.issues,
            "scope": "File inventory and numeric dependency declarations; no project code execution or lock resolution.",
            "files": sorted(self.files), "manifests": sorted(self.manifests),
            "locks": sorted(self.locks), "package_manager_hints": sorted(self.managers),
            "python_declarations": sorted(self.python_declarations, key=lambda row: json.dumps(row, sort_keys=True)),
            "dependency_declarations": sorted(self.declarations, key=lambda row: json.dumps(row, sort_keys=True)),
            "environment_files": {"dotenv_present": self.dotenv_present,
                                  "example_variable_names": sorted(self.env_names)},
            "limits": {"files": MAX_FILES, "entries": MAX_ENTRIES, "depth": MAX_DEPTH,
                       "bytes_per_file": MAX_FILE_BYTES, "total_content_bytes": MAX_TOTAL_BYTES},
            "observed": {"files_seen": min(self.files_seen, MAX_FILES),
                         "entries_seen": min(self.entries_seen, MAX_ENTRIES),
                         "content_bytes_read": self.bytes_read, "symlinks_skipped": self.symlinks_skipped,
                         "directories_skipped": self.directories_skipped},
            "incompleteness": sorted(self.issues, key=lambda row: json.dumps(row, sort_keys=True)),
        }


def interpreter_metadata() -> dict:
    packages = {}
    for name in PACKAGES:
        try:
            version = importlib.metadata.version(name)
            packages[name] = version if VERSION_RE.fullmatch(version) else None
        except Exception:
            # Broken metadata can contain paths or values; never echo its errors.
            packages[name] = None
    return {"scope": "current_interpreter_only_not_target_environment_verification",
            "python_version": ".".join(map(str, sys.version_info[:3])), "packages": packages}


def check_adk(report: dict, expected: str) -> dict:
    installed = report["interpreter"]["packages"].get("google-adk")
    declarations = [row for row in report["dependency_declarations"] if row["package"] == "google-adk"]
    versions = {row["exact_version"] for row in declarations if row["exact_version"] is not None}
    reasons = []
    if installed is None:
        reasons.append("interpreter_adk_absent_or_unresolved")
    elif installed != expected:
        reasons.append("interpreter_adk_mismatch")
    if not declarations:
        reasons.append("target_adk_declaration_absent")
    if any(row["exact_version"] is None or row["conditional"] for row in declarations):
        reasons.append("target_adk_declaration_unresolved")
    if len(versions) > 1:
        reasons.append("target_adk_declarations_conflict")
    if versions and versions != {expected}:
        reasons.append("target_adk_declaration_mismatch")
    if report["incompleteness"]:
        reasons.append("target_inventory_incomplete")
    return {"expected": expected, "status": "FAIL" if reasons else "PASS", "reasons": reasons,
            "scope": "Exact declarations and current interpreter only; no target-environment compatibility claim."}


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Existing readable project directory; never imported or changed.")
    parser.add_argument("--dry-run", action="store_true", help="Inventory names and planned scope only; read no project file contents or installed-package metadata.")
    parser.add_argument("--expect-adk", help="Require an exact numeric ADK version in target declarations and this interpreter; exit 3 on mismatch or unresolved evidence.")
    args = parser.parse_args(argv)
    if os.scandir not in os.supports_fd:
        emit({"error": "directory_descriptor_scanning_unsupported"})
        return 2
    if args.expect_adk is not None and not VERSION_RE.fullmatch(args.expect_adk):
        emit({"error": "invalid_expected_version"})
        return 2
    try:
        root = Path(args.project)
        if root.is_symlink() or not root.is_dir():
            raise OSError
        # Reject symlinks in parent components as well as the target itself.
        absolute = root.absolute()
        if any(part.is_symlink() for part in (absolute, *absolute.parents)):
            raise OSError
        with os.scandir(root) as scan:
            next(scan, None)
    except (OSError, ValueError):
        emit({"error": "project_must_be_a_real_readable_directory"})
        return 2
    report = Inspector(root, dry_run=args.dry_run).report()
    if args.dry_run:
        report["interpreter"] = {"status": "not_checked_in_dry_run"}
        if args.expect_adk is not None:
            report["adk_gate"] = {"status": "NOT_RUN_DRY_RUN", "expected": args.expect_adk}
        emit(report)
        return 0
    report["interpreter"] = interpreter_metadata()
    status = 0
    if args.expect_adk is not None:
        report["adk_gate"] = check_adk(report, args.expect_adk)
        status = 3 if report["adk_gate"]["status"] == "FAIL" else 0
    emit(report)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
