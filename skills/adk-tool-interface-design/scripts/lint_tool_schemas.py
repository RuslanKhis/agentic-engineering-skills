#!/usr/bin/env python3
"""Bounded, read-only lint of the model-facing interface of ADK tools.

Scans Python source with `ast` for functions referenced by `FunctionTool(...)`,
`LongRunningFunctionTool(...)` and `tools=[...]` on `LlmAgent(`/`Agent(`, plus
agent `description=` and `sub_agents=[...]`. Never imports or executes the
inspected project. Findings are syntactic observations for review, not a
verdict on model behaviour.
"""

import argparse
import ast
import itertools
import json
import os
from pathlib import Path
import re
import stat


EXCLUDED = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
            "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
            "dist", "build", "site-packages", "vendor", ".aws", ".ssh", ".config"}
TOOL_WRAPPERS = {"FunctionTool", "LongRunningFunctionTool"}
AGENT_CLASSES = {"LlmAgent", "Agent"}
AGENT_WRAPPERS = {"AgentTool"}
CONTEXT_NAMES = {"tool_context", "self", "cls"}
CONTEXT_TYPES = {"ToolContext", "ReadonlyContext", "CallbackContext", "InvocationContext"}
GENERIC_NAMES = {"data", "value", "values", "input", "inputs", "id", "obj", "object",
                 "param", "params", "arg", "payload", "item", "items", "val", "info"}
IDENTITY_NAMES = {"user_id", "tenant_id", "email", "user_email", "customer_id",
                  "account_id", "org_id", "organization_id", "principal", "username",
                  "api_key", "token", "access_token", "credential", "password"}
ANTONYMS = (("enable", "disable"), ("on", "off"), ("include", "exclude"),
            ("show", "hide"), ("allow", "deny"), ("allow", "block"), ("is", "not"))
STOPWORDS = {"the", "and", "for", "with", "from", "that", "this", "an", "of", "to",
             "in", "on", "by", "is", "are", "be", "it", "its", "or", "as", "at"}
TYPING_NAMES = {"List", "Dict", "Optional", "Literal", "Any", "Tuple", "Set", "Sequence",
                "Mapping", "Union", "Annotated", "Iterable", "FrozenSet", "Type"}
ENUM_BASES = {"Enum", "StrEnum", "IntEnum", "str, Enum"}
MODEL_BASES = {"BaseModel"}
BLOCKING_PREFIXES = ("requests.", "httpx.", "urllib.", "sqlite3.", "subprocess.", "psycopg",
                     "pymysql.", "mysql.", "boto3.", "socket.", "smtplib.", "ftplib.")
BLOCKING_NAMES = {"open", "time.sleep", "httpx.Client", "httpx.get", "httpx.post", "httpx.put",
                  "httpx.patch", "httpx.delete", "httpx.request", "urllib.request.urlopen"}
NON_DICT_RETURNS = {"str", "int", "float", "bool", "bytes", "list", "tuple", "set", "List", "Tuple", "Set"}
DOMAIN_DEFAULT = re.compile(r"[A-Z0-9 ]")
SENTENCE_END = re.compile(r"[.!?](?:\s+|$)")
WORD = re.compile(r"[A-Za-z0-9]+")
MIN_WORDS = 15
MIN_SENTENCES = 2
MIN_DESCRIPTION_WORDS = 8
JACCARD_THRESHOLD = 0.6


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


def call_name(node):
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def module_matches(path, module):
    """True when a scanned file path is the module named by the last dotted segment."""
    path = Path(path)
    return path.stem == module or (path.stem == "__init__" and path.parent.name == module)


def keyword(node, name):
    return next((k.value for k in node.keywords if k.arg == name), None)


def constant_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value for v in node.values
                       if isinstance(v, ast.Constant) and isinstance(v.value, str))
    return None


def annotation_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.split(".")[-1].split("[")[0]
    if isinstance(node, ast.Subscript):
        return annotation_name(node.value)
    if isinstance(node, ast.BinOp):
        left = annotation_name(node.left)
        return left if left != "None" else annotation_name(node.right)
    return ""


