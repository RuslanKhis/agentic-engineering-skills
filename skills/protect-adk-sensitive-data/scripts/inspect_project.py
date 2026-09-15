#!/usr/bin/env python3
"""Inventory safe dependency metadata in one package directory, without writes.

Python 3.11+; standard library only. Inspection is root-only: pass the package
directory itself, not a monorepo root. All directories and symlinks are skipped.
Lockfiles, source files, test configuration, and environment files are never
read. This inventories declarations; it does not resolve or assess compatibility.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import sys

if sys.version_info < (3, 11):
    print(
        "error: this optional inspector requires Python 3.11+; preserve the "
        "target interpreter and inspect dependency metadata manually",
        file=sys.stderr,
    )
    raise SystemExit(2)

import tomllib


MAX_ROOT_ENTRIES = 512
MAX_METADATA_BYTES = 262_144
MAX_REQUIREMENT_LINES = 4_096
MAX_DECLARED_CONSTRAINTS = 128
DEPENDENCIES = frozenset(
    {"google-adk", "google-cloud-dlp", "google-cloud-modelarmor", "google-genai", "pydantic"}
)
REQUIREMENTS = frozenset(
    f"requirements{suffix}.{extension}"
    for suffix in ("", "-dev", "-test", "-tests", "-prod", "-production", "-base")
    for extension in ("txt", "in")
)
MANIFESTS = REQUIREMENTS | {
    "pyproject.toml", "Pipfile", "setup.py", "setup.cfg", "environment.yml", "environment.yaml"
}
LOCKFILES = frozenset({"uv.lock", "poetry.lock", "Pipfile.lock", "pdm.lock", "pylock.toml", "requirements.lock", "pixi.lock"})
TEST_CONFIGS = frozenset({"pytest.ini", ".pytest.ini", "tox.ini", "noxfile.py", "conftest.py"})
RUNTIME_CONFIGS = frozenset({".python-version"})
RECOGNIZED = MANIFESTS | LOCKFILES | TEST_CONFIGS | RUNTIME_CONFIGS
READABLE = REQUIREMENTS | {"pyproject.toml", ".python-version"}
PACKAGE_MANAGER_FILES = {
    "uv.lock": "uv", "poetry.lock": "poetry", "Pipfile": "pipenv", "Pipfile.lock": "pipenv",
    "pdm.lock": "pdm", "pixi.lock": "pixi", "environment.yml": "conda", "environment.yaml": "conda",
    "setup.py": "setuptools", "setup.cfg": "setuptools",
}
VERSION = r"(?:\*|(?:[0-9]+!)?[0-9]+(?:\.[0-9]+)*(?:\.\*)?(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?)"
SPECIFIER = rf"(?:===|==|!=|~=|<=|>=|<|>|=|\^|~)?\s*{VERSION}"
SAFE_CONSTRAINT = re.compile(rf"{SPECIFIER}(?:\s*,\s*{SPECIFIER})*", re.ASCII)
REQUIREMENT = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[([A-Za-z0-9_,. -]+)\])?\s*(.*)", re.ASCII)


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse's default includes user-supplied arguments in diagnostics.
        self.exit(2, "error: invalid command arguments; use --help\n")


def empty_result(dry_run: bool) -> dict:
    return {
        "schema_version": 1,
        "mode": "dry_run" if dry_run else "inspect",
        "scope": "project_root_only",
        "compatibility": "not_assessed",
        "manifest_paths": [], "lock_paths": [], "runtime_config_paths": [], "test_config_paths": [],
        "package_manager_signals": [], "planned_content_reads": [], "files_read": [],
        "declared_constraints": [], "manual_review": [], "errors": [],
    }


def note(result: dict, code: str, path: str | None = None, dependency: str | None = None, *, error: bool = False) -> None:
    item = {"code": code}
    if path is not None:
        item["path"] = path
    if dependency is not None:
        item["dependency"] = dependency
    bucket = result["errors" if error else "manual_review"]
    if item not in bucket:
        bucket.append(item)


def canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def add_constraint(result: dict, name: str, value: object, source: str, section: str) -> None:
    if not isinstance(value, str):
        note(result, "unsupported_dependency_declaration", source, name)
        return
    value = value.strip()
    if not value or value in {"*", "==*", "=*"}:
        note(result, "unconstrained_dependency", source, name)
        return
    if len(value) > 128 or not SAFE_CONSTRAINT.fullmatch(value):
        note(result, "unsafe_or_unresolved_constraint_omitted", source, name)
        return
    item = {"dependency": name, "constraint": re.sub(r"\s+", "", value), "source": source, "section": section}
    if item not in result["declared_constraints"]:
        if len(result["declared_constraints"]) >= MAX_DECLARED_CONSTRAINTS:
            note(result, "constraint_inventory_limit_exceeded", error=True)
            return
        result["declared_constraints"].append(item)


def parse_requirement(result: dict, value: object, source: str, section: str) -> None:
    if not isinstance(value, str):
        note(result, "unsupported_dependency_declaration", source)
        return
    match = REQUIREMENT.fullmatch(value.strip())
    if not match:
        note(result, "unresolved_requirement_omitted", source)
        return
    name = canonical_name(match[1])
    if name not in DEPENDENCIES:
        return
    constraint = match[3].strip()
    if match[2]:
        note(result, "dependency_extras_omitted", source, name)
    if ";" in constraint:
        constraint = constraint.split(";", 1)[0].strip()
        note(result, "conditional_dependency_requires_manual_review", source, name)
    if constraint.startswith("(") and constraint.endswith(")"):
        constraint = constraint[1:-1].strip()
    add_constraint(result, name, constraint, source, section)


def parse_list(result: dict, values: object, source: str, section: str) -> None:
    if not isinstance(values, list):
        note(result, "unsupported_dependency_declaration", source)
        return
    for value in values:
        parse_requirement(result, value, source, section)


def parse_poetry_dependencies(result: dict, values: object, source: str, section: str) -> None:
    if not isinstance(values, dict):
        note(result, "unsupported_dependency_declaration", source)
        return
    for key, value in values.items():
        name = canonical_name(key)
        if name not in DEPENDENCIES and name != "python":
            continue
        if isinstance(value, dict):
            if any(field in value for field in ("workspace", "path", "git", "url", "source", "develop")):
                note(result, "dependency_source_requires_manual_review", source, name)
                continue
            if any(field in value for field in ("markers", "python", "platform", "optional", "extras")):
                note(result, "conditional_dependency_requires_manual_review", source, name)
            value = value.get("version")
        add_constraint(result, name, value, source, section)


def parse_pyproject(result: dict, content: str, source: str) -> None:
    try:
        data = tomllib.loads(content)
    except (tomllib.TOMLDecodeError, RecursionError):
        note(result, "invalid_toml", source, error=True)
        return
    project = data.get("project", {})
    if not isinstance(project, dict):
        note(result, "invalid_project_metadata", source, error=True)
        return
    if "requires-python" in project:
        add_constraint(result, "python", project["requires-python"], source, "project.requires-python")
    if "dependencies" in project:
        parse_list(result, project["dependencies"], source, "project.dependencies")
    optional = project.get("optional-dependencies", {})
    if isinstance(optional, dict):
        for values in optional.values():
            parse_list(result, values, source, "project.optional-dependencies")
    else:
        note(result, "unsupported_dependency_declaration", source)
    dynamic = project.get("dynamic", [])
    if not isinstance(dynamic, list) or any(key in dynamic for key in ("dependencies", "optional-dependencies", "requires-python")):
        note(result, "dynamic_metadata_requires_manual_review", source)
    groups = data.get("dependency-groups", {})
    if isinstance(groups, dict):
        for values in groups.values():
            parse_list(result, values, source, "dependency-groups")
    else:
        note(result, "unsupported_dependency_declaration", source)
    tool = data.get("tool", {})
    if not isinstance(tool, dict):
        note(result, "invalid_tool_metadata", source, error=True)
        return
    for manager in ("poetry", "uv", "pdm", "hatch", "pixi"):
        if manager in tool:
            result["package_manager_signals"].append(manager)
    if "pytest" in tool:
        result["test_config_paths"].append(source)
    poetry = tool.get("poetry", {})
    if isinstance(poetry, dict):
        for key in ("dependencies", "dev-dependencies"):
            if key in poetry:
                parse_poetry_dependencies(result, poetry[key], source, f"tool.poetry.{key}")
        groups = poetry.get("group", {})
        if isinstance(groups, dict):
            for group in groups.values():
                if isinstance(group, dict) and "dependencies" in group:
                    parse_poetry_dependencies(result, group["dependencies"], source, "tool.poetry.group.dependencies")
                else:
                    note(result, "unsupported_dependency_declaration", source)
        else:
            note(result, "unsupported_dependency_declaration", source)
    else:
        note(result, "unsupported_dependency_declaration", source)
    for config in tool.values():
        if isinstance(config, dict) and "workspace" in config:
            note(result, "workspace_constraints_require_manual_review", source)
    uv = tool.get("uv", {})
    if isinstance(uv, dict):
        if "sources" in uv:
            note(result, "dependency_sources_require_manual_review", source)
        if "dev-dependencies" in uv:
            parse_list(result, uv["dev-dependencies"], source, "tool.uv.dev-dependencies")


def parse_requirements(result: dict, content: str, source: str) -> None:
    lines = content.splitlines()
    if len(lines) > MAX_REQUIREMENT_LINES:
        note(result, "requirement_line_limit_exceeded", source, error=True)
        return
    continuation = False
    for raw in lines:
        line = raw.strip()
        if continuation or line.endswith("\\"):
            continuation = line.endswith("\\")
            note(result, "requirements_continuation_requires_manual_review", source)
            continue
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-r", "-c", "--requirement", "--constraint")):
            note(result, "requirements_include_not_followed", source)
            continue
        if line.startswith("-"):
            note(result, "requirements_option_requires_manual_review", source)
            continue
        parse_requirement(result, line.split("#", 1)[0].strip(), source, "requirements")


def read_metadata(path: Path, result: dict) -> str | None:
    """Read a bounded regular metadata file, refusing a final-component symlink."""
    descriptor = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        descriptor = os.open(path, flags)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            note(result, "nonregular_metadata_skipped", path.name, error=True)
            return None
        if info.st_size > MAX_METADATA_BYTES:
            note(result, "metadata_file_too_large", path.name, error=True)
            return None
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            raw = stream.read(MAX_METADATA_BYTES + 1)
        result["files_read"].append(path.name)
        if len(raw) > MAX_METADATA_BYTES:
            note(result, "metadata_file_too_large", path.name, error=True)
            return None
        return raw.decode("utf-8-sig")
    except (OSError, UnicodeError):
        note(result, "metadata_unreadable", path.name, error=True)
        return None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def inspect_project(project: Path, *, dry_run: bool = False) -> dict:
    """Return deterministic JSON-compatible metadata; never modify the project."""
    result = empty_result(dry_run)
    try:
        info = project.lstat()
        if stat.S_ISLNK(info.st_mode):
            note(result, "symlink_project_root_refused", error=True)
            return result
        if not stat.S_ISDIR(info.st_mode):
            note(result, "invalid_project_directory", error=True)
            return result
        entries = []
        for entry in project.iterdir():
            entries.append(entry)
            if len(entries) > MAX_ROOT_ENTRIES:
                note(result, "root_entry_limit_exceeded", error=True)
                return result
    except (OSError, ValueError):
        note(result, "invalid_project_directory", error=True)
        return result
    for path in sorted(entries):
        name = path.name
        if name not in RECOGNIZED:
            continue
        try:
            info = path.lstat()
        except OSError:
            note(result, "metadata_unreadable", name, error=True)
            continue
        if stat.S_ISLNK(info.st_mode):
            note(result, "symlink_metadata_skipped", name)
            continue
        if not stat.S_ISREG(info.st_mode):
            note(result, "nonregular_metadata_skipped", name)
            continue
        for key, names in (("manifest_paths", MANIFESTS), ("lock_paths", LOCKFILES),
                           ("runtime_config_paths", RUNTIME_CONFIGS), ("test_config_paths", TEST_CONFIGS)):
            if name in names:
                result[key].append(name)
        if name in REQUIREMENTS:
            result["package_manager_signals"].append("pip")
        if name in PACKAGE_MANAGER_FILES:
            result["package_manager_signals"].append(PACKAGE_MANAGER_FILES[name])
        if name in MANIFESTS and name not in READABLE:
            note(result, "manifest_content_not_inspected", name)
        if name not in READABLE:
            continue
        if info.st_size > MAX_METADATA_BYTES:
            note(result, "metadata_file_too_large", name, error=True)
            continue
        result["planned_content_reads"].append(name)
        if dry_run:
            continue
        content = read_metadata(path, result)
        if content is None:
            continue
        if name == "pyproject.toml":
            parse_pyproject(result, content, name)
        elif name == ".python-version":
            add_constraint(result, "python", content, name, "runtime_version")
        else:
            parse_requirements(result, content, name)
    for key in ("package_manager_signals", "test_config_paths"):
        result[key] = sorted(set(result[key]))
    result["declared_constraints"].sort(key=lambda item: (item["source"], item["section"], item["dependency"], item["constraint"]))
    for key in ("manual_review", "errors"):
        result[key].sort(key=lambda item: (item.get("path", ""), item["code"], item.get("dependency", "")))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = SafeArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Package directory; only recognized root metadata is inspected.")
    parser.add_argument("--dry-run", action="store_true", help="List metadata and planned reads without reading any file content.")
    args = parser.parse_args(argv)
    result = inspect_project(args.project, dry_run=args.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
