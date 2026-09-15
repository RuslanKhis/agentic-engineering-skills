# Evidence and design provenance

This skill adapts Chapter 2, “Operational Guardrails”, from *Agentic Engineering* and its MIT-licensed companion. The operational instructions are self-contained; the source paths below are provenance, not required imports or installed dependencies. No separate public book URL was supplied.

Source repository: [agentic-engineering-adk-gcp](https://github.com/RuslanKhis/agentic-engineering-adk-gcp), chapter folder `chapter-02-operational-guardrails`. The reviewed source manifest is `verification/flash-followup/source-sha256.txt`; current manuscript `CHAPTER_02_UPDATED.md`; comparison `MANUSCRIPT_COMPARISON_2026-09-15.md`. The corrected follow-up report supersedes the earlier report's Flash/browser verification gaps.

## Behaviour-to-evidence map

| Skill rule | Working source / successful test in the chapter | Evidence class and practical limit |
| --- | --- | --- |
| Count tool calls separately; prevent repeated failed dispatch | `guardrails.py`; `test_runtime_verification.py::test_repeated_failed_adk_tool_is_stopped_before_second_execution`, `test_parallel_tool_batch_cannot_exceed_step_limit` | Real ADK with fake model, offline. Seven-tool-call runtime limit; ordering tested on ADK 2.8.0. Companion blocks structured failures conservatively, irrespective of `retryable`. |
| Whole deadline, including before first event | `guardrails.py`; `test_deadline_interrupts_a_model_that_has_not_yielded_an_event` | Offline. Cooperative cancellation and iterator cleanup, not a guarantee remote work stopped. |
| Preserve cumulative state and charge all scopes on rejection | `safe_runtime.py`, `budget_store.py`; `test_session_overrun_is_still_accounted_to_user_and_tenant`, `test_user_daily_overrun_is_still_accounted_to_tenant`, `test_runtime_retains_conversation_on_a_second_turn` | Offline. One runtime instance, local post-response counters, caller-supplied identity. No shared reservations or durable state. |
| Test each actual serving entry point | `agent.py` versus `safe_runtime.py` | ADK Web loads the tool agent and does not automatically apply the separate runtime budget wrapper. |
| Approval must not claim payment | `human_review.py`, `test_refund_payment_boundary.py`; corrected Pro retest and Flash follow-up report | Offline serialized-request regressions plus separately verified live answers. An earlier Pro response falsely claimed payment; adding an explicit no-payment tool result/instruction corrected the targeted retest. No payment system exists. |
| Invalid inputs and publisher errors cannot report successful review | `test_refund_billing_verification.py::test_adk_tool_rejects_invalid_amount_without_publishing`, `test_publish_failure_cannot_report_pending_success` | Offline; real publisher SDK boundary substituted. Small amounts approved; large requests sent to a mock in live model tests. |
| Count HTTP attempts and completed usage, not partial snapshots | `scripts/live_model_limits.py`; `test_shared_ledger_blocks_41st_attempt_before_http`, `test_sdk_503_is_one_http_attempt_without_retry`, `test_streaming_uses_same_transport_counter` in `test_live_campaign_limits.py` | Offline transport regressions plus real bounded campaigns. Harness counters are not normal runtime limits; ordinary runtime lacks general usage deduplication. |
| Reconcile accepted API activation after parser failure | `scripts/preflight.py`, `test_preflight.py`; 13 September verification report | Offline CLI fixtures and live reconciliation/read-only checks. Repaired activation from a fresh disabled baseline was not tested. |
| Validate billing envelopes; separate infrastructure authority | `billing_guardrails/budget_event_handler.py`, `emergency_disable_billing.py`, `test_refund_billing_verification.py` | Offline. Handler flags latch; no source authentication, period/version reconciliation or deployed handler. Billing-disable helper is real, with no simulation safety. |

Source basenames without a prefix in the table are under `guarded_support_agent/` unless stated otherwise. These references trace lessons; the installed skill never needs to open those files to function.

## Historical live evidence is scoped

The final Flash follow-up recorded 78 fresh offline checks and a separate 19-submission, 38-generation-attempt live campaign using a local browser/runtime. Six small-refund answers explicitly stated no payment; six high-value answers and six streaming retests remained pending with one tool call per submission. The pressure runtime selected its reduced-output policy and emitted measured usage. The earlier normal-policy Pro correction passed its separately approved targeted retest.

Review publication remained a local mock. Live counter enforcement was not independently proved from usage metadata. No durable human review, reviewer delivery, payment execution, shared budget store, managed deployment, billing shutdown or cloud lifecycle was verified. Selected live answers do not prove universal model compliance. Browser timings showed real first-answer misses; streaming exposed content earlier within a response but did not eliminate model delay.

## Production principles, not inherited implementation claims

Atomic multi-scope reservation/settlement; authenticated identity; stable business-operation IDs; durable review/outbox; authorised reviewer transitions; provider idempotency/reconciliation; versioned billing controls and explicit reset; simulation-first emergency operations are production designs from the updated chapter. Implement and test them against the target architecture before claiming them.

The bundled invocation guard is newly adapted from the pre-execution principle. Its own offline tests establish only its stated local asynchronous contract. It is not copied ADK event instrumentation and does not turn the production designs into implemented services. New skill tests and independent fixture exercises are recorded separately in [validation results](validation-results.md).
