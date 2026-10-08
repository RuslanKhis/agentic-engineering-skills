#!/usr/bin/env python3
"""Bounded inventory of release references in an ADK project: model and judge IDs, prompt sources (hashed, never printed), eval sets and configs, deploy and CI files, dependency pins and secret version references. Emits a release manifest skeleton. Never imports or executes the inspected project."""

import argparse
import ast
import hashlib
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
GEMINI = re.compile(r"gemini-[A-Za-z0-9.-]*[A-Za-z0-9]")
ALIAS_SUFFIX = re.compile(r"-(latest|preview|exp)(?:-|$)")
RETIRING_DEFAULT_JUDGE = "gemini-2.5-flash"
JUDGE_METRICS = {"final_response_match_v2", "rubric_based_final_response_quality_v1",
                 "rubric_based_tool_use_quality_v1", "hallucinations_v1", "safety_v1",
                 "per_turn_user_simulator_quality_v1", "multi_turn_task_success_v1",
                 "multi_turn_trajectory_quality_v1", "multi_turn_tool_use_quality_v1",
                 "rubric_based_multi_turn_trajectory_quality_v1"}
JUDGE_CRITERIA = ("JudgeModelOptions", "LlmAsAJudgeCriterion", "RubricsBasedCriterion", "HallucinationsCriterion")
PROMPT_NAME = re.compile(r"(PROMPT|INSTRUCTION|SYSTEM)", re.IGNORECASE)
PROMPT_DIRS = {"prompt", "prompts"}
PROMPT_SUFFIXES = {".md", ".txt", ".j2", ".jinja", ".jinja2", ".prompt", ".yaml", ".yml"}
SECRET_VERSION = re.compile(r"secrets/[A-Za-z0-9_-]+/versions/(latest|\d+)")
SET_SECRETS = re.compile(r"[A-Z_][A-Z0-9_]*=([A-Za-z0-9_-]+):(latest|\d+)")
TEXT_COMMANDS = {
    "adk eval": "adk_eval_invocation",
    "adk conformance test": "adk_conformance_test_invocation",
    "adk conformance record": "adk_conformance_record_invocation",
    "adk deploy cloud_run": "adk_deploy_cloud_run",
    "adk deploy agent_engine": "adk_deploy_agent_engine",
    "adk deploy gke": "adk_deploy_gke",
    "gcloud run deploy": "gcloud_run_deploy",
    "--no-traffic": "cloud_run_no_traffic",
    "--tag": "cloud_run_tag",
    "update-traffic": "cloud_run_update_traffic",
    "--to-revisions": "cloud_run_to_revisions",
    "AgentEvaluator": "agent_evaluator_reference",
    "check_eval_results.py": "eval_csv_checker_reference",
}
TEXT_SUFFIXES = {".yml", ".yaml", ".sh", ".toml", ".cfg", ".ini", ".mk", ".json"}
TEXT_NAMES = {"Makefile", "Dockerfile", "Procfile", "Justfile"}


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


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify(model):
    """pinned | alias for a Gemini ID; non_gemini otherwise."""
    if not model.startswith("gemini-"):
        return "non_gemini"
    return "alias" if ALIAS_SUFFIX.search(model) else "pinned"


def model_in(text):
    match = GEMINI.search(text or "")
    return match.group(0) if match else None


def module_matches(path, module):
    """True when a scanned file path is the module named by the last dotted segment."""
    path = Path(path)
    return path.stem == module or (path.stem == "__init__" and path.parent.name == module)


