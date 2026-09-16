# Wire the intended Agent Runtime behaviour

Read when a managed-session, compaction, lazy-client or orchestration change works
in isolation but not through the real entrypoint, or when extending a small hosted
profile. Start with [agent-runtime.md](agent-runtime.md) for the design choice;
use [runtime-verification.md](runtime-verification.md) for executable acceptance
and [runtime-deployment-troubleshooting.md](runtime-deployment-troubleshooting.md)
when packaging or effective deployment configuration is involved.

## Distinguish the execution paths before repairing one

Record this matrix from the target's actual loaders and constructors. Use synthetic
non-secret identifiers in tests, and inspect code for external effects before
importing it.

| Path | Code execution | Session storage | Evidence required |
| --- | --- | --- | --- |
| Client calling a deployed runtime | Remote packaged agent | Backend selected by deployed wrapper | Accepted source/revision, actual remote session ID, complete tool/answer and stored events |
| Local Runner with managed sessions | Local process and its model/tool clients | Remote session service | Actual App reaches Runner; managed adapter receives the intended project/region/engine and authorised owner |
| Real Runner with in-memory sessions | Local ADK; model may still be remote | Local process | Replace every model/summariser/provider boundary to call the run offline |
| Mock runner and mock session service | Simulation | Simulation | Only the behaviour of those mocks; imports of real SDK types do not broaden the claim |

In the historical support agent, the remote terminal client reused one deployed
session successfully. The separate local managed-session runner passed a bare
agent and lost App compaction. The default compaction demonstration replaced a
Python list with a fixed summary. Its opt-in real Runner was model-bearing but
still used local session storage. Keep those results separate when diagnosing a
target with similarly named entrypoints.

For each path, identify the configuration load order, real/mock selectors, model
constructor, summariser, registered tools, exported App and Runner/server loader.
The historical module could switch to real mode when its mock import disappeared
from a deployment package. Its local branch also left a real model-name string,
so substituting the session service or database alone did not make a real Runner
offline. Select intended modes explicitly; test both the checkout and staged tree
in a fresh process with provider transports guarded.

Use the target's existing configuration precedence. Set the selected profile and
backend before importing objects that capture them. A CLI flag evaluated before
dotenv loading cannot be selected by a value read only afterwards. An environment
model setting cannot replace a literal model constructor. Do not change unrelated
customisations merely to match the companion's variable names.

## Preserve App, identity and lifecycle at the same seam

Pass the configured App into the supported Runner constructor and verify that the
remote loader also resolves that App. Do not rebuild a second App with copied
defaults or set an unrelated `app_name` to the engine ID without inspecting the
session adapter's contract. App name, full runtime resource, engine ID, user ID,
session ID and invocation ID have different roles. Keep a mapping where required;
none of these strings authenticates a caller.

A complete integration check follows one authorised conversation through:

1. Configuration and App construction, including tools, model, cache/compaction
   and summariser settings actually selected by the profile.
2. Session creation using the intended backend and an explicit supported retention
   choice. Record pending intent before a remote create and retain its returned ID.
3. Two turns using that same App, trusted owner and returned session ID. Use a
   unique fact from the first turn that the second cannot infer from its own text.
4. Inspection of stored events after the client exits. A plausible answer alone
   does not prove persistence. Keep remote and local storage results separate.
5. Exact owned-session deletion and authorised absence verification, plus closure
   of owned Runner/client resources. Preserve the primary failure and independently
   report cleanup failures; reconcile uncertain creation before creating again.

Use separate create/query/delete/close deadlines inside the intended operation
budget, leaving cleanup capacity after a failed turn. A timeout limits a
cooperative local wait, not previously accepted remote work. A response callback
does not signal session closure or substitute for retention. Negative wrong-user
tests under one credential establish only that API boundary; a tenant-isolation
claim needs distinct authenticated principals and the actual application gateway.

## Add compaction with evidence from the outgoing request

