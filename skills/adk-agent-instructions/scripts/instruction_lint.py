#!/usr/bin/env python3
"""Bounded, read-only lint of ADK agent instructions. Never imports or executes the inspected project.

Findings are inspection signals for a human or agent reviewer, not a verdict on
prompt quality. The templating rules mirror google-adk 2.8.0
(utils/instructions_utils.py): a `{name}` or `{prefix:name}` match is filled
from session state and raises KeyError when the key is absent, `{name?}` is
optional, and a match whose inner text is not a valid state name is left as
written. Backslash and dollar escapes are honoured only from google-adk 2.10.0.
"""

import argparse
import ast
import json
import os
from pathlib import Path
import re
import stat


EXCLUDED = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
            "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
            "dist", "build", "site-packages", "vendor", ".aws", ".ssh", ".config"}
# Coding-agent skill install directories hold these skills' own fixtures, not the project.
EXCLUDED = EXCLUDED | {".claude", ".agents", ".agent", ".codex", ".gemini", ".cursor", ".windsurf", ".antigravity", ".adk-evidence"}
AGENT_CLASSES = {"Agent", "LlmAgent"}
STATE_PREFIXES = ("app:", "user:", "temp:")
FRAMEWORK_TOOLS = {"transfer_to_agent", "finish_task", "load_artifacts", "load_memory",
                   "preload_memory", "google_search", "get_user_choice", "exit_loop"}
TEMPLATE = re.compile(r"{+[^{}]*}+")
JSON_OBJECT = re.compile(r"""{\s*["'][^"']+["']\s*:""")
SHOUT = re.compile(r"\b(?:CRITICAL|MUST|NEVER|ALWAYS|IMPORTANT)\b")
MANDATE = re.compile(r"\b(?:always|must|should always)\s+(?:call|use|invoke|run)\b"
                     r"|\bbefore\s+(?:responding|answering|replying)\b"
                     r"|\bnever\s+(?:respond|answer|reply)\s+without\b", re.IGNORECASE)
PROHIBITION = re.compile(r"\b(?:do not|don't|never|must not|avoid|refrain from)\b", re.IGNORECASE)
POSITIVE_CUE = re.compile(r"\b(?:instead|rather|prefer|use|ask|say|return|offer|explain|tell|respond with)\b",
                          re.IGNORECASE)
RULE = re.compile(r"\b(always|never|do not|don't|must not)\s+([^.!?\n]{3,80})", re.IGNORECASE)
BACKTICK = re.compile(r"`([A-Za-z_][A-Za-z0-9]*_[A-Za-z0-9_]*)`")
SNAKE_CALL = re.compile(r"\b(?:call|use|invoke|run|calling|using)\s+(?:the\s+)?`?([a-z][a-z0-9]*_[a-z0-9_]+)`?",
                        re.IGNORECASE)
STOP = {"the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "with", "about", "that",
        "this", "is", "are", "agent", "handles", "handle", "user", "users", "question", "questions",
        "request", "requests", "any", "all"}
SHOUT_THRESHOLD = 1.0


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


def valid_state_name(name):
    parts = name.split(":")
    if len(parts) == 1:
        return name.isidentifier()
    if len(parts) == 2 and parts[0] + ":" in STATE_PREFIXES:
        return parts[1].isidentifier()
    return False


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in STOP}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return round(len(a & b) / len(a | b), 2)


def normalise_name(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def snippet(text, limit=60):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit].rstrip() + "..."


