# Production policy, evaluation and recovery

Read when choosing data policy, supporting tenant-specific requirements, tuning
detectors, adding persistent or non-text data paths, or planning a controlled
rollout. Use only the sections relevant to the target. These are **production
guidance**, not supplied features or newly verified guarantees. Implementation
and detector evidence must come from the target's tests. Provider mechanics are
in [sdp.md](sdp.md), [model-armor.md](model-armor.md) and
[boundaries.md](boundaries.md); deployment and IAM are in
[cloud-lifecycle.md](cloud-lifecycle.md).

## Make the data policy executable

Inventory actual data classes and purposes before selecting detectors. Include
credentials, direct identifiers, financial/government identifiers, confidential
business data and linkable references. An opaque customer ID can still identify
someone through joins; an ordinary PII detector does not classify contract terms.

For every relevant boundary, complete this record using trusted configuration:

| Policy field | Decision to record |
| --- | --- |
| Boundary and purpose | Source, recipient/sink, authorised task, minimum necessary fields |
| Data class and allowed form | Raw only when expressly permitted; otherwise approved fragment, label, token or no value |
| Action and control | Allow, reject, redact, replace/mask or tokenise; enforcing schema, detector and template |
| Required coverage | Information types/custom patterns on this specific input, tool or output path; known gaps |
| Unavailable action | Withhold, quarantine, hold/discard export, or a separately defined restricted route |
| State and ownership | Policy ID/version, permitted tenant classes, owner, retained stores and deletion rule |
| Acceptance evidence | Positive/negative fixtures, expected action and allowed sinks; unresolved production checks |

For example, support text may replace an email with `EMAIL_ADDRESS`, while a
receipt tool accepts an authorised contact reference and resolves the address
privately. A raw payment value needed for a transaction belongs in an approved
deterministic collection workflow. Neither case requires exposing it to the
model. Retrieve only necessary fields at the source; public-result projection
is an additional boundary after retrieval.

Separate **required policy** from **configured coverage**. The historical deny
and PII sets in [sdp.md](sdp.md) do not implement every class above, and historical
output screening did not reuse the credential-deny template. Resolve policy
ambiguities with the responsible owner before enabling the affected path; other
bounded offline work can continue. Record the configuration used for a release
so later template, detector or managed-filter changes are reviewable.

## Select the complete runtime for each approved policy

When tenants need different templates, transformations or regions, resolve:

```text
verified principal -> authorised tenant -> approved policy ID -> runtime
```

The policy mapping is server-owned. Each selected runtime must use the matching
SDP services, direct Armor checks, native plugin template pair, tool policy and
release gate. The stock native plugin has one configured template pair;
switching the HTTP handler's protector alone leaves other boundaries unchanged.

Prefer separately configured runtimes keyed by an approved policy class, or a
custom boundary resolving a pre-approved policy from trusted invocation context.
Keep the set bounded and reuse/close clients through the existing lifecycle.
Keep mutable session/user state isolated even where policies share clients;
request text or model arguments cannot select projects, regions or templates.
Avoid changing a shared plugin's configuration during a request.

Before enabling this selection, prove two concurrent tenants use their intended
input/tool/output policies and cannot reuse each other's sessions. Check active
policy versions, regional placement and client reuse together. The companion's
tenant ownership checks use one central policy; they do not prove this design.

## Define unavailable and rollout modes explicitly

| Route | Required behaviour when a required check is unavailable |
| --- | --- |
| Private account/customer action | Withhold the action and answer; return a generic outcome |
| Approved public-information fallback | Enter a separate tested path with private tools disabled and no private history or sensitive persistence |
| Asynchronous ingestion | Quarantine under restricted access; index only after required inspection succeeds |
| Analytics/log export | Hold under the approved policy or discard; never substitute the original payload |
| Re-identification | Withhold recovery and alert its responsible operator using safe metadata |

A restricted fallback needs its own approved input/data policy, call graph and
tests showing private data cannot enter it. Treat unavailable screening as a
distinct decision; ordinary execution must never become the implicit fallback.
Quarantine itself is a sensitive store with an owner, access and retention rule.

