"""Classify extracted pages before any model call: density, route and hints.

Input is a page inventory produced by the target's extractor (or, when pypdf
is installed, built here from a PDF). Output is an ingestion report: per-page
character count, alphanumeric ratio, density class, table/drawing hints, the
written dimensions and scale statements found in the text layer, and the
route each page should take (text, OCR/vision, or both). The report is
information for the officer, reviewer and model; it is not a pass/fail gate.

Thresholds are starting defaults. Calibrate them on the supplied corpus and
record the chosen values with the case. See references/document-ingestion.md.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


DEFAULT_MIN_CHARS = 200
DEFAULT_MIN_ALNUM_RATIO = 0.5
DEFAULT_MIN_VECTOR_OPS = 8

SCALE_PATTERN = re.compile(r"\b(?:scale\s*)?1\s*:\s*\d{2,5}\b|\bscale\s+bar\b|\bnot\s+to\s+scale\b",
                           re.IGNORECASE)
DIMENSION_PATTERN = re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:mm|cm|m|metres?|meters?)\b", re.IGNORECASE)
TABLE_CAPTION = re.compile(r"\btable\s+\d+\b", re.IGNORECASE)
NUMERIC_CELL = re.compile(r"(?:^|\s)\d+(?:[.,]\d+)?(?:\s|$)")


def alnum_ratio(text: str) -> float:
    visible = [c for c in text if not c.isspace()]
    if not visible:
        return 0.0
    return sum(c.isalnum() for c in visible) / len(visible)


def table_hint(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    delimited = sum(("|" in line or "\t" in line) for line in lines)
    numeric_rows = sum(len(NUMERIC_CELL.findall(line)) >= 2 for line in lines)
    return bool(TABLE_CAPTION.search(text)) and (delimited >= 2 or numeric_rows >= 2) \
        or delimited >= 3 or numeric_rows >= 3


def classify_page(record: dict, *, min_chars: int = DEFAULT_MIN_CHARS,
                  min_alnum_ratio: float = DEFAULT_MIN_ALNUM_RATIO,
                  min_vector_ops: int = DEFAULT_MIN_VECTOR_OPS) -> dict:
    """Return the per-page classification; never mutates the input record."""
    text = record.get("text") or ""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    chars = len(text.strip())
    ratio = alnum_ratio(text)
    images = int(record.get("image_count") or 0)
    vector_ops = int(record.get("vector_drawing_ops") or 0)
    scales = sorted({m.group(0).strip() for m in SCALE_PATTERN.finditer(text)})
    dimensions = sorted({m.group(0).strip() for m in DIMENSION_PATTERN.finditer(text)})

    if chars == 0:
        density = "image_only" if images else "empty"
    elif chars < min_chars or ratio < min_alnum_ratio:
        density = "low_density"
    else:
        density = "text"

    table = table_hint(text)
    drawing = bool(scales) or (vector_ops >= min_vector_ops and bool(dimensions) and not table)
    # A drawing or table page keeps its native text (dimensions, cells) AND
    # needs the rendered page; a sparse page without those hints is a scan.
    if table or drawing:
        route = "both"
    elif density in ("image_only", "empty", "low_density"):
        route = "ocr_or_vision"
    elif images:
        route = "both"
    else:
        route = "text"
    return {
        "document": record.get("document"),
        "page": record.get("page"),
        "chars": chars,
        "alnum_ratio": round(ratio, 3),
        "image_count": images,
        "vector_drawing_ops": vector_ops,
        "density": density,
        "table_candidate": table,
        "drawing_candidate": drawing,
        "written_dimensions": dimensions,
        "scale_statements": scales,
        "route": route,
        "text_origin": "native" if chars else "none",
    }


def reading_order_anomalies(pages: list[dict]) -> list[str]:
    anomalies = []
    by_document: dict[str, list[int]] = {}
    for page in pages:
        number = page.get("page")
        if not isinstance(number, int) or number < 1:
            anomalies.append(f"{page.get('document')}: page number missing or invalid")
            continue
        by_document.setdefault(str(page.get("document")), []).append(number)
    for document, numbers in by_document.items():
        if numbers != sorted(numbers):
            anomalies.append(f"{document}: pages out of order {numbers}")
        expected = list(range(1, max(numbers) + 1))
        missing = sorted(set(expected) - set(numbers))
        if missing:
            anomalies.append(f"{document}: missing pages {missing}")
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        if duplicates:
            anomalies.append(f"{document}: duplicate pages {duplicates}")
    return anomalies


def qualify(pages: list[dict], **thresholds) -> dict:
    if not isinstance(pages, list) or not pages:
        raise ValueError("inventory must be a nonempty list of page records")
    classified = [classify_page(page, **thresholds) for page in pages]
    low = [p for p in classified if p["density"] == "low_density"]
    image_only = [p for p in classified if p["density"] in ("image_only", "empty")]
    visual_pass = [p for p in classified if p["route"] != "text"]
    return {
        "thresholds": {
            "min_chars": thresholds.get("min_chars", DEFAULT_MIN_CHARS),
            "min_alnum_ratio": thresholds.get("min_alnum_ratio", DEFAULT_MIN_ALNUM_RATIO),
            "min_vector_ops": thresholds.get("min_vector_ops", DEFAULT_MIN_VECTOR_OPS),
            "status": "defaults; calibrate on the target corpus",
        },
        "summary": {
            "pages": len(classified),
            "low_density_pages": [(p["document"], p["page"]) for p in low],
            "image_only_pages": [(p["document"], p["page"]) for p in image_only],
            "table_candidates": [(p["document"], p["page"]) for p in classified if p["table_candidate"]],
            "drawing_candidates": [(p["document"], p["page"]) for p in classified if p["drawing_candidate"]],
            "reading_order_anomalies": reading_order_anomalies(pages),
            "estimated_visual_pass_images": len(visual_pass),
        },
        "pages": classified,
        "ocr_executed": False,
        "visual_review_executed": False,
    }


def inventory_from_pdf(path: Path) -> list[dict]:
    """Build an inventory with pypdf when it is installed; otherwise raise."""
    try:
        from pypdf import PdfReader  # optional, never required by the tests
    except ImportError as exc:
        raise RuntimeError("blocked: pypdf not installed; supply --inventory from your extractor") from exc
    reader = PdfReader(str(path))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        xobjects = page.get("/Resources", {}).get("/XObject", {}) or {}
        images = sum(1 for key in xobjects if xobjects[key].get_object().get("/Subtype") == "/Image")
        pages.append({"document": path.name, "page": number,
                      "text": page.extract_text() or "", "image_count": images})
    return pages


def load_inventory(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("pages"), list):
        return data["pages"]
    if isinstance(data, list):
        return data
    raise ValueError("inventory must be a list of pages or an object with a pages list")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--inventory", type=Path, help="page inventory JSON from your extractor")
    source.add_argument("--pdf", type=Path, help="build the inventory with pypdf if installed")
    parser.add_argument("--min-chars", type=int, default=DEFAULT_MIN_CHARS,
                        help="below this a page is low density (default to calibrate)")
    parser.add_argument("--min-alnum-ratio", type=float, default=DEFAULT_MIN_ALNUM_RATIO,
                        help="below this a page is low density (default to calibrate)")
    parser.add_argument("--min-vector-ops", type=int, default=DEFAULT_MIN_VECTOR_OPS,
                        help="with a written dimension, this many vector ops marks a drawing")
    args = parser.parse_args()
    try:
        pages = inventory_from_pdf(args.pdf) if args.pdf else load_inventory(args.inventory)
    except RuntimeError as exc:
        print(exc)
        return 2
    try:
        report = qualify(pages, min_chars=args.min_chars, min_alnum_ratio=args.min_alnum_ratio,
                         min_vector_ops=args.min_vector_ops)
    except (ValueError, TypeError) as exc:
        print(f"invalid inventory: {exc}")
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
