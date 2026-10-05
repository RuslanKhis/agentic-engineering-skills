"""Local retrieval controls: heading units, SQLite FTS5 BM25, named references, fusion.

A no-cloud path for retrieval strategy: chunk extracted pages by operative unit,
query once per material issue, resolve named references in code, run one bounded
second round and emit a sufficiency report the next stage can consume. See
references/retrieval-strategy.md. The bundled gold set is synthetic; recall
against it is a fixture control, never evidence of answer quality.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
import sys
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path


GOLD = Path(__file__).resolve().parents[1] / "assets" / "retrieval-gold.json"

DEFAULT_HEADING = re.compile(
    r"^(?!.*,\s*page\s+\d+\s*$)"  # a contents entry is a pointer to a heading, not a heading
    r"(?:Policy\s+[A-Z]{1,3}\d+[A-Za-z]?\b.*|Table\s+\d+[A-Za-z]?\b.*|Figure\s+\d+\b.*"
    r"|Appendix\s+[A-Z0-9]+\b.*|Contents\b.*|Monitoring\b.*|Index\b.*|Glossary\b.*"
    r"|[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\s+SPD)\s*$"
)
SCREENED_HEADINGS = ("contents", "table of contents", "cover", "monitoring", "index", "glossary")
STOPWORDS = frozenset(
    "a an and are at be by does for how in is it many must need of on or that the this "
    "to which what where will with".split()
)
REFERENCE_PATTERNS = (
    ("Policy", re.compile(r"\bPolicy\s+([A-Z]{1,3}\s?\d+[A-Za-z]?)\b")),
    ("Table", re.compile(r"\bTable\s+(\d+[A-Za-z]?)\b")),
    ("Figure", re.compile(r"\bFigure\s+(\d+[A-Za-z]?)\b")),
    ("Appendix", re.compile(r"\bAppendix\s+([A-Z0-9]+)\b")),
)
SPD_PATTERN = re.compile(r"\b((?:[A-Z][A-Za-z]+\s+)+SPD)\b")


def fts5_available() -> bool:
    """Report whether this interpreter's SQLite can create an FTS5 table."""
    try:
        sqlite3.connect(":memory:").execute("CREATE VIRTUAL TABLE probe USING fts5(x)")
    except sqlite3.OperationalError:
        return False
    return True


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fixture_pages(fixture: dict) -> list[dict]:
    """Flatten a fixture's pages; the questions block never reaches the retriever."""
    return [dict(page) for page in fixture["pages"]]


def chunk_by_heading(pages: Iterable[dict], heading_pattern: re.Pattern = DEFAULT_HEADING) -> list[dict]:
    """Split extracted pages into operative units: heading to next heading, across pages."""
    by_document: dict[str, list[dict]] = {}
    for page in pages:
        by_document.setdefault(page["document"], []).append(page)
    units: list[dict] = []
    for document, document_pages in by_document.items():
        seen: dict[str, int] = {}
        current = None
        for page in sorted(document_pages, key=lambda item: item["page"]):
            number = page["page"]
            for line in page["text"].splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                if heading_pattern.match(stripped):
                    current = _new_unit(document, stripped, number, seen)
                    units.append(current)
                    continue
                if current is None:
                    current = _new_unit(document, "", number, seen)
                    units.append(current)
                current["lines"].append(stripped)
                current["page_end"] = number
    for unit in units:
        unit["text"] = "\n".join(unit.pop("lines"))
    return units


def _new_unit(document: str, heading: str, page: int, seen: dict[str, int]) -> dict:
    slug = _slug(heading) or f"preamble-p{page}"
    seen[slug] = seen.get(slug, 0) + 1
    if seen[slug] > 1:
        slug = f"{slug}-{seen[slug]}"
    return {"unit_id": f"{document}:{slug}", "document": document, "heading": heading,
            "page_start": page, "page_end": page, "lines": []}


