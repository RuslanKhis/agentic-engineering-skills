#!/usr/bin/env python3
"""Inventory ADK application, Cloud Run, Agent Runtime and GKE optimisation inputs offline."""
# Adapted from deploy-adk-on-google-cloud. Copyright (c) 2026 RuslanKhis.
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import sys

if sys.version_info < (3, 11):
    print("inspect_project requires Python 3.11 or newer; select a compatible interpreter.", file=sys.stderr)
    raise SystemExit(2)

import tomllib


BASELINE = {"google-adk": "2.8.0"}
AGENT_RUNTIME_BASELINE = {**BASELINE, "google-cloud-aiplatform": "1.153.1",
                          "google-genai": "2.19.0"}
# GKE's recorded requirements leave GenAI transitive; do not impose another mode's pin.
GKE_BASELINE = {**BASELINE, "google-cloud-aiplatform": "1.153.1"}
TRACKED_PACKAGES = ("google-adk", "google-genai", "google-cloud-aiplatform", "google-cloud-bigquery",
                    "google-cloud-storage", "pydantic", "pandas", "aiohttp", "sqlglot")
LIMITS = {"depth": 4, "directory_entries": 4096, "manifests": 64,
          "bytes_per_manifest": 131072, "total_manifest_bytes": 1048576,
          "requirement_line_characters": 4096}
SKIP_DIRS = {"node_modules", "venv", "env", "__pycache__", "dist", "build"}
VERSION = r"[0-9]+(?:\.[0-9]+)*(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"
SPEC = re.compile(rf"(?:===|==|!=|~=|<=|>=|<|>|\^|~){VERSION}(?:\.\*)?")
NAME = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[([A-Za-z0-9,_. -]+)\])?(.*)$")



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


def known_aiplatform_extras(values):
    """Report allowlisted compatibility signals, never arbitrary extra names."""
    if not isinstance(values, list):
        values = []
    normalised = {re.sub(r"[-_.]+", "-", value.strip()).lower()
                  for value in values if isinstance(value, str)}
    return {"adk": "adk" in normalised,
            "agent_engines": "agent-engines" in normalised}


