#!/usr/bin/env python3
"""Bounded audit of model strings and generation settings in an ADK project. Never imports or executes the inspected project."""

import argparse
import ast
import json
import os
from pathlib import Path
import re
import stat
try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import sys as _sys
    _sys.stderr.write("This helper needs Python 3.11 or later (it reads TOML with tomllib). "
                      "Run it with any available 3.11+ interpreter; the project itself can stay on its own version.\n")
    raise SystemExit(2)
PACKAGES = {"google-adk", "google-genai", "litellm"}
EXCLUDED = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "__pycache__",
            ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", "dist", "build",
            "site-packages", "vendor", ".aws", ".ssh", ".config"}
VERSION = re.compile(r"(?:===|==|!=|~=|>=|<=|>|<|\^|~)?\d+(?:\.(?:\d+|\*))*"
                     r"(?:,(?:===|==|!=|~=|>=|<=|>|<|\^|~)?\d+(?:\.(?:\d+|\*))*)*")
REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]*\])?(.*)$")
GEMINI = re.compile(r"gemini-(\d+)(?:\.(\d+))?[A-Za-z0-9.-]*")
LATEST_ALIAS = re.compile(r"gemini-[A-Za-z0-9.-]*-latest\b")
REJECTED_IN_CONFIG = {"tools": "LlmAgent.tools", "system_instruction": "LlmAgent.instruction",
                      "response_schema": "LlmAgent.output_schema"}
BACKEND_ENV = {"GOOGLE_GENAI_USE_VERTEXAI", "GOOGLE_GENAI_USE_ENTERPRISE"}
DEPRECATED_ENV = {"GOOGLE_GENAI_USE_VERTEXAI": "GOOGLE_GENAI_USE_ENTERPRISE"}
DEFAULT_TABLE = Path(__file__).resolve().parents[1] / "assets" / "model-lifecycle-2026-10-01.json"


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
    return (name.endswith(".py") or name == "pyproject.toml"
            or (name.lower().startswith("requirements") and name.endswith((".txt", ".in"))))


def model_name(text):
    """Return the bare Gemini model id inside a literal, or None."""
    if not isinstance(text, str):
        return None
    match = GEMINI.search(text)
    return match.group(0) if match else None


def generation(text):
    match = GEMINI.search(text or "")
    if not match:
        return None
    major, minor = match.group(1), match.group(2)
    if major == "3":
        return "3.x"
    if major == "2" and minor == "5":
        return "2.5"
    return f"{major}.{minor}" if minor else major