def screen_units(units: Sequence[dict]) -> tuple[list[dict], list[dict]]:
    """Separate operative units from contents, cover, monitoring and index material."""
    kept, screened = [], []
    for unit in units:
        heading = unit["heading"].lower()
        if any(heading.startswith(prefix) for prefix in SCREENED_HEADINGS):
            screened.append({"unit_id": unit["unit_id"], "reason": "navigation_or_monitoring_heading"})
        elif not heading and unit["text"].lower().startswith("contents"):
            screened.append({"unit_id": unit["unit_id"], "reason": "contents_text"})
        else:
            kept.append(unit)
    return kept, screened


def build_index(units: Sequence[dict], path: str = ":memory:") -> sqlite3.Connection:
    """Create an FTS5 index over operative units plus a metadata table for citation spans."""
    conn = sqlite3.connect(path)
    try:
        conn.execute("CREATE VIRTUAL TABLE units USING fts5(unit_id UNINDEXED, document UNINDEXED, heading, text)")
    except sqlite3.OperationalError as exc:
        raise RuntimeError("SQLite FTS5 is unavailable in this interpreter; use an interpreter built with FTS5") from exc
    conn.execute("CREATE TABLE unit_meta (unit_id TEXT PRIMARY KEY, document TEXT, heading TEXT, "
                 "text TEXT, page_start INTEGER, page_end INTEGER)")
    rows = [(u["unit_id"], u["document"], u["heading"], u["text"], u["page_start"], u["page_end"]) for u in units]
    conn.executemany("INSERT INTO units (unit_id, document, heading, text) VALUES (?, ?, ?, ?)",
                     [row[:4] for row in rows])
    conn.executemany("INSERT INTO unit_meta VALUES (?, ?, ?, ?, ?, ?)", rows)
    conn.commit()
    return conn


def _unit(conn: sqlite3.Connection, unit_id: str) -> dict:
    row = conn.execute("SELECT unit_id, document, heading, text, page_start, page_end FROM unit_meta "
                       "WHERE unit_id = ?", (unit_id,)).fetchone()
    keys = ("unit_id", "document", "heading", "text", "page_start", "page_end")
    return dict(zip(keys, row))


def _match_expression(query: str) -> tuple[str, list[str]]:
    terms = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if t not in STOPWORDS and len(t) > 1]
    terms = list(dict.fromkeys(terms))
    return " OR ".join(f'"{term}"' for term in terms), terms


def search_lexical(conn: sqlite3.Connection, query: str, k: int, offset: int = 0) -> list[dict]:
    """Rank units by FTS5 bm25() over an OR of quoted query terms; lower score ranks first."""
    expression, terms = _match_expression(query)
    if not terms:
        return []
    rows = conn.execute("SELECT unit_id, bm25(units) FROM units WHERE units MATCH ? "
                        "ORDER BY bm25(units), unit_id LIMIT ? OFFSET ?", (expression, k, offset)).fetchall()
    return [dict(_unit(conn, unit_id), score=score) for unit_id, score in rows]


def resolve_references(text: str) -> list[str]:
    """Find named references (policy codes, tables, figures, appendices, SPDs) in text."""
    found: list[str] = []
    for label, pattern in REFERENCE_PATTERNS:
        for match in pattern.finditer(text):
            found.append(f"{label} {re.sub(r'\s+', '', match.group(1)).upper() if label == 'Policy' else match.group(1)}")
    for match in SPD_PATTERN.finditer(text):
        found.append(re.sub(r"\s+", " ", match.group(1)))
    return list(dict.fromkeys(found))


def lookup_reference(conn: sqlite3.Connection, reference: str) -> list[dict]:
    """Deterministic lookup of a named reference by heading prefix or document identity."""
    normalised = re.sub(r"\s+", " ", reference.strip()).lower()
    rows = conn.execute(
        "SELECT unit_id FROM unit_meta WHERE lower(heading) = ? OR lower(heading) LIKE ? OR document = ? "
        "ORDER BY document, page_start, unit_id",
        (normalised, normalised + " %", _slug(reference))).fetchall()
    return [_unit(conn, unit_id) for (unit_id,) in rows]


