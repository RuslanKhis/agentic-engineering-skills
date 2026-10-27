"""Source stage: application documents and local-plan policies as numbered, immutable spans."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

POLICIES = Path(__file__).resolve().parent.parent / "cases" / "local-plan.json"


@dataclass(frozen=True)
class Span:
    span_id: str          # "<doc_id>@<version>:p<page>:<line>"
    doc_id: str
    version: str
    page: int
    line: int
    text: str


def load_case(case_dir: Path) -> dict:
    return json.loads((Path(case_dir) / "application.json").read_text(encoding="utf-8"))


def load_policies(path: Path = POLICIES) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def spans_for(documents: list[dict]) -> list[Span]:
    spans = []
    for doc in documents:
        for page in doc["pages"]:
            for n, line in enumerate(page["text"].split("\n"), 1):
                if line.strip():
                    spans.append(Span(f"{doc['doc_id']}@{doc['version']}:p{page['page']}:{n}",
                                      doc["doc_id"], doc["version"], page["page"], n, line))
    return spans


def case_spans(case: dict, policies: dict) -> list[Span]:
    return spans_for(case["documents"]) + spans_for(policies["documents"])


def representation(spans: list[Span], max_chars: int) -> str:
    """What the writer sees: one span per line, cut at max_chars."""
    text = "\n".join(f"[{s.span_id}] {s.text}" for s in spans)
    return text[:max_chars]


def manifest(spans: list[Span]) -> dict:
    """Identity of the source input: every span id with a hash of its text."""
    rows = {s.span_id: hashlib.sha256(s.text.encode()).hexdigest()[:16] for s in spans}
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    return {"spans": len(rows), "sha256": digest}
