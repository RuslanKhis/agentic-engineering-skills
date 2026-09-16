# Confirmation can pause execution

Use Python 3.11 and the standard library. Preserve the asynchronous public
function `execute_refund(store, provider, approval)`. All values here are
synthetic, supplied by trusted application code, not model authentication.

`approval` records the operator's decision: `operation_id`, `actor`, `reference`,
`revision`, `amount`, `currency`, and boolean `confirmed`. The local store's
`current(operation_id)` is an async read returning the current action with those
fields plus boolean `authorised` and `refundable`. The store can change while
the user is deciding. An execution must match the exact approved action and
current authority/business preconditions. This fixture has no concurrent store
updates after that read; distributed atomic balance reservation is out of scope.

The async provider method `refund(action)` increments an effect counter and
returns `{"refund_id": "fixture-refund"}`. It has no replay guarantee. Preserve
public result keys `ok`, `reason`, `data`. A rejected/stale/unauthorised action
returns `ok=False`, `data=None`, a safe reason and makes no provider call.
Success returns the provider data. Return uncertain provider failures honestly
without replay; caller cancellation must propagate. Do not add an ADK agent,
database, new confirmation UI or live service.
