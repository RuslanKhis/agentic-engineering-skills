# Local refund adapter exercise

This is a synthetic Python 3.11+ standard-library project. No real provider,
cloud service, framework, package installation or credentials are needed.
The host application already authenticates and authorises the operation ID.

Preserve `RefundService(provider).refund(operation_id, amount, *, confirmed=True)`
and its result keys: `status`, `operation_id`, `amount_minor`, `refund_id`.
Statuses are `applied`, `unknown`, `rejected`, and `cancelled`; refund ID is
`None` unless applied. Invalid inputs and operation/payload conflicts raise
`ValueError` before a provider call. The provider replay key stays internal.

USD amount is a string of ASCII digits, optionally a decimal point followed by
one or two digits. Leading zeros are accepted. No signs, exponent notation,
whitespace, or more than two fractional digits are allowed. Maximum input
length is 32 characters and range is 1 to 1,000,000 minor units inclusive.
Validate with exact arithmetic; equivalent spellings identify the same amount.
An operation ID is a nonempty string of at most 64 ASCII letters, digits,
underscores or hyphens. `confirmed=False` means cancelled, with zero calls.

`provider.issue_refund(operation_id, amount_minor, *, replay_key)` either returns
a receipt with matching `operation_id`, `amount_minor`, nonempty `refund_id`, and
`status="applied"`, raises `TimeoutError`, or raises `ProviderRejected`.

This fixture provider guarantees atomic key/payload binding and deduplicates
every successful side effect by replay key throughout its lifetime. Keys are
scoped to this provider object and never expire during this exercise. Changed
payload under an existing key is rejected. A timeout may happen before or after
commit. A rejection proves only that the current attempt did not apply a write;
it cannot rule out an effect of an earlier timed-out attempt. There is no lookup.

The existing budget is at most two immediate provider attempts per operation.
A timeout can be retried using the original key and canonical payload. A first
attempt rejection is terminal `rejected`; a rejection following a timeout is
`unknown`. Two timeouts are `unknown`. Repeating a completed, rejected, or unknown
operation with the same amount returns its stored result without dispatching
again. A changed amount for a previously dispatched ID raises `ValueError`.
Different valid spellings of the same amount must load the same operation.

Limit the guarantee to this service instance: use its existing in-memory ledger.
Do not claim restart or worker concurrency safety or introduce durable storage.
Preserve provider.py and this contract. Add tests and a concise README explaining
the implementation, test command and remaining production gaps.
