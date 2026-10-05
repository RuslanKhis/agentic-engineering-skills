# From requirements to system contracts

Use the questions relevant to the application's journey. A small read-only
assistant may need a short design; a system that changes money or publishes data
needs explicit operation and disclosure contracts. These are decision prompts,
not a requirement to build every capability.

## Explain a choice in conversation

For example, after the user confirms that an editable plan must survive a chat
disconnect:

> Because the plan must survive a disconnected conversation, I would store it as
> a versioned application record and have chat refer to it by ID. That gives the
> editor and later sessions the same authoritative saved plan. It adds revision
> and access-control handling compared with keeping the draft only in chat. I
> would verify that saving a revision, restarting the service and reopening it
> returns that revision to its owner and denies access to another user.

The requirement supports the choice; the reason explains the mechanism, the
tradeoff exposes its cost, and verification names observable behavior. If shared
editing later becomes a requirement, revisit writer permissions and concurrent
updates instead of presenting this initial choice as a complete collaboration
design. Keep checks proposed until executed.

## Size the first slice to the judge

Before any component is chosen, write down the three scope-gate answers: the
time and money available, who evaluates the result and what they will read,
and the artifact type (exploration, assignment, pilot, production). These
answers decide how much of this reference applies. A four-hour assignment
judged on five holdout predictions and a report needs the core judgment
working on real inputs and one quality measurement; it does not need officer
revisions, export acknowledgement, durable approval records or a hosting
roadmap. A production service that changes money needs most of this file.

**Proportionality rule.** When the artifact is judged on output quality, the
first implementation slice is the core judgment end to end on real inputs,
with a measured quality result and only the controls that keep spend safe
(a call budget and a stop). Identity, revisions, export acknowledgement,
recovery, checkpoint freezes and campaign tooling wait until that
measurement exists. Each deferred control gets one line in the design's
"Scope, evaluator and deferred controls" block: what it is, why it waits,
and what would bring it forward.

For example, with "3 to 4 hours, judged on holdout predictions, method and
report, an assignment":

> First slice: ingest the supplied documents, retrieve the operative policy
> for each case, draft a decision with reasons and conditions, score the
> five labelled development cases against their reasons, and regenerate the
> holdout predictions with the final method. Spend control: one model-call
> budget per case and a total stop. Deferred: officer revision workflow,
> export acknowledgement, saved-stage recovery, cloud hosting; each would
> start only after the development-case score is measured.

When `adk-agent-evaluation` is installed, its quality-iteration reference
gives the measurement loop for that first slice; the proportionality rule
stands on its own without it.

## Outcome and orchestration

Define the useful result and its authoritative source before choosing agents.
Separate language interpretation or synthesis from deterministic calculations,
policy checks and writes. A plausible response is not evidence of a completed
business operation.

Separate technical correctness from product usefulness. Ask which part of the
current journey should improve and what baseline exists. Where the design claims
a user or business benefit, propose a measurement and relevant guardrail: for
example, more completed tasks without increased correction or support effort.
Model quality, valid transactions and improved user outcomes need distinct evidence.
Treat an unmeasured benefit as a hypothesis; choose the first useful end-to-end
slice around it and revisit complexity if simpler interactions work as well.

| Choice | A reason to use it | Contract to record |
| --- | --- | --- |
| Ordinary application code | Inputs and rules already determine the action | Validation, output and error behavior |
| One agent with bounded tools | Language interpretation needs access to a small set of capabilities | Allowed tools, trusted scope, termination and public result |
| Sequential workflow | A step depends on the preceding result | Typed handoff and freshness for the current invocation |
| Parallel branches | Independent work can overlap | Separate outputs, join/merge policy, partial-failure policy and aggregate demand |
| Bounded refinement | Revision benefits from review | Final artifact owner, model-judged acceptance and deterministic stopping bound |
| Graph or dynamic work | Dependencies or runtime-sized work justify it | Edge contracts, fan-out cap, completion and cancellation ownership |

