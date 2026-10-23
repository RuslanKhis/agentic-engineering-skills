#!/usr/bin/env python3
"""Report an ADK web backend's versions, FastAPI feature gates and backend hazards, read-only.

Python 3.11+; standard library only. Reads manifests, uv.lock and bounded
source text; never imports or runs project code, never reads .env files,
never follows symlinks and makes no network calls. --dry-run has exactly the
same read-only effect. Exit codes: 0 inspection complete; 2 invalid input;
4 inspection incomplete (limits reached or files unreadable).

Findings are pointers for a person to read, not verdicts: a pattern match
says where to look, and its absence proves nothing.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    sys.stderr.write("inspect_backend.py needs Python 3.11 or later (it reads TOML with tomllib).\n")
    raise SystemExit(2)

import argparse
import json
import os
from pathlib import Path
import re
import stat
import tomllib

PACKAGES = ("fastapi", "starlette", "pydantic", "google-adk", "ag-ui-adk", "sse-starlette", "uvicorn",
            "sqlalchemy", "alembic", "asyncpg", "aiosqlite", "firebase-admin", "google-auth",
            "pydantic-settings", "opentelemetry-api")
# Versions are from FastAPI's release notes, read 23 October 2026.
FEATURES = (
    ("EventSourceResponse (fastapi.sse), 15 s keep-alive pings", (0, 135)),
    ("app.frontend() for a built single-page app", (0, 138)),
    ("native OpenTelemetry instrumentation", (0, 142)),
    ("automatic exporter set-up only when FASTAPI_OTEL_AUTO_CONFIGURE=true", (0, 143)),
)
# Each rule: id, file kinds, pattern, what to check. Patterns are deliberately narrow.
RULES = (
    ("adk_server_exposed", ("py",), r"\bget_fast_api_app\s*\(",
     "ADK's own server routes are unauthenticated; keep them private or local only (SB05)."),
    ("adk_cli_server", ("ops",), r"\badk\s+(?:api_server|web)\b",
     "`adk api_server` or `adk web` in a run command; only loopback for a builder-only demo (SB05)."),
    ("wildcard_cors", ("py", "ops"), r"allow_origins\s*=\s*\[\s*[\"']\*[\"']|--allow_origins[= ]+[\"']?\*",
     "A '*' origin; use same origin or an explicit allowlist (SB06)."),
    ("frontend_fallback", ("py",), r"\.frontend\s*\(",
     "app.frontend() answers unmatched browser GETs with index.html, under /api too; add an /api catch-all 404."),
    ("database_sessions", ("py",), r"\bDatabaseSessionService\s*\(",
     "ADK creates its five session tables itself; exclude them from application migrations."),
    ("migrations_without_filter", ("alembic_env",), r"\A(?![\s\S]*\binclude_object\b)",
     "Alembic env.py has no include_object filter; autogenerate would drop ADK's tables in a shared database."),
    ("background_tasks", ("py",), r"\bBackgroundTasks\b",
     "Work after the response gets no CPU under request-based billing; use Cloud Tasks for work that must not be lost."),
    ("multiple_workers", ("ops",), r"--workers[\"'=,\s]+(?:[2-9]|\d{2,})|WEB_CONCURRENCY[\"'=,\s]+(?:[2-9]|\d{2,})",
     "Several worker processes per container; run one process on Cloud Run."),
    ("unsigned_iap_header", ("py",), r"x-goog-authenticated-user-(?:email|id)",
     "Unsigned IAP identity headers can be forged when IAP is bypassed; verify x-goog-iap-jwt-assertion."),
    ("client_user_id", ("py",), r"\buser_id\s*=\s*(?:(?:body|payload|data|input|params)\b|request\.(?!state\b))",
     "user_id taken from request data; take it from the verified principal (SB03)."),
    ("agui_user_extractor", ("py",), r"\buser_id_extractor\s*=",
     "ag-ui-adk passes the client's RunAgentInput to this extractor; bind identity through dependencies= and request state."),
    ("docs_served", ("py",), r"\bFastAPI\s*\((?![^)]*docs_url\s*=\s*None)",
     "FastAPI() without docs_url=None; serve no docs or schema in a deployed build (SB07)."),
)
SIGNALS = (
    ("iap_assertion", r"x-goog-iap-jwt-assertion"),
    ("firebase_verify", r"\bverify_id_token\s*\("),
    ("dependency_overrides", r"\bdependency_overrides\b"),
    ("event_source_response", r"\bEventSourceResponse\b"),
    ("sse_starlette", r"\bsse_starlette\b"),
    ("cloud_tasks", r"\bgoogle\.cloud\s*(?:import\s+tasks|\.tasks)"),
    ("lifespan", r"\blifespan\s*="),
    ("openapi_dump", r"\.openapi\s*\(\s*\)"),
)
EXCLUDED_DIRS = {".git", ".hg", ".venv", "venv", "env", "node_modules", "__pycache__", ".pytest_cache",
                 ".mypy_cache", ".ruff_cache", ".tox", ".nox", "dist", "build", "coverage", "site-packages",
                 ".claude", ".agents", ".agent", ".codex", ".gemini", ".cursor", ".adk-evidence"}
OPS_FILES = {"Dockerfile", "Procfile", "Makefile", "docker-compose.yml", "docker-compose.yaml",
             "cloudbuild.yaml", "service.yaml", "app.yaml", "justfile"}
LIMITS = {"max_depth": 8, "max_entries": 5000, "max_files": 600, "max_file_bytes": 262144,
          "max_total_bytes": 8388608}
REQUIREMENT = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\[[^\]]*\])?\s*([^;#]*)")


def normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def version_tuple(value: str | None) -> tuple[int, ...] | None:
    match = re.match(r"^\s*(\d+)\.(\d+)(?:\.(\d+))?", value or "")
    return tuple(int(part) for part in match.groups() if part is not None) if match else None


def declared(text: str, kind: str) -> dict[str, str]:
    found: dict[str, str] = {}
    lines: list[str] = []
    if kind == "pyproject":
        data = tomllib.loads(text)
        project = data.get("project", {})
        lines += [d for d in project.get("dependencies", []) if isinstance(d, str)]
        for group in (project.get("optional-dependencies") or {}).values():
            lines += [d for d in group if isinstance(d, str)]
        for group in (data.get("dependency-groups") or {}).values():
            lines += [d for d in group if isinstance(d, str)]
    else:
        lines = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith(("#", "-"))]
    for line in lines:
        match = REQUIREMENT.match(line)
        if match and normalise(match[1]) in PACKAGES:
            found.setdefault(normalise(match[1]), match[2].strip() or "(any)")
    return found


def locked(text: str) -> dict[str, str]:
    data = tomllib.loads(text)
    return {normalise(p["name"]): p["version"] for p in data.get("package", [])
            if isinstance(p, dict) and normalise(str(p.get("name", ""))) in PACKAGES and "version" in p}


def read_bounded(path: Path, counts: dict) -> str | None:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > LIMITS["max_file_bytes"]:
        return None
    if counts["bytes"] + info.st_size > LIMITS["max_total_bytes"]:
        raise OverflowError
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as stream:
        raw = stream.read(LIMITS["max_file_bytes"] + 1)
    counts["bytes"] += len(raw)
    return raw.decode("utf-8", errors="replace")


def kind_of(path: Path) -> str | None:
    name = path.name
    if name.startswith(".env"):
        return None  # never read environment files
    if name == "env.py" and path.parent.name in {"migrations", "alembic"}:
        return "alembic_env"
    if name.endswith(".py"):
        return "py"
    if name in OPS_FILES or name.endswith((".sh", ".toml")) and name != "pyproject.toml":
        return "ops"
    if name == "pyproject.toml":
        return "pyproject"
    if re.fullmatch(r"requirements[\w.-]*\.(?:txt|in)", name):
        return "requirements"
    if name == "uv.lock":
        return "lock"
    return None


def scan(root: Path) -> dict:
    counts = {"entries": 0, "files": 0, "bytes": 0}
    declared_versions: dict[str, dict[str, str]] = {}
    resolved: dict[str, str] = {}
    findings: list[dict] = []
    signals: dict[str, list[str]] = {}
    warnings: set[str] = set()
    alembic_seen = False
    stack = [(root, 0)]
    while stack:
        directory, depth = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda e: e.name)
        except OSError:
            warnings.add("directory_unreadable")
            continue
        for entry in entries:
            counts["entries"] += 1
            if counts["entries"] > LIMITS["max_entries"]:
                warnings.add("entry_limit_reached")
                stack.clear()
                break
            if entry.is_symlink():
                continue
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            if entry.is_dir(follow_symlinks=False):
                if entry.name not in EXCLUDED_DIRS and depth < LIMITS["max_depth"]:
                    stack.append((path, depth + 1))
                elif depth >= LIMITS["max_depth"]:
                    warnings.add("depth_limit_reached")
                continue
            kind = kind_of(path)
            if kind is None:
                continue
            counts["files"] += 1
            if counts["files"] > LIMITS["max_files"]:
                warnings.add("file_limit_reached")
                stack.clear()
                break
            try:
                text = read_bounded(path, counts)
            except OverflowError:
                warnings.add("byte_limit_reached")
                stack.clear()
                break
            except OSError:
                warnings.add("file_unreadable")
                continue
            if text is None:
                warnings.add("file_skipped_size_or_type")
                continue
            try:
                if kind in ("pyproject", "requirements"):
                    for name, spec in declared(text, kind).items():
                        declared_versions.setdefault(name, {})[rel] = spec
                    continue
                if kind == "lock":
                    resolved.update(locked(text))
                    continue
            except (tomllib.TOMLDecodeError, KeyError, TypeError, AttributeError):
                warnings.add("manifest_unparsed")
                continue
            alembic_seen = alembic_seen or kind == "alembic_env"
            for rule, kinds, pattern, advice in RULES:
                if kind not in kinds:
                    continue
                for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append({"rule": rule, "file": rel, "line": line, "check": advice})
                    break
            if kind == "py":
                for name, pattern in SIGNALS:
                    if re.search(pattern, text, re.IGNORECASE):
                        signals.setdefault(name, []).append(rel)
    return {"declared": declared_versions, "resolved": resolved, "findings": findings,
            "signals": signals, "alembic_env_found": alembic_seen, "counts": counts,
            "limits": LIMITS, "warnings": sorted(warnings), "complete_within_scope": not warnings}


def feature_matrix(fastapi_version: str | None) -> list[dict]:
    current = version_tuple(fastapi_version)
    return [{"feature": name, "needs": ".".join(map(str, minimum)),
             "available": None if current is None else current >= minimum} for name, minimum in FEATURES]


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, "error: invalid arguments; use --help for the accepted interface.\n")


def main(argv: list[str] | None = None) -> int:
    parser = SafeArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project", required=True, type=Path, help="existing project directory (no symlink root)")
    parser.add_argument("--dry-run", action="store_true", help="same read-only inspection")
    args = parser.parse_args(argv)
    try:
        info = args.project.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise OSError
    except OSError:
        print(json.dumps({"error": "project_must_be_an_existing_non_symlink_directory"}))
        return 2
    result = scan(args.project.absolute())
    fastapi = result["resolved"].get("fastapi")
    notes = []
    adk = version_tuple(result["resolved"].get("google-adk"))
    if adk and adk[:2] == (2, 12):
        notes.append("google-adk 2.12.0 requires opentelemetry-api<=1.42.1, and FastAPI 0.142+ requires "
                     ">=1.44.0, so FastAPI resolves to 0.141.x or lower beside it (checked 23 October 2026).")
    if fastapi is None:
        notes.append("No uv.lock version for fastapi; record the resolved version from the lockfile or the "
                     "installed environment before relying on a feature gate.")
    output = {"schema_version": 1, "read_only": True, "project": result,
              "fastapi_features": feature_matrix(fastapi), "notes": notes,
              "limitations": ["Pattern matches point at code to read; they are not verdicts.",
                              "Only uv.lock is read for resolved versions; other lockfiles are not parsed.",
                              "Project code is never imported, so runtime behaviour is not checked."]}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result["complete_within_scope"] else 4


if __name__ == "__main__":
    raise SystemExit(main())