class Inspector:
    def __init__(self, root):
        if not all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_DIRECTORY")):
            raise InspectionError("Safe nonsymlink inspection is unavailable on this platform.")
        self.root = root
        self.root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.visited = {}
        self.processed = set()
        self.contents = {}
        self.total_bytes = 0
        self.entries = 0
        self.skipped_symlinks = 0
        self.depth_limited = False
        self.manifests = []
        self.declarations = {name: [] for name in TRACKED_PACKAGES}
        self.python_requirements = []
        self.managers = set()
        self.signals = set()
        self.config = dict.fromkeys(("dotenv", "dotenv_example", "dockerfile",
                                     "cloudbuild_yaml", "agent_entrypoint", "server_entrypoint",
                                     "agent_skills_module", "schema_module", "tool_module",
                                     "root_prompt", "setup_script", "cleanup_script",
                                     "kubernetes_deployment_candidate", "kubernetes_service_candidate",
                                     "kubernetes_hpa_candidate", "kubernetes_pdb_candidate",
                                     "kubernetes_vpa_candidate"), False)

    def close(self):
        os.close(self.root_fd)

    def directory_fd(self, parts):
        """Open descendants relative to held directories, never following symlinks."""
        fd = os.dup(self.root_fd)
        try:
            for part in parts:
                if part in {"", ".", ".."}:
                    raise InspectionError("A project path has an unsupported component.")
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=fd)
                os.close(fd)
                fd = child
            return fd
        except BaseException:
            os.close(fd)
            raise

    def read(self, path):
        parent_fd = None
        try:
            relative = path.relative_to(self.root)
            parent_fd = self.directory_fd(relative.parts[:-1])
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            with os.fdopen(os.open(relative.name, flags, dir_fd=parent_fd), "rb") as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise InspectionError("A referenced manifest is not a regular file.")
                data = stream.read(LIMITS["bytes_per_manifest"] + 1)
        except OSError:
            raise InspectionError("A manifest is unreadable, missing, or crosses a symlink.") from None
        finally:
            if parent_fd is not None:
                os.close(parent_fd)
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
        if name not in TRACKED_PACKAGES:
            return
        tail, separator, _marker = match.group(3).partition(";")
        tail = tail.strip()
        if tail.startswith("(") and tail.endswith(")"):
            tail = tail[1:-1].strip()
        item = {"source": source, "scope": scope, "conditional": bool(separator)}
        if name == "google-cloud-aiplatform":
            item["known_extras"] = known_aiplatform_extras((match.group(2) or "").split(","))
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

    def manifest(self, path, kind):
        if (path, kind) in self.processed:
            return
        self.processed.add((path, kind))
        if path not in self.visited:
            if len(self.visited) >= LIMITS["manifests"]:
                raise InspectionError("Manifest count limit exceeded; select a narrower project root.")
            source = f"manifest-{len(self.visited) + 1:03d}"
            record = {"id": source, "kinds": [],
                      "location": "root" if path.parent == self.root else "nested"}
            self.visited[path] = record
            self.manifests.append(record)
            self.contents[path] = self.read(path)
        record = self.visited[path]
        record["kinds"].append(kind)
        source = record["id"]
        content = self.contents[path]
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
                or any(part.startswith(".env") for part in candidate.relative_to(self.root).parts)):
            raise InspectionError("A requirements include is outside the root or has an unsupported file type.")
        if len(candidate.relative_to(self.root).parts) - 1 > LIMITS["depth"]:
            raise InspectionError("A requirements include exceeds the directory depth limit.")
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
            elif normalized in TRACKED_PACKAGES:
                if isinstance(value, str):
                    suffix = "==" + value if re.fullmatch(VERSION, value) else value
                    self.add_requirement(normalized + suffix, source)
                else:
                    item = {"source": source, "scope": "runtime",
                            "conditional": False, "kind": "unparsed"}
                    if normalized == "google-cloud-aiplatform":
                        item["known_extras"] = known_aiplatform_extras(
                            value.get("extras", []) if isinstance(value, dict) else [])
                    self.declarations[normalized].append(item)

    def scan(self, directory=None, depth=0):
        directory = self.root if directory is None else directory
        directory_fd = None
        try:
            relative = directory.relative_to(self.root)
            directory_fd = self.directory_fd(relative.parts)
            with os.scandir(directory_fd) as listing:
                entries = []
                for entry in listing:
                    self.entries += 1
                    if self.entries > LIMITS["directory_entries"]:
                        raise InspectionError("Directory entry limit exceeded; select a narrower project root.")
                    linked = entry.is_symlink()
                    entries.append((entry.name, linked,
                                    not linked and entry.is_dir(follow_symlinks=False),
                                    not linked and entry.is_file(follow_symlinks=False)))
            for name, linked, is_directory, is_file in sorted(entries):
                if linked:
                    self.skipped_symlinks += 1
                    continue
                if is_directory:
                    if name.startswith(".") or name in SKIP_DIRS:
                        continue
                    if name in {"application-optimizations", "optimized_agent"}:
                        self.signals.add("application_directory")
                    if name == "cloud-run":
                        self.signals.add("cloud_run_directory")
                    if name in {"agent-runtime", "agent-engine", "agent-engine-deployment"}:
                        self.signals.add("agent_runtime_directory")
                    if name == "gke":
                        self.signals.add("gke_directory")
                    if name == "k8s":
                        self.signals.add("kubernetes_directory")
                    if depth < LIMITS["depth"]:
                        self.scan(directory / name, depth + 1)
                    else:
                        self.depth_limited = True
                elif is_file:
                    path = directory / name
                    if name == "pyproject.toml":
                        self.manifest(path, "pyproject")
                    elif re.fullmatch(r"requirements[\w.-]*\.(?:txt|in)", name):
                        self.manifest(path, "requirements")
                    for filename, manager in {"uv.lock": "uv", "poetry.lock": "poetry",
                                              "Pipfile": "pipenv", "Pipfile.lock": "pipenv",
                                              "pdm.lock": "pdm"}.items():
                        if name == filename:
                            self.managers.add(manager)
                    names = {
                        "dotenv": {".env"},
                        "dotenv_example": {".env.example", ".env.sample", ".env.template"},
                        "dockerfile": {"Dockerfile"},
                        "cloudbuild_yaml": {"cloudbuild.yaml", "cloudbuild.yml"},
                        "agent_entrypoint": {"agent.py"},
                        "server_entrypoint": {"main.py", "app.py"},
                        "agent_skills_module": {"skills.py"},
                        "schema_module": {"schema.py"},
                        "tool_module": {"bigquery_tools.py", "parallel_tools.py"},
                        "root_prompt": {"root_agent.txt"},
                        "setup_script": {"deploy.sh", "setup_bigquery_testdata.py", "setup_gcs_bucket.py"},
                        "cleanup_script": {"delete.sh", "cleanup_gcp.py"},
                        "kubernetes_deployment_candidate": {"deployment.yaml", "deployment.yml"},
                        "kubernetes_service_candidate": {"service.yaml", "service.yml"},
                        "kubernetes_hpa_candidate": {"hpa.yaml", "hpa.yml"},
                        "kubernetes_pdb_candidate": {"pdb.yaml", "pdb.yml"},
                        "kubernetes_vpa_candidate": {"vpa.yaml", "vpa.yml",
                                                     "vpa-recommendation-only.yaml",
                                                     "vpa-recommendation-only.yml"},
                    }
                    for field, filenames in names.items():
                        if name in filenames:
                            self.config[field] = True
                    if name == "Dockerfile":
                        self.signals.add("container_build")
        except OSError:
            raise InspectionError("A project directory could not be inspected without following symlinks.") from None
        finally:
            if directory_fd is not None:
                os.close(directory_fd)


