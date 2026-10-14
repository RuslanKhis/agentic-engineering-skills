# Review the architecture through its failure windows

Use before finalizing a whole-system design or when reviewing an existing one.
Select failures from the promised behavior. Give a reason for cases that do not
apply; do not invent write machinery for a read-only product.

## Build the coverage grid first

Failure analysis written from memory differs from run to run: one design
covers a lost read, the next a partial change. Enumerate instead. List every
external system the design calls (each API, store, identity provider and the
model itself) as a row, and give each row a cell for every failure type:

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Then add one row for each action the agent can take that changes something
(book, move, cancel, send, pay, file a claim), with the failures of the
action itself:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |

"Over-broad" covers a request such as "cancel all my appointments"; "partially
applied" covers a move whose new booking succeeded while the old one was not
cancelled; "confirmation stale" covers a user approving a proposal after the
slot, price or record changed.

Every cell either cites the acceptance item that tests it, as `G04/A2` (goal
G04, acceptance item A2), or says `n/a: <reason>` with a reason of at least
two words, such as "n/a: read only". Number acceptance items A1, A2 in each
goal or ticket so they can be cited. "Untrusted or malformed content" covers
invalid model output, injected text in tool results and unexpected provider
payloads. Run `scripts/check_schedule.py` with `--design` to confirm every
cell cites an item that exists. The grids sit in the design's failure
section; the scenario table below adds the cross-cutting cases they cannot
express. A proof of concept fills the rows it touches in a few words each.

## Trace the actual path

Draw a short sequence through ingress, identity, session/state, model, tools,
authoritative stores and public output. At each boundary identify what may have
happened before the next participant learns about it.

For every chosen failure, answer:

1. What does the user see: rejection, partial output, confirmed result or uncertainty?
2. What data persists, and which invocation or operation does it belong to?
3. Could an external effect already have happened?
4. Is another attempt permitted, with which identity and remaining allowance?
5. Who recovers the work, and what observation establishes completion?

## Choose revealing scenarios

| Scenario | Evidence the design must make possible |
| --- | --- |
| Successful request | Authoritative result and completion; permitted control case exercises the same policy path. |
| Denied user or another tenant's conversation | No protected read/model disclosure or forbidden write; caller-controlled IDs cannot select authority. |
| Model/dependency unavailable or malformed reply | Bounded attempts, honest failure, and a specified fallback that preserves required protections. |
| Draft succeeds, review or later stream fails | Earlier text or stale session output is not released as a newly completed result. |
| Browser disconnect or deadline expires | Owned streams are closed; remote uncertainty and remaining work remain visible to the recovery path. |
| Provider commits, reply is lost | Same business operation is reconciled without an unsafe fresh dispatch. |
| One effect succeeds, a later step fails | Preserve verified completed effects alongside failed or uncertain ones; the final account cannot imply that nothing happened. |
| Process restart or overlapping workers | Required state and allowances survive; ownership conflicts cannot authorize duplicate effects. |
| Approval or entitlement changes while waiting | Material details and current authority are rechecked before the effect. |
| Forget/revoke races with queued work | Late writers/retries cannot silently resurrect erased memory or disconnected credentials. |
| Screening or telemetry path fails | Required policy is enforced before exposure; each enabled sink has a known policy. |
| Policy changes before an old conversation resumes | Incompatible retained or derived data is handled before reuse; changing a policy label alone is insufficient. |
| Burst traffic or exhausted budget | Admission, queueing and downstream saturation behavior are explicit; time and work remain bounded. |
| Tool result or retrieved document carries instructions while the agent holds a write tool | Which structure, not which sentence, prevents the action: the reader has no write or egress tool, or a capability check in code refuses; the forbidden call never runs and a test asserts its absence. |
| Remote A2A peer is unavailable, slow, or returns a state that needs user input | What the parent does on a deliberate timeout and on an error event; a pause reaches only the controlling user; peer text never acts as user authority or an approval. |
| Model returns prose or invalid data where a schema was required | How many repair attempts, what the explicit failure shape is, and that wrong-but-valid data is counted separately; nothing acts on an unvalidated payload. |
| Model or judge retirement lands mid-release | Pinned IDs and a dated calendar made it a planned migration; the re-baseline is its own release with a side-by-side on the frozen development set, and judge scores are not compared across judges. |
| Incident arrives and the telemetry needed to attribute it was never enabled | Which SLIs, gates, sinks and correlation identifiers the design named before the first shared deployment; the alert leads to a stored session and that session reproduces the turn. |
| Rollback or cleanup | Owned resources and retained data are accounted for; unrelated control data survives. |

## Define a verification ladder

Tie each critical invariant to a planned test at the boundary where it matters:

- **Offline deterministic checks:** real policy, tool and relevant Runner paths
  with controlled external responses. Assert attempted calls, stored effects and
  absence of forbidden effects. Vary retries, ordering, concurrency and invalid input.
- **Local integration evidence:** a real process restart for persistence, real
  sockets for streaming timing, actual browser handling where promised. A rendered
  spinner, static import or buffered response does not prove those contracts.
- **Bounded live checks:** verify SDK/provider behavior and model choices on an
  isolated, explicitly authorized target. Declare request/time/cost limits and
  distinguish a local client calling a real service from a hosted application.
- **Release/operation evidence:** appropriate load/quality cases, trusted logs,
  alerts, recovery/rollback and deletion checks before claiming those properties.

Evaluation needs expected case and metric coverage, failed and missing results,
separate initial state where independence is claimed, and calibrated judgement
criteria. A process exit or fluent answer cannot establish an authorized effect.

Record these as planned checks until actually executed. If evaluating an existing
system, identify the evidence that was inspected and its scope/date. For each
unresolved gap state the impacted promise, next experiment or decision, and owner.

End with a useful first implementation slice: one journey, its public result,
its most consequential failure, and observable acceptance criteria. Future
capabilities stay outside the slice unless the user requires them now.
