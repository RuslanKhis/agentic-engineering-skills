#!/usr/bin/env python3
"""Bounded, read-only inventory of an ADK agent's security surface.

Scans Python source with `ast` for `LlmAgent`/`Agent` and workflow agent
constructions, the tools they carry (FunctionTool, AgentTool, McpToolset,
OpenAPIToolset, built-ins), code executors, bash policies, callbacks, plugins,
remote A2A sub-agents and custom BaseTool subclasses. Reads dependency
manifests for the google-adk pin and shell/YAML deploy files for
unauthenticated-exposure hints. Classifies each tool as a private-data source,
an untrusted-content source or an egress path by name, parameter and call
heuristics, then reports a per-agent "lethal trifecta" summary. Never imports
or executes the inspected project. Findings are review prompts for a human
threat model, not a security verdict.
"""

import argparse
import ast
import itertools
import json
import os
from pathlib import Path
import re
import stat
import tomllib


EXCLUDED = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
            "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
            "dist", "build", "site-packages", "vendor", ".aws", ".ssh", ".config"}
LLM_AGENT_CLASSES = {"LlmAgent", "Agent"}
WORKFLOW_AGENT_CLASSES = {"SequentialAgent", "ParallelAgent", "LoopAgent"}
AGENT_CLASSES = LLM_AGENT_CLASSES | WORKFLOW_AGENT_CLASSES
REMOTE_AGENT_CLASSES = {"RemoteA2aAgent"}
TOOL_WRAPPERS = {"FunctionTool", "LongRunningFunctionTool"}
AGENT_WRAPPERS = {"AgentTool"}
MCP_CLASSES = {"McpToolset", "MCPToolset"}
OPENAPI_CLASSES = {"OpenAPIToolset"}
RUNNER_CLASSES = {"App", "Runner", "InMemoryRunner"}
STDIO_PARAMS = {"StdioServerParameters", "StdioConnectionParams"}
UNSAFE_EXECUTORS = {"UnsafeLocalCodeExecutor"}
CONTAINER_EXECUTORS = {"ContainerCodeExecutor"}
BASH_TOOL_CLASSES = {"BashTool"}
BASH_POLICY_CLASSES = {"BashToolPolicy"}
CALLBACK_KEYWORDS = ("before_agent_callback", "after_agent_callback", "before_model_callback",
                     "after_model_callback", "before_tool_callback", "after_tool_callback",
                     "on_model_error_callback", "on_tool_error_callback")
CONTEXT_NAMES = {"tool_context", "self", "cls"}
CONTEXT_TYPES = {"ToolContext", "ReadonlyContext", "CallbackContext", "InvocationContext"}
IDENTITY_NAMES = {"user_id", "tenant_id", "email", "user_email", "customer_id", "account_id",
                  "org_id", "organization_id", "principal", "username", "api_key", "token",
                  "access_token", "credential", "password", "role", "is_admin"}
WRITE_VERBS = {"create", "update", "delete", "send", "post", "pay", "refund", "execute",
               "transfer", "remove", "write", "publish", "approve", "cancel", "purchase",
               "charge", "submit", "upload", "modify", "patch", "grant", "revoke", "deploy",
               "drop", "insert", "email", "notify", "share", "forward", "schedule", "book"}
EGRESS_VERBS = {"send", "post", "email", "upload", "publish", "notify", "share", "forward",
                "webhook", "fetch", "download", "browse", "http", "request", "crawl", "scrape",
                "visit", "open", "get", "call", "message"}
EGRESS_PARAMS = {"url", "uri", "urls", "link", "links", "endpoint", "webhook", "webhook_url",
                 "to", "recipient", "recipients", "to_email", "to_address", "destination",
                 "callback_url", "address"}
NETWORK_PREFIXES = ("requests.", "httpx.", "urllib.", "aiohttp.", "http.client.", "smtplib.",
                    "websockets.", "socket.", "ftplib.", "paramiko.", "pycurl.")
UNTRUSTED_TOKENS = {"search", "retrieve", "retrieval", "rag", "fetch", "inbox", "scrape", "browse",
                    "crawl", "memory", "recall", "download", "web", "document", "documents", "page",
                    "pages", "ticket", "tickets", "review", "reviews", "feedback", "comment",
                    "comments", "message", "messages", "news", "feed", "read", "load", "chunk",
                    "chunks", "knowledge", "corpus", "wiki", "notes"}