def rrf(rankings: Sequence[Sequence[str]], k: int = 60) -> list[tuple[str, float]]:
    """Reciprocal rank fusion: score(d) = sum over lists of 1 / (k + rank)."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, unit_id in enumerate(ranking, start=1):
            scores[unit_id] = scores.get(unit_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


def search_hybrid(conn: sqlite3.Connection, query: str, k: int,
                  embed: Callable[[str], Sequence[float]] | None = None,
                  unit_vectors: dict[str, Sequence[float]] | None = None) -> list[dict]:
    """Fuse lexical and cosine rankings with RRF; lexical only when no embedder is supplied."""
    lexical = search_lexical(conn, query, k)
    if embed is None or not unit_vectors:
        return lexical
    query_vector = embed(query)
    dense = sorted(((cosine(query_vector, vector), unit_id) for unit_id, vector in unit_vectors.items()),
                   key=lambda item: (-item[0], item[1]))
    dense_ids = [unit_id for similarity, unit_id in dense[:k] if similarity > 0]
    fused = rrf([[unit["unit_id"] for unit in lexical], dense_ids])
    return [dict(_unit(conn, unit_id), score=score) for unit_id, score in fused[:k]]


def retrieve_for_issues(conn: sqlite3.Connection, issues: Sequence[str | dict], k: int = 4,
                        call_budget: int | None = None) -> dict:
    """One query per issue, deterministic reference lookups, then one bounded second round."""
    normalised = [issue if isinstance(issue, dict) else {"id": f"issue-{i + 1}", "query": issue}
                  for i, issue in enumerate(issues)]
    if call_budget is None:
        call_budget = 4 * len(normalised)
    report = {"k": k, "call_budget": call_budget, "calls_run": 0, "queries_run": 0, "lookups_run": 0,
              "second_round_ran": False, "budget_exhausted": False, "issues": {}}

    def spend(kind: str) -> bool:
        if report["calls_run"] >= call_budget:
            report["budget_exhausted"] = True
            return False
        report["calls_run"] += 1
        report[kind] += 1
        return True

    def add_found(entry: dict, units: Iterable[dict]) -> None:
        for unit in units:
            if unit["unit_id"] not in entry["found_ids"]:
                entry["found_ids"].append(unit["unit_id"])
                entry["found"].append({key: unit[key] for key in
                                       ("unit_id", "document", "heading", "page_start", "page_end")})

    def resolve(entry: dict, units: Iterable[dict], query: str) -> None:
        references = resolve_references(query)
        for unit in units:
            references.extend(resolve_references(unit["heading"] + "\n" + unit["text"]))
        for reference in dict.fromkeys(references):
            if reference in entry["resolved_references"] or reference in entry["unresolved_references"]:
                continue
            self_cited = [f["unit_id"] for f in entry["found"]
                          if f["heading"].lower().startswith(reference.lower())]
            if self_cited:
                entry["resolved_references"][reference] = self_cited
                continue
            if not spend("lookups_run"):
                return
            hits = lookup_reference(conn, reference)
            if hits:
                entry["resolved_references"][reference] = [hit["unit_id"] for hit in hits]
                add_found(entry, hits)
            else:
                entry["unresolved_references"].append(reference)

    for issue in normalised:
        entry = {"query": issue["query"], "found": [], "found_ids": [], "truncated": False,
                 "resolved_references": {}, "unresolved_references": [], "rounds": 0}
        report["issues"][issue["id"]] = entry
        if not spend("queries_run"):
            entry["skipped"] = "budget_exhausted"
            continue
        entry["rounds"] = 1
        hits = search_lexical(conn, issue["query"], k)
        entry["truncated"] = len(hits) == k
        add_found(entry, hits)
        resolve(entry, hits, issue["query"])

    for issue in normalised:
        entry = report["issues"][issue["id"]]
        if "skipped" in entry:
            continue
        needs_more = not entry["found"] or entry["unresolved_references"] or entry["truncated"]
        if not needs_more or report["budget_exhausted"]:
            continue
        if not spend("queries_run"):
            break
        report["second_round_ran"] = True
        entry["rounds"] = 2
        if entry["truncated"] and entry["found"] and not entry["unresolved_references"]:
            hits = search_lexical(conn, issue["query"], k, offset=k)
        else:
            hits = search_lexical(conn, issue["query"] + " " + " ".join(entry["unresolved_references"]), k)
        entry["truncated"] = len(hits) == k
        add_found(entry, hits)
        resolve(entry, hits, issue["query"])

    for entry in report["issues"].values():
        entry.pop("found_ids")
        if not entry["found"]:
            entry["found"] = "none_found"
    return report


def found_unit_ids(report: dict) -> dict[str, list[str]]:
    return {issue_id: [] if entry["found"] == "none_found" else [u["unit_id"] for u in entry["found"]]
            for issue_id, entry in report["issues"].items()}


def sufficiency_problems(report: dict) -> list[str]:
    """Name every reason the drafting stage must decline rather than reason from memory."""
    problems = []
    for issue_id, entry in report["issues"].items():
        if entry.get("skipped"):
            problems.append(f"{issue_id}: not searched ({entry['skipped']})")
        elif entry.get("found") == "none_found":
            problems.append(f"{issue_id}: none_found")
        for reference in entry.get("unresolved_references", []):
            problems.append(f"{issue_id}: unresolved reference {reference}")
        if entry.get("truncated") and not report.get("second_round_ran"):
            problems.append(f"{issue_id}: truncated search without a second round")
    if report.get("budget_exhausted"):
        problems.append("call budget exhausted before every issue was served")
    return problems


def recall_at_k(gold: dict, results: dict[str, Sequence[str]]) -> dict:
    """Per-question recall over required unit IDs; results come from the retriever, gold from the evaluator."""
    per_question = {}
    for question_id, expected in gold.items():
        required = set(expected["required_units"])
        if not required:
            raise ValueError(f"{question_id}: required_units must be nonempty")
        per_question[question_id] = len(required & set(results.get(question_id, []))) / len(required)
    mean = sum(per_question.values()) / len(per_question) if per_question else 0.0
    return {"per_question": per_question, "mean": mean}


def precision_at_k(gold: dict, results: dict[str, Sequence[str]]) -> dict:
    """Share of retrieved units that are required; an empty result set scores 0.0."""
    per_question = {}
    for question_id, expected in gold.items():
        required = set(expected["required_units"])
        found = list(dict.fromkeys(results.get(question_id, [])))
        per_question[question_id] = len(required & set(found)) / len(found) if found else 0.0
    mean = sum(per_question.values()) / len(per_question) if per_question else 0.0
    return {"per_question": per_question, "mean": mean}


def irrelevant_hits(gold: dict, results: dict[str, Sequence[str]]) -> dict[str, list[dict]]:
    """Listed off-topic units that reached the result set, with their rank: ranking noise, not a failure."""
    report = {}
    for question_id, expected in gold.items():
        listed = set(expected.get("irrelevant_units", []))
        found = list(dict.fromkeys(results.get(question_id, [])))
        report[question_id] = [{"unit_id": unit_id, "rank": rank}
                               for rank, unit_id in enumerate(found, start=1) if unit_id in listed]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, default=GOLD, help="fixture with pages and evaluator-side questions")
    parser.add_argument("--issues", help="JSON list of issue queries; defaults to the gold questions")
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--call-budget", type=int, default=None)
    args = parser.parse_args(argv)
    try:
        fixture = json.loads(args.gold.read_text(encoding="utf-8"))
        if args.issues:
            issues = json.loads(args.issues)
            if not isinstance(issues, list) or not all(isinstance(i, str) and i.strip() for i in issues):
                raise ValueError("--issues must be a JSON list of nonempty strings")
        else:
            issues = [{"id": qid, "query": q["question"]} for qid, q in fixture["questions"].items()]
        kept, screened = screen_units(chunk_by_heading(fixture_pages(fixture)))
        conn = build_index(kept)
        report = retrieve_for_issues(conn, issues, k=args.k, call_budget=args.call_budget)
        output = {"screened_units": screened, "report": report, "problems": sufficiency_problems(report)}
        if not args.issues:
            results = found_unit_ids(report)
            output["recall"] = recall_at_k(fixture["questions"], results)
            output["precision"] = precision_at_k(fixture["questions"], results)
            output["irrelevant_hits"] = irrelevant_hits(fixture["questions"], results)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
