# Implementation-depth recheck — 16 September 2026

The entry point remains a single skill with conditional references. This pass
reopened the manuscript, shipped implementation, tests, setup/preflight code and
dated migration, live-verification and cleanup reports. Three independent
read-only audits reviewed manuscript coverage, operational lessons and test
mechanics. The core retry/deadline/idempotency guidance was already well covered;
the useful gaps were concrete procedures, production boundary checks and
reproducible evaluation inputs.

## Added guidance and its support

Source coordinates below identify evidence in the original Chapter 1; they are
not files the installed skill needs to import or possess.

| Addition | Source and evidence classification |
| --- | --- |
| Validate provider success data, use trusted destination/authentication, distinguish mock and HTTPX interfaces | `MANUSCRIPT.md:663–693`. Production adapter requirements; the chapter's adapter is illustrative. The retained adapter fixture now tests the generated behaviour offline. |
| Revalidate the approved action and current authority immediately before dispatch | `MANUSCRIPT.md:713`, `:740–744`. Production principle; ADK consent tests alone do not establish freshness. The retained approval fixture checks changed details and permission with zero provider calls. |
| Safe structured diagnostics and visible unexpected defects | `MANUSCRIPT.md:515`, `:769`. Production improvement over broad exception translation and module-owned logging; synthetic response/exception redaction is exercised by the new adapter evaluation. |
| Owned event uniqueness, payload conflicts, projection ordering and retention | `MANUSCRIPT.md:773–831`. Conditional production workflow; PostgreSQL illustration was not executed by the chapter. No database was added or certified in this pass. |
| Effective dotenv/backend configuration; actual ADC identity, quota and permission; billing FAIL versus BLOCKED | `README.md:119–155`, `:184–188`; `verification/migration-audit-2026-09-13.md:116–125`; `verification/preflight.py`. Historical diagnosis and offline preflight tests. New synthetic incident review applies the distinctions without contacting accounts. |
| Saved activation intent, accepted operation recovery, ownership and independent readiness | `verification/setup.py:153–267`; `verification/budget-retest-audit-2026-09-13.md:161–186`. Historical live activation/completed repeat, with recovery/refusal branches tested offline. No fresh-project model/UI onboarding or new live recovery claim. |
| Local process/port/session ownership and qualified cleanup claims | `README.md:190–226`; `verification/cleanup-check-2026-09-15.md:64–69`, `:103–122`. Historical local lifecycle plus a wider inventory check. Retained storage from other chapter runs is not attributed to the Chapter 1 application. |
| Real ASGI/lifespan, finite model script, confirmation response ID, SSE and history assertions | `tests/test_http_smoke.py:34–81`, `:138–185`, `:203–216`. Tested offline plumbing, not live model reasoning. |
| Actual live-request admission, SDK options, shared allowance and stream usage accounting | `tests/test_live_limits.py:54–79`, `:120–136`, `:160–233`; `verification/live_limits.py:1–7`. Offline enforcement tests plus historical campaign use; no distributed budget or hard spending-cap claim. |
| Observer preflight, stage attribution, meaningful-text boundaries and actual versus scheduled waits | `verification/followup-audit-2026-09-13.md:126–137`, `:150–197`; `verification/budget-retest-audit-2026-09-13.md:101–104`, `:147–153`. Historical debugging lessons, not a new latency experiment. |

Primary documentation for authentication, confirmation limitations, runtime
configuration, service activation, HTTPX timeout phases and storage retention
was checked during the pass. Relevant operational references link those sources;
current documentation does not expand the tested version matrix.

## Retained forward evaluations

[forward-cases.md](forward-cases.md) documents exact fixture inputs, requests,
independent acceptance checks and how to repeat the exercise in a clean copy.
The two code fixtures deliberately start broken and are not production assets.
Evaluators received a copied skill, their own fixture and its request. They did
not receive the acceptance assertions, previous conclusions, other fixtures or
the companion source. All work used synthetic local providers or supplied facts.