PRIVATE_TOKENS = {"customer", "customers", "account", "accounts", "order", "orders", "invoice",
                  "invoices", "payment", "payments", "record", "records", "profile", "profiles",
                  "secret", "secrets", "credential", "credentials", "salary", "patient", "patients",
                  "user", "users", "employee", "employees", "contact", "contacts", "calendar",
                  "drive", "mail", "inbox", "email", "emails", "database", "db", "sql", "query",
                  "bigquery", "crm", "hr", "ticket", "tickets", "memory", "session", "history",
                  "file", "files", "document", "documents", "notes", "vault", "key", "keys",
                  "token", "tokens", "balance", "transactions", "transaction", "internal",
                  "private", "confidential"}
BUILTIN_TOOLS = {
    "google_search": {"untrusted"}, "GoogleSearchTool": {"untrusted"},
    "enterprise_web_search": {"untrusted"}, "EnterpriseWebSearchTool": {"untrusted"},
    "url_context": {"untrusted", "egress"}, "UrlContextTool": {"untrusted", "egress"},
    "built_in_code_execution": {"code_execution"}, "BuiltInCodeExecutor": {"code_execution"},
    "load_memory": {"private", "untrusted"}, "LoadMemoryTool": {"private", "untrusted"},
    "preload_memory": {"private", "untrusted"}, "PreloadMemoryTool": {"private", "untrusted"},
    "load_artifacts": {"private"}, "LoadArtifactsTool": {"private"},
    "VertexAiRagRetrieval": {"private", "untrusted"}, "VertexAiSearchTool": {"private", "untrusted"},
    "FilesRetrieval": {"private", "untrusted"}, "LlamaIndexRetrieval": {"private", "untrusted"},
    "transfer_to_agent": set(), "exit_loop": set(), "get_user_choice": set(),
}
PRIVATE_TOOLSET_TOKENS = {"bigquery", "spanner", "bigtable", "firestore", "postgres", "sql",
                          "database", "alloydb", "mysql", "sqlite", "redis", "memory"}
CVE_FLOOR = (2, 7, 0)
MANIFESTS = {"pyproject.toml"}
TEXT_FILES = {".sh", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".txt"}
TEXT_NAMES = {"Dockerfile", "Makefile", "Procfile", "Justfile"}
UNAUTH_PATTERN = re.compile(r"allow[-_]unauthenticated", re.IGNORECASE)
NO_UNAUTH_PATTERN = re.compile(r"no[-_]allow[-_]unauthenticated", re.IGNORECASE)
REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]*\])?(.*)$")
FIRST_VERSION = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")


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
    lower = name.lower()
    return (name.endswith(".py") or name in MANIFESTS or name in TEXT_NAMES
            or lower.startswith("requirements") and name.endswith((".txt", ".in"))
            or Path(name).suffix in TEXT_FILES)


def call_name(node):
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def dotted(node, aliases):
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        prefix = dotted(node.value, aliases)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def keyword(node, name):
    return next((k.value for k in node.keywords if k.arg == name), None)


def constant_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def annotation_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.split(".")[-1]
    if isinstance(node, ast.Subscript):
        return annotation_name(node.value)
    return ""


def tokens(name):
    return {part for part in (name or "").lower().replace("-", "_").split("_") if part}


def confirmation_mode(node):
    """Classify a require_confirmation keyword: absent, enabled, disabled or dynamic."""
    option = keyword(node, "require_confirmation")
    if option is None:
        return "absent"
    if isinstance(option, ast.Constant) and isinstance(option.value, bool):
        return "enabled" if option.value else "disabled"
    return "dynamic"


def is_true(node):
    return isinstance(node, ast.Constant) and node.value is True


def names_in(node):
    for child in ast.walk(node):
        if isinstance(child, ast.Attribute):
            yield child.attr
        elif isinstance(child, ast.Name):
            yield child.id
        elif isinstance(child, ast.keyword) and child.arg:
            yield child.arg


