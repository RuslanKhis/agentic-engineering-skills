# Diagnose failures without repeating accepted work

Read this for provisioning, retrieval, screening, hosted evidence, credential
expiry or cleanup failures. The entries distinguish observed failures from
proposed remedies. Preserve the current scope, journal and call budget; a
diagnosis does not authorise another model turn, write or deployment.

## Start with the failing boundary

Record the last proven stage, exact selected resource/identity, operation or
execution handle, safe error class, UTC window and remaining allowance. Separate
application outcome from provider effect: a blocked response can follow a
successful write. Prefer a narrow read or isolated synthetic component replay
to a complete re-run. Do not capture raw prompts, tokens or provider bodies in
public diagnostics; use an allowlist of stage/status/code and safe fingerprints.

| Symptom | First useful check | Unsafe inference to avoid |
| --- | --- | --- |
| Project lookup denied after a login/project change | Selected account, ADC override/quota project, explicit target and permission | UI selection or billing linkage must have fixed CLI access |
| Accepted create followed by immediate not-found | Recorded operation and exact owned resource path; bounded read reconciliation | Create failed, so allocate another resource/name |
| Operator RAG works, application has no passages | Runtime permission, release/manifest mapping and safe stage diagnostics | Empty result means the corpus contains no relevant policy |
| Setup retrieval gets a transient server error | Case fingerprint, persisted attempts and completed cases | Re-run setup/import/full smoke with a fresh budget |
| Final answer or tool result is blocked | Failing protection stage and whether a side effect already has a handle | No answer means no memory write occurred |
| Probe execution succeeds but result is missing | Exact execution, fixed log time window and pagination | Submit another probe to recover ambiguous evidence |
| Long cleanup begins returning 401 | Credential's actual expiry and selected identity | Acquisition time is token issue time, or IAM must be changed |
| Network delete reports a serverless reservation | Owned service/operation termination and reservation release | Force-delete an unrelated or provider-managed address |

## Durable setup retrieval recovery

The source added recovery only for read-like setup `retrieveContexts` requests:
three attempts per case, HTTP 500/502/503/504, with 2- and 5-second backoffs.
Those are a tested lab policy, not universal provider retry recommendations.
Its two cases therefore need allowance for up to six retrieval dispatches.
Do not transfer this policy to generation, corpus import, writes or the full
application smoke. HTTP 429 can require a quota remedy rather than more calls.

When adapting the mechanism:

1. Fingerprint candidate, corpus, immutable source/manifest version, cases,
   retrieval configuration, endpoint and retry policy. Reject changed inputs
   rather than silently reusing incompatible results.
2. Persist attempt count and `in_flight` before dispatch. Record a known
   retryable failure, terminal failure or completed result afterwards.
3. Resume completed cases without redispatch. Resume backoff with the remaining
   allowance. A stale `in_flight` request is uncertain; restarting the process
   must not reset the budget or invent a known failure.
4. An empty/irrelevant successful response is a failed evaluation, not a
   transport retry. Do not keep querying until a desired answer appears.
5. Exhaustion, malformed progress or a missing legacy attempt journal blocks
   automatic continuation. Keep cleanup available and retain evidence.

Test interruption before dispatch, after dispatch, during backoff and after a
case completes. The source's offline tests verify these cases; a later hosted
setup passed both cases but did not finish the downstream application smoke.

For a handle-less interrupted read, retain uncertainty and charge the dispatch
against its original allowance. Look for an exact response/audit correlation;
elapsed time or a healthy endpoint cannot recover the lost evaluation result.
If evidence cannot settle it, leave that case unevaluated. A human-approved new
read attempt can be planned with an explicit additional allowance and linked
to the old journal, without rewriting the unknown attempt as a failure or
resetting its counter. This is manual recovery design, not the source's automatic
resume behaviour. It does not apply to an unresolved import or memory write.

## Protection capacity and fail-closed diagnosis

Count work at the protection boundary. In this implementation, every nonempty
string that passes the deny inspection takes **two DLP RPCs** (inspect, then
de-identify) plus its Model Armor stage. Recursive tool-result screening visits
string values, including metadata, and parallel tools share only a per-process
semaphore. Four concurrent tasks is not four requests per minute or a project-
wide rate limit.

Use a workload estimate before proposing more quota:

```text
estimated DLP requests = 2 × strings passing inspection across all protection passes
project demand = sum of API replicas, workers, diagnostics and other project users
```

Twenty such strings imply roughly forty DLP calls before other input/output
passes and retries. This is a worked count from the source's call graph, not a
service quota or cost estimate. Inspect the actual target's paths; rejection,
empty strings, caching and different policy implementations change the count.

Use a small worksheet for the proposed continuation:

| Budget input | Record before dispatch |
| --- | --- |
| Quota dimensions | Effective limit and window for each relevant method, region and project; timestamp of readback |
| Competing demand | Other replicas/workers/users and headroom; unknown demand is not zero |
| Work per phase | Maximum strings per pass, DLP/Armor RPCs, retry amplification and maximum model/write attempts |
| Coordination | One shared admission/rate-control policy and the burst limit; local semaphores alone do not supply it |
| Remaining allowance | Already dispatched, uncertain dispatches, proposed continuation and reserved reconciliation/export/cleanup work |
| Stop rules | Capacity/error threshold, per-call deadline and total elapsed ceiling; no automatic budget reset |