Dynamic work can run sequentially. A reviewer is a probabilistic decision-maker;
its approval is different from a backend permission check. For proposed multiple
agents, name what each one uniquely owns and how its authority is restricted.

## State, knowledge and freshness

For each necessary data class, record owner/scope, authoritative source, writers,
readers, lifetime, persistence, version/freshness check and erasure path.

- **Conversation history and working state:** what must survive another turn,
  another replica or a process restart? Tag invocation-specific results so a failed
  new review cannot release yesterday's approved answer. Parallel writers need
  separate keys or an explicit merge/concurrency policy.
- **Exact user preferences:** place user-controlled settings in a deterministic
  profile when exact lookup/update behavior matters. Scope them using verified
  identity and make change/forget operations explicit.
- **Semantic memory:** select eligible facts, purpose, consent, correction,
  expiry and provenance. Submission, completed processing and actual retrievability
  are different states. Coordinate deletion with pending work and old retries.
- **RAG:** name who approves source versions and publishes a release; filter by
  caller entitlement before model exposure. Record freshness, citations and the
  behavior when evidence is missing, revoked or inconsistent. Separate ingestion
  from serving: stage and evaluate a candidate before promotion, retain passage
  and release identities, and define cutover behavior for caches/in-flight reads.
  An empty authorised search must not broaden its scope. Evaluate retrieval
  quality separately from whether the cited evidence supports the answer.
- **Artifacts:** distinguish uploaded/generated files from session metadata;
  specify access, versioning, retention and removal of both content and pointers.
- **Authoritative business records and analytical history:** memory cannot grant
  entitlement or establish current balance. Preserve source timestamps and state
  the freshness/completeness contract for derived history. A recently updated row
  does not establish ingestion completeness. Distinguish no matches, unavailable
  queries and incomplete history; use the operational authority for current truth.

## Identity, tools and data release

Trace three identities separately: authenticated user/tenant, calling workload,
and any delegated OAuth subject. Show where trusted code verifies each, derives
scope, and reauthorizes access. A conversation ID locates a resource; knowledge
of it is not permission. A service account's permissions do not establish the
end user's business authority.

Define each tool's permitted actions, validated arguments, credentials, public
result schema and side-effect boundary. Bind confirmations to material details
and recheck authority and business prerequisites immediately before execution.
Keep credential selection outside model arguments. For delegated OAuth, design
consent, refresh, revocation/disconnect, concurrent refresh and restart behavior.

Separate credential payload storage from trusted owner/account/client/scope and
connection-version metadata. Specify how disconnect denies new use across replicas,
invalidates stale refresh results and cached credentials, and accounts for calls
already dispatched. State the accepted revocation delay and unresolved provider
revocation. A temporary infrastructure failure must preserve valid durable consent
without enabling stronger fallback credentials.

When approval outlives a request, define durable reviewer authority, decision
state and expiry separately from execution. Bind review to the stored proposal
and recover notification delivery from durable intent; duplicate notifications
must not repeat effects. An approval permits execution but does not prove it
happened. Render consequential status from authoritative receipts, preserving
earlier successful effects when a later step fails.

Map sensitive data across ingress, model context, tool arguments/results, session
events, memories, artifacts, diagnostics and each telemetry exporter. Minimize
fields first. Specify allow/transform/block/indeterminate behavior at each required
boundary; an unavailable protection service needs an explicit outcome.

Resolve policy from verified identity and trusted configuration across the complete
runtime. Inspection services are recipients of the data they inspect and need to
fit that policy. New protection does not sanitise old sessions, summaries, caches
or evaluation data. Before reuse, choose compatible access, migration, deletion
or refusal; a policy-version marker alone does not transform stored contents.

Choose public-output release semantics. Raw event forwarding can expose private
arguments or diagnostics. Full-response screening adds buffering/latency; partial
streaming cannot retract already disclosed text. State which guarantee the design
offers and how its browser contract communicates partial and failed results.

## External effects and recovery

