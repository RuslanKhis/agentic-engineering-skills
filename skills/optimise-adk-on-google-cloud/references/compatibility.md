# Compatibility and evidence boundaries

Read before using version-sensitive examples or interpreting retained results.
Record the target interpreter, resolved dependencies, exact model and API
consumption path. Inspect configuration at the actual call site: an environment
variable does not override a model selected directly in source.

## Recorded environments

| Context | Recorded versions | Meaning |
| --- | --- | --- |
| Historical Part 1 application evidence | ADK 2.8.0; Google GenAI 2.23.0; Pydantic 2.13.5; pytest 9.1.1 | Resolved application environment behind the retained September 2026 checks |
| Historical Part 2 runtime evidence | Python 3.11; ADK 2.8.0; AI Platform SDK 1.153.1; Google GenAI 2.19.0; retained local freezes: Pydantic 2.13.5, pytest 9.1.1 | Routing/session/owned-lifecycle campaign; the supported Python range is not a multi-version test matrix |
| Skill authoring environment | Python 3.11.4; ADK 2.8.0; Google GenAI 2.19.0; Pydantic 2.13.4; pytest 8.4.2 | Local environment available during skill creation; no new live campaign is implied |
| Additional retained environment | Python 3.11.4; ADK 2.8.0; Google GenAI 2.23.0; Pydantic 2.13.5; pytest 9.1.1 | One offline real-SDK event serialisation test passed during skill creation; this was not a complete second-environment test run |
| Part 2 retained runtime environment | Python 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; Google GenAI 2.19.0; Pydantic 2.13.5; pytest 9.1.1 | Both new offline compaction/App contract tests passed; no provider or managed-session call |
| Historical Part 3 GKE evidence | Local CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.23.0; Pydantic 2.13.5; pytest 9.1.1; Cloud SDK 572.0.0 | Retained 89-test source and final private two-Pod live lifecycle; container base tag was Python 3.12.11 slim Bookworm, not a reproduced container package freeze |
| Part 3 observation component | Authoring OpenTelemetry API/SDK 1.41.1; retained GKE environment API/SDK 1.42.1 | Eight offline in-memory-export tests passed in each environment; no external exporter or Cloud Trace calls |
| Part 1 depth review, 16 September 2026 | Authoring CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.19.0; Pydantic 2.13.4 | 82 package tests passed, including 13 strict-preview tests and two real-ADK nested-generation admission tests; no provider calls |
| Part 1 depth review, retained runtime | CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.19.0; Pydantic 2.13.5; pytest 9.1.1 | All 15 new preview/nested-budget tests passed; this is not a second full-suite or provider test |
| Part 2 depth review, 16 September 2026 | Authoring CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.19.0; Pydantic 2.13.4 | 121 package tests passed, including 36 finite-stream and three token-compaction tests; no provider calls |
| Part 2 depth review, retained runtime | CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.19.0; Pydantic 2.13.5; pytest 9.1.1 | All 39 new stream/token-compaction tests passed; not a second complete suite or hosted test |
| Part 3 depth review, 16 September 2026 | CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.19.0; FastAPI 0.136.3; SQLAlchemy 2.0.51; OpenTelemetry 1.41.1 | 135 package tests passed, including 11 new GKE HTTP/session contracts and three additional saved-run regressions; no provider calls |
| Part 3 depth review, retained GKE environment | CPython 3.11.4; ADK 2.8.0; AI Platform SDK 1.153.1; GenAI 2.23.0; FastAPI 0.141.1; SQLAlchemy 2.0.52; OpenTelemetry 1.42.1 | 41 HTTP/session/checker tests passed; includes all 14 new tests and 27 pre-existing checker tests, not a second full suite or hosted check |

The historical application declares Python `>=3.11,<3.14`; this is not an exact
interpreter reproduction or this portable skill's dependency lock. Preserve a
target project's compatible dependency set. Inspect installed signatures and
exercise changed boundaries offline before adopting examples. Recheck model
availability, endpoint support and service limits for any new live experiment.