class Signals(ast.NodeVisitor):
    def __init__(self, table):
        self.table = table
        self.rows = set()
        self.aliases = {}
        self.bindings = {}

    def add(self, node, label, detail=None):
        self.rows.add((node.lineno, label, detail))

    def name(self, node):
        if isinstance(node, ast.Name):
            return self.aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            return self.name(node.value) + "." + node.attr
        if isinstance(node, ast.Call):
            return self.name(node.func)
        return ""

    def visit_Import(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name.split(".")[0]] = (
                item.name if item.asname else item.name.split(".")[0])

    def visit_ImportFrom(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name] = f"{node.module or ''}.{item.name}"

    def visit_Assign(self, node):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            self.bindings[node.targets[0].id] = node.value
        self.generic_visit(node)

    def deref(self, node):
        if isinstance(node, ast.Name) and node.id in self.bindings:
            return self.bindings[node.id]
        return node

    def constant(self, node):
        node = self.deref(node)
        return node.value if isinstance(node, ast.Constant) else None

    def keywords(self, call):
        return {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg}

    def visit_Constant(self, node):
        name = model_name(node.value) if isinstance(node.value, str) else None
        if name:
            self.add(node, "model_string", name)
            self.lifecycle(node, name)
        if isinstance(node.value, str) and LATEST_ALIAS.search(node.value):
            self.add(node, "model_alias_latest", LATEST_ALIAS.search(node.value).group(0))
        if isinstance(node.value, str) and node.value in BACKEND_ENV:
            self.add(node, "backend_variant_env_reference", node.value)
            if node.value in DEPRECATED_ENV:
                self.add(node, "deprecated_backend_env_name", f"{node.value} -> {DEPRECATED_ENV[node.value]}")
        self.generic_visit(node)

    def lifecycle(self, node, name):
        entry = self.table.get(name)
        if entry is None:
            self.add(node, "model_not_in_lifecycle_table", name)
            return
        self.add(node, f"model_{entry.get('status', 'unknown')}", name)

    def model_of(self, kwargs):
        """Return (literal, generation) for a call's model argument when statically known."""
        value = kwargs.get("model")
        if value is None:
            return None, None
        literal = self.constant(value)
        if literal is None:
            inner = self.deref(value)
            if isinstance(inner, ast.Call):
                literal = self.constant(self.keywords(inner).get("model"))
        return literal, generation(literal) if isinstance(literal, str) else None

    def thinking(self, node, config_call, gen, origin):
        kwargs = self.keywords(config_call)
        if "thinking_level" in kwargs and "thinking_budget" in kwargs:
            self.add(node, "thinking_level_and_budget_both_set", origin)
        if "thinking_budget" in kwargs and gen == "3.x":
            self.add(node, "thinking_budget_on_gemini_3", origin)
        if "thinking_level" in kwargs and gen == "2.5":
            self.add(node, "thinking_level_on_gemini_2_5", origin)

    def visit_Call(self, node):
        callee = self.name(node.func)
        kwargs = self.keywords(node)
        if callee.endswith("LiteLlm"):
            literal = self.constant(kwargs.get("model"))
            self.add(node, "litellm_model", literal if isinstance(literal, str) else None)
        if callee.endswith("Gemini") and "client_kwargs" in kwargs:
            client_kwargs = self.deref(kwargs["client_kwargs"])
            keys = sorted(k.value for k in client_kwargs.keys if isinstance(k, ast.Constant)) if isinstance(client_kwargs, ast.Dict) else None
            self.add(node, "gemini_client_kwargs", ",".join(keys) if keys else None)
        if callee.endswith("FallbackModel"):
            models = self.deref(kwargs.get("models")) if "models" in kwargs else None
            count = len(models.elts) if isinstance(models, (ast.List, ast.Tuple)) else None
            self.add(node, "fallback_model", count)
        if "model" in kwargs and not callee.endswith(("LiteLlm", "FallbackModel", "Gemini")):
            literal, _ = self.model_of(kwargs)
            self.add(node, "model_kwarg", literal if isinstance(literal, str) and model_name(literal) else
                     ("dynamic" if literal is None else "non_gemini"))
        _, gen = self.model_of(kwargs)
        planner = self.deref(kwargs.get("planner")) if "planner" in kwargs else None
        planner_call = planner if isinstance(planner, ast.Call) and self.name(planner.func).endswith("BuiltInPlanner") else None
        if planner_call is not None:
            thinking = self.deref(self.keywords(planner_call).get("thinking_config"))
            if isinstance(thinking, ast.Call):
                self.thinking(node, thinking, gen, "planner")
        config = self.deref(kwargs.get("generate_content_config")) if "generate_content_config" in kwargs else None
        if isinstance(config, ast.Call):
            fields = self.keywords(config)
            for field, owner in REJECTED_IN_CONFIG.items():
                if field in fields:
                    self.add(node, "generate_content_config_rejected_field", f"{field} -> {owner}")
            temperature = self.constant(fields.get("temperature"))
            if isinstance(temperature, (int, float)) and not isinstance(temperature, bool) and temperature < 1.0:
                self.add(node, "temperature_below_default_on_gemini_3" if gen == "3.x" else "temperature_below_default", temperature)
            thinking = self.deref(fields.get("thinking_config"))
            if thinking is not None:
                if planner_call is not None:
                    self.add(node, "thinking_config_planner_precedence")
                if isinstance(thinking, ast.Call):
                    self.thinking(node, thinking, gen, "generate_content_config")
        if "output_schema" in kwargs:
            tools = self.deref(kwargs.get("tools")) if "tools" in kwargs else None
            has_tools = tools is not None and not (isinstance(tools, (ast.List, ast.Tuple)) and not tools.elts)
            if has_tools:
                self.add(node, "schema_with_tools_path_depends_on_backend")
            if "output_key" not in kwargs:
                self.add(node, "output_schema_without_output_key")
            if self.constant(kwargs.get("mode")) == "task":
                self.add(node, "task_mode_skips_output_schema")
        self.generic_visit(node)


