#!/usr/bin/env python3
"""Read-only, bounded project inventory. Findings are hints, never a safety verdict."""
import argparse
import configparser
from collections import deque
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import re
import stat

PACKAGES = ("google-adk", "google-genai")
IDENTIFIERS = ("SafeAgentRuntime", "MockBudgetStore", "max_llm_calls", "before_model_callback",
               "after_model_callback", "before_tool_callback", "usage_metadata", "payment_processed")
SKIP_DIRS = {"venv", "env", "build", "dist", "node_modules", "site-packages", "__pycache__"}
CONFIGS = {"pyproject.toml", "Pipfile", "setup.cfg", "pytest.ini", "tox.ini", "uv.lock",
           "poetry.lock", "Pipfile.lock", "pdm.lock", "setup.py", "Makefile", ".python-version"}
MAX_FILES, MAX_BYTES, MAX_DEPTH = 5000, 262144, 12
MAX_DIRS, MAX_TOTAL_BYTES = 2000, 8 * 1024 * 1024
SENSITIVE = re.compile(r"credential|secret|private.?key|service.?account|^env(?:[._]|$)", re.I)
SAFE_PATH = re.compile(r"[A-Za-z0-9_./ -]{1,240}\Z")
VERSION = re.compile(r"[0-9]+(?:\.[0-9]+){0,3}(?:(?:a|b|rc|post|dev)[0-9]+)?\Z")
CONSTRAINT = re.compile(r"(?:[<>=!~^]{0,2}\s*[0-9]+(?:\.(?:[0-9]+|\*)){0,3}"
                        r"(?:(?:a|b|rc|post|dev)[0-9]+)?)(?:\s*,\s*"
                        r"[<>=!~^]{0,2}\s*[0-9]+(?:\.(?:[0-9]+|\*)){0,3}"
                        r"(?:(?:a|b|rc|post|dev)[0-9]+)?)*\Z")


