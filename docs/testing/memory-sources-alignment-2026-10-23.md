# Memory sources alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/memory-sources-comparison-2026-10-23.md).
In the repository: Memory Bank's consolidation and revision semantics with
rollback and label-scoped erasure in the memory-bank reference; the
five-ability gold structure in retrieval strategy; Docling in document
ingestion. After the trial: the 2.12.0 generate-config keys that travel on
`add_events_to_memory`, a pointer from the Memory Bank reference to the
gold structure, the write-side rules from the security skill (tainted turns,
no authority from memory), the keep-and-flag rule for a product setting
already held in memory, the sample request's `disable_memory_revisions`
corrected to keep revisions, the 2.12.0 facts on `BaseMemoryService` (still
no delete) and `search_memory` (fills `custom_metadata`), a minimal gold-case
shape, and the interpreter rule reconciled with the engineer's. **One
scenario case** (`memory-poisoned-fact-rollback-and-update-cases`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper changed; the memory
inspector's blind spot for a built-in `load_memory` import is recorded as
owed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or Vertex SDK installed, on a synthetic project, without the expected
answers; interrupted once by a usage limit and resumed.

### Memory: a stale address and a planted discount

The project: an ADK 2.12 concierge on Vertex Memory Bank with revisions on,
a nightly generate pass, and a gold set with one extraction case; a user
reporting an old address repeated and a planted "VIP discount" memory.

What the agent did: a pure memory policy (topic allow-list with entitlements
never a topic, recall filtering by scope, topic, author, tombstone, expiry
and size with newest-wins, write eligibility by consent and provenance, a
rollback plan to the last trusted revision); a provider gateway with a
write ledger and an offline double, the Vertex gateway naming the retrieve,
generate, list-revisions and rollback calls as not run; the gold set rewritten
to eleven cases across the five abilities with a rollback case; 25 offline
tests run, 3 Runner tests reported as not run; a notes file listing the
live Memory Bank steps.

Ease rating: **3 of 5**. Routing was clear and the revisions paragraph
answered the injection half; the ability vocabulary hid in a reference
introduced as being about documents.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The gold-set abilities lived in a document-oriented reference with no pointer from Memory Bank | A pointer added at the consolidation paragraph |
| A product setting already in semantic memory contradicted the profile rule with no guidance | The keep-and-flag rule |
| 2.8.0 facts on delete and `search_memory` metadata left 2.12.0 open | Both stated from the installed package, with the generate-config keys |
| The sample request disabled revisions two sections after the text said that gives up rollback | Corrected with a comment |
| The memory inspector missed a built-in `load_memory` import; the interpreter sentence put the target's interpreter first | Inspector change recorded as owed; the sentence reordered |
| No gold-case shape; the quarantined-reader rule not echoed on the write side | A minimal shape and the two write-side rules added |

## What this does not establish

No Memory Bank call ran; whether 2.12.0 passes `revision_labels` through
`add_events_to_memory` was read in the service's accepted-key set, not
exercised.
