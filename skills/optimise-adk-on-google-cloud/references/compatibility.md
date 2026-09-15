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
