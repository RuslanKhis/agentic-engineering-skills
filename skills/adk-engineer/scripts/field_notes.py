#!/usr/bin/env python3
"""Keep generalised field notes about these skills and prepare a report for review. Standard library only.

A field note records where real use diverged from what a skill says. Notes are
redacted when recorded and again when previewed; nothing is ever sent. The
``url`` subcommand prints a prefilled GitHub issue-form link for the user to
open, review and submit themselves; it never opens a browser or calls a network.

Subcommands:
  add      append one note (allowlisted keys only) to the local log
  preview  print the exact report text for pending notes and the redaction counts
  url      print the prefilled issue URL for one note, or write a Markdown
           report and print the blank form link when the URL would be too long
  mark     record that a note was offered, declined or kept local only

Log: ``$AGENTIC_ENGINEERING_HOME/field-notes/notes.jsonl`` (default home
``~/.agentic-engineering``). When that cannot be written, the log falls back to
``.agentic-field-notes/notes.jsonl`` in the project, with its own ``.gitignore``.
``AES_FIELD_NOTES=off`` records nothing; ``quiet`` records but asks the agent
not to offer sharing. ``AES_FIELD_NOTES_REDACT`` adds comma-separated terms
(client or product names) to redact.

Exit status: 0 on success (including when notes are off), 1 when a note is
rejected, 2 when input cannot be read.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import getpass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import quote, urlsplit

REPO = "RuslanKhis/agentic-engineering-skills"
TEMPLATE = "field-report.yml"
# Anonymous probe on 25 October 2026: 414 from about 8,240 characters, server errors
# from about 7,000 behind the sign-in redirect. The limit for signed-in users is unverified.
MAX_URL = 6000
MAX_FENCE_LINES = 15

KINDS = {
    "wrong-api": "Wrong or changed API",
    "failed-step": "A documented step failed",
    "missing-case": "Missing case",
    "misrouted": "Misrouted specialist",
    "overridden-default": "A default the user always overrides",
    "helper-error": "Helper script error",
    "other": "Other",
}
HOSTS = {
    "claude-code": "Claude Code",
    "codex": "Codex",
    "antigravity": "Google Antigravity",
    "gemini-cli": "Gemini CLI",
    "other": "Other",
}
EVIDENCE = {
    "observed-once": "Observed once",
    "reproduced-fresh": "Reproduced in a fresh session",
    "reproduced-fixture": "Reproduced with a fixture and a check",
}
# Allowlisted note fields: (form field id, form label, maximum characters).
FIELDS = (
    ("skill", "Skill", 64),
    ("skill_version", "Skill version", 80),
    ("host", "Coding agent", 40),
    ("model", "Model", 80),
    ("kind", "Kind of divergence", 40),
    ("said", "What the skill says", 600),
    ("happened", "What happened instead", 3000),
    ("repro", "Minimal reproduction", 2000),
    ("proposed", "Proposed correction", 1500),
    ("evidence", "Evidence", 40),
)
FIELD_IDS = {key for key, _, _ in FIELDS}
BOOKKEEPING = {"id", "recorded", "state"}
STATES = ("pending", "offered", "declined", "local-only")
REQUIRED = ("skill", "kind", "said", "happened")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

DOC_HOSTS = (
    "adk.dev", "google.github.io", "cloud.google.com", "docs.cloud.google.com", "ai.google.dev",
    "developers.google.com", "pypi.org", "docs.github.com", "agentskills.io", "docs.python.org",
    "code.claude.com", "developers.openai.com", "geminicli.com",
)
DOC_PATH_PREFIXES = ("github.com/google/", "github.com/googleapis/", "github.com/google-gemini/",
                     "github.com/" + REPO.lower() + "/")

INVISIBLE = re.compile("[­؜᠎​-‏‪-‮⁠-⁤⁦-⁩﻿]")
HTML_COMMENT = re.compile(r"<!--.*?(?:-->|$)", re.DOTALL)
FENCE = re.compile(r"^([ \t]*)(```|~~~)[^\n]*\n(.*?)^\1\2[ \t]*$", re.DOTALL | re.MULTILINE)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?(?:-----END [A-Z0-9 ]*PRIVATE KEY-----|\Z)", re.DOTALL),
    re.compile(r"\"private_key\"\s*:\s*\"[^\"]*\""),
    re.compile(r"\b(?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35,}"),
    re.compile(r"\bya29\.[0-9A-Za-z_\-]{20,}"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{20,}"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[=:]\s*['\"]?[^\s'\"]{8,}"),
)
SERVICE_ACCOUNT = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+\.iam\.gserviceaccount\.com\b")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}\b")
URL = re.compile(r"\b(?:https?|wss?|ftp)://[^\s<>\"'`)\]]+", re.IGNORECASE)
GCS_URI = re.compile(r"\bgs://[^\s<>\"'`)\]]+")
GCP_PROJECT = re.compile(
    r"(?i)(\bprojects/|--project[= ]|\bGOOGLE_CLOUD_PROJECT\s*=\s*['\"]?|\bproject(?:_id)?\s*[=:]\s*['\"]?)"
    r"(?!<)([a-z][a-z0-9\-]{4,28}[a-z0-9])")
BUCKET = re.compile(r"(?i)(\bbuckets?/|\bbucket(?:_name)?\s*[=:]\s*['\"]?)(?!<)([a-z0-9][a-z0-9._\-]{2,62})")
IPV4 = re.compile(r"(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])")
HOME_PATH = re.compile(
    r"(?<![\w.])(?:/Users/|/home/|[A-Za-z]:\\Users\\|/private/var/|/var/folders/|/private/tmp/|/tmp/|~/)"
    r"[^\s'\"`<>|]*")
KEEP_PATH_TAIL = re.compile(r"[/\\](site-packages|skills)[/\\]")
TOKEN = re.compile(r"(?<![A-Za-z0-9+/=_\-])[A-Za-z0-9+/=_\-]{32,}(?![A-Za-z0-9+/=_\-])")
GENERIC_TERMS = {"app", "agent", "agents", "src", "project", "repo", "code", "test", "tests", "demo",
                 "main", "work", "home", "user", "users", "skills", "docs", "backend", "frontend"}


def _entropy(text: str) -> float:
    counts = {c: text.count(c) for c in set(text)}
    return -sum(n / len(text) * math.log2(n / len(text)) for n in counts.values())


def _is_doc_url(url: str) -> bool:
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    host = (parts.hostname or "").lower()
    if parts.query or parts.username or parts.password:
        return False
    if host in DOC_HOSTS or any(host.endswith("." + h) for h in DOC_HOSTS):
        return True
    return any((host + parts.path.lower() + "/").startswith(p) for p in DOC_PATH_PREFIXES)


class Redactor:
    """Replace identifying or secret material with placeholders and count each kind."""

    def __init__(self, project_root: Path | None = None, extra_terms=()):
        terms = list(extra_terms)
        terms += [t for t in os.environ.get("AES_FIELD_NOTES_REDACT", "").split(",")]
        self.terms = []
        if project_root is not None and project_root.name:
            self.terms.append((project_root.name, "<project>"))
        try:
            self.terms.append((getpass.getuser(), "<user>"))
        except Exception:  # noqa: BLE001 - no user name in some sandboxes
            pass
        self.terms += [(t.strip(), "<redacted>") for t in terms if t.strip()]
        self.terms = [(t, p) for t, p in self.terms if len(t) >= 4 and t.lower() not in GENERIC_TERMS]
        self.counts: dict[str, int] = {}

    def _sub(self, pattern, replacement, text, label):
        def repl(match):
            value = replacement(match) if callable(replacement) else replacement
            if value != match.group(0):
                self.counts[label] = self.counts.get(label, 0) + 1
            return value
        return pattern.sub(repl, text)

    def _path(self, match):
        path = match.group(0)
        tail = KEEP_PATH_TAIL.search(path)
        return "<path>" + path[tail.start():].replace("\\", "/") if tail else "<path>"

    def _url(self, match):
        url = match.group(0).rstrip(".,;:")
        trailing = match.group(0)[len(url):]
        return (url if _is_doc_url(url) else "<url>") + trailing

    def _fence(self, match):
        body = match.group(3)
        lines = body.count("\n")
        if lines > MAX_FENCE_LINES:
            return f"{match.group(1)}[code block of {lines} lines removed; keep reproductions short]"
        return match.group(0)

    def _token(self, match):
        token = match.group(0)
        if re.fullmatch(r"[0-9a-f]{7,64}", token) or token.startswith("<"):
            return token  # commit SHAs and digests
        if "/" in token and token.count("/") > 2 and not re.search(r"[0-9]", token):
            return token  # a path-like word, not a key
        classes = sum(bool(re.search(p, token)) for p in (r"[a-z]", r"[A-Z]", r"[0-9]"))
        return "<secret>" if classes >= 2 and _entropy(token) >= 4.0 else token

    def redact(self, text: str) -> str:
        if not text:
            return text
        text = self._sub(INVISIBLE, "", text, "invisible characters")
        text = self._sub(HTML_COMMENT, "", text, "HTML comments")
        text = self._sub(FENCE, self._fence, text, "long code blocks")
        for pattern in SECRET_PATTERNS:
            text = self._sub(pattern, "<secret>", text, "secrets")
        text = self._sub(SERVICE_ACCOUNT, "<service-account>", text, "service accounts")
        text = self._sub(EMAIL, "<email>", text, "emails")
        text = self._sub(GCS_URI, lambda m: "gs://<bucket>" + m.group(0)[len(m.group(0).rstrip(".,;:")):],
                         text, "bucket names")
        text = self._sub(URL, self._url, text, "URLs")
        text = self._sub(GCP_PROJECT, lambda m: m.group(1) + "<gcp-project>", text, "GCP project IDs")
        text = self._sub(BUCKET, lambda m: m.group(1) + "<bucket>", text, "bucket names")
        text = self._sub(IPV4, lambda m: m.group(0) if m.group(0) in ("127.0.0.1", "0.0.0.0") else "<ip>",
                         text, "IP addresses")
        text = self._sub(HOME_PATH, self._path, text, "home paths")
        for term, placeholder in self.terms:
            pattern = re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", re.IGNORECASE)
            text = self._sub(pattern, placeholder, text, "project, user or client names")
        text = self._sub(TOKEN, self._token, text, "high-entropy strings")
        return text


def mode() -> str:
    value = os.environ.get("AES_FIELD_NOTES", "on").strip().lower()
    return value if value in ("on", "quiet", "off") else "on"


def default_log() -> Path:
    home = os.environ.get("AGENTIC_ENGINEERING_HOME") or str(Path.home() / ".agentic-engineering")
    return Path(home).expanduser() / "field-notes" / "notes.jsonl"


def fallback_log(project_root: Path) -> Path:
    return project_root / ".agentic-field-notes" / "notes.jsonl"


def log_paths(args) -> list[Path]:
    if args.notes:
        return [args.notes]
    return [p for p in (default_log(), fallback_log(args.project_root)) if p.is_file()] or [default_log()]


def read_notes(paths) -> list[tuple[Path, dict]]:
    notes = []
    for path in paths:
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            raise InputError(f"cannot read {path}: {exc}") from exc
        for number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                note = json.loads(line)
            except ValueError as exc:
                raise InputError(f"{path}:{number}: not JSON: {exc}") from exc
            if isinstance(note, dict):
                notes.append((path, {k: v for k, v in note.items() if k in FIELD_IDS | BOOKKEEPING}))
    return notes


class InputError(Exception):
    pass


def skill_version(skill_md: Path) -> str:
    try:
        data = skill_md.read_bytes()
    except OSError as exc:
        raise InputError(f"cannot read {skill_md}: {exc}") from exc
    text = data.decode("utf-8", errors="replace")
    front = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if front:
        meta = re.search(r"^metadata:\s*\n((?:[ \t]+.*\n?)*)", front.group(1), re.MULTILINE)
        if meta:
            version = re.search(r"^[ \t]+version:\s*['\"]?([^'\"\n]+?)['\"]?\s*$", meta.group(1), re.MULTILINE)
            if version:
                return version.group(1)
    return "sha256:" + hashlib.sha256(data).hexdigest()[:12]


def build_note(values: dict, redactor: Redactor) -> tuple[dict, list[str]]:
    errors = []
    unknown = sorted(set(values) - FIELD_IDS)
    if unknown:
        errors.append("keys outside the allowlist: " + ", ".join(unknown))
    note = {}
    for key, _, limit in FIELDS:
        value = values.get(key)
        if value is None or str(value).strip() == "":
            continue
        text = redactor.redact(str(value).strip())
        if len(text) > limit:
            text = text[: limit - 12].rstrip() + " [truncated]"
        note[key] = text
    for key in REQUIRED:
        if key not in note:
            errors.append(f"{key} is required")
    if "skill" in note and not SKILL_NAME.match(note["skill"]):
        errors.append("skill must be a skill directory name such as adk-engineer")
    for key, choices in (("kind", KINDS), ("host", HOSTS), ("evidence", EVIDENCE)):
        if key in note and note[key] not in choices:
            errors.append(f"{key} must be one of: {', '.join(choices)}")
    return note, errors


def append_note(note: dict, args) -> Path:
    targets = [args.notes] if args.notes else [default_log(), fallback_log(args.project_root)]
    line = json.dumps(note, ensure_ascii=False, sort_keys=True) + "\n"
    last_error = None
    for index, path in enumerate(targets):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if index == 1:
                ignore = path.parent / ".gitignore"
                if not ignore.exists():
                    ignore.write_text("*\n", encoding="utf-8")
            with path.open("a", encoding="utf-8") as handle:
                handle.write(line)
            if index == 1:
                print(f"NOTE: {default_log()} is not writable here; the note was saved in the project at "
                      f"{path} (git-ignored by its own .gitignore). Tell the user.")
            return path
        except OSError as exc:
            last_error = exc
    raise InputError(f"cannot write a field note: {last_error}")


def rewrite(path: Path, notes: list[dict]) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".notes-", suffix=".jsonl")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        for note in notes:
            handle.write(json.dumps(note, ensure_ascii=False, sort_keys=True) + "\n")
    os.replace(tmp, path)


def title_for(note: dict) -> str:
    said = re.sub(r"\s+", " ", note.get("said", ""))[:70]
    return f"[field] {note.get('skill', '?')}: {KINDS.get(note.get('kind'), 'Other')} — {said}"


def display(key: str, value: str) -> str:
    table = {"kind": KINDS, "host": HOSTS, "evidence": EVIDENCE}.get(key)
    return table.get(value, value) if table else value


def report_markdown(note: dict) -> str:
    """Mirror the issue form's rendered body: one ``### Label`` section per field."""
    parts = []
    for key, label, _ in FIELDS:
        value = note.get(key)
        parts.append(f"### {label}\n\n{display(key, value) if value else '_No response_'}\n")
    parts.append("### Privacy check\n\n- [ ] I reviewed this text; it contains no client or private data\n")
    return "\n".join(parts)


