#!/usr/bin/env python3
"""Inspect deployment evidence without executing project code or cloud commands."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys

if sys.version_info < (3, 11):
    print("inspect_project requires Python 3.11 or newer; select a compatible interpreter.", file=sys.stderr)
    raise SystemExit(2)

import tomllib


BASELINE = {"google-adk": "2.8.0", "google-cloud-aiplatform": "1.153.1"}
LIMITS = {"depth": 4, "directory_entries": 4096, "manifests": 64,
          "bytes_per_manifest": 131072, "total_manifest_bytes": 1048576,
          "requirement_line_characters": 4096}
SKIP_DIRS = {"node_modules", "venv", "env", "__pycache__", "dist", "build"}
VERSION = r"[0-9]+(?:\.[0-9]+)*(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"
SPEC = re.compile(rf"(?:===|==|!=|~=|<=|>=|<|>|\^|~){VERSION}(?:\.\*)?")
NAME = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[A-Za-z0-9,_. -]+\])?(.*)$")
APIS = {
    "cloud-run": ["aiplatform.googleapis.com", "artifactregistry.googleapis.com",
                  "cloudbuild.googleapis.com", "iam.googleapis.com", "run.googleapis.com",
                  "serviceusage.googleapis.com", "storage.googleapis.com"],
    "agent-runtime": ["aiplatform.googleapis.com", "iam.googleapis.com",
                      "serviceusage.googleapis.com", "storage.googleapis.com"],
    "gke": ["aiplatform.googleapis.com", "artifactregistry.googleapis.com",
            "cloudbuild.googleapis.com", "compute.googleapis.com", "container.googleapis.com",
            "iam.googleapis.com", "serviceusage.googleapis.com", "storage.googleapis.com"],
}


class InspectionError(Exception):
    """Errors contain fixed messages, never project source or filenames."""


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse normally echoes invalid choices and unknown arguments.
        self.print_usage(sys.stderr)
        self.exit(2, "inspect_project: invalid arguments; see --help (values omitted).\n")


def safe_spec(value):
    """Return only an allowlisted numeric version expression, never a URL."""
    if not isinstance(value, str) or len(value) > 256:
        return None
    value = re.sub(r"\s+", "", value)
    parts = value.split(",")
    return value if parts and all(SPEC.fullmatch(part) for part in parts) else None


class Inspector:
    def __init__(self, root):
        self.root = root
        self.visited = set()
        self.total_bytes = 0
        self.entries = 0
        self.skipped_symlinks = 0
        self.depth_limited = False
        self.manifests = []
        self.declarations = {name: [] for name in BASELINE}
        self.python_requirements = []
        self.python_version_pins = []
        self.managers = set()
        self.signals = set()
        self.config = {"dotenv": False, "dotenv_example": False,
                       "dockerfile": False, "cloudbuild_yaml": False,
                       "kubernetes_named_yaml": False}

    def regular_path(self, path):
        """Reject symlinks in every project-relative component before opening."""
        try:
            relative = path.relative_to(self.root)
            current = self.root
            for part in relative.parts:
                current = current / part
                if stat.S_ISLNK(current.lstat().st_mode):
                    raise InspectionError("A referenced manifest crosses a symlink; contents were not read.")
            if not stat.S_ISREG(path.lstat().st_mode):
                raise InspectionError("A referenced manifest is not a regular file.")
        except (OSError, ValueError):
            raise InspectionError("A referenced manifest is missing or unreadable.") from None

    def read(self, path):
        self.regular_path(path)
        try:
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            with os.fdopen(os.open(path, flags), "rb") as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise InspectionError("A referenced manifest is not a regular file.")
                data = stream.read(LIMITS["bytes_per_manifest"] + 1)
        except OSError:
            raise InspectionError("A manifest could not be read.") from None
        self.total_bytes += len(data)
        if len(data) > LIMITS["bytes_per_manifest"] or self.total_bytes > LIMITS["total_manifest_bytes"]:
            raise InspectionError("Manifest byte limit exceeded; select a narrower project root.")
        try:
            return data.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise InspectionError("A manifest is not valid UTF-8.") from None

    def add_requirement(self, value, source, scope="runtime"):
        if not isinstance(value, str):
            raise InspectionError("A dependency declaration has an unsupported data type.")
        if len(value) > LIMITS["requirement_line_characters"]:
            raise InspectionError("Requirement line limit exceeded.")
        match = NAME.match(value.strip())
        if not match:
            return
        name = re.sub(r"[-_.]+", "-", match.group(1)).lower()
        if name not in BASELINE:
            return
        tail, separator, _marker = match.group(2).partition(";")
        tail = tail.strip()
        if tail.startswith("(") and tail.endswith(")"):
            tail = tail[1:-1].strip()
        item = {"source": source, "scope": scope, "conditional": bool(separator)}
        if tail.startswith("@"):
            item["kind"] = "direct_reference"
        elif not tail or tail == "*":
            item["kind"] = "unconstrained"
        elif re.fullmatch(rf"=={VERSION}", re.sub(r"\s+", "", tail)):
            item.update(kind="exact_pin", version=re.sub(r"\s+", "", tail)[2:])
        elif safe_spec(tail):
            item.update(kind="range", specifier=safe_spec(tail))
        else:
            item["kind"] = "unparsed"
        self.declarations[name].append(item)

    def add_python(self, value, source):
        if not isinstance(value, str):
            raise InspectionError("A Python requirement has an unsupported data type.")
        expression = safe_spec(value)
        self.python_requirements.append({"source": source,
                                         "status": "declared" if expression else "unparsed",
                                         **({"specifier": expression} if expression else {})})

    def python_version_file(self, content, source):
        """Report only numeric declarations; named environments and paths stay private."""
        versions = [line.strip() for line in content.splitlines() if line.strip()]
        parsed = bool(versions) and all(
            len(value) <= 32 and re.fullmatch(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?", value)
            for value in versions
        )
        self.python_version_pins.append({"source": source,
                                         "status": "declared" if parsed else "unparsed",
                                         **({"versions": versions} if parsed else {})})

    def manifest(self, path, kind):
        if path in self.visited:
            return
        if len(self.visited) >= LIMITS["manifests"]:
            raise InspectionError("Manifest count limit exceeded; select a narrower project root.")
        self.visited.add(path)
        source = f"manifest-{len(self.visited):03d}"
        self.manifests.append({"id": source, "kind": kind,
                               "location": "root" if path.parent == self.root else "nested"})
        content = self.read(path)
        if kind == "python-version":
            self.python_version_file(content, source)
            return
        if kind == "pyproject":
            try:
                document = tomllib.loads(content)
            except tomllib.TOMLDecodeError:
                raise InspectionError("A pyproject manifest contains invalid TOML.") from None
            self.pyproject(document, source)
            return
        self.managers.add("pip-requirements")
        for raw in content.splitlines():
            if len(raw) > LIMITS["requirement_line_characters"]:
                raise InspectionError("Requirement line limit exceeded.")
            line = re.split(r"\s+#", raw.strip(), maxsplit=1)[0].strip()
            if not line or line.startswith("#"):
                continue
            include = re.match(r"^(?:(-r|-c)\s*|(--requirement|--constraint)(?:=|\s+))(.+)$", line)
            if include:
                option = include.group(1) or include.group(2)
                value = include.group(3).strip().strip("\"'")
                include_kind = "constraints" if option in {"-c", "--constraint"} or kind == "constraints" else "requirements"
                self.include(path, value, include_kind)
            elif line.startswith(("-r", "--requirement", "-c", "--constraint")):
                raise InspectionError("A requirements include is malformed.")
            elif line.endswith("\\"):
                raise InspectionError("Continued requirements lines are unsupported; inspect the declaration manually.")
            elif not line.startswith("-"):
                self.add_requirement(line, source, "constraint" if kind == "constraints" else "runtime")

    def include(self, parent, value, kind):
        # Only local requirement files can be opened; no URLs, .env files, or traversal outside root.
        if not value or "\x00" in value or ":" in value or "\\" in value or Path(value).is_absolute():
            raise InspectionError("A requirements include is not an allowed local path.")
        candidate = Path(os.path.abspath(parent.parent / value))
        if (not candidate.is_relative_to(self.root) or candidate.suffix not in {".txt", ".in"}
                or candidate.name.startswith(".env")):
            raise InspectionError("A requirements include is outside the root or has an unsupported file type.")
        self.manifest(candidate, kind)

    def pyproject(self, document, source):
        project = document.get("project", {})
        tool = document.get("tool", {})
        if not isinstance(project, dict) or not isinstance(tool, dict):
            raise InspectionError("A pyproject manifest has an invalid project or tool table.")
        self.managers.add("pyproject")
        dependencies = project.get("dependencies", [])
        if not isinstance(dependencies, list):
            raise InspectionError("A pyproject dependencies field is not an array.")
        for value in dependencies:
            self.add_requirement(value, source)
        optional = project.get("optional-dependencies", {})
        if not isinstance(optional, dict):
            raise InspectionError("A pyproject optional dependency field is not a table.")
        for values in optional.values():
            if not isinstance(values, list):
                raise InspectionError("A pyproject optional dependency group is not an array.")
            for value in values:
                self.add_requirement(value, source, "optional")
        if "requires-python" in project:
            self.add_python(project["requires-python"], source)
        for manager in ("poetry", "uv", "pdm", "hatch"):
            if manager in tool:
                self.managers.add(manager)
        poetry = tool.get("poetry", {})
        if not isinstance(poetry, dict):
            raise InspectionError("A Poetry configuration is not a table.")
        values = poetry.get("dependencies", {})
        if not isinstance(values, dict):
            raise InspectionError("A Poetry dependencies field is not a table.")
        for name, value in values.items():
            normalized = re.sub(r"[-_.]+", "-", name).lower()
            if normalized == "python":
                self.add_python(value, source)
            elif normalized in BASELINE:
                if isinstance(value, str):
                    suffix = "==" + value if re.fullmatch(VERSION, value) else value
                    self.add_requirement(normalized + suffix, source)
                else:
                    self.declarations[normalized].append({"source": source, "scope": "runtime",
                                                          "conditional": False, "kind": "unparsed"})

    def scan(self, directory=None, depth=0):
        directory = self.root if directory is None else directory
        try:
            with os.scandir(directory) as listing:
                entries = []
                for entry in listing:
                    self.entries += 1
                    if self.entries > LIMITS["directory_entries"]:
                        raise InspectionError("Directory entry limit exceeded; select a narrower project root.")
                    entries.append(entry)
            for entry in sorted(entries, key=lambda item: item.name):
                if entry.is_symlink():
                    self.skipped_symlinks += 1
                    continue
                name = entry.name
                if entry.is_dir(follow_symlinks=False):
                    if name.startswith(".") or name in SKIP_DIRS:
                        continue
                    if name in {"k8s", "kubernetes", "gke"}:
                        self.signals.add("kubernetes_directory")
                    if name in {"agent-engine", "agent-runtime"}:
                        self.signals.add("agent_runtime_directory")
                    if name == "cloud-run":
                        self.signals.add("cloud_run_directory")
                    if depth < LIMITS["depth"]:
                        self.scan(Path(entry.path), depth + 1)
                    else:
                        self.depth_limited = True
                elif entry.is_file(follow_symlinks=False):
                    path = Path(entry.path)
                    if name == "pyproject.toml":
                        self.manifest(path, "pyproject")
                    elif name == ".python-version":
                        self.manifest(path, "python-version")
                    elif re.fullmatch(r"requirements[\w.-]*\.(?:txt|in)", name):
                        self.manifest(path, "requirements")
                    for filename, manager in {"uv.lock": "uv", "poetry.lock": "poetry",
                                              "Pipfile": "pipenv", "Pipfile.lock": "pipenv",
                                              "pdm.lock": "pdm"}.items():
                        if name == filename:
                            self.managers.add(manager)
                    if name == ".env":
                        self.config["dotenv"] = True
                    if name in {".env.example", ".env.sample", ".env.template"}:
                        self.config["dotenv_example"] = True
                    if name == "Dockerfile":
                        self.config["dockerfile"] = True
                        self.signals.add("container_build")
                    if name in {"cloudbuild.yaml", "cloudbuild.yml"}:
                        self.config["cloudbuild_yaml"] = True
                    if name in {"deployment.yaml", "deployment.yml", "service.yaml", "service.yml", "k8s.yaml", "k8s.yml"}:
                        self.config["kubernetes_named_yaml"] = True
                        self.signals.add("kubernetes_manifest_name")
        except OSError:
            raise InspectionError("A project directory could not be inspected.") from None


def compatibility(inspector, mode):
    required = ["google-adk"]
    if mode == "agent-runtime" or (mode == "auto" and inspector.declarations["google-cloud-aiplatform"]):
        required.append("google-cloud-aiplatform")
    result = {}
    for name, expected in BASELINE.items():
        declarations = inspector.declarations[name]
        pins = sorted({item["version"] for item in declarations if item["kind"] == "exact_pin"})
        reasons = []
        if not declarations:
            reasons.append("no_declaration_found")
        if any(item["kind"] != "exact_pin" for item in declarations):
            reasons.append("declaration_not_an_exact_pin")
        if any(item["conditional"] or item["scope"] == "optional" for item in declarations):
            reasons.append("conditional_or_optional_declaration_requires_review")
        if declarations and all(item["scope"] == "constraint" for item in declarations):
            reasons.append("only_constraint_declarations_found")
        if any(pin != expected for pin in pins):
            reasons.append("different_from_recorded_baseline")
        if len(pins) > 1:
            reasons.append("conflicting_exact_pins")
        if inspector.depth_limited:
            reasons.append("inspection_depth_limit_reached")
        result[name] = {"required_for_selected_mode": name in required,
                        "recorded_baseline": expected,
                        "status": "unverified" if reasons else "matches_recorded_baseline",
                        "reasons": reasons, "exact_pins": pins, "declarations": declarations}
    return result, all(result[name]["status"] == "matches_recorded_baseline" for name in required)


def cloud_plan(args):
    if not args.project:
        return []
    common = [f"--account={args.account}", f"--project={args.project}",
              f"--billing-project={args.project}", "--quiet", "--format=json"]
    plan = [
        ("project_access", ["projects", "describe", args.project]),
        ("billing_status", ["billing", "projects", "describe", args.project]),
        ("enabled_apis", ["services", "list", "--enabled"]),
    ]
    if args.mode in {"cloud-run", "gke"}:
        plan.append(("build_identity", ["builds", "get-default-service-account", f"--region={args.region}"]))
    return [{"purpose": purpose, "argv": ["gcloud", *command, *common], "executed": False}
            for purpose, command in plan]


def main(argv=None):
    parser = SafeParser(description=__doc__, epilog=(
        "Always offline and read-only: no cloud commands, installs, imports of project code, or writes. "
        "JSON reports declarations, not installed versions or proven compatibility. Lockfiles and .env contents "
        "are never read. Numeric .python-version pins are separate from this tool's interpreter and Python constraints. "
        "Filename hints do not establish an architecture. Exit 0: inspection completed "
        "(possibly unverified); 2: invalid input, unreadable/invalid manifest, or exceeded hard limit; "
        "3: --require-baseline evidence gate not met. Use a stable project tree during inspection."))
    parser.add_argument("--root", required=True, help="Project directory; inspect bounded nonsymlink manifests beneath it.")
    parser.add_argument("--mode", choices=("auto", "cloud-run", "agent-runtime", "gke"), default="auto")
    parser.add_argument("--dry-run", action="store_true", help="Explicit synonym for the default offline, read-only inspection.")
    parser.add_argument("--require-baseline", action="store_true", help="Exit 3 unless required packages have unconditional exact recorded pins.")
    parser.add_argument("--project", help="Validated GCP project ID for planned read-only argv only; requires region, account, explicit mode.")
    parser.add_argument("--region", help="Regional deployment location for the plan; global is not a hosting region.")
    parser.add_argument("--account", help="Explicit email identity for the plan; never inferred from gcloud configuration.")
    args = parser.parse_args(argv)
    target_values = (args.project, args.region, args.account)
    if any(value is not None for value in target_values):
        if not all(target_values) or args.mode == "auto":
            parser.error("Complete explicit target required")
        if not re.fullmatch(r"[a-z][a-z0-9-]{4,28}[a-z0-9]", args.project):
            parser.error("Invalid project")
        if not re.fullmatch(r"[a-z]+-[a-z]+[0-9]+", args.region):
            parser.error("Invalid region")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+%-]{0,127}@[A-Za-z0-9](?:[A-Za-z0-9.-]{0,189})\.[A-Za-z]{2,24}", args.account):
            parser.error("Invalid account")
    try:
        supplied_root = Path(args.root).expanduser()
        if supplied_root.is_symlink() or not supplied_root.is_dir():
            raise InspectionError("Root must be an existing nonsymlink directory.")
        inspector = Inspector(supplied_root.resolve(strict=True))
        inspector.scan()
        packages, baseline_ok = compatibility(inspector, args.mode)
        required_tools = ["gcloud"] + (["kubectl", "gke-gcloud-auth-plugin"] if args.mode == "gke" else [])
        result = {
            "operation": "offline_read_only_inspection", "mode": args.mode,
            "network_calls": 0, "writes": 0,
            "python": {"interpreter": ".".join(map(str, sys.version_info[:3])),
                       "declared_requirements": inspector.python_requirements,
                       "version_pins": inspector.python_version_pins,
                       "requirement_satisfaction": "not_evaluated"},
            "package_manager_indicators": sorted(inspector.managers),
            "manifests": inspector.manifests,
            "packages": packages,
            "baseline_gate_passed": baseline_ok,
            "configuration_file_presence": inspector.config,
            "architecture_hints": sorted(inspector.signals),
            "prerequisites": {tool: {"available_on_path": bool(shutil.which(tool)),
                                     "required_for_selected_mode": tool in required_tools}
                              for tool in ("gcloud", "kubectl", "gke-gcloud-auth-plugin", "docker", "uv", "git")},
            "api_candidates_to_review": APIS.get(args.mode, []),
            "planned_read_only_cloud_commands": cloud_plan(args),
            "coverage": {"limits": LIMITS, "directory_entries_examined": inspector.entries,
                         "manifest_bytes_read": inspector.total_bytes,
                         "symlinks_skipped": inspector.skipped_symlinks,
                         "depth_limit_reached": inspector.depth_limited},
            "limitations": [
                "Observed declarations are not installed versions; no project code, lockfile content, or dotenv content was read.",
                "Matching the recorded baseline does not prove dependency resolution, Python compatibility, IAM, billing, API, model, or regional access.",
                "Different, missing, ranged, conditional, or unsupported declarations require validation; they are not declared incompatible.",
                "Only PEP 621 and basic Poetry dependency declarations plus local requirements/constraints files are parsed; other installer options and dependency formats require manual review.",
                "Python version pins report only numeric major.minor[.patch] declarations from .python-version; named environments, paths and other forms are unparsed with values omitted. No interpreter is selected or compatibility evaluated.",
                "Hidden/build/environment directories are skipped; inspection is bounded, excludes symlinks, and assumes files are not concurrently replaced.",
                "Architecture hints and API candidates are incomplete evidence, not deployment configuration or an authorization to deploy.",
            ],
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 3 if args.require_baseline and not baseline_ok else 0
    except (InspectionError, OSError, ValueError) as error:
        message = str(error) if isinstance(error, InspectionError) else "Project inspection failed; input details omitted."
        print(json.dumps({"error": message, "network_calls": 0, "writes": 0}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