| Case | Observed result |
| --- | --- |
| Provider adapter | The independent agent produced a repaired adapter and 10 tests, then its run ended at an agent usage limit before a final handoff. The parent inspected those files and executed all **10 generated tests** successfully. The separately authored **5 acceptance tests** also passed: validated success, malformed read responses, one effect/unknown refund after response loss or invalid data, invalid money with no dispatch, and safe diagnostics. This is verified output from an interrupted agent run, not an uninterrupted independent-agent completion. |
| Stale approval | Independent agent completed the repair and **9 generated tests** passed. Parent ran **4 acceptance tests**, including multiple changed-payload/authority subcases, rejection, matching approval and cancellation. Every stale or unauthorised case sent zero provider requests. |
| Operational incident | Independent agent produced a recovery plan separating effective configuration, CLI and runtime identity, intended quota, blocked billing inspection and generation readiness. It retained the old pending operation, refused mismatched-state reuse, treated already-enabled API state as a baseline, preserved an unrelated listener and qualified local/storage cleanup. No proposed external action was executed. |

The unmodified fixture inputs were tested first as negative controls:
adapter acceptance exited 1 with 13 failed subcases and one error; approval
acceptance exited 1 with eight failed subcases. These are expected failures of
deliberately defective inputs. They establish that the assertions detect the
target defects rather than always passing. Candidate repairs then passed every
acceptance test. Generated implementations remain disposable outputs; exact
inputs and independent assertions are now retained for future agent runs.

Checked output SHA-256 identities:

- Adapter `service.py`: `a1950dcf7fbfc5c0a4a6019987158a1a063f592d68a5bfb563d8a7ff8074a775`.
- Approval `service.py`: `093a955d237f286275fd3f663f57127f99d2723ca379ed4ca5f5cebb1ac1e955`.

## Commands and environment

Used the existing Chapter 1 interpreter: **Python 3.11.4**, **macOS 26.6.2
arm64**, **google-adk 2.8.0**, **httpx 0.28.1**, **tenacity 9.1.4**,
**google-genai 2.22.0**, **PyYAML 6.0.3**. No installation or pin change occurred.
Agent evaluations ran in Codex desktop; other agents and host-level automatic
skill discovery were not tested.

Command paths are parameterised below: `PYTHON` is that existing interpreter,
`SKILL_DIR` the installed skill, and `VALIDATOR` the available official
skill-creator validator. Candidate test commands ran from their temporary
project directories; acceptance commands and path variables are specified in
the linked reproduction instructions.

| Check | Actual result |
| --- | --- |
| `"$PYTHON" -B "$VALIDATOR" "$SKILL_DIR"` | Exit 0, `Skill is valid!`. |
| `"$PYTHON" -B -m unittest discover -s "$SKILL_DIR/tests" -v` | **12 helper tests passed**, no skips, 2.165 seconds; includes CLI help, dry-run, repeat, bounds and redaction. |
| `"$PYTHON" -B -m unittest -v` in adapter output | **10 tests passed**, 0.086 seconds. |
| Same command in approval output | **9 tests passed**, reported by the completing independent evaluator. |
| Acceptance discovery for `test_adapter.py` | **5 tests passed**, 0.010 seconds. |
| Acceptance discovery for `test_approval.py` | **4 tests passed**, 0.009 seconds. |
| `PYTHON_DOTENV_DISABLED=1 PYTHONDONTWRITEBYTECODE=1 "$PYTHON" -B -m unittest discover -s tests -v` in unchanged chapter | **59 tests passed**, no skips, 2.995 seconds. Scripted-model HTTP tests block sockets. ADK experimental-feature warnings remain. |
| Existing ADK executable `web --help` | Exit 0; verified documented host, port and disposable-storage flags without starting a server. |
| `"$PYTHON" -B -m pip check` | No broken requirements; local pip-cache permission warning only. |
| Python syntax, internal links, whitespace, frontmatter, unfinished markers and clean copy | Passed. Existing chapter source manifest still matches all 14 files; manuscript hash unchanged. |

No formatter/linter/type checker is configured for this chapter; no pass from
one is claimed. The normal helper suite intentionally excludes acceptance tests
requiring a generated candidate; run those explicitly as documented. No live
model request, real payment, API activation, deployment, IAM/secret mutation or
cloud cleanup ran. Production storage/concurrency, real provider semantics,
live confirmation wording and managed deployment still require their own
implementation and authorised validation.