def issue_url(note: dict, repo: str) -> str:
    query = [("template", TEMPLATE), ("title", title_for(note))]
    query += [(key, display(key, note[key])) for key, _, _ in FIELDS if note.get(key)]
    encoded = "&".join(f"{k}={quote(v, safe='')}" for k, v in query)
    return f"https://github.com/{repo}/issues/new?{encoded}"


def blank_form(repo: str) -> str:
    return f"https://github.com/{repo}/issues/new?template={TEMPLATE}"


def select(notes, ids, include_all):
    chosen = []
    for path, note in notes:
        if ids:
            if note.get("id") in ids:
                chosen.append((path, note))
        elif include_all or note.get("state", "pending") == "pending":
            chosen.append((path, note))
    missing = sorted(set(ids or ()) - {n.get("id") for _, n in chosen})
    if missing:
        raise InputError("no note with id " + ", ".join(missing))
    return chosen


def cmd_add(args) -> int:
    if mode() == "off":
        print("AES_FIELD_NOTES=off: nothing recorded.")
        return 0
    values = {}
    if args.from_json:
        try:
            raw = sys.stdin.read() if str(args.from_json) == "-" else args.from_json.read_text(encoding="utf-8")
            values = json.loads(raw)
        except (OSError, ValueError) as exc:
            raise InputError(f"cannot read note JSON: {exc}") from exc
        if not isinstance(values, dict):
            raise InputError("note JSON must be an object")
    for key, _, _ in FIELDS:
        flag = getattr(args, key, None)
        if flag is not None:
            values[key] = flag
    if args.skill_md and not values.get("skill_version"):
        values["skill_version"] = skill_version(args.skill_md)
    redactor = Redactor(args.project_root, args.redact)
    note, errors = build_note(values, redactor)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    existing = read_notes(log_paths(args))
    note["id"] = "fn-" + hashlib.sha256(json.dumps(note, sort_keys=True).encode()).hexdigest()[:8]
    note["recorded"] = _dt.date.today().isoformat()
    note["state"] = "pending"
    path = append_note(note, args)
    same = sum(1 for _, n in existing if n.get("skill") == note["skill"] and n.get("kind") == note["kind"]
               and n.get("said") == note["said"])
    print(f"Recorded {note['id']} in {path}.")
    print("Redactions: " + (", ".join(f"{k} {v}" for k, v in sorted(redactor.counts.items())) or "none"))
    print(f"Same skill, kind and quote recorded before: {same} time(s).")
    if mode() == "quiet":
        print("AES_FIELD_NOTES=quiet: recorded; do not offer sharing.")
    return 0


