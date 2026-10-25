# mem0, graphiti and unstructured alignment — 25 October 2026

Source note: [comparison](../research/mem0-graphiti-unstructured-comparison-2026-10-25.md).

## Changed journey

`adk-memory-architecture`, keeping a vendor or custom `BaseMemoryService`
that is not Memory Bank.

## Fresh-agent trial

A fresh agent with only the skill packages wrote a stand-in for a
vendor-style Mem0 adapter on ADK 2.12 (every exception caught and returned
as empty, `app_id` written as metadata and read as a scope,
`PreloadMemoryTool` recall) over a fake client, then took the ticket: users
forgotten after a key rotation, movers seeing both addresses, and an
erasure request. It installed google-adk 2.12.0 and pytest; no Mem0 or
graphiti package, network or model.

Result: a fixed adapter with typed unavailable and write errors, matching
write and read scopes, a current-only read, foreign-scope filtering, a
delta write of user events, and an erasure that tombstones, deletes and
then confirms against history rather than search; telemetry off; and a
recall path that tells the model memory is unavailable.

`pytest`: **11 passed** on the real Runner with a strict scripted model.
The original adapter: **9 failed, 2 passed**, the failures being the
intended ones; one of the two passes proves nothing, because the original
reads nothing at all. The agent noted that with the scope mismatch the
original never recalls anything, so "sees both addresses" needs a separate
explanation.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. No routing row for a vendor backend. Fixed.
2. The scope bug was named but not its fix. Fixed: `app_id` as an entity
   field on both sides (checked in Mem0's documentation).
3. What the model is told when recall fails, and whether to subclass the
   preload tool. Fixed: `LoadMemoryTool` or an instruction provider; no
   subclassing.
4. No per-user call named for removing history. Fixed: the hosted and
   open-source calls, and the operator purge where none exists (checked in
   the client source).
5. Hosted and open-source behaviour were mixed. Fixed.
6. No key-rotation pointer. Fixed.
7. The erasure sequence assumes workers and leases, and "content-free
   tombstones" is unclear for a single adapter. Not changed: the sequence
   is the skill's existing contract; a smaller form is a design question
   for its next review.
8. Clock skew in blocking replays after erasure. Not changed, same reason.
9. The inspector labelled a Mem0 adapter as Memory Bank. Fixed, with a
   test: a separate `custom_memory_service` signal.
10. The write-back sequence is written for 2.8.0. Not changed: the skill
    already says to re-check signatures on the target version.

## Limits

No live Mem0, graphiti or model: real filter syntax, `latest_only`
results, telemetry honouring and exception classes were not observed.
