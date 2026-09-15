#!/usr/bin/env python3
"""Read allowlisted project manifests without importing or executing project code.

Python 3.11+; standard library only. No network, shell, writes, lockfile parsing,
environment-file reads, dependency resolution, or target-interpreter activation.
Exit codes: 0 inspection complete; 2 invalid input; 3 explicit tested-pin gate
failed; 4 inspection incomplete. --dry-run has exactly the same read-only effect.
Use a trusted interpreter with -I -B to isolate Python's own startup behaviour.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    print("error: inspect_project.py requires Python 3.11 or newer.", file=sys.stderr)
    raise SystemExit(2)

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import stat
import time
import tomllib


TESTED_PYTHON = "3.11.4"
TESTED_PINS = {
    "google-adk": "2.8.0",
    "ag-ui-adk": "0.7.0",
    "ag-ui-protocol": "0.1.21",
    "google-cloud-aiplatform": "1.153.1",
    "google-genai": "2.19.0",
}
PYTHON_PACKAGES = frozenset(TESTED_PINS) | {
    "fastapi", "uvicorn", "httpx", "google-auth", "python-dotenv", "pydantic",
    "typing-extensions", "pytest", "pytest-asyncio",
}
CLIENT_REFERENCES = {
    "json": {
        "node": ">=18.18.0", "react": "18.3.1", "react-dom": "18.3.1",
        "@types/react": "18.3.18", "@types/react-dom": "18.3.5",
        "@vitejs/plugin-react": "4.3.4", "typescript": "5.7.3", "vite": "6.4.3",
    },
    "agui": {
        "node": ">=22.12.0", "@ag-ui/client": "0.0.57",
        "@copilotkit/react-core": "1.69.0", "@copilotkit/runtime": "1.69.0",
        "next": "15.5.24", "react": "19.2.1", "react-dom": "19.2.1",
        "zod": "3.25.76", "@types/node": "22.10.7", "@types/react": "19.0.7",
        "@types/react-dom": "19.0.3", "typescript": "5.7.3",
        "undici": "6.28.0", "qs": "6.16.0", "postcss": "8.5.28",
    },
}
CLIENT_PACKAGES = frozenset().union(*(set(v) for v in CLIENT_REFERENCES.values())) - {"node"}
MODES = ("json", "agui", "managed-json", "managed-agui")
EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
    ".nox", ".next", ".nuxt", ".cache", "dist", "build", "coverage",
    ".turbo", ".idea", ".vscode", "site-packages",
}
LOCKFILES = {
    "uv.lock", "poetry.lock", "Pipfile.lock", "pdm.lock", "package-lock.json",
    "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb",
}
VERSION_FILES = {".python-version", ".node-version", ".nvmrc", ".tool-versions"}
LIMITS = {"max_depth": 10, "max_entries": 5000, "max_manifests": 128,
          "max_file_bytes": 262144, "max_total_bytes": 2097152, "max_seconds": 10}
VERSION = r"[0-9]+(?:\.[0-9]+){0,3}(?:(?:a|b|rc|\.post|\.dev)[0-9]+)?"
PY_VERSION = re.compile(VERSION + r"\Z")
REQ_START = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\[([A-Za-z0-9_, .-]+)\])?(.*)$")
PY_SPEC = re.compile(r"(?:(?:~=|==|!=|<=|>=|<|>)\s*" + VERSION + r"(?:\.\*)?)(?:\s*,\s*(?:(?:~=|==|!=|<=|>=|<|>)\s*" + VERSION + r"(?:\.\*)?))*\Z")
NODE_ATOM = r"(?:[0-9]+|[xX*])(?:\.(?:[0-9]+|[xX*])){0,2}(?:-(?:alpha|beta|rc|canary)\.[0-9]+)?"
NODE_SPEC = re.compile(r"(?:[~^]|>=|<=|>|<|=)?" + NODE_ATOM + r"(?:(?:\s+|\s*\|\|\s*|\s+-\s+)(?:[~^]|>=|<=|>|<|=)?" + NODE_ATOM + r")*\Z")


def normalise_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def safe_constraint(value: object, *, node: bool = False) -> str | None:
    if not isinstance(value, str) or len(value) > 160:
        return None
    value = value.strip()
    pattern = NODE_SPEC if node else PY_SPEC
    return value if pattern.fullmatch(value) else None


def python_requirement(value: object, source: str) -> dict | None:
    if not isinstance(value, str) or len(value) > 4096:
        return None
    # Neither marker text, comments, URLs nor installer options enter the output.
    marker_present = ";" in value
    value = value.split(";", 1)[0].split(" #", 1)[0].strip()
    match = REQ_START.fullmatch(value)
    if not match:
        return None
    name = normalise_name(match[1])
    if name not in PYTHON_PACKAGES:
        return None
    constraint = safe_constraint(match[3])
    extras = sorted(set((match[2] or "").replace(" ", "").split(",")) & {"adk", "agent-engines", "standard"})
    expected = TESTED_PINS.get(name)
    return {"name": name, "constraint": constraint, "extras": extras,
            "source": source, "marker_present": marker_present,
            "reference_status": "tested_pin" if expected and constraint == "==" + expected else "unverified"}


def requirements_manifest(text: str) -> dict:
    found = []
    directives = {"includes": False, "constraints": False, "installer_options": False}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-r", "--requirement")):
            directives["includes"] = True
        elif line.startswith(("-c", "--constraint")):
            directives["constraints"] = True
        elif line.startswith("-"):
            directives["installer_options"] = True
        else:
            record = python_requirement(line, "requirements")
            if record:
                found.append(record)
    return {"dependencies": found, "directives_not_followed": directives}


def pyproject_manifest(text: str) -> dict:
    data = tomllib.loads(text)
    found = []
    python_constraints = []
    project = data.get("project", {})
    if isinstance(project, dict):
        if "requires-python" in project:
            python_constraints.append(safe_constraint(project["requires-python"]))
        groups = [("project.dependencies", project.get("dependencies", []))]
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, dict):
            groups += [("project.optional-dependencies", values) for values in optional.values()]
        for source, values in groups:
            if isinstance(values, list):
                found += [entry for value in values if (entry := python_requirement(value, source))]
    groups = data.get("dependency-groups", {})
    if isinstance(groups, dict):
        for values in groups.values():
            if isinstance(values, list):
                found += [entry for value in values if (entry := python_requirement(value, "dependency-groups"))]
    tool = data.get("tool", {})
    poetry = tool.get("poetry", {}) if isinstance(tool, dict) else {}
    if isinstance(poetry, dict):
        dependencies = poetry.get("dependencies", {})
        if isinstance(dependencies, dict):
            for name, value in dependencies.items():
                version = value.get("version") if isinstance(value, dict) else value
                if name == "python":
                    python_constraints.append(safe_constraint(version))
                elif isinstance(version, str):
                    if PY_VERSION.fullmatch(version):
                        version = "==" + version
                    entry = python_requirement(name + " " + version, "tool.poetry.dependencies")
                    if entry:
                        found.append(entry)
                else:
                    entry = python_requirement(name + " @unsupported", "tool.poetry.dependencies")
                    if entry:
                        found.append(entry)
    return {"dependencies": found, "python_constraints": python_constraints}


def reject_duplicate_keys(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def package_manifest(text: str) -> dict:
    data = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    if not isinstance(data, dict):
        raise ValueError("manifest must be an object")
    found = []
    for source in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        values = data.get(source, {})
        if isinstance(values, dict):
            for name, value in values.items():
                if name in CLIENT_PACKAGES:
                    version = safe_constraint(value, node=True)
                    matches = [mode for mode, pins in CLIENT_REFERENCES.items() if version and pins.get(name) == version]
                    found.append({"name": name, "constraint": version, "source": source,
                                  "reference_matches": matches, "reference_status": "tested_pin" if matches else "unverified"})
    # Read only known override package keys; never return arbitrary paths/values.
    def overrides(values: object, depth: int = 0) -> None:
        if not isinstance(values, dict) or depth > 4:
            return
        for name, value in values.items():
            if name in CLIENT_PACKAGES:
                if isinstance(value, dict):
                    overrides(value, depth + 1)
                else:
                    found.append({"name": name, "constraint": safe_constraint(value, node=True), "source": "overrides"})
            elif name == "@ai-sdk/provider-utils":
                overrides(value, depth + 1)
    overrides(data.get("overrides"))
    engines = data.get("engines", {})
    node = safe_constraint(engines.get("node"), node=True) if isinstance(engines, dict) else None
    manager = data.get("packageManager")
    if not isinstance(manager, str) or not re.fullmatch(r"(?:npm|pnpm|yarn|bun)@[0-9]+(?:\.[0-9]+){1,2}", manager):
        manager = None
    return {"dependencies": found, "node_constraint": node, "package_manager": manager}


def version_manifest(text: str, name: str) -> dict:
    values = []
    if name == ".tool-versions":
        for line in text.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[0] in {"python", "nodejs"} and PY_VERSION.fullmatch(parts[1]):
                values.append({"runtime": "node" if parts[0] == "nodejs" else "python", "version": parts[1]})
    else:
        value = text.strip()
        if name != ".python-version" and value.startswith("v"):
            value = value[1:]
        if PY_VERSION.fullmatch(value):
            values.append({"runtime": "python" if name == ".python-version" else "node", "version": value})
    return {"versions": values, "status": "declared" if values else "unverified"}


def safe_relative(path: Path) -> str:
    # JSON escapes control characters too; redact unusual directory components.
    return "/".join(part if re.fullmatch(r"[A-Za-z0-9_.@ -]{1,100}", part) else "[redacted-path]" for part in path.parts)


def kind_for(name: str) -> str | None:
    if name in LOCKFILES:
        return "lockfile"
    if re.fullmatch(r"requirements[A-Za-z0-9_.-]*\.txt", name):
        return "requirements"
    return {"pyproject.toml": "pyproject", "package.json": "package", **dict.fromkeys(VERSION_FILES, "version")}.get(name)


def scan_project(project: Path, *, limits: dict | None = None) -> dict:
    limits = dict(LIMITS if limits is None else limits)
    manifests, lockfiles, warnings = [], [], set()
    counts = {"entries": 0, "manifests": 0, "bytes_read": 0, "symlinks_skipped": 0}
    deadline = time.monotonic() + limits["max_seconds"]
    stack = [(project, Path(), 0)]
    while stack:
        directory, relative, depth = stack.pop()
        if time.monotonic() >= deadline or counts["entries"] >= limits["max_entries"]:
            warnings.add("walk_limit_reached")
            break
        try:
            before = directory.lstat()
            if stat.S_ISLNK(before.st_mode):
                counts["symlinks_skipped"] += 1
                continue
            # O_NOFOLLOW prevents a swapped symlink on platforms that support it.
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            if os.scandir in os.supports_fd and hasattr(os, "O_DIRECTORY"):
                dir_fd = os.open(directory, flags)
                try:
                    with os.scandir(dir_fd) as entries:
                        items = []
                        for entry in entries:
                            if counts["entries"] >= limits["max_entries"] or time.monotonic() >= deadline:
                                warnings.add("walk_limit_reached")
                                break
                            counts["entries"] += 1
                            items.append((entry.name, entry.stat(follow_symlinks=False)))
                finally:
                    os.close(dir_fd)
            else:
                with os.scandir(directory) as entries:
                    items = []
                    for entry in entries:
                        if counts["entries"] >= limits["max_entries"] or time.monotonic() >= deadline:
                            warnings.add("walk_limit_reached")
                            break
                        counts["entries"] += 1
                        items.append((entry.name, entry.stat(follow_symlinks=False)))
        except OSError:
            warnings.add("directory_unreadable_or_changed")
            continue
        for name, info in sorted(items):
            if stat.S_ISLNK(info.st_mode):
                counts["symlinks_skipped"] += 1
                continue
            path, rel = directory / name, relative / name
            if stat.S_ISDIR(info.st_mode):
                if name not in EXCLUDED_DIRS and not name.startswith(".env"):
                    if depth < limits["max_depth"]:
                        stack.append((path, rel, depth + 1))
                    else:
                        warnings.add("depth_limit_reached")
                continue
            kind = kind_for(name)
            if not kind or not stat.S_ISREG(info.st_mode):
                continue
            if kind == "lockfile":
                lockfiles.append({"path": safe_relative(rel), "content_inspected": False})
                continue
            if counts["manifests"] >= limits["max_manifests"]:
                warnings.add("manifest_limit_reached")
                continue
            counts["manifests"] += 1
            record = {"path": safe_relative(rel), "kind": kind}
            manifests.append(record)
            if info.st_size > limits["max_file_bytes"] or counts["bytes_read"] + info.st_size > limits["max_total_bytes"]:
                record["status"] = "size_limit_not_read"
                warnings.add("byte_limit_reached")
                continue
            try:
                # Recheck the whole in-project path, then refuse a changed inode.
                current = project
                for component in rel.parts:
                    current = current / component
                    if stat.S_ISLNK(current.lstat().st_mode):
                        raise OSError("path changed")
                fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
                with os.fdopen(fd, "rb") as stream:
                    opened = os.fstat(stream.fileno())
                    if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                        raise OSError("file changed")
                    budget = min(limits["max_file_bytes"], limits["max_total_bytes"] - counts["bytes_read"])
                    raw = stream.read(budget + 1)
                counts["bytes_read"] += len(raw)
                if len(raw) > budget:
                    raise ValueError("file grew beyond limit")
                text = raw.decode("utf-8")
                parsed = (requirements_manifest(text) if kind == "requirements" else
                          pyproject_manifest(text) if kind == "pyproject" else
                          package_manifest(text) if kind == "package" else
                          version_manifest(text, name))
                record.update(parsed)
                record.setdefault("status", "inspected")
            except (OSError, ValueError, RecursionError):
                record["status"] = "unreadable_invalid_or_changed"
                warnings.add("manifest_not_inspected")
    return {"manifests": sorted(manifests, key=lambda item: item["path"]),
            "lockfiles": sorted(lockfiles, key=lambda item: item["path"]),
            "counts": counts, "limits": limits, "warnings": sorted(warnings),
            "complete_within_scope": not warnings}


def installed_packages() -> list[dict]:
    records = []
    for name in sorted(PYTHON_PACKAGES):
        try:
            raw = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            records.append({"name": name, "version": None, "status": "missing"})
            continue
        except Exception:
            # Metadata can be malformed. Never print exceptions or metadata paths.
            records.append({"name": name, "version": None, "status": "unverified"})
            continue
        version = raw if isinstance(raw, str) and PY_VERSION.fullmatch(raw) else None
        status = "unverified" if not version else ("tested_pin" if TESTED_PINS.get(name) == version else "different_from_tested" if name in TESTED_PINS else "installed_unverified")
        records.append({"name": name, "version": version, "status": status})
    return records


def tested_gate(installed: list[dict], mode: str | None, required: bool) -> dict:
    names = {"google-adk", "google-genai"}
    if mode and "agui" in mode:
        names |= {"ag-ui-adk", "ag-ui-protocol"}
    if mode and mode.startswith("managed-"):
        names.add("google-cloud-aiplatform")
    by_name = {item["name"]: item for item in installed}
    failures = [{"name": name, "expected": TESTED_PINS[name], "status": by_name[name]["status"]}
                for name in sorted(names) if by_name[name]["status"] != "tested_pin"] if mode else []
    return {"requested": required, "mode": mode, "checked_packages": sorted(names) if mode else [],
            "matches_reference_pins": not failures if mode else None, "failures": failures,
            "scope": "Invoking-interpreter reference pins only; no dependency resolution, client installation, credentials, or runtime compatibility verification."}


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse normally quotes invalid argv, which may contain pasted secrets.
        self.exit(2, "error: invalid arguments; use --help for the accepted interface.\n")


def main(argv: list[str] | None = None) -> int:
    parser = SafeArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Existing project directory; symlink roots are refused.")
    parser.add_argument("--dry-run", action="store_true", help="Same read-only inspection; never writes or runs project code.")
    parser.add_argument("--mode", choices=MODES, help="Select relevant reference Python pins for the optional strict gate.")
    parser.add_argument("--require-tested-stack", action="store_true", help="Exit 3 for missing, different or unverified selected installed pins; requires --mode.")
    args = parser.parse_args(argv)
    if args.require_tested_stack and not args.mode:
        parser.error("--require-tested-stack requires --mode")
    try:
        info = args.project.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise OSError("not a normal directory")
    except OSError:
        print(json.dumps({"error": "project_must_be_an_existing_non_symlink_directory"}))
        return 2
    installed = installed_packages()
    scan = scan_project(args.project.absolute())
    gate = tested_gate(installed, args.mode, args.require_tested_stack)
    result = {"schema_version": 1, "read_only": True,
              "interpreter": {"implementation": platform.python_implementation(), "version": platform.python_version(),
                              "scope": "invoking_interpreter_only", "reference_python": TESTED_PYTHON},
              "reference_python_pins": TESTED_PINS, "reference_client_stacks": CLIENT_REFERENCES,
              "installed_python": installed, "project": scan, "tested_stack_gate": gate,
              "limitations": ["Only allowlisted manifest fields and lockfile presence are inspected.",
                              "Version differences are unverified, not proof of incompatibility; pins are never changed.",
                              "Conditional requirements, includes, custom build backends and dependency resolution are not evaluated.",
                              "Node and client installed versions, cloud credentials and live integrations are not checked.",
                              "Use a trusted interpreter and a stable project tree; concurrent filesystem changes can make inspection incomplete."]}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
    if not scan["complete_within_scope"]:
        return 4
    return 3 if args.require_tested_stack and not gate["matches_reference_pins"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