def cmd_preview(args) -> int:
    notes = select(read_notes(log_paths(args)), args.id, args.all)
    if not notes:
        print("No pending field notes.")
        return 0
    redactor = Redactor(args.project_root, args.redact)
    for _, note in notes:
        clean = {k: redactor.redact(v) if k in FIELD_IDS else v for k, v in note.items()}
        print(f"=== {note.get('id')} ({note.get('state', 'pending')}) ===")
        print(f"Title: {title_for(clean)}\n")
        print(report_markdown(clean))
    print("Redactions at preview: " + (", ".join(f"{k} {v}" for k, v in sorted(redactor.counts.items()))
                                       or "none (notes are also redacted when recorded)"))
    print("Nothing has been sent. Read the text above before opening any link.")
    return 0


def cmd_url(args) -> int:
    notes = select(read_notes(log_paths(args)), [args.id], False)
    path, note = notes[0]
    redactor = Redactor(args.project_root, args.redact)
    clean = {k: redactor.redact(v) if k in FIELD_IDS else v for k, v in note.items()}
    url = issue_url(clean, args.repo)
    if len(url) <= MAX_URL:
        print(url)
        print(f"({len(url)} characters.) Opening it only fills the form; the user reviews, ticks the privacy "
              "check and presses Submit. Nothing has been sent.")
    else:
        out = args.out or path.parent / f"field-report-{note.get('id')}.md"
        out.write_text(f"Title: {title_for(clean)}\n\n{report_markdown(clean)}", encoding="utf-8")
        print(blank_form(args.repo))
        print(f"The prefilled URL would be {len(url)} characters (limit {MAX_URL}); the report is in {out}. "
              "Open the blank form above and paste each section. Nothing has been sent.")
    if not args.no_mark:
        mark(path, note.get("id"), "offered")
    return 0


