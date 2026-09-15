"""Offline behavioural checks for the read-only inventory helper."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
SPEC = importlib.util.spec_from_file_location("memory_inspector", SCRIPT)
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)


@pytest.fixture(autouse=True)
def baseline_runtime(monkeypatch):
    monkeypatch.setattr(
        inspector,
        "runtime_versions",
        lambda: {"python": "3.11.4", "installed": {"google-adk": "2.8.0"}},
    )


def test_reads_signals_without_executing_or_echoing_source(tmp_path):
    (tmp_path / "agent.py").write_text(
        'raise RuntimeError("must not execute")\n'
        'from google.adk.sessions import InMemorySessionService\n'
        'secret = "synthetic-sensitive-canary"\n',
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text("google-adk==2.8.0\n", encoding="utf-8")
    report, code = inspector.inspect_project(tmp_path)
    assert code == 0
    assert report["signals"]["sessions"] == ["agent.py"]
    assert "synthetic-sensitive-canary" not in json.dumps(report)
    assert report["security"] == "not_evaluated"
    assert report["compatibility"] == "adk_baseline_matches_other_contracts_unchecked"


def test_credential_files_and_external_symlinks_are_not_read(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "private.py").write_text("from google.cloud import bigquery\n")
    project = tmp_path / "project"
    project.mkdir()
    (project / ".env").write_text("SECRET=synthetic-env-canary\n")
    (project / "secret.json").write_text('{"token":"synthetic-json-canary"}')
    (project / "external").symlink_to(outside, target_is_directory=True)
    (project / "linked.py").symlink_to(outside / "private.py")
    report, _ = inspector.inspect_project(project)
    assert report["coverage"]["read_files"] == 0
    assert report["signals"]["bigquery"] == []
    assert "canary" not in json.dumps(report)


def test_dry_run_does_not_read_project_files(tmp_path, monkeypatch):
    (tmp_path / "agent.py").write_text("this is not valid Python")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("dry run must not walk project files")

    monkeypatch.setattr(inspector.os, "walk", forbidden)
    report, code = inspector.inspect_project(tmp_path, dry_run=True)
    assert code == 0
    assert report["dry_run"] is True
    assert report["coverage"]["read_files"] == 0


@pytest.mark.parametrize(
    "content,expected",
    [
        ("google-adk==1.20.0", "declared_installed_adk_mismatch"),
        ("google-adk==2.8.0\ngoogle-adk==2.9.0", "conflicting_declared_adk_pins"),
    ],
)
def test_pin_conflict_is_actionable_without_mutating(tmp_path, content, expected):
    manifest = tmp_path / "requirements.txt"
    manifest.write_text(content)
    report, code = inspector.inspect_project(tmp_path)
    assert code == 3
    assert report["compatibility"] == expected
    assert manifest.read_text() == content


def test_matching_unsupported_major_fails_clearly(tmp_path, monkeypatch):
    (tmp_path / "requirements.txt").write_text("google-adk==1.20.0")
    monkeypatch.setattr(
        inspector, "runtime_versions",
        lambda: {"python": "3.11.4", "installed": {"google-adk": "1.20.0"}},
    )
    report, code = inspector.inspect_project(tmp_path)
    assert code == 3
    assert report["compatibility"] == "unsupported_adk_major_for_source_guidance"


def test_ranges_are_not_reported_as_resolved_pins(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies = ["google-adk>=2.7,<3"]\n'
    )
    report, code = inspector.inspect_project(tmp_path)
    assert code == 0
    assert report["compatibility"] == "not_established"
    assert report["declarations"][0]["operator"] == ">="


@pytest.mark.parametrize("version", ["2.8.0.post1", "2.8.0.dev1", "2.8.0+vendor"])
def test_version_suffix_is_not_silently_treated_as_the_baseline(tmp_path, version):
    (tmp_path / "requirements.txt").write_text(f"google-adk=={version}\n")
    report, code = inspector.inspect_project(tmp_path)
    assert report["declarations"][0]["version"] == version
    assert report["compatibility"] == "declared_installed_adk_mismatch"
    assert code == 3


def test_explicit_rag_adapter_is_found_without_instantiating_client(tmp_path):
    (tmp_path / "retrieval.py").write_text(
        "from google.cloud.aiplatform_v1.types import vertex_rag_service\n"
        "def retrieve(client, request):\n"
        "    return client.retrieve_contexts(request=request)\n"
    )
    report, code = inspector.inspect_project(tmp_path)
    assert code == 0
    assert report["signals"]["rag"] == ["retrieval.py"]
    assert report["security"] == "not_evaluated"


def test_repeat_is_identical_and_creates_nothing(tmp_path):
    (tmp_path / "requirements.txt").write_text("google-adk==2.8.0")
    before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    first = inspector.inspect_project(tmp_path)
    second = inspector.inspect_project(tmp_path)
    assert first == second
    assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before


def test_bounded_scan_reports_incomplete_coverage(tmp_path, monkeypatch):
    for index in range(3):
        (tmp_path / f"file{index}.py").write_text("value = 1\n")
    monkeypatch.setattr(inspector, "LIMIT_FILES", 1)
    report, _ = inspector.inspect_project(tmp_path)
    assert report["coverage"]["read_files"] == 1
    assert any("file limit" in warning for warning in report["warnings"])


def test_missing_project_has_clean_error(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project", str(tmp_path / "missing")],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 2
    assert "existing non-symlink directory" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("arguments", [["--help"], ["--dry-run"]])
def test_cli_help_and_dry_run(tmp_path, arguments):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project", str(tmp_path), *arguments],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0
    if "--dry-run" in arguments:
        assert json.loads(result.stdout)["dry_run"] is True
    else:
        assert "--project" in result.stdout