def inspect(project, required=None):
    report = {"scope": "Static hints only; successful inspection is not a safety verdict.",
              "python": {"version": platform.python_version(), "implementation": platform.python_implementation()},
              "installed": {}, "declared": {"python": [], **{p: [] for p in PACKAGES}},
              "config_files": [], "guardrail_identifiers": {}, "warnings": [],
              "excluded_symlinks": 0, "files_considered": 0, "directories_considered": 1, "bytes_read": 0,
              "limits": {"files": MAX_FILES, "bytes_per_file": MAX_BYTES, "depth": MAX_DEPTH,
                         "directories": MAX_DIRS, "total_bytes": MAX_TOTAL_BYTES}}

    def warn(code):
        if code not in report["warnings"]:
            report["warnings"].append(code)

    def constraint(name, value):
        if isinstance(value, str) and len(value) <= 100 and CONSTRAINT.fullmatch(value.strip()):
            value = re.sub(r"\s+", "", value)
            if value not in report["declared"][name]:
                report["declared"][name].append(value)
        else:
            warn("unsupported_or_invalid_selected_version_constraint")

    def dependency(value):
        if not isinstance(value, str):
            warn("malformed_dependency_list")
            return
        match = re.match(r"^\s*(google[-_]adk|google[-_]genai)\s*(.*)$", value, re.I)
        if match:
            constraint(match[1].lower().replace("_", "-"), match[2])
        elif any(p in value.lower().replace("_", "-") for p in PACKAGES):
            warn("unsupported_selected_dependency_declaration")

    def dependencies(values):
        if not isinstance(values, list):
            warn("malformed_dependency_list")
        else:
            for value in values:
                dependency(value)

    for package in PACKAGES:
        try:
            version = metadata.version(package)
            report["installed"][package] = version if VERSION.fullmatch(version) else "unreportable"
            if report["installed"][package] == "unreportable":
                warn("invalid_installed_version_metadata")
        except metadata.PackageNotFoundError:
            report["installed"][package] = None
        except Exception:
            report["installed"][package] = None
            warn("installed_metadata_unreadable")

    def parse_config(name, content):
        if name == ".python-version":
            constraint("python", content.strip())
        elif name.startswith("requirements") and name.endswith(".txt"):
            for line in content.splitlines():
                if line.strip().startswith(("-r", "--requirement", "-c", "--constraint")):
                    warn("requirements_includes_not_followed")
                if not line.lstrip().startswith("#"):
                    dependency(line)
        elif name in ("pyproject.toml", "Pipfile"):
            try:
                import tomllib
            except ImportError:
                warn("toml_inspection_requires_python_3_11")
                return
            data = tomllib.loads(content)
            project_data = data.get("project", {})
            if "requires-python" in project_data:
                constraint("python", project_data["requires-python"])
            dependencies(project_data.get("dependencies", []))
            for deps in project_data.get("optional-dependencies", {}).values():
                dependencies(deps)
            for deps in data.get("dependency-groups", {}).values():
                dependencies(deps)
            poetry = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            for group in (poetry, data.get("packages", {}), data.get("dev-packages", {})):
                for package, value in group.items():
                    normalized = package.lower().replace("_", "-")
                    if normalized in (*PACKAGES, "python"):
                        constraint(normalized, value)
            for key, value in data.get("requires", {}).items():
                if key in ("python_version", "python_full_version"):
                    constraint("python", value)
        elif name == "setup.cfg":
            config = configparser.ConfigParser(interpolation=None)
            config.read_string(content)
            if config.has_option("options", "python_requires"):
                constraint("python", config.get("options", "python_requires"))
            for section in ("options", "options.extras_require"):
                for key, value in config.items(section) if config.has_section(section) else []:
                    if key == "install_requires" or section == "options.extras_require":
                        for dep in value.splitlines():
                            dependency(dep)

    def walk():
        pending = deque([project])
        scanned = 0
        while pending:
            directory, dirs, files = pending.popleft(), [], []
            try:
                with os.scandir(directory) as entries:
                    for entry in entries:
                        scanned += 1
                        if scanned > MAX_FILES + MAX_DIRS:
                            warn("entry_scan_limit_reached")
                            break
                        (dirs if entry.is_dir(follow_symlinks=False) else files).append(entry.name)
            except OSError:
                warn("directory_unreadable")
            yield directory, dirs, files
            if scanned > MAX_FILES + MAX_DIRS:
                break
            pending.extend(Path(directory, name) for name in dirs)

    for directory, dirs, files in walk():
        depth = len(Path(directory).relative_to(project).parts)
        retained = []
        for name in sorted(dirs):
            if report["directories_considered"] >= MAX_DIRS:
                warn("directory_count_limit_reached")
                break
            report["directories_considered"] += 1
            child = Path(directory, name)
            if child.is_symlink():
                report["excluded_symlinks"] += 1
            elif not name.startswith(".") and name not in SKIP_DIRS and not SENSITIVE.search(name):
                if depth < MAX_DEPTH:
                    retained.append(name)
                else:
                    warn("directory_depth_limit_reached")
        dirs[:] = retained
        for name in sorted(files):
            report["files_considered"] += 1
            if report["files_considered"] > MAX_FILES:
                warn("file_count_limit_reached")
                break
            path = Path(directory, name)
            if path.is_symlink():
                report["excluded_symlinks"] += 1
                continue
            if (name.startswith(".") and name != ".python-version") or SENSITIVE.search(name):
                continue
            is_config = name in CONFIGS or (name.startswith("requirements") and name.endswith(".txt"))
            if not is_config and not name.endswith(".py"):
                continue
            relative = path.relative_to(project).as_posix()
            if not SAFE_PATH.fullmatch(relative):
                warn("unsafe_filename_omitted")
                continue
            if is_config:
                report["config_files"].append(relative)
            if name.endswith(".lock") or name in ("Makefile", "pytest.ini", "tox.ini"):
                continue
            try:
                fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
                with os.fdopen(fd, "rb") as stream:
                    info = os.fstat(stream.fileno())
                    if not stat.S_ISREG(info.st_mode):
                        warn("non_regular_file_skipped")
                        continue
                    if info.st_size > MAX_BYTES:
                        warn("file_size_limit_reached")
                        continue
                    raw = stream.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    warn("file_size_limit_reached")
                    continue
                report["bytes_read"] += len(raw)
                if report["bytes_read"] > MAX_TOTAL_BYTES:
                    warn("total_read_limit_reached")
                    break
                content = raw.decode("utf-8")
                parse_config(name, content)
                if name.endswith(".py"):
                    for identifier in IDENTIFIERS:
                        count = len(re.findall(r"\b" + identifier + r"\b", content))
                        if count:
                            entry = report["guardrail_identifiers"].setdefault(identifier, {"occurrences": 0, "files": []})
                            entry["occurrences"] += count
                            entry["files"].append(relative)
            except (OSError, UnicodeError, ValueError, TypeError, AttributeError,
                    RecursionError, configparser.Error):
                warn("file_unreadable_or_configuration_malformed")
        if report["files_considered"] > MAX_FILES or report["bytes_read"] > MAX_TOTAL_BYTES:
            break
    if required is not None:
        report["adk_compatibility"] = {"required": required, "matches": report["installed"]["google-adk"] == required}
        if not report["adk_compatibility"]["matches"]:
            warn("required_adk_version_not_installed_in_inspector_interpreter")
    report["complete_within_scope"] = not report["warnings"]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Existing project directory; never imported or executed")
    parser.add_argument("--dry-run", action="store_true", help="Same read-only inspection; this program never writes")
    parser.add_argument("--require-adk", help="Optional exact installed google-adk version to check; never installs")
    args = parser.parse_args()
    root = Path(args.project).absolute()
    if root.is_symlink() or any(parent.is_symlink() for parent in root.parents) or not root.is_dir():
        parser.error("project must be an existing directory with no symlink path components")
    if args.require_adk is not None and not VERSION.fullmatch(args.require_adk):
        parser.error("require-adk must be a numeric release version")
    result = inspect(root, args.require_adk)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["complete_within_scope"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
