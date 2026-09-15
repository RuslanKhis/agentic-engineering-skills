#!/usr/bin/env python3
"""Bounded, read-only ADK inventory. Never imports target code or reads .env."""

import argparse
import ast
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys
import tomllib


PACKAGES = ("google-adk", "google-genai", "httpx")
IGNORED = {"venv", "env", "node_modules", "dist", "build", "__pycache__"}
VERSION_TEXT = r"\d+(?:\.\d+){1,3}(?:(?:a|b|rc)\d+|\.(?:post|dev)\d+)?"
VERSION = re.compile(VERSION_TEXT + r"\Z")
REQUIREMENT = re.compile(
    r"(?i)(?<![\w.-])(google[-_]adk|google[-_]genai|httpx)"
    r"(?:\[[a-z0-9_,.-]+\])?\s*"
    r"((?:===|==|~=|>=|<=|!=|>|<)\s*"
    + VERSION_TEXT
    + r"(?:\s*,\s*(?:==|~=|>=|<=|!=|>|<)\s*"
    + VERSION_TEXT
    + r")*)"
    r"(?=$|[\s;\"'#\]])"
)
CONSTRUCTORS = {
    "google.adk.Agent": "LlmAgent",
    "google.adk.Workflow": "Workflow",
    **{
        f"google.adk.agents.{name}": name
        for name in (
            "LlmAgent",
            "Agent",
            "SequentialAgent",
            "ParallelAgent",
            "LoopAgent",
        )
    },
}


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def version_argument(value):
    if not VERSION.fullmatch(value):
        raise argparse.ArgumentTypeError("use an exact numeric version, such as 2.8.0")
    return value


def directory_argument(value):
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", value):
        raise argparse.ArgumentTypeError(
            "use a single directory name without paths or wildcards"
        )
    return value


def file_kind(path):
    if path.name == ".env" or path.name.startswith(".env."):
        return "configuration-presence-only"
    if path.name in {"pyproject.toml", "uv.lock", "poetry.lock"}:
        return "manifest"
    if path.name.startswith("requirements") and path.suffix == ".txt":
        return "manifest"
    if path.suffix == ".py":
        return "python"
    if path.name in {"pytest.ini", "tox.ini", "setup.cfg", "Makefile"}:
        return "test-configuration-presence-only"
    return None


def inventory(root, max_files, excluded_dirs=()):
    """Bound traversal, excluding symlinks and hidden/generated subdirectories."""
    files, seen = [], 0
    errors = []

    def on_error(_error):
        errors.append({"code": "directory-read-error"})

    for directory, dirs, names in os.walk(root, followlinks=False, onerror=on_error):
        dirs[:] = sorted(
            name
            for name in dirs
            if not name.startswith(".")
            and name not in IGNORED
            and name not in excluded_dirs
            and not (Path(directory) / name).is_symlink()
            and not (Path(directory) / name / "pyvenv.cfg").exists()
        )
        for name in sorted(names):
            seen += 1
            if seen > max_files:
                errors.append({"code": "file-limit-exceeded"})
                return files, errors
            path = Path(directory) / name
            kind = file_kind(path)
            if kind and not path.is_symlink() and path.is_file():
                files.append((path, kind))
    return sorted(files), errors


def qualified(node, aliases):
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return qualified(node.value, aliases) + "." + node.attr
    return ""


def analyse_python(text):
    """Only inspect AST; no literals from target source enter the returned data."""
    tree = ast.parse(text)
    aliases = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                aliases[alias.asname or alias.name] = node.module + "." + alias.name
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    aliases[alias.asname] = alias.name
    bindings = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bindings[target.id] = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if isinstance(node.value, ast.Call):
                bindings[node.target.id] = node.value

    def keywords(call):
        return {kw.arg: kw.value for kw in call.keywords if kw.arg is not None}

    def state_key(call):
        if CONSTRUCTORS.get(qualified(call.func, aliases)) not in {"LlmAgent", "Agent"}:
            return None
        value = keywords(call).get("output_key")
        return (
            value.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str)
            else None
        )

    surfaces, findings = [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        kind = CONSTRUCTORS.get(qualified(node.func, aliases))
        if not kind:
            continue
        surfaces.append({"kind": kind, "line": node.lineno})
        params = keywords(node)
        if kind == "LoopAgent":
            bound = params.get("max_iterations")
            if not isinstance(bound, ast.Constant):
                code = (
                    "loop-bound-unresolved"
                    if bound is not None
                    else "loop-bound-missing"
                )
                findings.append({"code": code, "line": node.lineno})
            elif type(bound.value) is not int or bound.value < 1:
                findings.append({"code": "loop-bound-invalid", "line": node.lineno})
        if kind == "ParallelAgent":
            children = params.get("sub_agents")
            if not isinstance(children, (ast.List, ast.Tuple)):
                findings.append(
                    {"code": "parallel-children-unresolved", "line": node.lineno}
                )
                continue
            keys = []
            for child in children.elts:
                call = bindings.get(child.id) if isinstance(child, ast.Name) else child
                if isinstance(call, ast.Call):
                    key = state_key(call)
                    if key is not None:
                        keys.append(key)
                    else:
                        findings.append(
                            {"code": "parallel-key-unresolved", "line": child.lineno}
                        )
                else:
                    findings.append(
                        {"code": "parallel-key-unresolved", "line": child.lineno}
                    )
            if len(keys) != len(set(keys)):
                findings.append(
                    {"code": "parallel-output-key-collision", "line": node.lineno}
                )
    return surfaces, findings


def requirements(text, filename):
    items = []
    candidates = []
    if filename.endswith((".toml", ".lock")):
        document = tomllib.loads(text)
        project = document.get("project", {})
        candidates.extend(project.get("dependencies", []))
        for dependencies in project.get("optional-dependencies", {}).values():
            candidates.extend(dependencies)
        poetry = document.get("tool", {}).get("poetry", {})
        for package, spec in poetry.get("dependencies", {}).items():
            name = str(package).lower().replace("_", "-")
            if name not in PACKAGES:
                continue
            version = spec.get("version") if isinstance(spec, dict) else spec
            if isinstance(version, str):
                if VERSION.fullmatch(version):
                    candidates.append(name + "==" + version)
                else:
                    candidates.append(name + " " + version)
            else:
                items.append({"package": name, "specifier": "unresolved"})
        for entry in document.get("package", []):
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "")).lower().replace("_", "-")
            value = str(entry.get("version", ""))
            if name in PACKAGES and VERSION.fullmatch(value):
                items.append({"package": name, "specifier": "==" + value})
    else:
        candidates = [line.split("#", 1)[0].strip() for line in text.splitlines()]
    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        match = REQUIREMENT.match(candidate.strip())
        if match:
            items.append(
                {
                    "package": match[1].lower().replace("_", "-"),
                    "specifier": re.sub(r"\s", "", match[2]),
                }
            )
        else:
            declared_name = re.match(r"[A-Za-z0-9_.-]+", candidate.strip())
            if declared_name:
                name = declared_name[0].lower().replace("_", "-")
                if name in PACKAGES:
                    items.append({"package": name, "specifier": "unresolved"})
    return sorted({(i["package"], i["specifier"]) for i in items})


