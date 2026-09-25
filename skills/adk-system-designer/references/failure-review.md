# Review the architecture through its failure windows

Use before finalizing a whole-system design or when reviewing an existing one.
Select failures from the promised behavior. Give a reason for cases that do not
apply; do not invent write machinery for a read-only product.

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