class FunctionFacts:
    """Syntactic facts about one candidate tool function."""

    def __init__(self, path, node, aliases):
        self.path = path
        self.node = node
        self.name = node.name
        self.line = node.lineno
        self.aliases = aliases
        args = node.args
        self.params = list(itertools.chain(args.posonlyargs, args.args, args.kwonlyargs))

    def visible_params(self):
        for param in self.params:
            if param.arg in CONTEXT_NAMES:
                continue
            if param.annotation is not None and annotation_name(param.annotation) in CONTEXT_TYPES:
                continue
            yield param.arg

    def body_nodes(self):
        stack = list(self.node.body)
        while stack:
            node = stack.pop()
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue
            yield node
            stack.extend(ast.iter_child_nodes(node))

    def network_calls(self):
        for node in self.body_nodes():
            if isinstance(node, ast.Call):
                name = dotted(node.func, self.aliases)
                if name.startswith(NETWORK_PREFIXES) or name in {"urlopen", "urllib.request.urlopen"}:
                    yield name

    def classify(self):
        """Return (flags, details) for private/untrusted/egress/write/identity."""
        flags, details = set(), {}
        name_tokens = tokens(self.name)
        params = set(self.visible_params())
        identity = sorted(params & IDENTITY_NAMES)
        if identity:
            flags.add("identity")
            details["identity_parameters"] = identity
        network = sorted(set(self.network_calls()))
        egress_params = sorted(params & EGRESS_PARAMS)
        egress_verbs = sorted(name_tokens & EGRESS_VERBS)
        if network or egress_params or egress_verbs:
            flags.add("egress")
            details["egress_evidence"] = {"network_calls": network, "parameters": egress_params,
                                          "name_tokens": egress_verbs}
        write_verbs = sorted(name_tokens & WRITE_VERBS)
        if write_verbs:
            flags.add("write")
            details["write_tokens"] = write_verbs
        untrusted = sorted(name_tokens & UNTRUSTED_TOKENS)
        if untrusted or (network and not write_verbs):
            flags.add("untrusted")
            details["untrusted_tokens"] = untrusted
        private = sorted(name_tokens & PRIVATE_TOKENS)
        if private and not write_verbs:
            flags.add("private")
            details["private_tokens"] = private
        return flags, details