def analyse_text(text, state_keys, max_words, tools, known_names):
    """Return (metrics, findings) for one instruction text; never echoes the text."""
    findings = []
    word_count = len(text.split())
    buckets = {"resolved": set(), "optional": set(), "unresolved": set(), "artifact": set()}
    literal = 0
    json_like = bool(JSON_OBJECT.search(text))
    for match in TEMPLATE.finditer(text):
        inner = match.group().lstrip("{").rstrip("}").strip()
        optional = inner.endswith("?")
        base = inner.removesuffix("?") if optional else inner
        if base.startswith("artifact."):
            buckets["artifact"].add(base)
        elif valid_state_name(base):
            if base in state_keys:
                buckets["resolved"].add(base)
            elif optional:
                buckets["optional"].add(base)
            else:
                buckets["unresolved"].add(base)
        else:
            literal += 1
            if ('"' in inner or "'" in inner) and ":" in inner:
                json_like = True
    placeholders = {key: sorted(value) for key, value in buckets.items()}
    placeholders["literal_matches_left_unchanged"] = literal
    if placeholders["unresolved"]:
        findings.append({"code": "unresolved_placeholder",
                         "detail": "not in --state-keys and not optional; raises KeyError at request time: "
                                   + ", ".join(placeholders["unresolved"])})
    if json_like:
        findings.append({"code": "literal_braces_need_provider_or_escape",
                         "detail": "JSON-like braces found; identifier-shaped tokens inside examples are still "
                                   "templated. Use an InstructionProvider or {name?}; backslash escape only from 2.10.0"})
    if "\\{" in text or "${" in text:
        findings.append({"code": "escape_syntax_requires_2_10",
                         "detail": "backslash or dollar escapes are filled from state on google-adk < 2.10.0"})
    if word_count > max_words:
        findings.append({"code": "instruction_over_budget",
                         "detail": f"{word_count} words exceeds --max-words {max_words}"})
    shouts = len(SHOUT.findall(text))
    density = round(shouts * 100 / word_count, 2) if word_count else 0.0
    if shouts >= 2 and density > SHOUT_THRESHOLD:
        findings.append({"code": "shouting_modifier_density",
                         "detail": f"{shouts} upper-case modifiers, {density} per 100 words"})
    mandates = sorted({m.group().lower() for m in MANDATE.finditer(text)})
    if mandates:
        findings.append({"code": "mandatory_tool_call_phrasing", "detail": ", ".join(mandates)})
    sentences = [s for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    prohibition_only = sum(1 for s in sentences if PROHIBITION.search(s) and not POSITIVE_CUE.search(s))
    if prohibition_only:
        findings.append({"code": "prohibition_only_sentences",
                         "detail": f"{prohibition_only} sentence(s) forbid without naming the wanted behaviour"})
    referenced = set(BACKTICK.findall(text)) | set(SNAKE_CALL.findall(text))
    placeholder_names = set().union(*buckets.values())
    mentioned = sorted(r for r in referenced if r not in known_names and r not in state_keys
                       and r not in placeholder_names and r not in FRAMEWORK_TOOLS)
    if tools is not None:
        never_mentioned = sorted(t for t in tools if not re.search(r"\b" + re.escape(t) + r"\b", text))
        if never_mentioned:
            findings.append({"code": "tool_never_mentioned", "detail": ", ".join(never_mentioned)})
        unknown = sorted(r for r in mentioned if r not in tools)
        if unknown:
            findings.append({"code": "unknown_tool_reference",
                             "detail": "named like a tool but not in tools=: " + ", ".join(unknown)})
    rules = [(("never" if kw.lower() != "always" else "always"), rest.strip())
             for kw, rest in RULE.findall(text)]
    seen = set()
    for kind_a, text_a in rules:
        for kind_b, text_b in rules:
            if kind_a == "always" and kind_b == "never":
                score = jaccard(tokens(text_a), tokens(text_b))
                key = (text_a, text_b)
                if score > 0.5 and key not in seen:
                    seen.add(key)
                    findings.append({"code": "possible_contradiction",
                                     "detail": f"human review: 'always {snippet(text_a)}' vs "
                                               f"'never {snippet(text_b)}' (overlap {score})"})
    metrics = {"word_count": word_count, "placeholders": placeholders, "shouting_per_100_words": density,
               "prohibition_only_sentences": prohibition_only, "tools_mentioned": mentioned}
    return metrics, findings


class AgentCalls(ast.NodeVisitor):
    """Collect LlmAgent(...)/Agent(...) keyword arguments without evaluating anything."""

    def __init__(self):
        self.aliases = {}
        self.constants = {}
        self.functions = set()
        self.entries = []
        self.target = None

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

    def visit_Module(self, node):
        for statement in node.body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.functions.add(statement.name)
            elif isinstance(statement, (ast.Import, ast.ImportFrom)):
                self.visit(statement)
        for statement in node.body:
            if isinstance(statement, ast.Assign) and len(statement.targets) == 1 \
                    and isinstance(statement.targets[0], ast.Name):
                literal = self.literal_text(statement.value)
                if literal:
                    self.constants[statement.targets[0].id] = literal
        self.generic_visit(node)

    def literal_text(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value, "string"
        if isinstance(node, ast.JoinedStr):
            parts = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
            return "".join(parts), "fstring"
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left, right = self.literal_text(node.left), self.literal_text(node.right)
            if left and right:
                kind = "fstring" if "fstring" in (left[1], right[1]) else "string"
                return left[0] + right[0], kind
            return None
        if isinstance(node, ast.Name):
            return self.constants.get(node.id)
        if isinstance(node, ast.Call):
            if self.name(node.func).split(".")[-1] in {"dedent", "cleandoc"} and node.args:
                return self.literal_text(node.args[0])
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"strip", "lstrip", "rstrip"}:
                return self.literal_text(node.func.value)
            if isinstance(node.func, ast.Attribute) and node.func.attr == "format":
                inner = self.literal_text(node.func.value)
                return (inner[0], "fstring") if inner else None
        return None

    def classify(self, node):
        literal = self.literal_text(node)
        if literal:
            return literal[0], literal[1]
        if isinstance(node, ast.Lambda) or isinstance(node, ast.Call):
            return None, "provider"
        if isinstance(node, ast.Name) and node.id in self.functions:
            return None, "provider"
        return None, "unresolved_reference"

    def visit_Assign(self, node):
        previous = self.target
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            self.target = node.targets[0].id
        self.generic_visit(node)
        self.target = previous

    def visit_AnnAssign(self, node):
        previous = self.target
        if isinstance(node.target, ast.Name):
            self.target = node.target.id
        self.generic_visit(node)
        self.target = previous

    def references(self, node):
        refs = []
        if not isinstance(node, (ast.List, ast.Tuple)):
            return None
        for element in node.elts:
            if isinstance(element, ast.Name):
                refs.append(("var", element.id))
            elif isinstance(element, ast.Attribute):
                refs.append(("name", element.attr))
            elif isinstance(element, ast.Call):
                if self.name(element.func).split(".")[-1] in AGENT_CLASSES:
                    refs.append(("line", element.lineno))
                    continue
                inner = next((a for a in element.args if isinstance(a, ast.Name)), None)
                keyword = next((k.value for k in element.keywords
                                if k.arg in {"func", "agent", "tool"} and isinstance(k.value, ast.Name)), None)
                chosen = inner or keyword
                refs.append(("var", chosen.id) if chosen else ("name", self.name(element.func).split(".")[-1]))
            else:
                refs.append(("name", "<expression>"))
        return refs

    def visit_Call(self, node):
        if self.name(node.func).split(".")[-1] in AGENT_CLASSES:
            keywords = {k.arg: k.value for k in node.keywords if k.arg}
            entry = {"line": node.lineno, "variable": self.target, "name": None, "mode": None,
                     "include_contents": None, "instruction": (None, "absent"), "description": (None, "absent"),
                     "static_instruction": False, "global_instruction": False, "tools": None, "sub_agents": None}
            name = keywords.get("name")
            if isinstance(name, ast.Constant) and isinstance(name.value, str):
                entry["name"] = name.value
            for key in ("mode", "include_contents"):
                value = keywords.get(key)
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    entry[key] = value.value
            if "instruction" in keywords:
                entry["instruction"] = self.classify(keywords["instruction"])
            if "description" in keywords:
                entry["description"] = self.classify(keywords["description"])
            entry["static_instruction"] = "static_instruction" in keywords
            entry["global_instruction"] = "global_instruction" in keywords
            if "tools" in keywords:
                entry["tools"] = self.references(keywords["tools"]) or [("name", "<expression>")]
            if "sub_agents" in keywords:
                entry["sub_agents"] = self.references(keywords["sub_agents"]) or [("name", "<expression>")]
            self.entries.append(entry)
        previous = self.target
        self.target = None
        self.generic_visit(node)
        self.target = previous


class Lint:
    def __init__(self, args):
        self.args = args
        self.state_keys = set(args.state_keys)
        self.result = {"schema_version": 1, "read_only": True, "changes_made": False,
                       "dry_run": args.dry_run, "partial": False, "files_inspected": 0,
                       "directory_entries_seen": 0,
                       "limits": {"max_files": args.max_files, "max_bytes_per_file": args.max_bytes,
                                  "max_depth": args.max_depth, "max_entries": args.max_entries,
                                  "max_words": args.max_words, "shouting_threshold_per_100_words": SHOUT_THRESHOLD,
                                  "excluded_directories": sorted(EXCLUDED),
                                  "sensitive_files_excluded": True, "symlinks_followed": False},
                       "state_keys": sorted(self.state_keys), "agents": [], "issues": [],
                       "summary": {"agents": 0, "finding_counts": {}}}
        self.seen = 0
        self.stopped = False
        self.records = []
        self.child_findings = {}

    def issue(self, path, reason):
        self.result["partial"] = True
        self.result["issues"].append({"path": path, "reason": reason})

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

    def inspect_python(self, path, relative):
        try:
            content = self.read(path, relative)
            if content is None:
                return
            visitor = AgentCalls()
            visitor.visit(ast.parse(content))
        except (OSError, UnicodeError):
            self.issue(relative, "unreadable_file")
            return
        except (SyntaxError, ValueError, TypeError, AttributeError, RecursionError):
            self.issue(relative, "malformed_file")
            return
        self.result["files_inspected"] += 1
        entries = visitor.entries
        for entry in entries:
            entry["name"] = entry["name"] or entry["variable"] or f"agent@{entry['line']}"
        by_var = {e["variable"]: e for e in entries if e["variable"]}
        by_line = {e["line"]: e for e in entries}

        def resolve(refs):
            resolved, names = [], []
            for kind, value in refs or []:
                target = by_var.get(value) if kind == "var" else by_line.get(value) if kind == "line" else None
                if target is not None:
                    resolved.append(target)
                    names.append(target["name"])
                else:
                    names.append(value)
            return resolved, names

        known_names = {e["name"] for e in entries}
        for entry in entries:
            children, child_names = resolve(entry["sub_agents"])
            tool_entries, tool_names = resolve(entry["tools"])
            record = {"path": relative, "line": entry["line"], "source": "ast", "name": entry["name"],
                      "variable": entry["variable"], "mode": entry["mode"],
                      "include_contents": entry["include_contents"],
                      "instruction_kind": entry["instruction"][1], "description_kind": entry["description"][1],
                      "tools": tool_names if entry["tools"] is not None else None,
                      "sub_agents": child_names if entry["sub_agents"] is not None else None,
                      "findings": []}
            findings = record["findings"]
            text, kind = entry["instruction"]
            tools_for_text = [t for t in tool_names if t.isidentifier()] if entry["tools"] is not None else None
            if kind in {"string", "fstring"}:
                metrics, text_findings = analyse_text(text, self.state_keys, self.args.max_words,
                                                      tools_for_text, known_names | set(child_names))
                record.update(metrics)
                findings.extend(text_findings)
                if kind == "fstring":
                    findings.append({"code": "fstring_instruction",
                                     "detail": "placeholders rendered at import time; only literal parts were linted"})
                if entry["mode"] in {"task", "single_turn"} and "transfer_to_agent" in text:
                    findings.append({"code": "transfer_mentioned_in_non_chat_mode",
                                     "detail": f"mode={entry['mode']} receives no transfer instructions"})
            elif kind == "provider":
                findings.append({"code": "instruction_provider_detected",
                                 "detail": "callable instruction; state templating is bypassed, lint the rendered text"})
            elif kind == "unresolved_reference":
                findings.append({"code": "instruction_unresolved_reference",
                                 "detail": "instruction value defined elsewhere; lint the source or rendered text"})
            if entry["static_instruction"] and kind != "absent":
                findings.append({"code": "instruction_sent_as_dynamic_content",
                                 "detail": "static_instruction set, so instruction travels as request content, "
                                           "not system instruction (2.8.0)"})
            if entry["global_instruction"]:
                findings.append({"code": "deprecated_global_instruction",
                                 "detail": "use google.adk.plugins.global_instruction_plugin.GlobalInstructionPlugin"})
            if children:
                for child in children:
                    description, description_kind = child["description"]
                    if description_kind == "absent" or (description is not None and not description.strip()):
                        self.child_findings.setdefault(child["line"], []).append(
                            {"code": "missing_description", "detail": "sub-agent routing relies on description"})
                    elif description is not None:
                        if len(description.split()) < 8:
                            self.child_findings.setdefault(child["line"], []).append(
                                {"code": "short_description", "detail": f"{len(description.split())} word(s)"})
                        if normalise_name(description) == normalise_name(child["name"]):
                            self.child_findings.setdefault(child["line"], []).append(
                                {"code": "description_equals_name", "detail": "adds nothing to the routing table"})
                for index, first in enumerate(children):
                    for second in children[index + 1:]:
                        a, b = first["description"][0], second["description"][0]
                        if a and b:
                            score = jaccard(tokens(a), tokens(b))
                            if score > 0.6:
                                findings.append({"code": "similar_sibling_descriptions",
                                                 "detail": f"{first['name']} vs {second['name']} (jaccard {score})"})
            self.records.append((entry["line"], record))
        for line, record in self.records:
            record["findings"].extend(self.child_findings.pop(line, []))
        for _, record in self.records:
            record["findings"].sort(key=lambda f: (f["code"], f["detail"]))
            self.result["agents"].append(record)
        self.records = []
        self.child_findings = {}

    def inspect_prompt(self, path, relative, name, description_path=None):
        try:
            content = self.read(path, relative)
            if content is None:
                return
            description = None
            if description_path is not None and description_path.is_file() and not description_path.is_symlink():
                description = self.read(description_path, relative)
        except (OSError, UnicodeError):
            self.issue(relative, "unreadable_file")
            return
        self.result["files_inspected"] += 1
        metrics, findings = analyse_text(content, self.state_keys, self.args.max_words, None, set())
        record = {"path": relative, "line": 1, "source": "prompt_file", "name": name, "variable": None,
                  "mode": None, "include_contents": None, "instruction_kind": "string",
                  "description_kind": "string" if description is not None else "absent",
                  "tools": None, "sub_agents": None, "findings": findings}
        record.update(metrics)
        if description is not None and len(description.split()) < 8:
            findings.append({"code": "short_description", "detail": f"{len(description.split())} word(s)"})
        findings.sort(key=lambda f: (f["code"], f["detail"]))
        self.result["agents"].append(record)

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
                continue
            is_prompt = path.name == "instruction.md" and path.parent.parent.name == "prompts"
            if path.suffix == ".py" or is_prompt:
                if self.seen >= self.args.max_files:
                    self.issue(relative, "file_count_limit")
                    self.stopped = True
                    return
                self.seen += 1
                if is_prompt:
                    self.inspect_prompt(path, relative, path.parent.name, path.parent / "description.txt")
                else:
                    self.inspect_python(path, relative)

    def finish(self):
        self.result["agents"].sort(key=lambda a: (a["path"], a["line"], a["name"]))
        counts = {}
        for agent in self.result["agents"]:
            for finding in agent["findings"]:
                counts[finding["code"]] = counts.get(finding["code"], 0) + 1
        self.result["summary"] = {"agents": len(self.result["agents"]),
                                  "finding_counts": dict(sorted(counts.items()))}
        self.result["issues"].sort(key=lambda item: json.dumps(item, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Reads bounded Python source and prompts/<agent>/instruction.md files; skips secrets, "
               "dependency directories and symlinks. Findings direct review; they are not a quality verdict.")
    parser.add_argument("--project", required=True, help="project directory to inspect without executing code")
    parser.add_argument("--prompt-file", action="append", default=[], metavar="PATH",
                        help="additional Markdown or text instruction file to lint (repeatable)")
    parser.add_argument("--state-keys", default="", metavar="k1,k2",
                        help="comma-separated session state keys the application guarantees (prefixes allowed)")
    parser.add_argument("--max-words", type=positive, default=1000,
                        help="instruction word budget before instruction_over_budget (default: 1000)")
    parser.add_argument("--dry-run", action="store_true", help="perform the same read-only scan and report no changes")
    parser.add_argument("--max-files", type=positive, default=500, help="maximum eligible files (default: 500)")
    parser.add_argument("--max-entries", type=positive, default=10000,
                        help="stop at this total directory-entry count; reaching the cap is partial (default: 10000)")
    parser.add_argument("--max-bytes", type=positive, default=262144, help="maximum bytes read per file (default: 262144)")
    parser.add_argument("--max-depth", type=positive, default=8, help="maximum subdirectory depth (default: 8)")
    args = parser.parse_args()
    args.state_keys = [key.strip() for key in args.state_keys.split(",") if key.strip()]
    root = Path(args.project)
    try:
        if root.is_symlink() or not root.is_dir():
            parser.error("project must be an accessible directory, not a symlink")
        with os.scandir(root):
            pass
    except OSError:
        parser.error("project must be an accessible directory, not a symlink")
    prompt_files = []
    for value in args.prompt_file:
        path = Path(value)
        if path.is_symlink() or not path.is_file():
            parser.error(f"prompt file must be an existing regular file: {path.name}")
        try:
            relative = str(path.resolve().relative_to(root.resolve()))
        except ValueError:
            relative = path.name
        prompt_files.append((path, relative))
    lint = Lint(args)
    lint.walk(root)
    for path, relative in prompt_files:
        lint.inspect_prompt(path, relative, path.parent.name if path.name == "instruction.md" else path.stem)
    lint.finish()
    print(json.dumps(lint.result, indent=2, sort_keys=True))
    return 1 if lint.result["partial"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