def mark(path: Path, note_id: str, state: str) -> None:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if isinstance(row, dict) and row.get("id") == note_id:
            row["state"] = state
        rows.append(row)
    rewrite(path, rows)


def cmd_mark(args) -> int:
    notes = select(read_notes(log_paths(args)), args.id, True)
    for path, note in notes:
        mark(path, note["id"], args.state)
        print(f"{note['id']}: {args.state}")
    return 0


class Deprecated(argparse.Action):
    """An old flag spelling that still works: hidden from --help, noted on stderr."""

    def __init__(self, option_strings, dest, note, nargs=None, const=None, default=argparse.SUPPRESS, **kwargs):
        self.note = note
        super().__init__(option_strings, dest, nargs=nargs, const=const, default=default,
                         help=argparse.SUPPRESS, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(f"{parser.prog}: {option_string} is deprecated; {self.note}", file=sys.stderr)
        setattr(namespace, self.dest, self.const if self.nargs == 0 else values)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--notes", type=Path, help="log file (default: the shared home log, then the project fallback)")
    common.add_argument("--project", type=Path, default=Path.cwd(),
                        help="project whose name is redacted and whose fallback log is used (default: cwd)")
    common.add_argument("--project-root", dest="project", type=Path, action=Deprecated, note="use --project")
    common.add_argument("--redact", action="append", default=[], help="another term to redact (repeatable)")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", parents=[common], help="record one note")
    for key, label, _ in FIELDS:
        add.add_argument("--" + key.replace("_", "-"), dest=key, help=label)
    add.add_argument("--skill-md", type=Path, help="installed SKILL.md; derives skill_version when absent")
    add.add_argument("--from-json", type=Path, help="read the note's fields from a JSON object file or -")
    add.set_defaults(func=cmd_add)

    preview = sub.add_parser("preview", parents=[common], help="print the exact report text")
    preview.add_argument("--id", action="append", help="note id (repeatable); default: pending notes")
    preview.add_argument("--all", action="store_true", help="include notes already offered or declined")
    preview.set_defaults(func=cmd_preview)

    url = sub.add_parser("url", parents=[common], help="print the prefilled issue URL for one note")
    url.add_argument("--id", required=True)
    url.add_argument("--repo", default=REPO)
    url.add_argument("--out", type=Path, help="Markdown report path when the URL is too long")
    url.add_argument("--no-mark", action="store_true", help="do not mark the note as offered")
    url.set_defaults(func=cmd_url)

    marker = sub.add_parser("mark", parents=[common], help="set a note's state")
    marker.add_argument("--id", action="append", required=True)
    marker.add_argument("--state", choices=STATES, required=True)
    marker.set_defaults(func=cmd_mark)

    args = parser.parse_args(argv)
    args.project_root = args.project.resolve()
    try:
        return args.func(args)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