First limit new messages and tool results. Then select App compaction settings for
the actual workload. Current [ADK compaction documentation](https://adk.dev/context/compaction/)
describes token and sliding-window strategies; resolve exact behaviour against
the pinned SDK rather than reading a threshold as an admission limit.

For the ADK 2.8.0 boundary, capture three separate things: input sent to the
summariser, compaction metadata appended to storage, and context sent to the next
model call. Assert required synthetic facts in the summary and next request, old
raw markers absent where intended, and original events still available in storage.
The model-quality experiment is separate from deterministic SDK orchestration.

Use a deliberately small test trigger rather than waiting through a long normal
conversation. Test token-based and sliding-window paths separately; a passing
interval test does not exercise a token threshold. Prior observed token usage can
trigger summarisation before a later request, but a large new input can still
reach the model. Input admission belongs before that boundary.

Retention counts events, not turns, and the SDK may retain more raw events than
the requested tail to keep a function call and its response together. Construct a
test that puts the proposed split inside a tool pair and inspect the next actual
request. Never manually truncate history to an exact event count at the expense
of the tool protocol. Count summariser generations and failures in the same
conversation work budget, below all model callers where possible.

When moving from a routing-only profile to compaction, verify that the profile
does not still disable it, the summariser receives the intended model/configuration,
and the deployed package preserves the App. A locally observed compaction event
cannot establish hosted configuration, summary quality or physical data deletion.

## Make rare-path clients lazy without hiding additional work

Inspect import time, client construction, first operation and later reuse as
separate stages. A lazy factory does not prove that another SDK import has not
already loaded a heavy package. A process cache is neither a cross-worker singleton
nor durable state, and it can retain an earlier project's configuration.

Python's `functools.cache` keeps its mapping coherent across threads but can invoke
the factory more than once during concurrent first access. If exactly one initial
client matters, use the target's supported initialisation/coordination and closure
policy; do not hold a thread lock across an awaited operation. See the
[Python cache contract](https://docs.python.org/3.11/library/functools.html#functools.cache).

In fresh-process tests, inject a factory recording construction and use a barrier
for concurrent first use. Check import/module state, tool reachability, cache reuse
and cleanup separately. The companion's sequential fake-factory pass established
same-process reuse only. Inspect model calls inside tools too: a model-selected
tool that invokes another model adds work even if its SDK client is cached.

For an infrequent BigQuery metrics tool, inspect required dataset/schema, date
range validation, authorised identity, job bytes/time, result bounds and blocking
retrieval. The historical routing deployment created no metrics dataset or access
grant and excluded that tool. Its pass therefore cannot be reused as a metrics
integration result. Use [application.md](application.md) for those query boundaries.

## Extend a verified profile one capability at a time

| Addition | Local evidence before an approved live check | Claim still requiring a real boundary |
| --- | --- | --- |
| Metrics tool | Actual tool registration, synthetic authorised/denied/date-bound cases, bounded query and result adapters | Dataset/schema, workload IAM and complete selected tool output |
| Compaction | Actual App, token and interval triggers, summariser input, next request and retained stored events | Hosted profile propagation and real summary quality |
| Grouped context lookup | Controlled overlap, required versus optional failure, overall deadline including slot wait, cancellation and shared capacity | Actual dependency response bounds, access and sustained aggregate load |
| Known Workflow | Trusted state inputs, `node_input` handoff, deterministic policy result and actual explanation stage | Real model explanation preserves the checked decision; no extra consequential tool is selected |
| Retry wrapper | In-flight timeout, cancellation, typed SDK errors, exact attempt counts and lost-response reconciliation | Provider retryability and capacity under the intended model/backend |

Keep one owner of retries and distinguish a logical generation from SDK attempts.
Do not wrap a whole agent turn if it can repeat a submitted ticket, export or job.
The historical synchronous mock retry loop did not verify an async GenAI retry
policy, and one language-agent node does not impose one generation. Keep the
existing profile's verdict and record each extension's independent acceptance.