Separate a conversation, an invocation/processing attempt and a logical business
operation. A retry, duplicate click and restarted worker may refer to the same
business operation. Its identity must survive the failure window being claimed.

For writes, document the authoritative preconditions, durable operation identity,
canonical payload, approval binding and provider replay contract. Verify key scope,
retention and lookup semantics before promising deduplication. Atomically claim or
load the same operation, reject changed payloads, and retain uncertain outcomes.
An expired worker lease does not establish that an earlier request stopped.

Classify failures by effect and observed outcome. Invalid input or denied authority
needs correction; a transient failure permits a bounded retry only when repetition
is safe; an uncertain write needs recovery of the existing operation. Assign one
owner for the combined policy across application and SDK retries.

Trace provider success followed by lost response or failure to record the receipt.
Name the recovery owner and its evidence: supported status lookup, safe replay of
the same operation, or manual reconciliation. A later rejected attempt cannot prove
an earlier attempt had no effect. Local database transactions do not make remote
effects atomic; two different operations may also need a shared balance constraint.

For event-driven updates, include unique event identity, changed-payload rejection,
out-of-order delivery, concurrent consumers and ledger retention. Model instructions
and ordinary session persistence do not supply durable execution guarantees.

For deferred work, durably record acceptance and dispatch intent before acknowledging
the job. Specify owner-qualified status/result access and recovery. Keep the business
job identity distinct from a paused tool-call continuation so resumption reaches the
right call under the chosen contract. An in-process background task is not a
durable queue.

## Latency, capacity, budgets and operations

Ask for useful targets or document provisional ranges with a measurement plan.
Track time to first meaningful content and time to a complete correct result,
including queue/admission time and streamed response consumption. Retain failures
and distinguish cold/warm observations.

Inventory model, simulator, judge, retrieval, screening and tool calls per user
request. Include internal SDK retries and parallel branches. Estimate expected and
bounded work separately; never substitute a loop count for total model requests.
At a stable arrival rate, concurrency is roughly arrival rate times time in flight;
use burst/load measurements to validate headroom and downstream saturation.

For each allowance, state unit, scope, enforcement point and persistence: attempts,
tokens, elapsed time, concurrent work, query bytes or estimated money. Define what
stops, degrades or remains recoverable when it is exhausted. When an allowance must
survive restart, retain usage and the original deadline. A billing notification is
an observation mechanism; determine how the application enforces admission itself.

For a shared allowance, specify atomic admission/reservation and later settlement
across workers. Accounting after work finishes can oversubscribe a budget; unknown
usage may require retaining a reservation until reconciliation. State queue limits,
fairness and backpressure where overload is possible. Separate readiness, shutdown
and recovery responsibilities for workers handling ongoing requests or jobs.

Choose admission behavior when the control store is unavailable. Keep an operator
stop independent of automatic budget resets and outside agent authority. Reserve
allowance for reconciliation and owned cleanup; state which essential operations
remain available after new expensive work stops.

Name operators for failures, uncertain effects, rollback and deletion. Plan how
configuration/policy versions and deployment identity will be verified in the
running process. Cleanup needs resource ownership and absence checks; deleting a
service does not imply deleting its retained sessions, artifacts or provider data.

## When the application answers analytical questions

Define metric, population, units, row grain, time window, joins and expected
freshness, including denominator, zero versus missing data, reporting timezone
and interval boundaries. Use reviewed parameterized queries when the complete meaning is fixed;
retrieve only authorized relevant schemas for ad-hoc authoring. Separate model
proposals from query validation and execution under a restricted identity.

Record scan/cost limits independently of returned row limits. Preserve the
analytical operation behind a follow-up such as “sort that result.” Test known
answers and forbidden executions separately; SQL that runs can still multiply
rows incorrectly or answer the wrong business question.

Keep result selection separate from presentation order when interpreting
follow-ups. Public results distinguish complete, truncated, empty and unavailable
evidence; failed or incomplete retrieval cannot establish absence. Query completion
time does not establish freshness of the underlying records.