For a verified available allowance of `A` DLP calls per minute and at most `C`
calls per admitted turn, `floor(A / C)` is only a throughput upper bound. Apply
headroom and burst constraints, account for every quota dimension and pace the
actual dispatches. This arithmetic neither implements a limiter nor proves
provider enforcement behaviour. If `A` or `C` is unknown, do not invent a safe
turn rate; use an explicitly bounded diagnostic or resolve the missing input.

On quota/unavailability failures:

1. Preserve fail-closed behaviour and already-known write/operation records.
2. Identify inspect versus de-identify versus Armor input/output. Correlate the
   matching project, quota dimension, endpoint, identity and timestamp. An
   earlier quota-exhaustion sample does not establish a later error's cause.
3. Read effective quotas independently of a requested increase. A saved quota
   preference is not a granted capacity change.
4. If a narrower approved experiment is useful, replay synthetic protected
   samples through the real policy method under the serving identity. Bound
   each RPC, call count and total time, and avoid unnecessary model calls or
   rebuilding all backends. A passing replay leaves an unreproduced failure's
   cause unknown and does not establish a complete hosted pass.
5. For a proposed remedy, consider smaller projected payloads, fewer redundant
   protection passes with proven coverage, or coordinated admission/rate
   control across replicas. Batching must preserve field boundaries, policy
   results and all-or-nothing publication. These are production changes to
   validate; the chapter did not prove batching or pacing as a live fix.

Do not simply omit IDs/status strings from an existing all-string policy.
Classifying some fields as trusted requires a defined schema and tests for
untrusted values in those fields. Failures, cancellation and policy-version
changes must not release partially protected results or reuse stale approvals.

## Hosted probe results and time budgets

A successful job execution and an unambiguous application result are separate
assertions. Filter by the exact owned execution and use a fixed timestamp window
covering dispatch/queueing through completion, with explicit clock allowance.
Keep all query parameters identical while following page tokens; empty pages
with a continuation token are not exhausted searches. Google's [Logging
reference](https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list)
documents this behaviour and recommends selective timestamp filters.

For a probe promising exactly one result, collect to exhausted pagination within
the deadline, require exactly one valid marker, and reject duplicates across
pages. The source used a 60-second/10-page bound and five-minute clock allowance;
choose target-appropriate limits. An incomplete search remains incomplete even
after finding one plausible marker. Preserve the same job identity; do not
submit a replacement to make the evidence green.

Account for queue/startup separately from job execution timeout. Likewise, an
inclusive Runner interval contains tools, protection, session and memory work;
it is not inference-only latency. Overlapping RPC intervals cannot be added as
if sequential, and one observation per workflow cannot establish a percentile.

## Token expiry during long operations

An opaque token returned by a CLI can already be cached. Use its actual expiry
metadata, a refreshable credential object, or fresh acquisition per bounded
operation. For a cache, derive a monotonic deadline from the remaining lifetime
with safety margin; reject missing, malformed, timezone-less or insufficient
expiry before dispatch. Preserve the selected impersonated identity and quota
project. Never log the bearer or put it in shell command arguments.

The source's REST adapter adopted expiry-aware caching after a cleanup monitor
hit 401. Its tests prove refresh and non-disclosure with doubles; an equivalent
new live long-duration token-expiry experiment was not recorded. Do not replay
a potentially mutating request automatically on 401. Establish credential
health and reconcile its resource/operation outcome first.

## Resume a smoke only from proven progress

Maintain a phase journal with fixture/source identity, attempted chat/write
counts and known job/operation handles. A failed preflight can be repeated only
when evidence proves no application write was attempted and no job remains
unresolved. After partial application work, use a specifically designed
continuation that validates prerequisite state and executes only remaining
phases. Do not call the whole smoke again against changed or erased fixtures.

The source had a narrowly guarded restart continuation for one recognised
traffic-metadata failure. It was not a general retry flag. Report such evidence
as composite acceptance and preserve which revision and control-user baseline
each phase exercised. A new source, altered fixture or incompatible failure
requires a newly planned attempt, within separately established authority.

## Close the lifecycle without overstating it

Stop owned serving/writing activity, settle known operations, export complete
execution evidence, then remove exact owned resources in dependency order.
Capture the final audit job too before deleting its parent. A missing pre-delete
inventory stays missing; later absent resources cannot recreate that evidence.

RAG cleanup depends on deployment mode. Serverless corpus cleanup and Spanner
deprovisioning differ; Spanner-mode `Unprovisioned` deletes that backend's data
irreversibly. Inspect the actual mode, all owned regions and other users before
proposing the appropriate action. Do not switch modes or deprovision a shared
backend to get an empty listing. See Google's [RAG deployment modes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/deployment-modes).

If a provider reservation still blocks subnet deletion, retain the journal,
report the exact dependency and retry only scoped observation/deletion after
release. Past release duration is not a deadline guarantee. Distinguish active
capacity, retained/soft-deleted storage, pending operations and delayed charges;
an empty visible VPC is neither proof of all-project cleanup nor a billing cap.

Find the implementation tests and dated evidence for these lessons in
[provenance.md](provenance.md).
