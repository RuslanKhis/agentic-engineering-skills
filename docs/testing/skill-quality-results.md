# Skill quality checks — 15 September 2026

## Package and helper validation

Ran `python scripts/check_repo.py` in a fresh temporary virtual environment on
macOS with Python **3.12.9**, PyYAML **6.0.3**, markdown-it-py **4.0.0** and
pytest **9.1.1**. These were maintainer dependencies; ADK was not installed in
that environment.

| Check | Result |
| --- | --- |
| Distributable packages | 12 packages; 109 Markdown files and 40 Python files; zero reported errors or warnings |
| Evaluation input structure | 24 activation cases and 6 contextual scenarios valid; all twelve skills have positive and near-miss labels |
| Validator and runner regression tests | 35 passed |
| Existing helper suites | 314 passed; 12 optional SDK/telemetry checks skipped |
| Combined local test result | **349 passed, 12 skipped**; process exit 0 |
| Skill-creator validator for revised `adk-engineer` | Passed |

The helper total includes 16 memory tests run with pytest. Workflow's SDK
runtime tests and the guardrails `adk_boundary.py` suite were outside this tier.
The [coverage guide](skill-quality.md) explains those boundaries. GitHub Actions
was added for Python 3.11/3.12, but a hosted CI run was not executed in this task.

The empty-discovery problem was reproduced separately: top-level unittest
discovery reported zero tests and success. The new runner's regression tests
verify that empty and failing selected suites return a nonzero result.

## Independent router composition walkthrough

A fresh Codex subagent received the revised router, a minimal synthetic existing
Agents CLI project and the [read-only design request](artifacts/skill-quality-design/prompt.txt).
Its available fixture skills were the router, memory specialist and Google's
workflow/code skills from the previously reviewed 1.5.0 download. It received
neither the expected answer nor this review's findings.

The [resulting design](artifacts/skill-quality-design/design.md) was checked
against the fixture and task:

| Observation | Assessment |
| --- | --- |
| Applied the composition reference and memory specialist | Recorded in the execution agent's source list; the design reflects their division of responsibilities |
| Kept the accepted SQLite profile approach | Proposed explicit consent, trusted identity, restart persistence and forgetting within the existing data boundary |
| Preserved the requested design-only scope | No implementation or platform execution; all fixture files retained their original SHA-256 hashes |
| Preserved uncertainty | Identified the placeholder serving boundary and unverified installed SDK; did not claim working authentication, runtime tests or Cloud Run durability |

The synthetic [input project](artifacts/skill-quality-design/project/.agents-cli-spec.md)
and [provenance record](artifacts/skill-quality-design/provenance.json) retain
file hashes and limits. Its manifest and serving code are minimal context for
a design exercise, not a validated Agents CLI scaffold or runnable application.
The exact model identifier and usage were not recorded.

This was one explicit-router design walkthrough. It does not establish natural
skill activation, working generated code, combined platform compatibility or
improvement over a baseline. The other authored scenarios remain unevaluated.

Follow [the evaluation protocol](skill-quality.md) for repeated, paired tests
before making performance or reliability improvement claims.