def compatibility(inspector, mode):
    result = {}
    baseline = {"agent-runtime": AGENT_RUNTIME_BASELINE, "gke": GKE_BASELINE}.get(mode, BASELINE)
    for name in TRACKED_PACKAGES:
        expected = baseline.get(name)
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
        if expected and any(pin != expected for pin in pins):
            reasons.append("different_from_recorded_baseline")
        if len(pins) > 1:
            reasons.append("conflicting_exact_pins")
        if (mode in {"agent-runtime", "gke"} and name == "google-cloud-aiplatform"
                and any(item.get("known_extras", {}).get("adk", False) for item in declarations)):
            reasons.append("adk_extra_conflicts_with_recorded_adk_baseline")
        if inspector.depth_limited:
            reasons.append("inspection_depth_limit_reached")
        if expected:
            status = "unverified" if reasons else "matches_recorded_baseline"
        else:
            status = "declarations_only" if declarations else "not_declared"
        result[name] = {"required_for_selected_mode": expected is not None,
                        "recorded_baseline": expected, "status": status,
                        "reasons": reasons, "exact_pins": pins, "declarations": declarations}
    return result, all(result[name]["status"] == "matches_recorded_baseline" for name in baseline)


def main(argv=None):
    parser = SafeParser(description=__doc__, epilog=(
        "Always offline and read-only: no cloud commands, installs, imports of project code, or writes. "
        "JSON reports declarations, not installed versions or proven compatibility. Lockfiles and .env contents "
        "are never read. Filename hints do not establish an architecture. Exit 0: inspection completed "
        "(possibly unverified); 2: invalid input, unreadable/invalid manifest, or exceeded hard limit; "
        "3: --require-baseline evidence gate not met. Use a stable project tree during inspection."))
    parser.add_argument("--root", required=True, help="Project directory; inspect bounded nonsymlink manifests beneath it.")
    parser.add_argument("--mode", choices=("auto", "application", "cloud-run", "agent-runtime", "gke"), default="auto",
                        help="Agent Runtime adds SDK and GenAI declaration gates; GKE adds only the SDK gate. Auto retains the ADK-only gate.")
    parser.add_argument("--dry-run", action="store_true", help="Explicit synonym for the default offline, read-only inspection.")
    parser.add_argument("--require-baseline", action="store_true", help="Exit 3 unless required packages have unconditional exact recorded pins.")
    args = parser.parse_args(argv)
    inspector = None
    try:
        supplied_root = Path(args.root).expanduser()
        if supplied_root.is_symlink() or not supplied_root.is_dir():
            raise InspectionError("Root must be an existing nonsymlink directory.")
        inspector = Inspector(supplied_root.resolve(strict=True))
        inspector.scan()
        packages, baseline_ok = compatibility(inspector, args.mode)
        result = {
            "operation": "offline_read_only_inspection", "mode": args.mode,
            "network_calls": 0, "writes": 0,
            "python": {"interpreter": ".".join(map(str, sys.version_info[:3])),
                       "declared_requirements": inspector.python_requirements,
                       "requirement_satisfaction": "not_evaluated"},
            "package_manager_indicators": sorted(inspector.managers),
            "manifests": inspector.manifests,
            "packages": packages,
            "baseline_gate_passed": baseline_ok,
            "configuration_file_presence": inspector.config,
            "architecture_hints": sorted(inspector.signals),
            "coverage": {"limits": LIMITS, "directory_entries_examined": inspector.entries,
                         "manifest_bytes_read": inspector.total_bytes,
                         "symlinks_skipped": inspector.skipped_symlinks,
                         "depth_limit_reached": inspector.depth_limited},
            "limitations": [
                "Observed declarations are not installed versions; no project code, lockfile content, or dotenv content was read.",
                "Matching the recorded baseline does not prove dependency resolution, Python compatibility, IAM, billing, API, model, or regional access.",
                "Preserve target pins. Different, missing, ranged, conditional, or unsupported declarations require validation, not an automatic dependency change.",
                "Only PEP 621 and basic Poetry dependency declarations plus local requirements/constraints files are parsed; other installer options and dependency formats require manual review.",
                "Only allowlisted aiplatform extras are reported. Other extras are not validated. Agent Runtime and GKE gates reject the adk extra against the recorded SDK 1.153.1 and ADK 2.8.0 baseline.",
                "Hidden/build/environment directories are skipped unless explicitly referenced as manifests. Descendant symlinks are never followed. Use a stable tree; this is not an atomic project snapshot.",
                "Presence hints do not prove wiring, runtime mode, successful tools, cache hits, permissions, or hosting readiness.",
                "Kubernetes candidate filenames are not parsed; API validity, selectors, probes, resources, identity and admitted cluster configuration require separate inspection.",
            ],
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 3 if args.require_baseline and not baseline_ok else 0
    except (InspectionError, OSError, ValueError, RecursionError) as error:
        message = str(error) if isinstance(error, InspectionError) else "Project inspection failed; input details omitted."
        print(json.dumps({"error": message, "network_calls": 0, "writes": 0}), file=sys.stderr)
        return 2
    finally:
        if inspector is not None:
            inspector.close()


if __name__ == "__main__":
    raise SystemExit(main())