For a shadow rollout, preserve the currently approved enforcement path and use
a separately governed direct caller to compare candidate decisions. Authorise
the additional data processing and bounded live calls under the existing scope;
record decision metadata rather than content. Define candidate acceptance and
stop conditions before starting. The native plugin's
`block_on_screening_failure=False` changes failure handling and still blocks
successful matches; it does not implement observation-only behaviour.
Restricted modes and shadow rollout are not implemented by the companion.

## Evaluate detectors separately from orchestration

1. Build a versioned, labelled synthetic corpus for supported languages, local
   telephone/name formats, usernames, copied forms and context-poor identifiers.
   Include benign lookalikes, overlapping information types, misspellings,
   unusual separators and legitimate internal handoffs. Add transcription
   errors/spoken digits only if the product accepts transcripts.
2. Label each case with data class, boundary, expected detection/action, approved
   transformed meaning and prohibited sinks. Include deliberately generated
   output cases; input canaries repeated by a model do not establish independent
   output coverage. Have an appropriate reviewer resolve ambiguous labels.
3. Use doubles to verify ordering, incomplete-result handling and sink absence.
   Use separately authorised provider calls to measure real detection. A mock
   returning a finding proves no detector accuracy. For adversarial encodings,
   specify the supported normalise/reject/quarantine policy before testing.
4. Report true/false positives and false negatives, precision `TP / (TP + FP)`
   and recall `TP / (TP + FN)` by information type **and** input/tool/output
   boundary. State whether counts represent cases or individual findings;
   record sample size and undefined denominators rather than inventing a score.
   Also check residual disallowed content and preservation of useful intent.
5. Tune thresholds, hotwords, exclusions and custom detectors from observed
   errors. Retain benign controls and a separate evaluation subset so tuning
   examples alone cannot establish improvement. Set acceptance thresholds with
   the policy owner; a global score can hide an unacceptable credential miss.
6. Record detector/template/filter configuration and versions where exposed,
   fixture revision and evaluation results. Review policy changes under the
   target's change process, repeat affected boundary regressions and representative
   cases, then enable only the approved configuration. Managed aliases and
   retired filter versions require re-evaluation when behaviour changes.

The corpus, denominators, separate evaluation subset and acceptance gates are
implementation recipes derived from the chapter's evaluation guidance. No
representative accuracy study is supplied by the companion or bundled tests.

## Govern historical and derived data

For each store that actually exists, record permitted content, access principal,
policy version, retention period, deletion mechanism and derivative provenance.
Include session state/summaries, caches, memory, artifacts, queues, indexes,
evaluation/replay datasets and retained backups where present. Provenance should
locate derivatives without embedding their sensitive contents.

| Extension | Decisions and checks before reuse |
| --- | --- |
| Existing sessions | Migrate, delete or restart incompatible history; protect summaries from approved source content; test restore, retry, rewind and replay |
| Durable memory | Store the minimum useful fact through an approved write schema; authorise/project reads; protect source and derived facts independently |
| RAG | Classify at ingestion, authorise document/chunk retrieval, minimise and protect passages before the assembled model request; locate the actual injection path |
| Files/media | Choose supported screening/extraction routes; restrict or reject unsupported types; govern the original recording/file as well as extracted text |
| Deletion | Follow source-to-derivative provenance through stores and retention policies; verify deletion or document specifically retained copies and access constraints |

Updating an old session's policy marker does not sanitise its contents. A summary
may disclose a fact without repeating the original text. Test that prohibited
values disappear from both source and derived destinations under the intended
deletion workflow. Process-local locks/storage do not establish durable or
distributed guarantees.

For encoded or extracted input, inspect the same canonical representation the
model receives. Allow only supported decoding/normalisation, bound expansion
and processing, and prevent reinterpretation after the verdict. File screening
does not by itself produce a de-identified file. Verify current modality support
and test the target's extraction path; the companion implements text only.

## Choose transformation and recovery capability by purpose

