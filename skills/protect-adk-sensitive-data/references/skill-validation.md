# Skill creation validation — 15 September 2026

This creation record is preserved as dated evidence. The later
[depth recheck](#depth-recheck--16-september-2026) records new resources, gaps
found and fresh checks; the original counts below are not current suite totals.

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

## Depth recheck — 16 September 2026

Reopened the committed skill and Chapter 8 implementation, setup/cleanup scripts,
public audits, manuscript comparison and updated manuscript at repository HEAD
`51b41e83cdf6adc8904d7039b283c292989203fc`. Three independent source reviews
covered runtime behaviour, operational experience and manuscript production
advice. Their recommendations were checked against the source and incorporated
into this one skill. No private credential/audit contents were needed.

The review found useful missing implementation detail, not evidence that every
possible production scenario is covered. Keep the concise entry point and load
the following depth only for the relevant task:

| Rechecked experience | Where it now changes the agent's work | Evidence boundary |
| --- | --- | --- |
| Regional SDP, separate deny/PII decisions, complete response checks, queue/RPC bounds | `sdp.md`, optional `google_sdp_adapter.py`, typed SDK tests | Historical provider path plus new offline adapter; live acceptance of this adaptation still required |
| Callback mutation before persistence, `None` success, multiple tools, safe release events and client reuse | `implementation-recipes.md`, `boundaries.md` | Historical runner tests and freshly inspected ADK source; skeletons require target helpers and regression tests |
| Native Armor's missing call limits, supplied-client closure and exception logs; telemetry overrides | `implementation-recipes.md`, `model-armor.md` | Fresh source observations on ADK 2.8.0; historical gateway did not implement all added hardening |
| Project/ADC/quota separation, regional references, resource dependency order and runtime identity | `cloud-lifecycle.md` | Historical setup and runtime probes; no claim of current project access |
| TLS trust, interpreter selection, typed enums, token shape, IAM pagination, 429 classification and delete return values | `troubleshooting.md` | Dated failure/repair records and local SDK contract checks; no inference that payment caused recovery |
| Actual transport budgets, SDK/core retries, private diagnostics, partial cleanup and retained storage | `troubleshooting.md`, `cloud-lifecycle.md` | Historical bounded-campaign and cross-chapter cleanup lessons, with wire-count/access limitations preserved |
| Hosted entry points, bypass routes, readiness, multiple replicas and effective residency | `cloud-lifecycle.md` | Production guidance; the historical live gateway was local |
| Trusted tenant-to-runtime policy, restricted failure modes, shadow rollout and detector evaluation | `production-policy.md` | Manuscript advice translated into implementable decisions and acceptance criteria; not companion features |
| Derived-data retention/deletion, token recovery, retry capacity and incident rollback | `production-policy.md` | Production guidance; incident procedure explicitly labelled a derived recommendation |

### Defect found in the earlier forward-test output

The September 15 generated greenfield adapter accepted endpoints matching
`(?:[a-z][a-z0-9-]*-)?dlp\.googleapis\.com`. Its 59 mocked tests passed, yet
that expression excluded the documented and historically used regional endpoint
`dlp.us-central1.rep.googleapis.com`. The recheck reproduced the configuration
rejection offline, before client construction. This was a **generated fixture
defect**, not a newly discovered companion application defect or live failure.

The skill now ships a regional adapter that derives the endpoint from trusted
location, validates all full template names, avoids inline policy overrides,
and has real SDK-shaped offline regressions. This is why runnable provider
details were added instead of relying only on general instructions. Official
SDP processing-location and API references were checked for those contracts.

### Fresh package and standalone checks

Used the same existing Python 3.11.4 environment and exact package versions
recorded in [compatibility.md](compatibility.md); no dependency changes.

| Command/check | Actual result |
| --- | --- |
| `python -B -m unittest discover -s skills/protect-adk-sensitive-data/tests -v` | **44 passed**: 14 inspector, 14 controller, 3 adapter configuration and 13 SDK-dependent adapter tests; zero skips |
| Skill-creator `quick_validate.py skills/protect-adk-sensitive-data` | `Skill is valid!` |
| Inspector `--help`, chapter `--dry-run`, chapter normal inspection | All exit 0; dry-run `files_read=[]`; normal inspection reports declarations and manual-review warning, not compatibility |
| `python -B -m tabnanny skills/protect-adk-sensitive-data` | Exit 0 |
| YAML, Python syntax and shell syntax | Frontmatter/UI valid; automatic invocation retained; all 6 Python files and 5 Python examples parse; both shell examples pass `bash -n` |
| Complete copy without companion source; `python -I -B` with socket connect/connect_ex/create_connection blocked | **44 passed**; installed SDK supplies message types, provider constructors/transports are doubled |
| Same copy with `python -I -S -B`, excluding site packages | **31 passed, 13 skipped** with explicit missing-SDK reason; this verifies standard-library operation only |

The adapter cases cover regional routing/full names, typed requests without
inline overrides, deny/incomplete/malformed responses, transformation summaries,
UTF-8 size bounds, host/queue/RPC budget, cancellation, safe errors, reuse and
close failures. They do not establish live response shape or detector accuracy.
No new formatter/linter dependency was introduced; syntax, indentation and
whitespace checks are the checks actually performed.

### Fresh independent forward tests

Three fresh agents received separate temporary copies of the expanded skill,
minimal raw fixtures and realistic requests. They received no book, companion
application, conversation history or expected-answer rubric. They could inspect
the installed SDK; cloud/network calls and dependency changes were excluded.
The main agent reviewed their code, tests, plans and reports after execution.

| Request | Observed result |
| --- | --- |
| Prepare a regional SDP integration from approved template names, without credentials; preserve the existing input function and pins | Copied both assets with licence; added trusted config loading and lifecycle instructions. **15 project tests passed**, plus **44 bundled tests** under guards blocking ADC, real client construction, sockets/DNS and gRPC channels. Existing input function/config/pins unchanged; live activation prerequisites explicit |
| Bound the native Armor plugin's supplied client with an existing ingress deadline/semaphore; prevent sensitive SDK failure logs | Generated an async facade and lifecycle integration. **15 tests passed**, including five actual ADK Runner cases with a scripted model and real ModelArmorAsyncClient over a channel-free transport double. Covered prompt/output failures, canary absence from events/logs, shared deadlines/concurrency, cancellation, retry kwargs and closure; pins preserved |
| Diagnose a replacement-project cutover with API/TLS/429 failures, different tenant policies, weak attempt accounting and incomplete cleanup | Produced an actionable prioritised plan. Kept CLI and runtime evidence separate, required trusted tenant-to-complete-runtime selection, rejected paid health probes and unproved budget/cleanup claims, and did not infer a Vertex fix from AI Studio payment. No cloud contact or fabricated target values |

Both regional and operations agents identified stale “standard library only”
wording in their copies. The final `validation.md` and `compatibility.md` now
scope that claim to the inspector/controller and explicitly describe optional
SDK tests and skipped coverage. A further pointer distinguishes GAPIC
`retry=None` from transport-level retries: the native trial proves argument
forwarding and no application retry, not a universal wire-attempt or billing cap.
An additional independent review of the adapter/controller/tests/SDP reference
found no actionable defects; its separate adapter run passed all **16 tests**.

The six September 15 scenarios remain dated evidence, not six reruns. The three
new trials address the added depth. Native trial code is disposable fixture
output, not another bundled asset. The supplied callback examples are adaptation
skeletons, and the production-policy/deployment recipes remain guidance.

### Final package and limits

The skill has **19 files**, with **5 added and 8 existing files modified** in this
recheck. The entry point remains 121 lines and routes conditionally to details.
Unchanged files remain part of the standalone distribution:

```text
protect-adk-sensitive-data/
├── LICENSE
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── google_sdp_adapter.py
│   └── sdp_boundary.py
├── scripts/inspect_project.py
├── references/
│   ├── boundaries.md
│   ├── cloud-lifecycle.md
│   ├── compatibility.md
│   ├── implementation-recipes.md
│   ├── model-armor.md
│   ├── production-policy.md
│   ├── sdp.md
│   ├── skill-validation.md
│   ├── troubleshooting.md
│   └── validation.md
└── tests/
    ├── test_google_sdp_adapter.py
    ├── test_inspect_project.py
    └── test_sdp_boundary.py
```

New files are the regional adapter and its tests, implementation recipes,
production policy and troubleshooting. Modified files are the entry point and
the seven existing references. Local links/anchors resolve within the package;
whitespace and unfinished-marker checks pass, with no copied personal resource
identifiers or machine-local paths. MIT notices are retained.

This recheck made **no cloud API calls or mutations**, created no cloud
resources, and performed no new paid campaign or cleanup. Public documentation
was read; that is not cloud access evidence. Historical live results remain
historical. The new adapter needs separately approved benign/PII live acceptance,
and hosted deployment, real identity, detector accuracy, effective residency and
exporter privacy need target-specific evidence. Existing approval requirements
still apply to consequential operations.

No manuscript or companion application was modified. The known original
empty/truncated-inspection and public-result-constraint gaps remain separately
recorded in E3; advice here does not retroactively fix them. No commit, push,
publication, installation or dependency change occurred. The skill was supplied
directly to Codex agents; automatic discovery and other coding-agent hosts were
not newly smoke-tested. Other concurrent repository changes are outside this
skill's recheck.
