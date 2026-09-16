# Local Refund Adapter

Repairs to the synthetic refund adapter implementation adhering to [`CONTRACT.md`](CONTRACT.md) and the principles of the `safe-api-tool-calls` skill.

## Implementation Overview

The repaired [`RefundService`](service.py) addresses the following key reliability and safety requirements:

1. **Exact Money & Input Validation**:
   - `operation_id`: Validated as a non-empty ASCII string (`1 <= len <= 64`) matching `^[A-Za-z0-9_-]+$`.
   - `amount`: Enforces string type, maximum 32 characters, and format `^[0-9]+(?:\.[0-9]{1,2})?$`. Disallows signs, exponents, whitespace, or excess precision.
   - Exact integer arithmetic converts dollars and cents directly to minor units (cents) within the range `[1, 1_000_000]` ($0.01 to $10,000.00). Equivalent spellings (e.g. `"12.5"`, `"12.50"`, `"012.50"`) resolve to the exact same canonical minor units (`1250`).
   - Invalid inputs raise `ValueError` before any provider interaction.

2. **Confirmation Boundary**:
   - `confirmed=False` returns `{"status": "cancelled", "operation_id": ..., "amount_minor": ..., "refund_id": None}` with zero provider calls.
   - Unconfirmed operations are not recorded as dispatched, allowing subsequent confirmation.

3. **Stable Replay Identity & Lost Response Recovery**:
   - A single private `replay_key` is generated per dispatched operation and reused across retries.
   - For a response lost after commit (`commit_then_timeout`), retrying with the original replay key allows the provider to deduplicate the side effect and return the existing receipt, preventing duplicate refunds.
   - The private replay key is never leaked in returned dictionaries.

4. **Attempt Budget & Outcome Classification**:
   - Maximum budget of 2 immediate attempts per operation.
   - Attempt 1 success &rarr; `applied`.
   - Attempt 1 rejection &rarr; terminal `rejected` (no retry dispatched).
   - Attempt 1 timeout &rarr; immediate retry with original key and canonical payload:
     - Attempt 2 success &rarr; `applied`.
     - Attempt 2 rejection &rarr; `unknown` (honestly reporting uncertainty because attempt 1 may have committed).
     - Attempt 2 timeout &rarr; `unknown` (two timeouts exhausted).

5. **In-Memory Ledger & Idempotency**:
   - Repeating a completed (`applied`), `rejected`, or `unknown` operation with the same amount returns the stored result without calling the provider again.
   - Submitting a changed amount for a previously dispatched operation ID raises `ValueError` before any provider call.
   - Defensive copying (`dict(...)`) isolates stored results from caller mutation.

## Test Verification

Run all unit tests with:

```bash
python3 -m unittest discover -v
```

### Actual Results

```text
test_previously_dispatched_called_with_confirmed_false_returns_stored_result (test_service.ConfirmationTests) ... ok
test_unconfirmed_does_not_block_later_confirmed_dispatch (test_service.ConfirmationTests) ... ok
test_unconfirmed_returns_cancelled_with_zero_provider_calls (test_service.ConfirmationTests) ... ok
test_success_keeps_public_contract (test_service.ExistingTests) ... ok
test_changed_amount_on_dispatched_id_raises_value_error (test_service.IdempotencyAndLedgerTests) ... ok
test_repeating_completed_operation_returns_stored_without_dispatch (test_service.IdempotencyAndLedgerTests) ... ok
test_repeating_rejected_operation_returns_stored_without_dispatch (test_service.IdempotencyAndLedgerTests) ... ok
test_repeating_unknown_operation_returns_stored_without_dispatch (test_service.IdempotencyAndLedgerTests) ... ok
test_repeating_with_equivalent_amount_spellings (test_service.IdempotencyAndLedgerTests) ... ok
test_returned_result_is_isolated_from_mutation (test_service.IdempotencyAndLedgerTests) ... ok
test_invalid_amount_formats_raise_value_error (test_service.InputValidationTests) ... ok
test_invalid_operation_id_types_and_formats (test_service.InputValidationTests) ... ok
test_valid_amount_boundaries (test_service.InputValidationTests) ... ok
test_valid_operation_id_boundaries (test_service.InputValidationTests) ... ok
test_replay_key_stays_internal_and_keys_match_contract (test_service.ReplayKeyPrivacyTests) ... ok
test_commit_then_timeout_followed_by_rejection_is_unknown (test_service.RetryAndRecoveryTests) ... ok
test_first_attempt_rejection_is_terminal_rejected_without_retry (test_service.RetryAndRecoveryTests) ... ok
test_lost_response_after_commit_recovered_with_single_effect (test_service.RetryAndRecoveryTests) ... ok
test_timeout_before_commit_retried_and_succeeds (test_service.RetryAndRecoveryTests) ... ok
test_timeout_then_rejection_is_unknown (test_service.RetryAndRecoveryTests) ... ok
test_two_timeouts_is_unknown (test_service.RetryAndRecoveryTests) ... ok

----------------------------------------------------------------------
Ran 21 tests in 0.002s

OK
```

## In-Memory Guarantee Limits & Production Gaps

In accordance with [`CONTRACT.md`](CONTRACT.md), this implementation intentionally restricts its guarantees to the current service instance:

1. **Ephemeral Process Memory**:
   - The ledger is stored in an in-memory dictionary (`self.operations`). State does not survive process restarts, crashes, or redeployments.
   - *Production requirement*: Durable persistence (e.g., transactional SQL database) with unique constraints binding operation IDs to canonical payloads and provider keys.

2. **Worker Concurrency & Races**:
   - There is no distributed locking or atomic check-and-set across multiple workers or threads.
   - *Production requirement*: Distributed locks, database transactions with row-level locking, or conditional inserts to coordinate competing workers.

3. **Indeterminate Outcome Reconciliation**:
   - The synthetic provider offers no status query or lookup API. Outcomes marked `unknown` remain unresolved within the process.
   - *Production requirement*: Background reconciliation workflows, provider transaction inquiry APIs, or asynchronous webhook ingestion to resolve `unknown` statuses before manual escalation.

4. **Authentication & Authorization**:
   - As specified by contract, the adapter relies on the host application to authenticate callers and verify permission to operate on the given operation ID.