| Need | Candidate transformation and required decision |
| --- | --- |
| Preserve a value's role in a sentence | Information-type replacement; verify useful intent survives |
| Remove the value | Redaction; accept the resulting loss of detail |
| Display an approved fragment | Masking with explicitly permitted characters/suffix |
| Correlate without recovering the original | Keyed one-way token, such as HMAC; govern equality/linkability and key scope |
| Recover under separate authority | Reversible tokenisation, such as deterministic encryption; design recovery authority and key lifecycle first |
| Preserve legacy length/alphabet | Format-preserving transformation only when that compatibility is necessary |

Prefer irreversible replacement when recovery serves no approved purpose. Stable
tokens reveal equality and can enable joins; scope them to the smallest useful
tenant, purpose and period. Structured context can scope correlation; a free-text
request has no implicit context column. Choose suitable key separation or a
structured design when tenants must not correlate values. Opaque public message
references should not derive from private contact data.

For reversible free text, verify the provider's current surrogate-annotation and
re-identification requirements; use approved key management, such as a KMS-wrapped
key, rather than raw key material in application requests. Put recovery behind
a separate private identity/service accepting narrow field-level requests with
purpose and authority checks plus safe audit metadata. The recovered value may
belong only in trusted delivery/transaction code; an ordinary agent tool must
not provide general token recovery. The companion provisions label replacement
only; these choices are unimplemented production guidance.

## Budget retries and capacity by boundary

Carry one absolute deadline from trusted ingress through identity, queueing,
screening and execution. Retry selected transient failures with bounded backoff
and jitter inside the remaining budget; policy matches are deterministic
outcomes, not retry candidates. Reconcile uncertain side effects using the
domain's idempotency contract before a retry. The companion's bounded campaign
disabled paid retries; it does not supply a coordinated production retry loop.

Estimate attempts per complete simple/tool turn, including per-field screening
and repeated model calls, before choosing service concurrency and tenant/user
limits. Observe safe metadata for direction, policy version, outcome,
unavailable/partial/skipped checks, payload-size bucket, latency and inspection
volume. Govern opaque correlation mappings separately. Measure the actual
deployment before making tail-latency or capacity claims; small warm medians
are insufficient. Preserve every required boundary when optimising calls.

## Contain incidents and review policy rollback

This short procedure is **derived production guidance**, not a chapter-tested
incident or rollback implementation. Apply it only to the affected data route:

1. Withhold the affected path or enter its already approved restricted mode.
   Preserve safe outcome, policy/version and correlation metadata; avoid copying
   exposed values into tickets, traces or reproduction fixtures.
2. Identify affected sinks, retained derivatives and uncertain tool side effects.
   Engage the responsible data/credential owner for exposure response and any
   authorised revocation, data remediation or delivery reconciliation.
3. Compare the active policy with the recorded release configuration. Restore a
   previous version only if it still meets current requirements and its session,
   runtime and detector compatibility are verified. A rollback changes future
   handling; it does not erase retained data or reverse a completed side effect.
4. Reproduce with synthetic fixtures, rerun the affected boundary and detector
   cases, reconcile retained data/actions, and document remaining exposure before
   resuming the approved route. Apply the target's existing change authority;
   this reference grants no permission for cloud mutation or credential rotation.

## Source and evidence boundary

These recipes derive from `CHAPTER_08_UPDATED.md`, aligned 15 September 2026:
“Define the policy before choosing the service” (84–122); “Model-facing
screening” (126–134); “Redaction, replacement, masking, and tokenisation”
(398–419); “Multi-tenant policy selection” (778–792); “Sessions, memory, RAG,
and attachments” (794–844); “Logging without creating a second data leak”
(882–904); “Failure policy is part of the security design” and “Detector errors
are product errors too” (906–934); production/upgrade tests (1013–1045).
The incident recipe combines those principles with the exposure-response policy
(107) and side-effect reconciliation requirement (1122); it is an adaptation.
The dated manuscript review, sections 6–8, explicitly limits coverage,
preflight, retry, accuracy and latency claims. See [compatibility.md](compatibility.md)
for optional source provenance; no manuscript file is needed to use this skill.