def is_bool_annotation(node):
    if node is None:
        return False
    if annotation_name(node) == "bool":
        return True
    if isinstance(node, ast.Subscript) and annotation_name(node.value) == "Optional":
        return annotation_name(node.slice) == "bool"
    return False


def words(text):
    return [w.lower() for w in WORD.findall(text or "")]


def sentence_count(text):
    return len([s for s in SENTENCE_END.split(text.strip()) if s.strip()])


def first_sentence(text):
    parts = [s for s in SENTENCE_END.split(text.strip()) if s.strip()]
    return parts[0] if parts else ""


def tokens(text):
    return {w for w in words(text.replace("_", " ")) if len(w) > 2 and w not in STOPWORDS}


def name_tokens(name):
    return set(words(name.replace("_", " ")))


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def mutually_exclusive(first, second):
    if {first, second} == {"on", "off"}:
        return True
    for positive_word, negative_word in ANTONYMS:
        for left, right in ((positive_word, negative_word), (negative_word, positive_word)):
            prefix_left, prefix_right = left + "_", right + "_"
            if first.startswith(prefix_left) and second.startswith(prefix_right):
                if first[len(prefix_left):] == second[len(prefix_right):]:
                    return True
    return False


class FunctionFacts:
    """Syntactic facts about one candidate tool function."""

    def __init__(self, path, node, classes=None):
        self.path = path
        self.node = node
        self.classes = classes or {}
        self.is_async = isinstance(node, ast.AsyncFunctionDef)
        self.name = node.name
        self.line = node.lineno
        self.docstring = ast.get_docstring(node) or ""
        self.params = []
        self.variadic = False
        args = node.args
        for param in itertools.chain(args.posonlyargs, args.args, args.kwonlyargs):
            self.params.append(param)
        if args.vararg is not None or args.kwarg is not None:
            self.variadic = True

    def visible_params(self):
        for param in self.params:
            if param.arg in CONTEXT_NAMES:
                continue
            if param.annotation is not None and annotation_name(param.annotation) in CONTEXT_TYPES:
                continue
            yield param

    def body_nodes(self):
        """Yield nodes of this function body, excluding nested defs and lambdas."""
        stack = list(self.node.body)
        while stack:
            node = stack.pop()
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue
            yield node
            stack.extend(ast.iter_child_nodes(node))

    def returns(self):
        for node in self.body_nodes():
            if isinstance(node, ast.Return):
                yield node

    def returns_error_dict(self):
        for statement in self.returns():
            value = statement.value
            if isinstance(value, ast.Dict):
                for key, item in zip(value.keys, value.values):
                    if (isinstance(key, ast.Constant) and key.value == "status"
                            and isinstance(item, ast.Constant) and item.value == "error"):
                        return True
        return False

    def blocking_calls(self):
        for node in self.body_nodes():
            if isinstance(node, ast.Call):
                name = dotted(node.func)
                if name in BLOCKING_NAMES or name.startswith(BLOCKING_PREFIXES):
                    yield node.lineno, name

    def type_findings(self, param):
        annotation = param.annotation
        if annotation is None:
            return
        if isinstance(annotation, ast.Name) and annotation.id in {"list", "dict", "List", "Dict"}:
            yield ("bare_container_annotation", f"{param.arg}: {annotation.id} without item types")
        if isinstance(annotation, ast.BinOp):
            yield ("pep604_union_parameter", f"{param.arg}: X | Y syntax; verify the pinned builder accepts it")
        subscript_name = annotation_name(annotation.value) if isinstance(annotation, ast.Subscript) else ""
        if subscript_name == "Union":
            members = annotation.slice.elts if isinstance(annotation.slice, ast.Tuple) else [annotation.slice]
            if len([m for m in members if annotation_name(m) != "None"]) > 1:
                yield ("complex_parameter_type_review", f"{param.arg}: Union of several types")
        base = annotation_name(annotation)
        if isinstance(annotation, (ast.Name, ast.Attribute)) and base[:1].isupper() and base not in TYPING_NAMES:
            kind = self.classes.get(base)
            if kind == "enum":
                return
            detail = "pydantic model" if kind == "model" else "class not resolved to an Enum"
            yield ("complex_parameter_type_review", f"{param.arg}: {base} ({detail}); prefer primitives or an Enum")

    def findings(self):
        found = []
        if not self.docstring.strip():
            found.append(("missing_docstring", "no docstring; the model sees no description"))
        else:
            word_count = len(words(self.docstring))
            sentences = sentence_count(self.docstring)
            if word_count < MIN_WORDS or sentences < MIN_SENTENCES:
                found.append(("short_docstring",
                              f"{sentences} sentence(s), {word_count} word(s); explain what, when, inputs and limits"))
            if "tool_context" in self.docstring or "ToolContext" in self.docstring:
                found.append(("docstring_mentions_context", "the injected context is invisible to the model"))
        if self.variadic:
            found.append(("variadic_parameter", "*args/**kwargs are dropped from the declaration"))
        defaults = dict(zip([p.arg for p in reversed(self.node.args.args)], reversed(self.node.args.defaults)))
        defaults.update({p.arg: d for p, d in zip(self.node.args.kwonlyargs, self.node.args.kw_defaults) if d is not None})
        bool_params = []
        for param in self.visible_params():
            if param.annotation is None:
                found.append(("untyped_parameter", param.arg))
            found.extend(self.type_findings(param))
            default = defaults.get(param.arg)
            if (isinstance(default, ast.Constant) and isinstance(default.value, str) and default.value
                    and DOMAIN_DEFAULT.search(default.value)
                    and annotation_name(param.annotation) not in {"Literal"}
                    and self.classes.get(annotation_name(param.annotation)) != "enum"):
                found.append(("domain_default_review",
                              f"{param.arg}: string default looks like a domain value the model should supply"))
            if param.arg in GENERIC_NAMES:
                found.append(("generic_parameter_name", param.arg))
            if param.arg in IDENTITY_NAMES:
                found.append(("identity_parameter_review",
                              f"{param.arg}: confirm identity comes from trusted context, not the model"))
            if is_bool_annotation(param.annotation) or param.arg in {"on", "off"}:
                bool_params.append(param.arg)
        for first, second in itertools.combinations(sorted(bool_params), 2):
            if mutually_exclusive(first, second):
                found.append(("exclusive_boolean_pair", f"{first}/{second}: prefer one enum parameter"))
        if not self.is_async:
            for line, name in self.blocking_calls():
                found.append(("sync_io_blocks_parallelism", f"line {line}: {name} in a sync def"))
                break
        if not self.returns_error_dict():
            for node in self.body_nodes():
                if isinstance(node, ast.Raise):
                    found.append(("raise_in_tool_body", f"line {node.lineno}: no status error dict returned"))
                    break
        for statement in self.returns():
            value = statement.value
            if value is None:
                continue
            if isinstance(value, ast.Constant) and value.value is not None:
                found.append(("non_dict_return", f"line {statement.lineno}: literal {type(value.value).__name__}"))
            elif isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.JoinedStr)):
                found.append(("non_dict_return", f"line {statement.lineno}: literal {type(value).__name__.lower()}"))
            elif isinstance(value, ast.Dict):
                if any(k is None for k in value.keys):
                    continue
                keys = {k.value for k in value.keys if isinstance(k, ast.Constant)}
                if "status" not in keys:
                    found.append(("missing_status_key", f"line {statement.lineno}"))
        returns_annotation = annotation_name(self.node.returns) if self.node.returns is not None else ""
        if returns_annotation in NON_DICT_RETURNS and not any(kind == "non_dict_return" for kind, _ in found):
            found.append(("non_dict_return", f"line {self.line}: annotated -> {returns_annotation}"))
        return found