def kind_of(relative, name, parent_names):
    lower = name.lower()
    if lower.startswith("dockerfile") or lower.endswith(".dockerfile"):
        return "dockerfile"
    if lower.startswith("cloudbuild") and lower.endswith((".yaml", ".yml")):
        return "cloudbuild"
    if ".github/workflows/" in relative.replace("\\", "/") and lower.endswith((".yml", ".yaml")):
        return "github_workflow"
    if lower.endswith(".evalset.json"):
        return "evalset"
    if lower.endswith(".test.json"):
        return "legacy_test_json"
    if lower == "test_config.json" or lower.endswith("_eval_config.json") or lower == "eval_config.json":
        return "eval_config"
    if lower.endswith(".py"):
        return "python"
    if lower == "pyproject.toml":
        return "pyproject"
    if lower.startswith("requirements") and lower.endswith((".txt", ".in")):
        return "requirements"
    if lower == "spec.yaml" and parent_names:
        return "conformance_spec"
    if parent_names & PROMPT_DIRS and Path(lower).suffix in PROMPT_SUFFIXES:
        return "prompt_file"
    if lower.endswith(".json"):
        return "json"
    if Path(lower).suffix in TEXT_SUFFIXES or name in TEXT_NAMES:
        return "text"
    return None


class Signals(ast.NodeVisitor):
    """Collect release references from one Python module without executing it."""

    def __init__(self, is_prompt_module):
        self.rows = set()
        self.prompts = []
        self.aliases = {}
        self.bindings = {}
        self.judge_nodes = set()
        self.is_prompt_module = is_prompt_module
        self.module_statements = set()
        self.constants = {}
        self.deferred_models = []

    def visit_Module(self, node):
        self.module_statements = {id(statement) for statement in node.body}
        self.generic_visit(node)

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
            self.aliases[item.asname or item.name] = f"{node.module or ''}.{item.name}".lstrip(".")

    def deref(self, node):
        if isinstance(node, ast.Name) and node.id in self.bindings:
            return self.bindings[node.id]
        return node

    def literal(self, node):
        node = self.deref(node)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        return None

    def prompt(self, node, name, text):
        self.prompts.append({"line": node.lineno, "name": name, "sha256": digest(text), "chars": len(text)})
        self.add(node, "prompt_literal", name)

    def visit_Assign(self, node):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target = node.targets[0].id
            self.bindings[target] = node.value
            text = self.literal(node.value)
            if text is not None and id(node) in self.module_statements:
                self.constants[target] = text
            if text is not None and (PROMPT_NAME.search(target) or (self.is_prompt_module and target.isupper() and len(text) >= 40)):
                self.prompt(node, target, text)
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and id(node) not in self.judge_nodes:
            model = model_in(node.value)
            if model:
                self.add(node, "model_string", model)
                self.add(node, "model_alias" if classify(model) == "alias" else "model_pinned", model)
            for match in SECRET_VERSION.finditer(node.value):
                self.add(node, "secret_version_alias" if match.group(1) == "latest" else "secret_version_pinned",
                         "versions/latest" if match.group(1) == "latest" else "versions/<n>")
        self.generic_visit(node)

    def model_argument(self, node, value, short):
        """Classify model=: literal, resolved constant, deferred reference or dynamic.

        A Name bound to a string constant in this module resolves here. An
        imported name or module attribute (`config.AGENT_MODEL`) is deferred and
        resolved against module-level constants of the scanned files. Subscripts,
        function calls and other expressions are model_dynamic; a capitalised
        call (`Gemini(...)`, `LiteLlm(...)`) is a model object inspected on its own.
        """
        text = self.literal(value)
        if text is not None:
            if isinstance(value, (ast.Name, ast.Attribute)):
                self.resolved_model(node, text)
            return
        target = self.deref(value)
        if isinstance(target, (ast.Name, ast.Attribute)):
            self.deferred_models.append((node.lineno, self.name(target).lstrip(".")))
            return
        if isinstance(target, ast.Call):
            callee = self.name(target.func).rsplit(".", 1)[-1]
            if callee[:1].isupper():
                return
        self.add(node, "model_dynamic", short or None)

    def resolved_model(self, node, text):
        self.add(node, "model_reference_resolved", text)
        model = model_in(text)
        if model and model == text:
            self.add(node, "model_alias" if classify(model) == "alias" else "model_pinned", model)

    def visit_Dict(self, node):
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant) and key.value == "judge_model":
                self.judge(node, value)
        self.generic_visit(node)

    def judge(self, node, value_node):
        value = self.literal(value_node)
        if value is not None:
            self.judge_nodes.add(id(self.deref(value_node)))
        if value is None:
            self.add(node, "judge_model_dynamic")
            return
        self.add(node, "judge_model", value)
        if value == RETIRING_DEFAULT_JUDGE:
            self.add(node, "judge_model_retiring_default", value)
        elif classify(value) == "alias":
            self.add(node, "judge_model_alias", value)
        else:
            self.add(node, "judge_model_pinned", value)

    def visit_Call(self, node):
        callee = self.name(node.func)
        kwargs = {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg}
        short = callee.rsplit(".", 1)[-1]
        if short == "JudgeModelOptions":
            if "judge_model" in kwargs:
                self.judge(node, kwargs["judge_model"])
            else:
                self.add(node, "judge_model_unset", RETIRING_DEFAULT_JUDGE)
        elif short in JUDGE_CRITERIA and "judge_model_options" not in kwargs:
            self.add(node, "judge_model_unset", RETIRING_DEFAULT_JUDGE)
        if short in ("LlmAgent", "Agent") or callee.endswith((".LlmAgent", ".Agent")):
            if "model" not in kwargs:
                self.add(node, "agent_model_unset_default", "LlmAgent.DEFAULT_MODEL")
            for field in ("instruction", "global_instruction"):
                if field in kwargs:
                    value = kwargs[field]
                    text = self.literal(value)
                    if isinstance(value, (ast.Name, ast.Attribute)):
                        self.add(node, "prompt_reference", f"{field}={self.name(value)}")
                    elif text is not None:
                        self.prompt(node, field, text)
                    else:
                        self.add(node, "prompt_dynamic", field)
        if "model" in kwargs:
            self.model_argument(node, kwargs["model"], short)
        if callee.endswith(("AgentEvaluator.evaluate", "AgentEvaluator.evaluate_eval_set")):
            runs = self.deref(kwargs.get("num_runs")) if "num_runs" in kwargs else None
            detail = runs.value if isinstance(runs, ast.Constant) else ("dynamic" if runs is not None else "default")
            self.add(node, "agent_evaluator_call", f"num_runs={detail}")
            if "output_file" not in kwargs:
                self.add(node, "agent_evaluator_without_output_file")
        self.generic_visit(node)