class Collector(ast.NodeVisitor):
    """Collect function definitions, agents, toolsets, tool wrappers and runners per file."""

    def __init__(self, path):
        self.path = path
        self.aliases = {}
        self.functions = []
        self.agents = []
        self.agent_vars = {}
        self.toolset_vars = {}
        self.wrapper_vars = {}
        self.executor_vars = {}
        self.param_vars = {}
        self.remote_vars = {}
        self.plugins = []
        self.observations = []
        self.class_depth = 0

    def observe(self, line, subject, kind, detail):
        self.observations.append((line, subject, kind, detail))

    def visit_Import(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name.split(".")[0]] = (
                item.name if item.asname else item.name.split(".")[0])

    def visit_ImportFrom(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name] = f"{node.module or ''}.{item.name}"

    def visit_ClassDef(self, node):
        bases = {annotation_name(b) for b in node.bases}
        if "BaseTool" in bases:
            mentioned = set(names_in(node))
            if "require_confirmation" in mentioned and "confirmed" not in mentioned:
                self.observe(node.lineno, node.name, "custom_tool_ignores_confirmation",
                             "BaseTool subclass sets require_confirmation but never reads tool_confirmation.confirmed; "
                             "only FunctionTool enforces the verdict in the pinned source")
        self.class_depth += 1
        self.generic_visit(node)
        self.class_depth -= 1

    def visit_FunctionDef(self, node):
        if self.class_depth == 0:
            self.functions.append(node)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Assign(self, node):
        value = node.value
        if isinstance(value, ast.Call):
            name = call_name(value)
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if name in AGENT_CLASSES:
                    self.agent_vars[target.id] = value
                elif name in REMOTE_AGENT_CLASSES:
                    self.remote_vars[target.id] = value
                elif name in MCP_CLASSES | OPENAPI_CLASSES or name.endswith("Toolset"):
                    self.toolset_vars[target.id] = value
                elif name in TOOL_WRAPPERS | AGENT_WRAPPERS:
                    self.wrapper_vars[target.id] = value
                elif name.endswith("CodeExecutor"):
                    self.executor_vars[target.id] = name
                elif name in STDIO_PARAMS or name.endswith("ConnectionParams"):
                    self.param_vars[target.id] = name
        self.generic_visit(node)

    def visit_Call(self, node):
        name = call_name(node)
        if name in AGENT_CLASSES:
            self.agents.append(self.agent_entry(node, name))
        elif name in RUNNER_CLASSES:
            plugins = keyword(node, "plugins")
            if isinstance(plugins, (ast.List, ast.Tuple)):
                for element in plugins.elts:
                    label = call_name(element) if isinstance(element, ast.Call) else (
                        element.id if isinstance(element, ast.Name) else "<dynamic>")
                    self.plugins.append({"name": label, "path": self.path, "line": node.lineno,
                                         "runner": name})
            elif plugins is not None:
                self.plugins.append({"name": "<dynamic>", "path": self.path, "line": node.lineno,
                                     "runner": name})
        elif name in BASH_POLICY_CLASSES:
            prefixes = keyword(node, "allowed_command_prefixes")
            if prefixes is None:
                self.observe(node.lineno, name, "bash_policy_allow_all",
                             "allowed_command_prefixes defaults to ('*',); list the permitted command prefixes")
            elif isinstance(prefixes, (ast.List, ast.Tuple)) and any(constant_str(e) == "*" for e in prefixes.elts):
                self.observe(node.lineno, name, "bash_policy_allow_all",
                             "allowed_command_prefixes contains '*', which allows every command")
        elif name in BASH_TOOL_CLASSES and keyword(node, "policy") is None:
            self.observe(node.lineno, name, "bash_policy_allow_all",
                         "BashTool without an explicit policy uses the allow-all default")
        elif name in CONTAINER_EXECUTORS and is_true(keyword(node, "network_enabled")):
            self.observe(node.lineno, name, "container_executor_network_enabled",
                         "network_enabled=True lets model-generated code reach the network, including the metadata endpoint")
        if any(k.arg == "allow_unauthenticated" and is_true(k.value) for k in node.keywords):
            self.observe(node.lineno, name or "<call>", "unauthenticated_exposure_hint",
                         "allow_unauthenticated=True in a Python deploy call")
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and UNAUTH_PATTERN.search(node.value) and not NO_UNAUTH_PATTERN.search(node.value):
            self.observe(node.lineno, "<string>", "unauthenticated_exposure_hint",
                         "string mentions allow-unauthenticated; confirm the served endpoint requires authentication")

    def executor_name(self, node):
        if isinstance(node, ast.Call):
            return call_name(node)
        if isinstance(node, ast.Name):
            return self.executor_vars.get(node.id, node.id)
        return None

    def agent_entry(self, node, kind):
        entry = {"name": constant_str(keyword(node, "name")), "class": kind, "path": self.path,
                 "line": node.lineno, "tool_elements": [], "tools_literal": True,
                 "sub_agent_vars": [], "remote_sub_agents": [],
                 "include_contents": constant_str(keyword(node, "include_contents")),
                 "mode": constant_str(keyword(node, "mode")),
                 "code_executor": None, "callbacks": [], "instruction_present": False}
        executor = keyword(node, "code_executor")
        if executor is not None:
            entry["code_executor"] = self.executor_name(executor) or "<dynamic>"
        for key in CALLBACK_KEYWORDS:
            if keyword(node, key) is not None:
                entry["callbacks"].append(key)
        entry["instruction_present"] = keyword(node, "instruction") is not None
        tools = keyword(node, "tools")
        if isinstance(tools, (ast.List, ast.Tuple)):
            entry["tool_elements"] = list(tools.elts)
        elif tools is not None:
            entry["tools_literal"] = False
        sub_agents = keyword(node, "sub_agents")
        if isinstance(sub_agents, (ast.List, ast.Tuple)):
            for element in sub_agents.elts:
                if isinstance(element, ast.Name):
                    entry["sub_agent_vars"].append(element.id)
                elif isinstance(element, ast.Call) and call_name(element) in REMOTE_AGENT_CLASSES:
                    entry["remote_sub_agents"].append(constant_str(keyword(element, "name")) or call_name(element))
        return entry


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
                       "heuristic": "name, parameter and call-based classification; confirm every row by reading the tool body",
                       "adk_pins": [], "agents": [], "plugins": [], "findings": [], "counts": {}, "issues": []}
        self.seen = 0
        self.stopped = False
        self.collectors = []

    def issue(self, path, reason):
        self.result["partial"] = True
        self.result["issues"].append({"path": path, "reason": reason})

    def finding(self, path, line, subject, kind, detail=""):
        self.result["findings"].append({"path": path, "line": line, "subject": subject,
                                        "finding": kind, "detail": detail})
        self.result["counts"][kind] = self.result["counts"].get(kind, 0) + 1

    # ----- file reading ---------------------------------------------------

    def read(self, path, relative):
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(fd, "rb") as source:
            metadata = os.fstat(source.fileno())
            if not stat.S_ISREG(metadata.st_mode):
                self.issue(relative, "not_regular_file")
                return None
            if metadata.st_size > self.args.max_bytes:
                self.issue(relative, "file_size_limit")
                return None
            raw = source.read(self.args.max_bytes + 1)
        if len(raw) > self.args.max_bytes:
            self.issue(relative, "file_size_limit")
            return None
        return raw.decode("utf-8-sig")

    def inspect(self, path, relative):
        try:
            content = self.read(path, relative)
            if content is None:
                return
            if path.suffix == ".py":
                collector = Collector(relative)
                collector.visit(ast.parse(content))
                self.collectors.append(collector)
            elif path.name == "pyproject.toml":
                document = tomllib.loads(content)
                project = document.get("project", {})
                for value in list(project.get("dependencies", [])) + [
                        v for group in project.get("optional-dependencies", {}).values() for v in group]:
                    if not isinstance(value, str):
                        raise ValueError("invalid dependency array")
                    self.requirement(relative, value)
                poetry = document.get("tool", {}).get("poetry", {})
                for group in [poetry] + list(poetry.get("group", {}).values()):
                    for name, value in group.get("dependencies", {}).items():
                        if isinstance(value, dict):
                            value = value.get("version", "")
                        if isinstance(value, str):
                            self.pin(relative, name, value)
            elif path.name.lower().startswith("requirements"):
                for line in content.splitlines():
                    self.requirement(relative, line)
            else:
                for number, line in enumerate(content.splitlines(), 1):
                    if UNAUTH_PATTERN.search(line) and not NO_UNAUTH_PATTERN.search(line):
                        self.finding(relative, number, path.name, "unauthenticated_exposure_hint",
                                     "deploy file mentions allow-unauthenticated; confirm the served endpoint requires authentication")
            self.result["files_inspected"] += 1
        except (OSError, UnicodeError):
            self.issue(relative, "unreadable_file")
        except (SyntaxError, ValueError, TypeError, AttributeError, RecursionError):
            self.issue(relative, "malformed_file")

    def requirement(self, path, line):
        match = REQUIREMENT.match(line.split("#", 1)[0].strip())
        if match:
            name, value = match.groups()
            self.pin(path, name, value.split(";", 1)[0].strip())

    def pin(self, path, name, constraint):
        if name.lower().replace("_", "-") != "google-adk":
            return
        constraint = re.sub(r"\s+", "", constraint)
        match = FIRST_VERSION.search(constraint)
        version = tuple(int(part or 0) for part in match.groups()) if match else None
        status = "unknown"
        if version is not None:
            status = "below_cve_floor" if version < CVE_FLOOR else "at_or_above_cve_floor"
        self.result["adk_pins"].append({"path": path, "constraint": constraint if match else None,
                                        "lowest_version": ".".join(map(str, version)) if version else None,
                                        "status": status})
        if status == "below_cve_floor":
            self.finding(path, 0, "google-adk", "known_cve_range",
                         f"lowest resolvable version {'.'.join(map(str, version))} is below 2.7.0; adk web RCE and "
                         "forged-confirmation fixes landed in 2.5.0 to 2.7.0 (see compatibility reference)")

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

    # ----- analysis -------------------------------------------------------

    def analyse(self):
        functions, agent_vars, toolset_vars, wrapper_vars, param_vars, remote_vars = {}, {}, {}, {}, {}, {}
        for collector in self.collectors:
            for node in collector.functions:
                functions.setdefault(node.name, FunctionFacts(collector.path, node, collector.aliases))
            for name, call in collector.agent_vars.items():
                agent_vars.setdefault(name, (collector, call))
            for name, call in collector.toolset_vars.items():
                toolset_vars.setdefault(name, (collector, call))
            for name, call in collector.wrapper_vars.items():
                wrapper_vars.setdefault(name, (collector, call))
            param_vars.update(collector.param_vars)
            remote_vars.update(collector.remote_vars)
            self.result["plugins"].extend(collector.plugins)
            for line, subject, kind, detail in collector.observations:
                self.finding(collector.path, line, subject, kind, detail)
        self.functions, self.agent_vars, self.toolset_vars = functions, agent_vars, toolset_vars
        self.wrapper_vars, self.param_vars, self.remote_vars = wrapper_vars, param_vars, remote_vars
        entries = {}
        for collector in self.collectors:
            for raw in collector.agents:
                entry = self.describe_agent(collector, raw)
                entries[id(raw)] = entry
                self.result["agents"].append(entry)
        by_var = {}
        for variable, (collector, call) in agent_vars.items():
            for raw in collector.agents:
                if raw["line"] == call.lineno and raw["path"] == collector.path:
                    by_var[variable] = entries[id(raw)]
        for entry in self.result["agents"]:
            subs = []
            for variable in dict.fromkeys(entry.pop("sub_agent_vars")):
                if variable in remote_vars:
                    entry["remote_sub_agents"].append(constant_str(keyword(remote_vars[variable], "name")) or variable)
                    continue
                target = by_var.get(variable)
                subs.append({"variable": variable, "name": target["name"] if target else None,
                             "include_contents": target["include_contents"] if target else None,
                             "mode": target["mode"] if target else None, "resolved": target is not None})
                if target is None:
                    self.finding(entry["path"], entry["line"], variable, "unresolved_agent_reference",
                                 "sub-agent defined outside the scanned files or built dynamically")
            entry["sub_agents"] = subs
            if entry["remote_sub_agents"]:
                entry["flags"] = sorted(set(entry["flags"]) | {"untrusted", "remote"})
                writes = [t["name"] for t in entry["tools"] if "write" in t.get("flags", [])]
                if writes:
                    self.finding(entry["path"], entry["line"], entry["name"] or "<unnamed agent>",
                                 "remote_content_with_write_tools",
                                 f"remote A2A sub-agent output reaches an agent holding write tools ({', '.join(writes)}); "
                                 "a compromised peer can steer them")
        for entry in self.result["agents"]:
            entry["trifecta"] = self.trifecta(entry, by_var)
        for entry in self.result["agents"]:
            if not entry["trifecta"]["all_three"]:
                continue
            subject = entry["name"] or "<unnamed agent>"
            if entry["class"] in LLM_AGENT_CLASSES:
                self.finding(entry["path"], entry["line"], subject, "trifecta_present",
                             "private data, untrusted content and egress reachable in one agent context (own tools plus sub-agents); "
                             "a successful injection can exfiltrate: split the agent or remove one leg")
            elif not any(by_var.get(s["variable"], {}).get("trifecta", {}).get("all_three") for s in entry["sub_agents"]):
                self.finding(entry["path"], entry["line"], subject, "trifecta_across_workflow",
                             "no single child has all three legs, but the workflow chains them through shared session state; "
                             "check that untrusted content cannot steer a later step's consequential action")
        self.result["findings"].sort(key=lambda item: (item["path"], item["line"], item["finding"], item["subject"], item["detail"]))
        self.result["agents"].sort(key=lambda item: (item["path"], item["line"]))
        self.result["plugins"].sort(key=lambda item: json.dumps(item, sort_keys=True))
        self.result["adk_pins"].sort(key=lambda item: json.dumps(item, sort_keys=True))
        self.result["issues"].sort(key=lambda item: json.dumps(item, sort_keys=True))
        self.result["counts"] = dict(sorted(self.result["counts"].items()))

    def describe_agent(self, collector, raw):
        subject = raw["name"] or "<unnamed agent>"
        entry = {"name": raw["name"], "class": raw["class"], "path": raw["path"], "line": raw["line"],
                 "include_contents": raw["include_contents"], "mode": raw["mode"],
                 "code_executor": raw["code_executor"], "callbacks": raw["callbacks"],
                 "instruction_present": raw["instruction_present"], "tools": [], "toolsets": [],
                 "sub_agent_vars": raw["sub_agent_vars"], "remote_sub_agents": list(raw["remote_sub_agents"]),
                 "tools_literal": raw["tools_literal"], "flags": set()}
        gated_by_callback = "before_tool_callback" in raw["callbacks"]
        if raw["code_executor"] in UNSAFE_EXECUTORS:
            self.finding(raw["path"], raw["line"], subject, "unsafe_code_executor",
                         f"{raw['code_executor']} runs model-generated code in the agent process; use a sandboxed executor")
        if raw["code_executor"]:
            entry["flags"].add("code_execution")
        if not raw["tools_literal"]:
            self.finding(raw["path"], raw["line"], subject, "tools_not_literal",
                         "tools= is not a list literal; inventory the runtime list by hand")
        for element in raw["tool_elements"]:
            self.describe_tool(collector, raw, entry, element, gated_by_callback)
        entry["flags"] = sorted(entry["flags"])
        return entry

    def describe_tool(self, collector, raw, entry, element, gated_by_callback):
        subject = raw["name"] or "<unnamed agent>"
        path, line = raw["path"], getattr(element, "lineno", raw["line"])
        call, variable = None, None
        if isinstance(element, ast.Call):
            call = element
        elif isinstance(element, ast.Name):
            variable = element.id
            if variable in self.toolset_vars:
                call = self.toolset_vars[variable][1]
            elif variable in self.wrapper_vars:
                call = self.wrapper_vars[variable][1]
        if call is not None:
            name = call_name(call)
            if name in TOOL_WRAPPERS:
                target = call.args[0] if call.args else keyword(call, "func")
                function = target.id if isinstance(target, ast.Name) else None
                self.describe_function(entry, path, line, subject, function, name, confirmation_mode(call), gated_by_callback)
                return
            if name in AGENT_WRAPPERS:
                target = call.args[0] if call.args else keyword(call, "agent")
                target_name = target.id if isinstance(target, ast.Name) else None
                entry["tools"].append({"name": target_name, "kind": "agent_tool", "line": line, "flags": []})
                if target_name:
                    entry["sub_agent_vars"].append(target_name)
                return
            if name in MCP_CLASSES:
                self.describe_mcp(entry, path, line, subject, call, gated_by_callback)
                return
            if name in OPENAPI_CLASSES:
                entry["toolsets"].append({"kind": "openapi_toolset", "line": line,
                                          "tool_filter": "absent" if keyword(call, "tool_filter") is None else "present",
                                          "flags": ["egress", "untrusted"]})
                entry["flags"].update({"egress", "untrusted"})
                self.finding(path, line, subject, "egress_capable_tool",
                             "OpenAPIToolset sends model-chosen arguments to an external API; treat as egress, and its "
                             "descriptions and responses as unfenced untrusted text")
                return
            if name in BASH_TOOL_CLASSES:
                entry["tools"].append({"name": name, "kind": "bash_tool", "line": line, "flags": ["code_execution", "write"]})
                entry["flags"].add("code_execution")
                return
            if name.endswith("Toolset") or name.endswith("toolset"):
                flags = set()
                if any(token in name.lower() for token in PRIVATE_TOOLSET_TOKENS):
                    flags.add("private")
                entry["toolsets"].append({"kind": name, "line": line, "flags": sorted(flags),
                                          "tool_filter": "absent" if keyword(call, "tool_filter") is None else "present"})
                entry["flags"].update(flags)
                return
            if name in BUILTIN_TOOLS:
                self.describe_builtin(entry, path, line, subject, name)
                return
            entry["tools"].append({"name": name, "kind": "other", "line": line, "flags": []})
            return
        if variable is not None:
            if variable in BUILTIN_TOOLS:
                self.describe_builtin(entry, path, line, subject, variable)
            elif variable in self.functions:
                self.describe_function(entry, path, line, subject, variable, "bare", "absent", gated_by_callback)
            else:
                entry["tools"].append({"name": variable, "kind": "unresolved", "line": line, "flags": []})
                self.finding(path, line, variable, "unresolved_tool_reference",
                             "tool defined outside the scanned files or built dynamically")
            return
        entry["tools"].append({"name": None, "kind": "other", "line": line, "flags": []})

    def describe_builtin(self, entry, path, line, subject, name):
        flags = BUILTIN_TOOLS[name]
        entry["tools"].append({"name": name, "kind": "builtin", "line": line, "flags": sorted(flags)})
        entry["flags"].update(flags)
        if "untrusted" in flags:
            self.finding(path, line, name, "untrusted_content_source",
                         "built-in tool returns external or recalled content the model will read as context")
        if "egress" in flags:
            self.finding(path, line, name, "egress_capable_tool",
                         "built-in tool fetches a model-chosen URL; data placed in the URL leaves the perimeter")

    def describe_function(self, entry, path, line, subject, function, via, confirmation, gated_by_callback):
        if function is None or function not in self.functions:
            entry["tools"].append({"name": function, "kind": "unresolved", "line": line, "flags": []})
            self.finding(path, line, function or "<dynamic>", "unresolved_tool_reference",
                         "tool defined outside the scanned files or built dynamically")
            return
        facts = self.functions[function]
        flags, details = facts.classify()
        gate = []
        if confirmation in {"enabled", "dynamic"}:
            gate.append(f"require_confirmation:{confirmation}")
        if gated_by_callback:
            gate.append("before_tool_callback")
        entry["tools"].append({"name": function, "kind": "function_tool" if via in TOOL_WRAPPERS else "function",
                               "line": line, "defined_at": f"{facts.path}:{facts.line}",
                               "flags": sorted(flags - {"identity"}), "gate": gate, "details": details})
        entry["flags"].update(flags - {"identity", "write"})
        if confirmation == "dynamic":
            self.finding(path, line, function, "confirmation_callable_review",
                         "require_confirmation is a callable; it must return a strict bool, a truthy non-bool or None "
                         "is not a gate (community report google/adk-python#7010)")
        if "identity" in flags:
            self.finding(facts.path, facts.line, function, "identity_parameter_review",
                         f"{', '.join(details['identity_parameters'])}: the model supplies this value; "
                         "read identity from ToolContext or session state instead")
        if "egress" in flags:
            evidence = details["egress_evidence"]
            self.finding(facts.path, facts.line, function, "egress_capable_tool",
                         "network calls: " + (", ".join(evidence["network_calls"]) or "none") +
                         "; url-like parameters: " + (", ".join(evidence["parameters"]) or "none") +
                         "; name tokens: " + (", ".join(evidence["name_tokens"]) or "none"))
        if "untrusted" in flags:
            self.finding(facts.path, facts.line, function, "untrusted_content_source",
                         "returns retrieved, fetched or recalled content; its text is attacker-reachable and unfenced")
        if "write" in flags and not gate:
            plugin_note = f"; {len(self.result['plugins'])} runner plugin(s) present, confirm one gates it" if self.result["plugins"] else ""
            self.finding(facts.path, facts.line, function, "write_tool_without_gate",
                         f"write-like name ({', '.join(details['write_tokens'])}) with no require_confirmation "
                         f"and no before_tool_callback on the agent{plugin_note}")

    def describe_mcp(self, entry, path, line, subject, call, gated_by_callback):
        tool_filter = keyword(call, "tool_filter")
        filter_kind = "absent"
        allowed = []
        if isinstance(tool_filter, (ast.List, ast.Tuple)):
            filter_kind = "list"
            allowed = sorted(constant_str(e) for e in tool_filter.elts if constant_str(e) is not None)
        elif tool_filter is not None:
            filter_kind = "predicate"
        params = keyword(call, "connection_params")
        transport = "unknown"
        if isinstance(params, ast.Call):
            transport = call_name(params)
        elif isinstance(params, ast.Name):
            transport = self.param_vars.get(params.id, "unknown")
        confirmation = confirmation_mode(call)
        toolset = {"kind": "mcp_toolset", "line": line, "tool_filter": filter_kind, "allowed_tools": allowed,
                   "transport": transport, "tool_name_prefix": keyword(call, "tool_name_prefix") is not None,
                   "header_provider": keyword(call, "header_provider") is not None,
                   "require_confirmation": confirmation, "flags": ["untrusted"]}
        entry["toolsets"].append(toolset)
        entry["flags"].add("untrusted")
        if filter_kind == "absent":
            self.finding(path, line, subject, "mcp_unfiltered",
                         "McpToolset without tool_filter exposes every server tool; allowlist by name")
        if transport in STDIO_PARAMS:
            self.finding(path, line, subject, "mcp_stdio_transport",
                         f"{transport} spawns a local process with the agent's own identity and environment")
        if confirmation == "dynamic":
            self.finding(path, line, subject, "confirmation_callable_review",
                         "McpToolset require_confirmation is a callable; it must return a strict bool")
        self.finding(path, line, subject, "untrusted_content_source",
                     f"MCP server ({transport}) supplies tool descriptions and results; both are attacker-reachable text")
        gate = confirmation in {"enabled", "dynamic"} or gated_by_callback
        for name in allowed:
            if tokens(name) & WRITE_VERBS and not gate:
                self.finding(path, line, f"{name} (mcp)", "write_tool_without_gate",
                             "allowlisted MCP tool has a write-like name with no require_confirmation on the toolset "
                             "and no before_tool_callback on the agent")
            if tokens(name) & EGRESS_VERBS:
                entry["flags"].add("egress")
                self.finding(path, line, f"{name} (mcp)", "egress_capable_tool",
                             "allowlisted MCP tool name suggests it sends data outside the agent")

    def trifecta(self, entry, by_var, visited=None):
        visited = visited if visited is not None else set()
        own = set(entry["flags"])
        combined, sources = set(own), {"own": sorted(own), "sub_agents": {}}
        visited.add(id(entry))
        for sub in entry["sub_agents"]:
            target = by_var.get(sub["variable"])
            if target is None or id(target) in visited:
                continue
            nested = self.trifecta(target, by_var, visited)
            sources["sub_agents"][sub["variable"]] = nested["sources"]["own"]
            combined |= {flag for flag, present in (("private", nested["has_private_data_source"]),
                                                     ("untrusted", nested["has_untrusted_content_source"]),
                                                     ("egress", nested["has_egress"])) if present}
        summary = {"has_private_data_source": "private" in combined,
                   "has_untrusted_content_source": "untrusted" in combined,
                   "has_egress": "egress" in combined,
                   "has_code_execution": "code_execution" in combined,
                   "has_remote_agent_content": "remote" in combined,
                   "sources": sources}
        summary["all_three"] = summary["has_private_data_source"] and summary["has_untrusted_content_source"] and summary["has_egress"]
        return summary


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Reads bounded source, manifests and deploy text only; skips secrets, dependency directories and symlinks. "
               "Findings are review prompts for a threat model, not a security verdict.")
    parser.add_argument("--project", required=True, help="project directory to inspect without executing code")
    parser.add_argument("--dry-run", action="store_true", help="perform the same read-only scan and report no changes")
    parser.add_argument("--max-files", type=positive, default=500, help="maximum eligible files (default: 500)")
    parser.add_argument("--max-entries", type=positive, default=10000,
                        help="stop at this total directory-entry count, including exclusions (default: 10000)")
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
    inventory = Inventory(args)
    inventory.walk(root)
    inventory.analyse()
    print(json.dumps(inventory.result, indent=2, sort_keys=True))
    return 1 if inventory.result["partial"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
