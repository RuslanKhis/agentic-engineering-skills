#!/usr/bin/env python3
"""Bounded offline inventory. Does not import project code or contact providers."""

from __future__ import annotations

import argparse
import ast
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys

PACKAGES = (
    "google-adk",
    "google-genai",
    "google-cloud-aiplatform",
    "google-cloud-bigquery",
    "google-cloud-dlp",
    "google-cloud-modelarmor",
    "redis",
)
SKIP_DIRS = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    "dist", "build", "verification", "audit-evidence", "skills",
}
SIGNALS = {
    "sessions": ("SessionService", "get_session", "create_session"),
    "rag": (
        "retrieveContexts", "retrieve_contexts", "VertexAiRagRetrieval",
        "vertex_rag_service", "rag_corpora",
    ),
    "memory_bank": ("MemoryService", "generate_memories", "MemoryBank"),
    "bigquery": ("bigquery", "QueryJobConfig"),
}
LIMIT_FILES = 2000
LIMIT_BYTES = 8 * 1024 * 1024
LIMIT_FILE_BYTES = 512 * 1024
DEPENDENCY = re.compile(
    r"\b(google[-_]adk|google[-_]genai|google[-_]cloud[-_]aiplatform|"
    r"google[-_]cloud[-_]bigquery|google[-_]cloud[-_]dlp|"
    r"google[-_]cloud[-_]modelarmor|redis)"
    r"(?:\[[A-Za-z0-9_,.\-]+\])?\s*(==|~=|>=|<=|>|<|\^)\s*"
    r"([0-9][0-9A-Za-z.!+_*\-]*)(?=$|[\s,;\"'\]#])",
    re.IGNORECASE,
)


def runtime_versions() -> dict:
    installed = {}
    for package in PACKAGES:
        try:
            installed[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            installed[package] = None
    return {"python": sys.version.split()[0], "installed": installed}


def inspect_project(project: Path, *, dry_run: bool = False) -> tuple[dict, int]:
    """Return a value-only report; never echo source lines or config values."""
    if project.is_symlink() or not project.is_dir():
        raise ValueError("project must be an existing non-symlink directory")
    root = project.resolve()
    runtime = runtime_versions()
    report = {
        "schema_version": 1,
        "dry_run": dry_run,
        "runtime": runtime,
        "limits": {"files": LIMIT_FILES, "bytes": LIMIT_BYTES},
        "declarations": [],
        "signals": {key: [] for key in SIGNALS},
        "manifests": [],
        "coverage": {"visited_files": 0, "read_files": 0, "read_bytes": 0},
        "warnings": [],
        "compatibility": "not_established",
        "security": "not_evaluated",
    }
    if dry_run:
        report["plan"] = (
            "Read bounded Python and dependency manifest files; skip hidden "
            "directories, symlinks and credential files; emit names and versions only. "
            "No project files will be read in this dry run."
        )
        return report, 0

    warnings = set()
    declarations = set()
    coverage = report["coverage"]

    def on_error(_error: OSError) -> None:
        warnings.add("some directories could not be read")

    stop = False
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=on_error):
        base = Path(directory)
        dirs[:] = sorted(
            name for name in dirs
            if not name.startswith(".") and name not in SKIP_DIRS
            and not (base / name).is_symlink()
        )
        for name in sorted(files):
            coverage["visited_files"] += 1
            if coverage["visited_files"] > LIMIT_FILES:
                warnings.add("file limit reached; inspect omitted files manually")
                stop = True
                break
            path = base / name
            if path.is_symlink() or name.startswith("."):
                continue
            manifest = (
                name == "pyproject.toml"
                or (name.startswith("requirements") and path.suffix == ".txt")
                or name in {"uv.lock", "poetry.lock", "Pipfile", "Pipfile.lock"}
            )
            if not manifest and path.suffix != ".py":
                continue
            relative = path.relative_to(root).as_posix()
            if manifest:
                report["manifests"].append(relative)
            try:
                # Recheck containment and type before reading; not a hostile-FS sandbox.
                if not path.resolve().is_relative_to(root) or not path.is_file():
                    continue
                size = path.stat().st_size
                if size > LIMIT_FILE_BYTES:
                    warnings.add("oversized files skipped")
                    continue
                if coverage["read_bytes"] + size > LIMIT_BYTES:
                    warnings.add("byte limit reached; inspect omitted files manually")
                    stop = True
                    break
                with path.open("rb") as stream:
                    raw = stream.read(LIMIT_FILE_BYTES + 1)
                if len(raw) > LIMIT_FILE_BYTES:
                    warnings.add("growing or oversized files skipped")
                    continue
                source = raw.decode("utf-8")
            except (OSError, UnicodeError):
                warnings.add("some candidate files could not be read")
                continue
            coverage["read_files"] += 1
            coverage["read_bytes"] += len(raw)
            if manifest:
                for match in DEPENDENCY.finditer(source):
                    package, operator, version = match.groups()
                    declarations.add(
                        (relative, package.lower().replace("_", "-"), operator, version)
                    )
                continue
            try:
                tree = ast.parse(source)
            except (SyntaxError, ValueError, RecursionError):
                warnings.add("some Python files could not be parsed")
                continue
            identifiers = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    identifiers.add(node.id)
                elif isinstance(node, ast.Attribute):
                    identifiers.add(node.attr)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    identifiers.update(alias.name for alias in node.names)
                    if isinstance(node, ast.ImportFrom) and node.module:
                        identifiers.add(node.module)
            for mode, needles in SIGNALS.items():
                if any(needle in word for needle in needles for word in identifiers):
                    report["signals"][mode].append(relative)
        if stop:
            break

    report["declarations"] = [
        {"file": file, "package": package, "operator": operator, "version": version}
        for file, package, operator, version in sorted(declarations)
    ]
    # Declarations can describe separate environments or conditional dependencies.
    # Treat conflicts as requiring a human/agent resolution, never choose a pin.
    pins = {
        version for _, package, operator, version in declarations
        if package == "google-adk" and operator == "==" and "*" not in version
    }
    installed = runtime["installed"]["google-adk"]
    code = 0
    if len(pins) > 1:
        report["compatibility"] = "conflicting_declared_adk_pins"
        code = 3
    elif pins and installed and installed not in pins:
        report["compatibility"] = "declared_installed_adk_mismatch"
        code = 3
    elif any(
        version.split(".")[0] != "2"
        for version in pins | ({installed} if installed else set())
    ):
        report["compatibility"] = "unsupported_adk_major_for_source_guidance"
        code = 3
    elif pins == {"2.8.0"} and installed == "2.8.0":
        report["compatibility"] = "adk_baseline_matches_other_contracts_unchecked"
    else:
        warnings.add("resolve target pins and verify SDK interfaces before implementation")
    warnings.add("declaration extraction is partial; lockfiles and markers need manual review")
    warnings.add("signals include tests and do not establish runtime behaviour or security")
    report["warnings"] = sorted(warnings)
    return report, code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Target project directory")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show the inspection plan and interpreter metadata without reading project files",
    )
    args = parser.parse_args(argv)
    if sys.version_info < (3, 11):
        parser.error("inspector requires Python 3.11+; do not change the target environment")
    try:
        report, code = inspect_project(args.project, dry_run=args.dry_run)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