class Collector(ast.NodeVisitor):
    """Collect function definitions, tool references and agent constructions."""

    def __init__(self, path):
        self.path = path
        self.functions = {}
        self.tool_refs = []
        self.agents = []
        self.agent_vars = {}
        self.sub_agent_refs = []
        self.classes = {}
        self.pending = []
        self.class_depth = 0
        self.aliases = {}

    def visit_Import(self, node):
        for item in node.names:
            if item.asname:
                self.aliases[item.asname] = item.name
            else:
                head = item.name.split(".")[0]
                self.aliases[head] = head

    def visit_ImportFrom(self, node):
        for item in node.names:
            self.aliases[item.asname or item.name] = f"{node.module or ''}.{item.name}".strip(".")

    def tool_ref(self, node, line, via):
        """Record a function reference written as a name or a module attribute."""
        display = dotted(node)
        if not display:
            return False
        head, _, rest = display.partition(".")
        imported = head in self.aliases
        full = self.aliases.get(head, head) + (f".{rest}" if rest else "")
        self.tool_refs.append({"display": display, "parts": full.split("."), "imported": imported,
                               "path": self.path, "line": line, "via": via})
        return True

    def visit_ClassDef(self, node):
        bases = {annotation_name(b) for b in node.bases}
        if bases & ENUM_BASES:
            self.classes[node.name] = "enum"
        elif bases & MODEL_BASES:
            self.classes[node.name] = "model"
        self.class_depth += 1
        self.generic_visit(node)
        self.class_depth -= 1

    def visit_FunctionDef(self, node):
        if self.class_depth == 0:
            self.pending.append(node)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call) and call_name(node.value) in AGENT_CLASSES:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.agent_vars[target.id] = node.value
        self.generic_visit(node)

    def tool_entry(self, element, line):
        if isinstance(element, (ast.Name, ast.Attribute)):
            self.tool_ref(element, line, "bare")
            return "function"
        if isinstance(element, ast.Call):
            name = call_name(element)
            if name in TOOL_WRAPPERS:
                return "function"
            if name in AGENT_WRAPPERS:
                target = element.args[0] if element.args else keyword(element, "agent")
                if isinstance(target, ast.Name):
                    self.sub_agent_refs.append({"agent": target.id, "path": self.path,
                                                "line": element.lineno, "via": name})
                return "agent_tool"
            if name.endswith("Toolset") or name.endswith("toolset"):
                return "toolset"
            return "other"
        return "other"

    def visit_Call(self, node):
        name = call_name(node)
        if name in TOOL_WRAPPERS:
            target = node.args[0] if node.args else keyword(node, "func")
            if isinstance(target, (ast.Name, ast.Attribute)):
                self.tool_ref(target, node.lineno, name)
        elif name in AGENT_WRAPPERS:
            target = node.args[0] if node.args else keyword(node, "agent")
            if isinstance(target, ast.Name):
                self.sub_agent_refs.append({"agent": target.id, "path": self.path,
                                            "line": node.lineno, "via": name})
        elif name in AGENT_CLASSES:
            agent = {"name": constant_str(keyword(node, "name")), "path": self.path,
                     "line": node.lineno, "description": constant_str(keyword(node, "description")),
                     "description_present": keyword(node, "description") is not None,
                     "mode": constant_str(keyword(node, "mode")), "tool_count": None,
                     "toolsets": 0, "tools_literal": True, "sub_agents": []}
            tools = keyword(node, "tools")
            if isinstance(tools, (ast.List, ast.Tuple)):
                agent["tool_count"] = len(tools.elts)
                for element in tools.elts:
                    if self.tool_entry(element, node.lineno) == "toolset":
                        agent["toolsets"] += 1
            elif tools is not None:
                agent["tools_literal"] = False
            sub_agents = keyword(node, "sub_agents")
            if isinstance(sub_agents, (ast.List, ast.Tuple)):
                for element in sub_agents.elts:
                    if isinstance(element, ast.Name):
                        agent["sub_agents"].append(element.id)
                        self.sub_agent_refs.append({"agent": element.id, "path": self.path,
                                                    "line": node.lineno, "via": "sub_agents"})
            self.agents.append(agent)
        self.generic_visit(node)


