#!/usr/bin/env python3
"""Bounded source inventory. Never imports or executes the inspected project."""

import argparse
import ast
import json
import os
from pathlib import Path
import re
import stat
import tomllib


PACKAGES = {"google-adk", "httpx", "tenacity", "google-genai"}
EXCLUDED = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
            "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
            "dist", "build", "site-packages", "vendor", ".aws", ".ssh", ".config"}
LOCKS = {"uv.lock", "poetry.lock", "Pipfile.lock", "pdm.lock", "requirements.lock"}
VERSION = re.compile(r"(?:===|==|!=|~=|>=|<=|>|<|\^|~)?\d+(?:\.(?:\d+|\*))*"
                     r"(?:,(?:===|==|!=|~=|>=|<=|>|<|\^|~)?\d+(?:\.(?:\d+|\*))*)*")
REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]*\])?(.*)$")


def positive(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def sensitive(name):
    lower = name.lower()
    return (lower.startswith((".env", "secret", "credential"))
            or lower in {".netrc", ".npmrc", ".pypirc", "token.json", "tokens.json"})


def eligible(name):
    return (name.endswith(".py") or name in {"pyproject.toml", ".python-version"}
            or (name.lower().startswith("requirements") and name.endswith((".txt", ".in"))))


class Signals(ast.NodeVisitor):
    def __init__(self):
        self.aliases = {}
        self.rows = set()
        self.in_async = False
        self.in_retry = False

    def name(self, node):
        if isinstance(node, ast.Name):
            return self.aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            return self.name(node.value) + "." + node.attr
        if isinstance(node, ast.Call):
            return self.name(node.func)
        return ""

    def add(self, node, label):
        self.rows.add((node.lineno, label))

    def visit_Import(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name.split(".")[0]] = (
                item.name if item.asname else item.name.split(".")[0])

    def visit_ImportFrom(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name] = f"{node.module or ''}.{item.name}"

    def visit_FunctionDef(self, node):
        previous = self.in_async, self.in_retry
        self.in_async = isinstance(node, ast.AsyncFunctionDef)
        self.in_retry = any(self.name(d).endswith(".safe_api_call") or self.name(d) in {
            "retry", "tenacity.retry", "safe_api_call", "backoff.on_exception",
            "backoff.on_predicate"} for d in node.decorator_list)
        if self.in_retry:
            self.add(node, "retry_decorator")
        for child in node.body:
            self.visit(child)
        self.in_async, self.in_retry = previous

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node):
        name = self.name(node.func)
        labels = {
            "asyncio.timeout": "cooperative_deadline", "asyncio.timeout_at": "cooperative_deadline",
            "asyncio.wait_for": "cooperative_deadline", "anyio.fail_after": "cooperative_deadline",
            "anyio.move_on_after": "cooperative_deadline", "httpx.AsyncClient": "httpx_async_client",
            "httpx.Client": "httpx_sync_client", "httpx.Timeout": "httpx_transport_timeout",
            "tenacity.AsyncRetrying": "retry_loop", "tenacity.Retrying": "retry_loop"}
        if name in labels:
            self.add(node, labels[name])
        if name.endswith(".expired"):
            self.add(node, "deadline_expiry_check")
        if name in {"FunctionTool", "google.adk.tools.FunctionTool",
                    "google.adk.tools.function_tool.FunctionTool"}:
            option = next((k.value for k in node.keywords if k.arg == "require_confirmation"), None)
            label = "confirmation_not_configured"
            if option is not None:
                label = "confirmation_dynamic"
                if isinstance(option, ast.Constant) and isinstance(option.value, bool):
                    label = "confirmation_required" if option.value else "confirmation_disabled"
            self.add(node, label)
        if self.in_retry and name in {"uuid.uuid1", "uuid.uuid4", "uuid.uuid7"}:
            self.add(node, "uuid_inside_retry_function")
        if self.in_async and (name in {"time.sleep", "open", "builtins.open", "urllib.request.urlopen"}
                              or name.startswith("requests.")
                              or name in {f"httpx.{verb}" for verb in ("get", "post", "put", "patch", "delete", "request", "stream", "head", "options")}
                              or name.startswith("subprocess.")
                              or name in {f"pathlib.Path.{method}" for method in ("read_text", "read_bytes", "write_text", "write_bytes", "open")}):
            self.add(node, "blocking_call_in_async")
        self.generic_visit(node)