ADK Skills are experimental in the 2.8.0 baseline; the
[official Skills documentation](https://adk.dev/skills/) also marks the feature
experimental. Pin and test discovery, loading and any enabled script execution
when upgrading. Resolve SDK option questions against the installed package and
the [Google GenAI API reference](https://googleapis.github.io/python-genai/).
Documentation for a newer release does not prove compatibility with either
recorded environment.

Use `--mode agent-runtime` for the inspector's three-package runtime gate.
`auto`, `application` and `cloud-run` keep the ADK-only baseline. For runtime,
AI Platform SDK 1.153.1's `adk` extra conflicts with ADK 2.8.0: installed
distribution metadata requires ADK `>=1.0.0,<2.0.0` for that extra. The recorded
combination selects `agent_engines` and pins ADK separately. A different version
or extra needs its own dependency resolution check; never silently rewrite it.
The inspector only reports allowlisted known extras and cannot certify arbitrary
optional dependency combinations.

Use `--mode gke` for ADK 2.8.0 and AI Platform SDK 1.153.1 declaration checks.
GKE's requirements leave GenAI transitive; this mode does not impose Runtime's
2.19.0 pin on the recorded 2.23.0 GKE resolution. The known `[adk]` extra conflict
also fails the GKE gate. Kubernetes filename hints are presence candidates only;
the inspector does not parse manifests or identify the authoritative generator.
The optional session-observation asset needs OpenTelemetry API; its tests also
need the SDK. Preserve the target's compatible packages and test export locally.

The optional formatting asset uses Pydantic 2 and Python 3.11 syntax. Its limits
are an adaptable manuscript-derived contract, not ADK defaults. Use its safe
parser/encoder boundary for untrusted previews; direct validation diagnostics can
contain input. Strict Pydantic scalar declarations alone did not prevent a
Decimal-to-float conversion in the recorded environment, so the asset explicitly
checks plain JSON cell types before validation.

The optional finite-stream asset needs only Python 3.11 standard-library APIs.
Its ADK event interoperability test requires exactly the recorded ADK 2.8.0
baseline and skips on another version. Its single-invocation STOP policy, exact
identity requirements and byte budgets must match the target's decoded adapter;
it is neither a general wire decoder nor a tool-result semantic validator.
The token-compaction tests also require ADK 2.8.0 and use synthetic usage with
deterministic models. No hosted compaction or real summarisation quality is implied.

The new GKE HTTP tests require the recorded ADK 2.8.0 factory/loader contract and
its FastAPI/TestClient dependencies; missing ADK or a different version skips
that baseline. SQLite session tests require `sqlalchemy`, `aiosqlite` and
`greenlet`. ADK's optional `db` extra provides SQLAlchemy, but did not install
greenlet in the macOS arm64 laptop recheck. Use SQLAlchemy's `asyncio` extra at
the target's compatible version when preparing that test environment; preserve
existing pins. The managed-session tests
also require `google-cloud-aiplatform`, and the native span test requires the
OpenTelemetry SDK. Missing optional test dependencies produce explicit skips.
Both recorded environments used Starlette 1.6.0,
HTTPX 0.28.1 and aiosqlite 0.22.1. TestClient emitted an HTTPX deprecation warning;
no dependency was changed to silence it. These in-process tests establish SDK
semantics, not PostgreSQL compatibility, streaming delivery or native skill discovery.

## Describe coverage precisely

- **Part 1 historical live:** separate Skills loading, request-level formatter history
  exclusion and explicit cache reuse. Two later cache-test turns each reported
  5,414 cached input tokens. A later application campaign verified real query,
  currency and CSV results and cleanup.
- **Offline:** scripted models and substituted provider clients checked routing,
  output truncation, server call limits and retry controls. Synthetic token
  metadata demonstrates the check's behaviour, not provider usage.
- **Part 1 narrow hosted coverage:** the schema smoke used stored schema, two logical
  calls, one SDK attempt and a 512-token output ceiling; explicit caching was
  disabled. Those limits are verification inputs, not production defaults.
- **Not established:** general cache-hit rates, script sandboxing, automatic
  formatter integration, hosted full-tool/cache behaviour, clean-project
  onboarding or a performance improvement.

- **Part 2 historical live:** routing-only profile, expected billing/technical
  tool results and complete answers, two-turn remote session continuity,
  selected negative authentication/session reads, repeat setup, and cleanup
  after accepted-delete operation recovery. Four submissions yielded seven
  observed logical generations; one agent did not imply one generation.
- **Part 2 offline:** simulated memory, retry, workflow, buffer and job examples.
  This skill additionally exercises real ADK App/compaction orchestration using
  deterministic model boundaries. That establishes context selection, not
  summarisation quality or hosted compaction.
- **Part 2 not established:** full metrics/compaction profile, the real local
  runner with managed sessions, Memory Bank ingestion, browser/token delivery,
  durable jobs, cross-IAM-principal isolation, fresh-project activation and
  measured hosting/model capacity improvements.

- **Part 3 historical live:** final same-region provisioning succeeded after
  earlier capacity failures. The private two-Pod lab passed routing, developer-UI
  interaction, stored-event continuity through a different replacement Pod UID,
  repeat setup, exact-session deletion and full owned infrastructure cleanup.
  Five model-bearing submissions produced nine logical generations. Both Ready
  Pods shared one node; this does not establish node/zone resilience.
- **Part 3 offline:** 89 companion tests exercised application HTTP/session/tool
  orchestration with substituted model transport, manifest generation, ownership
  and uncertain-operation recovery. Developer-UI telemetry consent tests had
  telemetry disabled. The portable skill's custom-span tests use real local
  OpenTelemetry export, including negative controls for exception/parent leaks.
- **Part 3 not established:** first-time API activation or fresh-project setup,
  HPA/VPA, public HTTPS/IAP/tenant isolation, PostgreSQL lifecycle/migrations,
  full trace export/privacy, partial delivery through an edge, in-flight drain,
  production rollback/load, advanced capacity/snapshot/sandbox features or speedup.

Attach a new claim only to evidence that exercises its actual boundary. Keep
historical failures and subsequent repair results distinguishable.