class Lint:
    def __init__(self, args):
        self.args = args
        self.result = {"schema_version": 1, "read_only": True, "changes_made": False,
                       "dry_run": args.dry_run, "partial": False, "files_inspected": 0,
                       "directory_entries_seen": 0,
                       "limits": {"max_files": args.max_files, "max_bytes_per_file": args.max_bytes,
                                  "max_depth": args.max_depth, "max_entries": args.max_entries,
                                  "max_tools": args.max_tools, "excluded_directories": sorted(EXCLUDED),
                                  "sensitive_files_excluded": True, "symlinks_followed": False},
                       "tools": [], "agents": [], "findings": [], "counts": {}, "issues": [],
                       "unresolved_tool_references": 0}
        self.seen = 0
        self.stopped = False
        self.functions = {}
        self.classes = {}
        self.pending = []
        self.tool_refs = []
        self.agents = []
        self.agent_vars = {}
        self.sub_agent_refs = []

    def issue(self, path, reason):
        self.result["partial"] = True
        self.result["issues"].append({"path": path, "reason": reason})

    def finding(self, path, line, subject, kind, detail=""):
        self.result["findings"].append({"path": path, "line": line, "subject": subject,
                                        "finding": kind, "detail": detail})
        self.result["counts"][kind] = self.result["counts"].get(kind, 0) + 1

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
            collector = Collector(relative)
            collector.visit(ast.parse(raw.decode("utf-8-sig")))
            self.classes.update(collector.classes)
            for node in collector.pending:
                self.pending.append((relative, node))
            self.tool_refs.extend(collector.tool_refs)
            self.agents.extend(collector.agents)
            self.sub_agent_refs.extend(collector.sub_agent_refs)
            for name, call in collector.agent_vars.items():
                self.agent_vars.setdefault(name, []).append((relative, call))
            self.result["files_inspected"] += 1
        except (OSError, UnicodeError):
            self.issue(relative, "unreadable_file")
        except (SyntaxError, ValueError, RecursionError):
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
            elif path.suffix == ".py":
                if self.seen >= self.args.max_files:
                    self.issue(relative, "file_count_limit")
                    self.stopped = True
                    return
                self.seen += 1
                self.inspect(path, relative)

    def resolve(self, ref):
        """Return the scanned definitions a tool reference points at.

        A bare, non-imported name matches every same-named top-level function.
        A module attribute (`tools.fn`, `pkg.tools.fn`) or an imported name
        (`from .tools import fn`, `from pkg import tools as t`; `t.fn`) matches
        the function in the scanned file whose stem (or package directory for
        `__init__.py`) is the last module segment; an imported name falls back
        to a unique same-named function for re-exports.
        """
        parts = [part for part in ref["parts"] if part]
        if not parts:
            return []
        candidates = self.functions.get(parts[-1], [])
        if len(parts) == 1:
            return list(candidates)
        matched = [facts for facts in candidates if module_matches(facts.path, parts[-2])]
        if matched:
            return matched
        if ref["imported"] and len(candidates) == 1:
            return list(candidates)
        return []

    def analyse(self):
        for path, node in self.pending:
            self.functions.setdefault(node.name, []).append(FunctionFacts(path, node, self.classes))
        resolved, unresolved = {}, {}
        for ref in self.tool_refs:
            definitions = self.resolve(ref)
            if not definitions:
                unresolved.setdefault(ref["display"], ref)
                continue
            for facts in definitions:
                resolved.setdefault(id(facts), (facts, []))[1].append(ref)
        for display in sorted(unresolved):
            ref = unresolved[display]
            self.finding(ref["path"], ref["line"], display, "unresolved_tool_reference",
                         "function defined outside the scanned files, re-exported or built dynamically; "
                         "this tool was not linted")
        self.result["unresolved_tool_references"] = len(unresolved)
        by_name = {}
        for facts, refs in resolved.values():
            by_name.setdefault(facts.name, []).append((facts, refs))
        tools = []
        for name in sorted(by_name):
            definitions = sorted(by_name[name], key=lambda item: (item[0].path, item[0].line))
            if len(definitions) > 1:
                for facts, _ in definitions:
                    self.finding(facts.path, facts.line, name, "duplicate_tool_name",
                                 "the same tool name is defined more than once; later registration shadows earlier")
            for facts, refs in definitions:
                entry = {"name": name, "path": facts.path, "line": facts.line,
                         "references": len(refs), "findings": []}
                for kind, detail in facts.findings():
                    entry["findings"].append(kind)
                    self.finding(facts.path, facts.line, name, kind, detail)
                tools.append((facts, entry))
        for (left, left_entry), (right, right_entry) in itertools.combinations(tools, 2):
            if left.name == right.name:
                continue
            if jaccard(name_tokens(left.name), name_tokens(right.name)) > JACCARD_THRESHOLD:
                self.finding(right.path, right.line, f"{left.name}/{right.name}", "similar_tool_names",
                             "names share most tokens; consolidate or make the difference explicit")
            if left.docstring and right.docstring and jaccard(
                    tokens(first_sentence(left.docstring)), tokens(first_sentence(right.docstring))) > JACCARD_THRESHOLD:
                self.finding(right.path, right.line, f"{left.name}/{right.name}", "similar_tool_descriptions",
                             "first docstring sentences overlap; state when to use each")
        self.result["tools"] = [entry for _, entry in tools]
        for agent in self.agents:
            entry = {"name": agent["name"], "path": agent["path"], "line": agent["line"],
                     "tool_count": agent["tool_count"], "toolsets": agent["toolsets"],
                     "mode": agent["mode"], "sub_agents": len(agent["sub_agents"]), "findings": []}
            subject = agent["name"] or "<unnamed agent>"
            if agent["tool_count"] is not None and agent["tool_count"] > self.args.max_tools:
                entry["findings"].append("tool_count_exceeds_max")
                self.finding(agent["path"], agent["line"], subject, "tool_count_exceeds_max",
                             f"{agent['tool_count']} entries in tools=[...] above {self.args.max_tools}")
            if agent["toolsets"]:
                entry["findings"].append("toolset_count_unknown")
                self.finding(agent["path"], agent["line"], subject, "toolset_count_unknown",
                             f"{agent['toolsets']} toolset(s) expand at runtime; count with get_tools")
            if not agent["tools_literal"]:
                entry["findings"].append("tools_not_literal")
                self.finding(agent["path"], agent["line"], subject, "tools_not_literal",
                             "tools= is not a list literal; count at runtime")
            self.result["agents"].append(entry)
        checked = set()
        for ref in self.sub_agent_refs:
            variable = ref["agent"]
            if variable in checked:
                continue
            checked.add(variable)
            definitions = self.agent_vars.get(variable)
            if not definitions:
                self.finding(ref["path"], ref["line"], variable, "unresolved_agent_reference",
                             "agent defined outside the scanned files or built dynamically")
                continue
            for path, call in definitions:
                name = constant_str(keyword(call, "name")) or variable
                description_node = keyword(call, "description")
                description = constant_str(description_node)
                if description_node is None:
                    self.finding(path, call.lineno, name, "missing_agent_description",
                                 "a sub-agent or AgentTool target with no description is unroutable")
                elif description is None:
                    continue
                elif len(words(description)) < MIN_DESCRIPTION_WORDS or description.strip() == name:
                    self.finding(path, call.lineno, name, "short_agent_description",
                                 f"{len(words(description))} word(s); the parent sees this text verbatim")
        self.result["findings"].sort(key=lambda item: (item["path"], item["line"], item["finding"], item["subject"], item["detail"]))
        self.result["tools"].sort(key=lambda item: json.dumps(item, sort_keys=True))
        self.result["agents"].sort(key=lambda item: json.dumps(item, sort_keys=True))
        self.result["issues"].sort(key=lambda item: json.dumps(item, sort_keys=True))
        self.result["counts"] = dict(sorted(self.result["counts"].items()))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Reads bounded Python source only; skips secrets, dependency directories and symlinks. "
               "Findings are review prompts, not a verdict on model behaviour.")
    parser.add_argument("--project", required=True, help="project directory to inspect without executing code")
    parser.add_argument("--dry-run", action="store_true", help="perform the same read-only scan and report no changes")
    parser.add_argument("--max-tools", type=positive, default=20,
                        help="flag agents whose tools=[...] literal has more entries (default: 20)")
    parser.add_argument("--max-files", type=positive, default=500, help="maximum Python files (default: 500)")
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
    lint = Lint(args)
    lint.walk(root)
    lint.analyse()
    print(json.dumps(lint.result, indent=2, sort_keys=True))
    return 1 if lint.result["partial"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
