# Qualify checkpoints before continuation

Read before resuming an application stage from saved producer output. Define
the contract in the target application's existing stores and interfaces; this
reference is a design and acceptance procedure, not a bundled recovery service.
Framework checkpoints and populated state keys alone grant neither reuse nor
exactly-once effects.

## Retain a complete dependency identity

For each reusable stage, retain an immutable manifest that resolves:

| Dependency | Qualification |
| --- | --- |
| Source snapshot and full inputs | Exact source/content identities, all effective inputs and upstream artifact versions; references resolve to complete unchanged private content |
| Instructions and schema | Effective instructions, tool contract and serialized response schema, including dynamically compiled definitions |
| Model configuration | Backend/route, requested and available returned model identity, generation/reasoning/output settings and relevant adapter configuration |
| Response and projection | Authoritative raw response with attempt identity, native validated projection and their verified correspondence |
| Producer implementation | Relevant code/dependency versions and runtime manifest, including new, uncommitted or ignored files that affect execution |
| Review dependencies | Exact draft revision/content, frame, producing invocation and full image/visual inputs or verified references |

Store hashes alongside retrievable content or verified references. A hash does
not authenticate the producer or owner: resolve evidence under trusted
caller/session authority and retain origin/attempt identities separately. A
sanitized public log can point to authorized private evidence; it need not expose
complete inputs. Missing evidence leaves reuse unqualified.

Compare effective dependencies with the proposed continuation before using the
checkpoint. Reuse only unaffected stages; a code edit outside a producer's actual
dependencies need not invalidate it. Any compatibility mapping for an intentional
version change needs explicit, tested justification rather than relabelling old
output with the new identity. Revalidate current authorization and publication
policy before effects even when inference is reusable.

## Invalidate by dependency, preserve history

Represent which stage consumes each artifact. A changed dependency invalidates
its consumer and every descendant that depends on it, including saved reviews
and exports. Independent unaffected branches may remain qualified. A warning
change to a draft still changes a review's exact input and invalidates that review.
Use an atomic version check or equivalent fencing at commit so a concurrent
change cannot publish a review validated against the previous draft.

Keep the failed original, its response and warnings immutable. Append a separate
continuation record with parent attempt/checkpoint IDs, reason for continuation,
qualified and invalidated dependencies, tested snapshot, authority/envelope
reference and new attempt identities. Diagnostic counterfactuals stay explicitly
non-authoritative; edited or fabricated responses cannot become producer evidence.

Deduplicate logical operation identity plus its bound inputs/authority before
dispatch. Include failed, interrupted, pending and no-response attempts in the
lookup, not only successes. Reconnect/reconcile an existing accepted operation
where supported. A permitted new attempt has a separately recorded identity and
consumes continuation quota; it does not erase the prior call or unknown cost.
Without an authorized reconciliation or safe retry contract, leave the outcome
uncertain and stop rather than dispatching a duplicate. Use
[model-call controls](model-call-controls.md) when transport caps are required.

## Exercise realistic persistence before paid execution

Drive realistic complete outputs through the actual Runner, serialization,
configured checkpoint write, reopen and producer-reuse path with controlled model
responses. Measure the whole stored envelope in bytes, not just native fields or
tokens. Exercise just below, at and above the storage limit, with metadata,
warnings and visual inputs represented. Verify failure before the next paid stage.
An in-memory alias or tiny fixture does not establish durable storage fit.

Where supported, remove redundant copies through lossless compaction or verified,
access-controlled references to complete private inputs. Prove round-trip evidence
and warning preservation and safe failure on missing, changed or unauthorized
references. Truncation is not successful compaction. Reopen via the configured
service; claims of process-restart durability require an actual restart.

## Observable acceptance cases

Run these through the application's real continuation boundary with a counted
model/transport double and its configured store. They are cases to implement in
the target, not tests already shipped or measured by this skill.

| Case | Required observation |
| --- | --- |
| Downstream-only repair with qualified upstream producers | Zero upstream model sends; affected stage and required descendants execute; original failed record unchanged |
| Changed source, input, instruction, schema, config, code or projection | Reuse rejected for each affected dependency; descendants invalidated before dispatch; unaffected branch control still reusable |
| Review after draft/frame/invocation/image change | Old review rejected; unchanged-input control qualifies; publication race cannot commit a stale review |
| Failed/interrupted/no-response duplicate, including after restart | Zero duplicate dispatch; consumed calls and unknown holds persist; permitted new attempt has distinct linked identity |
| Realistic payload near/over storage limit | Runner/write/reopen/reuse succeeds within the limit or fails visibly before downstream dispatch; evidence and warnings round-trip intact |
| Diagnostic edited response | Cannot enter the authoritative checkpoint or publication path |
| Saved-stage success without fresh complete case | Recovery gate passes only; full-route, clean latency and release gates remain unverified |