class Inventory:
    def __init__(self, args, lifecycle):
        self.args = args
        self.lifecycle = lifecycle
        self.result = {"schema_version": 1, "read_only": True, "changes_made": False,
                       "dry_run": args.dry_run, "partial": False, "files_inspected": 0,
                       "directory_entries_seen": 0,
                       "limits": {"max_files": args.max_files, "max_bytes_per_file": args.max_bytes,
                                  "max_depth": args.max_depth, "max_entries": args.max_entries,
                                  "excluded_directories": sorted(EXCLUDED),
                                  "sensitive_files_excluded": True, "symlinks_followed": False,
                                  "prompt_text_emitted": False},
                       "dependencies": [], "signals": [], "issues": [], "skipped": [],
                       "manifest": {"components": {}}}
        self.models = {}
        self.judges = {}
        self.prompts = []
        self.eval_sets = []
        self.eval_configs = []
        self.deploy = {"dockerfiles": [], "cloudbuild": [], "github_workflows": [], "conformance_specs": 0}
        self.secret_refs = {"pinned": 0, "latest": 0}
        self.seen = 0
        self.stopped = False
        self.constants = {}
        self.deferred_models = []

    def issue(self, path, reason):
        self.result["partial"] = True
        self.result["issues"].append({"path": path, "reason": reason})

    def signal(self, path, label, detail=None, line=None):
        row = {"path": path, "signal": label}
        if line is not None:
            row["line"] = line
        if detail is not None:
            row["detail"] = detail
        self.result["signals"].append(row)

    def model(self, path, model):
        entry = self.models.setdefault(model, {"id": model, "classification": classify(model), "locations": 0})
        entry["locations"] += 1
        if self.lifecycle is not None and "lifecycle_status" not in entry:
            table = self.lifecycle.get("models", {}).get(model)
            entry["lifecycle_status"] = table.get("status") if isinstance(table, dict) else "not_in_table"

    def dependency(self, path, name, value):
        name = name.lower().replace("_", "-")
        if name not in PACKAGES:
            return
        if isinstance(value, dict):
            value = None if any(k in value for k in ("git", "url", "path")) else value.get("version")
        constraint = re.sub(r"\s+", "", value) if isinstance(value, str) else ""
        valid = bool(VERSION.fullmatch(constraint))
        pinned = valid and constraint.startswith("==") and not constraint.startswith("===")
        self.result["dependencies"].append({"path": path, "name": name,
                                            "constraint": constraint if valid else None,
                                            "status": "parsed" if valid else "redacted",
                                            "exact_pin": pinned})

    def requirement(self, path, line):
        match = REQUIREMENT.match(line.split("#", 1)[0].strip())
        if match:
            name, value = match.groups()
            self.dependency(path, name, value.split(";", 1)[0].strip())

    def text_scan(self, relative, content):
        for command, label in TEXT_COMMANDS.items():
            if command in content:
                self.signal(relative, label)
        for model in sorted(set(GEMINI.findall(content))):
            self.model(relative, model)
            self.signal(relative, "model_alias" if classify(model) == "alias" else "model_pinned", model)
        for match in SECRET_VERSION.finditer(content):
            self.secret(relative, match.group(1))
        for match in SET_SECRETS.finditer(content):
            self.secret(relative, match.group(2))
        for match in re.finditer(r"judge_model\W+(gemini-[A-Za-z0-9.-]*[A-Za-z0-9])", content):
            self.judge(relative, match.group(1))

    def secret(self, relative, version):
        if version == "latest":
            self.secret_refs["latest"] += 1
            self.signal(relative, "secret_version_alias", "versions/latest")
        else:
            self.secret_refs["pinned"] += 1
            self.signal(relative, "secret_version_pinned", "versions/<n>")

    def judge(self, relative, value, line=None):
        self.judges[value] = self.judges.get(value, 0) + 1
        self.signal(relative, "judge_model", value, line)
        if value == RETIRING_DEFAULT_JUDGE:
            self.signal(relative, "judge_model_retiring_default", value, line)
        elif classify(value) == "alias":
            self.signal(relative, "judge_model_alias", value, line)
        else:
            self.signal(relative, "judge_model_pinned", value, line)

    def eval_json(self, relative, content, kind):
        document = json.loads(content)
        if kind == "legacy_test_json" or (isinstance(document, list) and document and isinstance(document[0], dict) and "query" in document[0]):
            self.signal(relative, "eval_legacy_test_json", "migrate with AgentEvaluator.migrate_eval_data_to_new_schema")
            self.eval_sets.append({"path": relative, "format": "legacy_test_json", "sha256": digest(content),
                                   "cases": len(document) if isinstance(document, list) else None})
            return
        if isinstance(document, dict) and "eval_cases" in document:
            cases = document.get("eval_cases") if isinstance(document.get("eval_cases"), list) else []
            ids = [case.get("eval_id") for case in cases if isinstance(case, dict)]
            self.eval_sets.append({"path": relative, "format": "evalset", "eval_set_id": document.get("eval_set_id"),
                                   "cases": len(cases), "sha256": digest(content)})
            self.signal(relative, "eval_set", document.get("eval_set_id"))
            if len(set(ids)) != len(ids):
                self.signal(relative, "eval_set_duplicate_case_ids")
            if not cases:
                self.signal(relative, "eval_set_empty")
            return
        if isinstance(document, dict) and isinstance(document.get("criteria"), dict):
            criteria = document["criteria"]
            judged = []
            for metric, criterion in criteria.items():
                if isinstance(criterion, dict):
                    options = criterion.get("judge_model_options") or criterion.get("judgeModelOptions")
                    if isinstance(options, dict) and isinstance(options.get("judge_model"), str):
                        self.judge(relative, options["judge_model"])
                        judged.append(metric)
                        if "num_samples" not in options and "numSamples" not in options:
                            self.signal(relative, "judge_num_samples_default", metric)
                    elif metric in JUDGE_METRICS:
                        self.signal(relative, "judge_model_unset", f"{metric} -> {RETIRING_DEFAULT_JUDGE}")
                elif metric in JUDGE_METRICS:
                    self.signal(relative, "judge_model_unset", f"{metric} -> {RETIRING_DEFAULT_JUDGE}")
            self.eval_configs.append({"path": relative, "criteria": sorted(criteria), "judged_metrics": sorted(judged),
                                      "sha256": digest(content)})
            self.signal(relative, "eval_config", ",".join(sorted(criteria)))
            return
        if kind == "eval_config":
            self.signal(relative, "eval_config_without_criteria")

    def inspect(self, path, relative, kind):
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
            if not raw and kind in ("evalset", "legacy_test_json", "eval_config", "json"):
                # A zero-byte JSON file is usually a report being written into the
                # scanned tree (for example `> inventory.json`); it holds no references.
                self.result["skipped"].append({"path": relative, "reason": "skipped_empty"})
                return
            content = raw.decode("utf-8")
            if kind == "python":
                visitor = Signals(Path(relative).stem in {"prompt", "prompts", "instructions", "instruction"})
                visitor.visit(ast.parse(content))
                for line, label, detail in sorted(visitor.rows, key=lambda row: (row[0], row[1], str(row[2]))):
                    if label == "model_string":
                        self.model(relative, detail)
                        continue
                    if label == "judge_model":
                        self.judges[detail] = self.judges.get(detail, 0) + 1
                    elif label.startswith("secret_version_"):
                        self.secret_refs["latest" if label.endswith("alias") else "pinned"] += 1
                    self.signal(relative, label, detail, line)
                for item in visitor.prompts:
                    self.prompts.append({"path": relative, **item})
                self.constants[relative] = visitor.constants
                self.deferred_models.extend((relative, line, name) for line, name in visitor.deferred_models)
                if "adk eval" in content or "adk conformance" in content:
                    self.text_scan(relative, content)
            elif kind == "pyproject":
                document = tomllib.loads(content)
                for name in document.get("project", {}).get("dependencies", []):
                    self.requirement(relative, name)
                for group in document.get("project", {}).get("optional-dependencies", {}).values():
                    for name in group:
                        self.requirement(relative, name)
                poetry = document.get("tool", {}).get("poetry", {})
                for section in (poetry.get("dependencies", {}), *(g.get("dependencies", {}) for g in poetry.get("group", {}).values())):
                    for name, value in section.items():
                        self.dependency(relative, name, value)
            elif kind == "requirements":
                for line in content.splitlines():
                    self.requirement(relative, line)
            elif kind in ("evalset", "legacy_test_json", "eval_config", "json"):
                self.eval_json(relative, content, kind)
            elif kind == "prompt_file":
                self.prompts.append({"path": relative, "name": Path(relative).name, "sha256": digest(content), "chars": len(content)})
                self.signal(relative, "prompt_file")
            else:
                if kind == "dockerfile":
                    self.deploy["dockerfiles"].append(relative)
                elif kind == "cloudbuild":
                    self.deploy["cloudbuild"].append(relative)
                elif kind == "github_workflow":
                    self.deploy["github_workflows"].append(relative)
                elif kind == "conformance_spec":
                    self.deploy["conformance_specs"] += 1
                if kind in ("dockerfile", "cloudbuild", "github_workflow", "conformance_spec"):
                    self.signal(relative, f"{kind}_present")
                self.text_scan(relative, content)
            self.result["files_inspected"] += 1
        except (OSError, UnicodeError):
            self.issue(relative, "unreadable_file")
        except (SyntaxError, ValueError, TypeError, AttributeError, RecursionError, KeyError):
            self.issue(relative, "malformed_file")

    def walk(self, directory, prefix="", depth=0, parents=frozenset()):
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
                    self.walk(path, relative, depth + 1, parents | {path.name.lower()})
                    if self.stopped:
                        return
            else:
                kind = kind_of(relative, path.name, parents)
                if kind is None:
                    continue
                if self.seen >= self.args.max_files:
                    self.issue(relative, "file_count_limit")
                    self.stopped = True
                    return
                self.seen += 1
                self.inspect(path, relative, kind)

    def resolve_models(self):
        """Resolve deferred model= references to module-level string constants in scanned files."""
        for relative, line, name in self.deferred_models:
            parts = [part for part in name.split(".") if part]
            value = None
            if len(parts) > 1:
                for path in sorted(self.constants):
                    if module_matches(path, parts[-2]) and parts[-1] in self.constants[path]:
                        value = self.constants[path][parts[-1]]
                        break
            if value is None:
                self.signal(relative, "model_reference_unresolved", name, line)
                continue
            self.signal(relative, "model_reference_resolved", value, line)
            model = model_in(value)
            if model and model == value:
                self.signal(relative, "model_alias" if classify(model) == "alias" else "model_pinned", model, line)

    def finish(self):
        self.resolve_models()
        unset = [row for row in self.result["signals"] if row["signal"] == "judge_model_unset"]
        pins = {d["name"]: d["constraint"] for d in self.result["dependencies"] if d["constraint"]}
        components = {
            "adk_version": {"version": pins.get("google-adk", "unknown"),
                            "exact_pin": any(d["exact_pin"] for d in self.result["dependencies"] if d["name"] == "google-adk")},
            "dependency_pins": {name: pins.get(name, "unknown") for name in sorted(PACKAGES)},
            "agent_models": sorted(self.models.values(), key=lambda m: m["id"]) or "unknown",
            "judge_models": ([{"id": name, "locations": count, "classification": "retiring_default" if name == RETIRING_DEFAULT_JUDGE else classify(name)}
                              for name, count in sorted(self.judges.items())]
                             + ([{"id": RETIRING_DEFAULT_JUDGE, "locations": len(unset), "classification": "unset_default"}] if unset else [])) or "unknown",
            "prompts": sorted(self.prompts, key=lambda p: (p["path"], p.get("line", 0), p["name"])) or "unknown",
            "tool_schema_hash": "unknown",
            "eval_sets": sorted(self.eval_sets, key=lambda e: e["path"]) or "unknown",
            "eval_configs": sorted(self.eval_configs, key=lambda e: e["path"]) or "unknown",
            "deploy_configs": {key: (sorted(value) if isinstance(value, list) else value) for key, value in self.deploy.items()},
            "deploy_reference": {"image_digest": "unknown", "cloud_run_revision": "unknown", "agent_runtime_revision": "unknown"},
            "secret_versions": {"pinned_references": self.secret_refs["pinned"], "latest_references": self.secret_refs["latest"], "versions": "unknown"},
        }
        self.result["manifest"] = {"components": components,
                                   "note": "Skeleton from static inspection. Fill unknown fields from the build and deploy system; verify hashes against the running revision."}
        for field in ("dependencies", "signals", "issues", "skipped"):
            self.result[field].sort(key=lambda item: json.dumps(item, sort_keys=True))


def load_lifecycle(path, parser):
    if path is None:
        return None
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
    parser = argparse.ArgumentParser(description=__doc__, epilog="Reads bounded source, manifests, eval assets and deploy files; skips secrets, dependency directories and symlinks. Prompt text is reported as sha256 only. Signals direct inspection and are not a verdict on provider or platform behaviour. Exit 0: complete scan; 1: partial scan; 2: bad arguments.")
    parser.add_argument("--project", required=True, help="project directory to inspect without executing code")
    parser.add_argument("--dry-run", action="store_true", help="perform the same read-only scan and report no changes")
    parser.add_argument("--lifecycle", type=Path, default=None, help="optional model lifecycle JSON table (same shape as adk-model-and-output-contracts' assets/model-lifecycle-*.json) to annotate model IDs with a status")
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
    inventory = Inventory(args, load_lifecycle(args.lifecycle, parser))
    inventory.walk(root)
    inventory.finish()
    print(json.dumps(inventory.result, indent=2, sort_keys=True))
    return 1 if inventory.result["partial"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
