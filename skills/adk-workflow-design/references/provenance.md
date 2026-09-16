# Provenance and evidence boundaries

This skill derives from Chapter 0 of *Agentic Engineering*, its companion code,
independent execution work and the revised manuscript. The source is the author's
[MIT-licensed companion repository](https://github.com/RuslanKhis/agentic-engineering-adk-gcp).
No published book URL was available when this skill was created. No book, source
checkout, previous conversation or cloud account is needed to use the skill.

The locally inspected source revision was
`c909d7e5d285ae582abb3899bbe162fa55f075dd`. All 13 current application/test/pin
fingerprints matched the September 13 follow-up source manifest when rechecked
on September 15. Source paths below are provenance labels under
`chapter-00-setting-the-stage`, not dependencies or links to installed skill files.

The depth review on **16 September 2026** reopened the revised manuscript,
application/tests, audit controls, historical reports and broader cleanup
recheck at repository revision `51b41e83cdf6adc8904d7039b283c292989203fc`.
It added implementation procedures to the skill rather than changing the
manuscript or companion. New mechanisms inspected in the installed ADK 2.8.0
source are distinguished from newly executed offline recipes below.

| Skill rule | Grounding | Evidence level and limits |
| --- | --- | --- |
| Select ordinary code when rules suffice; avoid unnecessary agents | Revised chapter's modularity/workflow argument; `workflows/dynamic/agent.py` | Production principle plus an entirely offline dynamic example. |
| Ordered real-value handoff; propagate failure without replaying completed work | `workflows/sequential/agent.py`; `tests/test_workflows.py` sequential/failure cases | Real ADK with model-boundary doubles; historical model/UI success for the normal path. |
| Actual concurrent overlap and separate populated state | `workflows/parallel/agent.py`; barrier test | Offline scheduler test plus historical overlapping model requests. No summariser implemented. |
| Match advertised capability to real tools/data | Parallel live failure, repaired `PLANNING_BOUNDARY`, outbound-prompt regression and live retest | Original answer invented dates/research; repair passed one live retest. Prompt adherence is not guaranteed or an auth control. |
| Semantic stop plus deterministic cap; count actual sends | `workflows/loop/agent.py`; approval/exhaustion tests | Real exit tool in offline tests; 3-request approval and 11-request exhaustion paths. Live approval covered; live exhaustion not covered. |
| Assert the actual typed output; identify simulated values | `workflows/graph/agent.py`; typed-handoff test | Offline and historical model/UI data flow. Fixed time is simulated; source's “no cost”/“right now” wording is misleading and not reusable as a factual claim. |
| Preserve scalar/list contract and child orchestration | `workflows/dynamic/agent.py`; documented-input and populated-session cases | Entirely offline. Non-list JSON remains original text. Interrupted-child recovery not tested. |
| Hook before actual request; retain passthrough; sanitised telemetry | `workflows/callbacks/agent.py`; callback-order test | Offline real Runner and historical live callback. No SQL, auth, caching or error-recovery implementation. |
| Event commit, state durability, final-result selection, alias/cache semantics | Revised manuscript, installed ADK 2.8.0 source; `tests/test_http.py` | SDK inspection plus actual local HTTP/SQLite restart and deletion tests. Conceptual currency consumer is not shipped runnable code. |
| Reserve sends; preserve counters/deadline; reconcile uncertain outcomes | `audit_controls.py`; permit, transport, resume and streaming-deadline tests | Offline SDK/transport doubles plus historical bounded campaign. Campaign-specific implementation/constants are deliberately not bundled. |
| Measure meaningful UI content; preserve inconclusive intervals | September 13 follow-up browser evidence | Historical small live sample. Streaming sequential warm n=3 met the agreed threshold; callback interval crossed it. Owner acceptance is not a new timing measurement. |
| Isolate identity/data; use idempotency, deadlines and scoped lifecycle | Revised chapter's labelled production extensions; partial local cleanup tests | Production principles until separately implemented and tested in the target project. No enterprise certification implied. |

Historical audit files: `INDEPENDENT_AUDIT_2026-09-13.md`,
`verification/2026-09-13-followup-source-sha256.json`,
`verification/2026-09-13-followup-offline-tests.txt`,
`verification/2026-09-13-followup-dependencies.txt`,
`verification/2026-09-13-followup-live-state.json`,
`verification/2026-09-13-followup-browser.json` and
`verification/2026-09-13-followup-cleanup.json`.

The completed historical campaign recorded **33 offline tests**, **16 live browser
submissions / 27 model attempts**, and one offline dynamic UI submission. All
five model workflows had functional live evidence through local ADK Web and
Vertex/ADC. The fixed five-second callback latency gate remained inconclusive;
it must not be described as an unconditional end-to-end pass. These counts are
historical evidence, not results from executing this skill.

API-key mode, cloud-hosted application deployment, authenticated tenant isolation,
real travel/time/record APIs, RAG/memory/privacy workers, load/HA/security
certification and interrupted dynamic-child replay were not established by this
chapter. The API activation branch was actually exercised in the historical lab,
but grants no authority or fresh-project guarantee elsewhere.

Bundled script tests are new deterministic tests. Bundled runtime tests adapt the
source's MIT-licensed real-Runner/boundary-double approach and preserve the licence
notice in `LICENSE`. Creation-time results and independent forward tests are in
[validation-results.md](validation-results.md); they do not inherit historical
model-quality or cloud-lifecycle passes.

## Depth-review additions and their authority

| Added guidance | Source and evidence boundary |
| --- | --- |
| Reject a previous final state key after a later failed turn | New real-Runner, same-session two-turn reproduction and bundled regression. Four substituted model calls; no provider call. The earlier fresh-session failure test alone missed this case. |
| Copy–modify–reassign nested state; select session/user/app/temp scope | Installed `google.adk.sessions.state`, `_session_util` and `in_memory_session_service`; new callback fixture asserts the assigned delta and fetched state. Durable database/restart semantics remain a separate target-project check. |
| Exact agent versus plugin callback keywords and chain order | Installed `llm_agent`, `base_agent`, `base_llm_flow` and `flows.llm_flows.functions`. New Runner tests reproduce the empty-dictionary chain hazard and repeated nonempty denial with an allowed control. This is SDK 2.8.0 mechanics, not verified customer authentication. |
| Typed result provenance, empty output and progress separation | Existing graph/dynamic code and HTTP tests; new ordinary-code Workflow fixture returns typed data, progress and `[]`, then writes completion state. The stream is fully consumed; no model call occurs. |
| Supervised dynamic child calls and data-ID versus execution-ID distinction | Installed `agents.context.run_node` documentation/implementation plus existing duplicate-input tests. New interrupted-child recovery was not executed. |
| Strict send limits, durable reservations, full-body deadlines and owned-client shutdown | `audit_controls.py` and its HTTP-transport/lifespan/resume tests; historical approved model campaign. The new reference is a portable design recipe, not a bundled provisioner or a freshly retested cloud launcher. |
| Local process ownership, causal streaming, timing intervals and scoped SQLite cleanup | `tests/test_http.py`, gated ASGI streaming regression, September 13 browser observations and README. The runbook adapts previously tested procedures; no new browser or model sample is implied. |
| Ordered project/backend/ADC diagnosis and honest broad cleanup | README, September 13 preflight failures and September 15 project cleanup recheck. Official authentication, service-list, error and retention documentation checked on September 16. No current account or cloud state was read or mutated for this skill review. |
| Deployment/data-store handoff and deterministic versus probabilistic validation | Revised manuscript's explicitly labelled production extensions. Planning guidance only; Cloud Run, build triggers, authentication, RAG and memory remain separate implementation scopes. |

The broader cleanup report retained provider storage and unresolved inventory
questions. Only its evidence rules were generalised: reconcile direct service
state, distinguish inaccessible from empty, and disclose retention. Personal IDs,
project-wide deletion commands and campaign-specific quotas were not copied.
