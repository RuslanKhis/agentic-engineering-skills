"""Ingestion controls: a header-only scan never passes as a text page."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
FIXTURE = Path(__file__).resolve().parents[1] / "assets" / "ingestion-fixture"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


qualify = load("qualify_ingestion")
generator = load("make_ingestion_fixture")


@pytest.fixture
def inventory():
    return json.loads((FIXTURE / "inventory.json").read_text(encoding="utf-8"))["pages"]


def page(inventory, name):
    return next(p for p in inventory if p["document"] == name)


def test_header_only_scan_is_low_density_and_routed_to_ocr_or_vision(inventory):
    result = qualify.classify_page(page(inventory, "scanned-page.pdf"))
    assert result["density"] == "low_density"
    assert result["route"] == "ocr_or_vision"
    assert result["image_count"] == 1
    # A high alphanumeric ratio on 34 characters is not evidence of a text page.
    assert result["alnum_ratio"] > 0.9 and result["chars"] < 60


def test_prose_page_routes_to_text(inventory):
    result = qualify.classify_page(page(inventory, "text-page.pdf"))
    assert result["density"] == "text"
    assert result["route"] == "text"
    assert result["table_candidate"] is False
    assert result["drawing_candidate"] is False


def test_table_page_is_flagged_and_routed_both(inventory):
    result = qualify.classify_page(page(inventory, "table-page.pdf"))
    assert result["table_candidate"] is True
    assert result["drawing_candidate"] is False
    assert result["route"] == "both"


def test_drawing_page_separates_dimensions_from_scale(inventory):
    result = qualify.classify_page(page(inventory, "drawing-page.pdf"))
    assert result["drawing_candidate"] is True
    assert "6.0 m" in result["written_dimensions"]
    assert any("1:200" in s for s in result["scale_statements"])
    assert result["route"] == "both"


def test_report_summary_counts_visual_pass_and_flags(inventory):
    report = qualify.qualify(inventory)
    summary = report["summary"]
    assert summary["pages"] == 4
    assert ("scanned-page.pdf", 1) in summary["low_density_pages"]
    assert summary["table_candidates"] == [("table-page.pdf", 1)]
    assert summary["drawing_candidates"] == [("drawing-page.pdf", 1)]
    assert summary["estimated_visual_pass_images"] == 3
    assert summary["reading_order_anomalies"] == []
    assert report["ocr_executed"] is False
    assert report["visual_review_executed"] is False


def test_missing_and_out_of_order_pages_are_anomalies():
    pages = [{"document": "plan.pdf", "page": 3, "text": "x" * 300},
             {"document": "plan.pdf", "page": 1, "text": "y" * 300}]
    anomalies = qualify.qualify(pages)["summary"]["reading_order_anomalies"]
    assert any("out of order" in a for a in anomalies)
    assert any("missing pages [2]" in a for a in anomalies)


def test_thresholds_change_classification(inventory):
    scan = page(inventory, "scanned-page.pdf")
    assert qualify.classify_page(scan, min_chars=20)["density"] == "text"
    prose = page(inventory, "text-page.pdf")
    assert qualify.classify_page(prose, min_chars=1000)["density"] == "low_density"
    garbled = {"document": "g.pdf", "page": 1, "text": "@#% ^&* ()!! ~~~ " * 30}
    assert qualify.classify_page(garbled)["density"] == "low_density"


def test_empty_text_with_image_is_image_only_and_empty_inventory_rejected():
    result = qualify.classify_page({"document": "s.pdf", "page": 1, "text": "", "image_count": 1})
    assert result["density"] == "image_only" and result["route"] == "ocr_or_vision"
    assert result["text_origin"] == "none"
    with pytest.raises(ValueError):
        qualify.qualify([])


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generator_is_deterministic_and_matches_committed_assets(tmp_path):
    first, second = tmp_path / "a", tmp_path / "b"
    generator.write_fixture(first)
    generator.write_fixture(second)
    names = sorted(p.name for p in first.iterdir())
    assert names == ["drawing-page.pdf", "inventory.json", "scanned-page.pdf",
                     "table-page.pdf", "text-page.pdf"]
    for name in names:
        assert sha256_of(first / name) == sha256_of(second / name)
        assert sha256_of(first / name) == sha256_of(FIXTURE / name), name


def test_fixture_pdfs_have_pdf_header_and_trailer():
    for pdf in FIXTURE.glob("*.pdf"):
        data = pdf.read_bytes()
        assert data.startswith(b"%PDF-"), pdf.name
        assert data.rstrip().endswith(b"%%EOF"), pdf.name
        assert b"/Type /Page" in data


def test_inventory_is_labelled_as_generator_knowledge():
    manifest = json.loads((FIXTURE / "inventory.json").read_text(encoding="utf-8"))
    assert manifest["kind"] == "generator_knowledge_not_extraction_result"
    assert len(manifest["pages"]) == 4


def test_pypdf_inventory_when_available():
    pytest.importorskip("pypdf")
    scanned = qualify.inventory_from_pdf(FIXTURE / "scanned-page.pdf")
    prose = qualify.inventory_from_pdf(FIXTURE / "text-page.pdf")
    assert len(scanned[0]["text"]) < 60 and scanned[0]["image_count"] == 1
    assert len(prose[0]["text"]) > 200 and prose[0]["image_count"] == 0
    assert qualify.classify_page(scanned[0])["route"] == "ocr_or_vision"


def test_pdf_path_is_blocked_without_pypdf(monkeypatch):
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pypdf":
            raise ImportError("simulated absence")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(RuntimeError, match="blocked: pypdf not installed"):
        qualify.inventory_from_pdf(FIXTURE / "scanned-page.pdf")