def inspect(
    root,
    *,
    max_files=4000,
    max_bytes=1048576,
    dry_run=False,
    required_adk=None,
    excluded_dirs=(),
):
    paths, errors = inventory(root, max_files, excluded_dirs)
    output = {
        "mode": "dry-run" if dry_run else "read-only",
        "files": [],
        "declarations": [],
        "surfaces": [],
        "findings": [],
        "errors": errors,
        "explicitly_excluded_directory_names": sorted(set(excluded_dirs)),
    }
    for path, kind in paths:
        relative = path.relative_to(root).as_posix()
        output["files"].append({"path": relative, "kind": kind})
        if dry_run or kind.endswith("presence-only"):
            continue
        try:
            # Bound bytes as well as file count, and reject symlink races where possible.
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(fd, "rb") as stream:
                raw = stream.read(max_bytes + 1)
            if len(raw) > max_bytes:
                output["errors"].append({"code": "file-size-limit", "path": relative})
                continue
            text = raw.decode("utf-8")
            if kind == "manifest":
                for package, specifier in requirements(text, path.name):
                    output["declarations"].append(
                        {"path": relative, "package": package, "specifier": specifier}
                    )
            elif kind == "python":
                surfaces, findings = analyse_python(text)
                output["surfaces"].extend({"path": relative, **s} for s in surfaces)
                output["findings"].extend({"path": relative, **f} for f in findings)
        except (
            OSError,
            UnicodeError,
            SyntaxError,
            ValueError,
            TypeError,
            AttributeError,
            RecursionError,
        ):
            output["errors"].append(
                {"code": "file-read-or-parse-error", "path": relative}
            )
    output["complete"] = not output["errors"]
    if dry_run:
        output["project_contents_read"] = False
        return output, 0 if output["complete"] else 2
    installed = {}
    for package in PACKAGES:
        try:
            value = importlib.metadata.version(package)
            installed[package] = (
                value if VERSION.fullmatch(value) else "unrecognised-version"
            )
        except importlib.metadata.PackageNotFoundError:
            installed[package] = None
    output["runtime"] = {
        "python": ".".join(map(str, sys.version_info[:3])),
        "packages": installed,
    }
    output["compatibility"] = "not-requested"
    if not output["complete"]:
        return output, 2
    if required_adk:
        specs = [
            d["specifier"]
            for d in output["declarations"]
            if d["package"] == "google-adk"
        ]
        # Ranges and conflicting nested services require explicit package-manager review.
        matches = (
            installed["google-adk"] == required_adk
            and bool(specs)
            and all(spec == "==" + required_adk for spec in specs)
        )
        output["compatibility"] = (
            "exact-adk-match" if matches else "reconciliation-required"
        )
        if not matches:
            return output, 3
    return output, 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        type=Path,
        required=True,
        help="Project/service directory to inspect",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List intended reads; do not read source contents",
    )
    parser.add_argument(
        "--max-files",
        type=positive_int,
        default=4000,
        help="Traversal file limit (default: 4000)",
    )
    parser.add_argument(
        "--max-bytes",
        type=positive_int,
        default=1048576,
        help="Per-file byte limit (default: 1048576)",
    )
    parser.add_argument(
        "--require-adk-version",
        type=version_argument,
        help="Return 3 unless installed and declared ADK match this exact version",
    )
    parser.add_argument(
        "--exclude-dir",
        type=directory_argument,
        action="append",
        default=[],
        help="Explicitly exclude a directory name at every depth (repeatable)",
    )
    args = parser.parse_args(argv)
    try:
        root = args.project.resolve(strict=True)
    except (OSError, RuntimeError):
        parser.error("project directory does not exist or cannot be resolved")
    if not root.is_dir():
        parser.error("project must be a directory")
    output, status = inspect(
        root,
        max_files=args.max_files,
        max_bytes=args.max_bytes,
        dry_run=args.dry_run,
        required_adk=args.require_adk_version,
        excluded_dirs=args.exclude_dir,
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
