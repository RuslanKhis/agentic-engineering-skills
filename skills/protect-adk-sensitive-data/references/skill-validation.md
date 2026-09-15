# Skill creation validation — 15 September 2026

This record covers the skill package, not a new live validation of Google Cloud
or the companion application. All work used the existing Python 3.11.4 virtual
environment on macOS 26.6.2 arm64. No packages were installed and no cloud
resources, IAM policies, APIs, secrets or deployments were changed.

## Package checks

Commands used the repository's existing `.venv/bin/python`; `python` below is
that interpreter, not a newly installed runtime. Paths are relative to the
repository root unless noted.

| Command/check | Actual result |
| --- | --- |
| Installed skill-creator `quick_validate.py skills/protect-adk-sensitive-data` | `Skill is valid!` |
| `python -B -m unittest discover -s skills/protect-adk-sensitive-data/tests -v` | **28 passed**: 14 inspector, 14 SDP controller |
| `python -B skills/protect-adk-sensitive-data/scripts/inspect_project.py --help` | Exit 0; root-only scope and dry-run documented |
| Same helper with `chapter-08-sensitive-data --dry-run` | Exit 0; `files_read=[]`, no constraints read, no writes |
| Same helper with `chapter-08-sensitive-data` | Exit 0; ADK/DLP/Armor/Pydantic constraints inventoried; extras omission flagged, compatibility explicitly not assessed |
| `python -B -m tabnanny skills/protect-adk-sensitive-data` | Exit 0 |
| `python -B scripts/check_yaml.py` | 27 repository YAML files parsed, including the new UI metadata |
| Python AST / Markdown shell-fence checks | All four bundled Python files parsed; both shell blocks passed `bash -n` |
| Frontmatter/UI/link checks | Valid YAML, matching name under 64 characters, valid UI description/prompt, automatic invocation allowed; all 21 local links resolve inside the package |
| Text/package checks | 14 non-empty files; no empty directories, unfinished markers, trailing whitespace, machine-local paths or copied personal resource identifiers; MIT notice retained |
| `git diff --check` | Exit 0; new untracked skill files also received the separate whitespace check above |

There is no configured formatter/linter for this new skills directory; Black
and Ruff were not installed in the existing environment. No formatter/linter
pass is claimed. Syntax, indentation and whitespace checks are named above.
The suite initially had 27 tests. A final explicit older-interpreter guard in
the optional inspector added one regression, bringing the final suite to 28.
Older-version rejection is simulated in tests, not an actual Python 3.10 run.

Controller tests covered incomplete inspections, failure/timeout/cancellation,
deterministic repetition, concurrency, bounds and synthetic PII protection
before model, session, tool and captured logging sinks. Fake provider functions
establish control flow, not live detector accuracy.

## Standalone copy

Copied the complete skill into a fresh OS temporary directory, alongside a
minimal Python/ADK manifest fixture and without the book or companion source.
Ran helper help, dry-run and normal inspection from that directory: all exited
0, and dry-run read no contents. Repeated the package tests from the copy with
socket connection methods patched to fail. The final copy passed **28 tests**.
The existing virtual environment supplied the interpreter; no companion module
was imported and its repository was not placed on `PYTHONPATH`.

## Independent forward tests

Three independent Codex agents received a copied skill, raw synthetic fixtures
and realistic user requests. They did not receive the chapter, companion source,
conversation or an expected-answer rubric. The environment was explicitly
offline and used the existing interpreter. Each agent recorded actual changes,
commands and limitations. The main agent reviewed their reports and changed
files after execution.

| Scenario and request | Observed outcome |
| --- | --- |
| Greenfield: implement input preparation for a planned ADK assistant with injected host model/history, preserving pins | Adapted the asset, added byte/concurrency/deadline bounds and metadata-only logging; retained MIT notice. **28 fixture tests passed**; rejected/incomplete inputs called no sinks |
| Existing customised project: fix input ordering and public shipment results while preserving signatures/domain/auth | Moved protection before history/log/model; projected and validated custom `SHP:` references, statuses and 512-character notes before and after screening. **53 tests passed**; original metadata, pins, signatures and tests preserved |
| Missing prerequisites: prepare real SDP without project access, templates or ADC | Prepared a lazy typed SDK adapter, config validation before client creation and a readiness document. Expanded greenfield suite: **59 passed**, including 31 SDK-shaped adapter cases; one expected warning for a synthetic unknown enum. No production fallback or dependency change; real activation remains pending |
| Consequential: prepare APIs, templates, runtime IAM, bounded smoke and cleanup | Generated a deterministic draft manifest and separate setup/smoke/cleanup workflow; **4 planner tests passed**. Five proposed template names, budgets and unresolved identities/policy were explicit. No cloud executor or ownership claim; concrete-scope approval and separate cleanup confirmation remain required |
| Near miss: static website Cloud Armor WAF rate limiting | Declined this skill's activation and documented the relevant WAF inventory/policy next step; no SDP/Model Armor setup added |
| Second invocation on the fixed customised project | Re-inspected, reran **53 tests**, and compared SHA-256 snapshots: zero added, removed or changed source files; no duplicate protection or dependencies |

The fixture copies preceded the inspector's additional interpreter-guard test;
their bundled-resource runs therefore recorded 27 passing tests. Skill workflow
instructions and the distributed SDP asset used for those cases did not change.
The final resource suite and standalone copy independently cover all 28 tests.

The SDP preparation agent inspected the installed SDK and corrected an initial
wrong enum-symbol guess before implementation. It reported that failed probe
separately, used the correct nested enum and did not change SDK versions. Its
adapter is fixture output, not an additional bundled production adapter.
The cloud planner is also fixture output; its four tests do not prove live
idempotent provisioning or deletion. Neither is required to install this skill.

## Versions, scope and limitations

Exact creation environment: macOS 26.6.2 arm64, Python 3.11.4, ADK 2.8.0,
DLP 3.38.0, Model Armor 0.7.1, google-genai 2.19.0, Pydantic 2.13.4,
FastAPI 0.136.3, pytest 8.4.2 and PyYAML 6.0.3. The shipped helper/controller
use the standard library; fixture tests also used the existing pytest/SDK
packages. The original chapter's declared pytest range differs from this
environment, as recorded in [compatibility.md](compatibility.md).

All new executable evidence is **fresh offline**. There were no new live
Google Cloud calls, detector-accuracy evaluation, native ADK callback integration
tests, hosted deployment or cross-platform Python runs. Callback/infrastructure
guidance traces to the dated companion evidence, not these fixture tests.
The historical 20-case live campaign remains **historical live**.

Codex forward tests supplied the skill directly; installation and automatic host
discovery were not exercised. Automatic invocation is enabled in metadata.
No other coding-agent host is claimed as smoke-tested. The approval scenario
tests planning behaviour in an offline environment, not host-level enforcement
against a cloud account. Future consequential actions still need the concrete
scope and approval specified in [SKILL.md](../SKILL.md).

Created only the 14 files in this skill folder in the repository. Temporary
fixtures were separate. The manuscript and original companion application were
not modified. The two known companion gaps (truncated inspection and weak public
result constraints) remain separately documented in the evidence map. No commit,
push, publication, installation, deployment or cloud-resource creation occurred.