class Inventory:
    def __init__(self, args):
        self.args = args
        self.result = {"schema_version": 1, "read_only": True, "changes_made": False,
                       "dry_run": args.dry_run, "partial": False, "files_inspected": 0,
                       "directory_entries_seen": 0,
                       "limits": {"max_files": args.max_files, "max_bytes_per_file": args.max_bytes,
                                  "max_depth": args.max_depth, "max_entries": args.max_entries,
                                  "excluded_directories": sorted(EXCLUDED),
                                  "sensitive_files_excluded": True, "symlinks_followed": False},
                       "dependencies": [], "lockfiles": [], "signals": [], "issues": []}
        self.seen = 0
        self.stopped = False

    def issue(self, path, reason):
        self.result["partial"] = True
        self.result["issues"].append({"path": path, "reason": reason})

    def dependency(self, path, name, value):
        name = name.lower().replace("_", "-")
        if name not in PACKAGES | {"python"}:
            return
        if isinstance(value, dict):
            value = None if any(k in value for k in ("git", "url", "path")) else value.get("version")
        constraint = re.sub(r"\s+", "", value) if isinstance(value, str) else ""
        valid = bool(VERSION.fullmatch(constraint))
        self.result["dependencies"].append({"path": path, "name": name,
                                            "constraint": constraint if valid else None,
                                            "status": "parsed" if valid else "redacted"})

    def requirement(self, path, line):
        match = REQUIREMENT.match(line.split("#", 1)[0].strip())
        if match:
            name, value = match.groups()
            self.dependency(path, name, value.split(";", 1)[0].strip())

    def requirements(self, path, values):
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            raise ValueError("invalid dependency array")
        for value in values:
            self.requirement(path, value)

    def inspect(self, path, relative):
        try:
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
            with os.fdopen(fd, "rb") as source:
                metadata = os.fstat(source.fileno())
                if not stat.S_ISREG(metadata.st_mode):
                    self.issue(relative, "not_regular_file")
                    return
                if metadata.st_size > self.args.max_bytes:
                    self.issue(relative, "file_size_limit")
                    return
                raw = source.read(self.args.max_bytes + 1)
            if len(raw) > self.args.max_bytes:
                self.issue(relative, "file_size_limit")
                return
            content = raw.decode("utf-8-sig")
            if path.name == "pyproject.toml":
                document = tomllib.loads(content)
                project = document.get("project", {})
                if "requires-python" in project:
                    self.dependency(relative, "python", project["requires-python"])
                self.requirements(relative, project.get("dependencies", []))
                for values in project.get("optional-dependencies", {}).values():
                    self.requirements(relative, values)
                poetry = document.get("tool", {}).get("poetry", {})
                groups = [poetry] + list(poetry.get("group", {}).values())
                for group in groups:
                    for name, value in group.get("dependencies", {}).items():
                        self.dependency(relative, name, value)
            elif path.name == ".python-version":
                for line in content.splitlines():
                    if line.strip() and not line.lstrip().startswith("#"):
                        self.dependency(relative, "python", line.strip())
            elif path.suffix == ".py":
                visitor = Signals()
                visitor.visit(ast.parse(content))
                self.result["signals"].extend({"path": relative, "line": line, "signal": label}
                                              for line, label in sorted(visitor.rows))
            else:
                for line in content.splitlines():
                    self.requirement(relative, line)
            self.result["files_inspected"] += 1
        except (OSError, UnicodeError):
            self.issue(relative, "unreadable_file")
        except (SyntaxError, ValueError, TypeError, AttributeError, RecursionError):
            self.issue(relative, "malformed_file")

    def walk(self, directory, prefix="", depth=0):
        try:
            entries = []
            with os.scandir(directory) as listing:
                for entry in listing:
                    self.result["directory_entries_seen"] += 1
                    if self.result["directory_entries_seen"] >= self.args.max_entries:
                        self.issue(prefix or ".", "entry_count_limit")
                        self.stopped = True
                        return
                    entries.append(Path(entry.path))
            entries.sort(key=lambda path: path.name)
        except OSError:
            self.issue(prefix or ".", "unreadable_directory")
            return
        for path in entries:
            if sensitive(path.name) or path.name in EXCLUDED:
                continue
            relative = f"{prefix}/{path.name}" if prefix else path.name
            if path.is_symlink():
                self.issue(relative, "symlink_skipped")
                continue
            if path.is_dir():
                if depth >= self.args.max_depth:
                    self.issue(relative, "depth_limit")
                else:
                    self.walk(path, relative, depth + 1)
                    if self.stopped:
                        return
            elif eligible(path.name) or path.name in LOCKS:
                if self.seen >= self.args.max_files:
                    self.issue(relative, "file_count_limit")
                    self.stopped = True
                    return
                self.seen += 1
                if path.name in LOCKS:
                    self.result["lockfiles"].append(relative)
                else:
                    self.inspect(path, relative)


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="Reads only bounded source/manifests; skips secrets, dependency directories and symlinks. Signals are not a safety verdict.")
    parser.add_argument("--project", required=True, help="project directory to inspect without executing code")
    parser.add_argument("--dry-run", action="store_true", help="perform the same read-only scan and report no changes")
    parser.add_argument("--max-files", type=positive, default=500, help="maximum eligible files, including lock names (default: 500)")
    parser.add_argument("--max-entries", type=positive, default=10000, help="stop at this total directory-entry count, including exclusions; reaching the cap is conservatively partial (default: 10000)")
    parser.add_argument("--max-bytes", type=positive, default=262144, help="maximum bytes read per source file (default: 262144)")
    parser.add_argument("--max-depth", type=positive, default=8, help="maximum subdirectory depth (default: 8)")
    args = parser.parse_args()
    root = Path(args.project)
    try:
        if root.is_symlink() or not root.is_dir():
            parser.error("project must be an accessible directory, not a symlink")
        with os.scandir(root):
            pass
    except OSError:
        parser.error("project must be an accessible directory, not a symlink")
    inventory = Inventory(args)
    inventory.walk(root)
    for field in ("dependencies", "signals", "issues"):
        inventory.result[field].sort(key=lambda item: json.dumps(item, sort_keys=True))
    inventory.result["lockfiles"].sort()
    print(json.dumps(inventory.result, indent=2, sort_keys=True))
    return 1 if inventory.result["partial"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