class Audit:
    def __init__(self, args, table):
        self.args = args
        self.table = table.get("models", {})
        self.result = {"schema_version": 1, "read_only": True, "changes_made": False,
                       "dry_run": args.dry_run, "partial": False, "files_inspected": 0,
                       "directory_entries_seen": 0,
                       "lifecycle_table": {"captured": table.get("captured"), "note": table.get("note"),
                                           "models_listed": len(self.table)},
                       "limits": {"max_files": args.max_files, "max_bytes_per_file": args.max_bytes,
                                  "max_depth": args.max_depth, "max_entries": args.max_entries,
                                  "excluded_directories": sorted(EXCLUDED),
                                  "sensitive_files_excluded": True, "symlinks_followed": False},
                       "dependencies": [], "signals": [], "issues": []}
        self.seen = 0
        self.stopped = False

    def issue(self, path, reason):
        self.result["partial"] = True
        self.result["issues"].append({"path": path, "reason": reason})

    def dependency(self, path, name, value):
        name = name.lower().replace("_", "-")
        if name not in PACKAGES:
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

    def inspect(self, path, relative):
        try:
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
            with os.fdopen(fd, "rb") as source:
                if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                    self.issue(relative, "not_regular_file")
                    return
                raw = source.read(self.args.max_bytes + 1)
            if len(raw) > self.args.max_bytes:
                self.issue(relative, "file_size_limit")
                return
            content = raw.decode("utf-8")
            if path.name == "pyproject.toml":
                document = tomllib.loads(content)
                project = document.get("project", {})
                values = project.get("dependencies", [])
                for group in project.get("optional-dependencies", {}).values():
                    values = values + list(group)
                if any(not isinstance(v, str) for v in values):
                    raise ValueError("invalid dependency array")
                for value in values:
                    self.requirement(relative, value)
                poetry = document.get("tool", {}).get("poetry", {})
                for group in [poetry] + list(poetry.get("group", {}).values()):
                    for name, value in group.get("dependencies", {}).items():
                        self.dependency(relative, name, value)
            elif path.suffix == ".py":
                visitor = Signals(self.table)
                visitor.visit(ast.parse(content))
                for line, label, detail in sorted(visitor.rows, key=lambda row: (row[0], row[1], str(row[2]))):
                    row = {"path": relative, "line": line, "signal": label}
                    if detail is not None:
                        row["detail"] = detail
                    self.result["signals"].append(row)
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
            elif eligible(path.name):
                if self.seen >= self.args.max_files:
                    self.issue(relative, "file_count_limit")
                    self.stopped = True
                    return
                self.seen += 1
                self.inspect(path, relative)


def load_table(path, parser):
    try:
        if path.is_symlink():
            parser.error("lifecycle table must be a regular file, not a symlink")
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        parser.error("lifecycle table is missing or not valid JSON")
    if not isinstance(document, dict) or not isinstance(document.get("models"), dict):
        parser.error("lifecycle table must be an object with a models mapping")
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="Reads bounded source and manifests; skips secrets, dependency directories and symlinks. Signals direct inspection and are not a verdict on provider behaviour. The lifecycle table is a dated snapshot that the user must refresh.")
    parser.add_argument("--project", required=True, help="project directory to inspect without executing code")
    parser.add_argument("--dry-run", action="store_true", help="perform the same read-only scan and report no changes")
    parser.add_argument("--lifecycle", type=Path, default=DEFAULT_TABLE, help="model lifecycle JSON table (default: bundled dated snapshot)")
    parser.add_argument("--max-files", type=positive, default=500, help="maximum eligible files (default: 500)")
    parser.add_argument("--max-entries", type=positive, default=10000, help="stop at this total directory-entry count; reaching the cap is conservatively partial (default: 10000)")
    parser.add_argument("--max-bytes", type=positive, default=262144, help="maximum bytes read per file (default: 262144)")
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
    audit = Audit(args, load_table(args.lifecycle, parser))
    audit.walk(root)
    for field in ("dependencies", "signals", "issues"):
        audit.result[field].sort(key=lambda item: json.dumps(item, sort_keys=True))
    print(json.dumps(audit.result, indent=2, sort_keys=True))
    return 1 if audit.result["partial"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
