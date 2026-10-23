# Memory Bank revisions, LongMemEval and Docling compared with this toolkit — 23 October 2026

## Scope and snapshot

Three memory sources read on 23 October 2026: Google's documentation page
"Memory revisions" for Gemini Enterprise Agent Platform (updated
2026-10-21, fetched raw);
[xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) at
commit `9e0b455` (MIT code; its 500 questions are hosted on Hugging Face and
were neither downloaded nor imported); and
[docling-project/docling](https://github.com/docling-project/docling) at
commit `29caea8` (MIT; PyPI 2.142.0 of 2026-10-22), read, never run.

**Conclusion.** The memory skill's reconciliation table and erasure rules
now rest on the product's documented semantics rather than on the recipe
that uses them: consolidation creates, updates (duplicative, complementary
or contradictory) or deletes (invalidated) within a scope; revisions are on
by default; `previous_revision` and `rollback` with `target_revision_id`
restore a poisoned fact; `revision_labels` and a label filter on the
revision list make erasure by source possible. LongMemEval's five abilities
give the gold set a structure in which knowledge updates and abstention are
named cases. Docling is named as the extractor to reach for when a project
has none, with its version, interpreter floor and the weights it downloads.

## Method

The product page was read for the three outcomes, the rollback and the
label mechanics; the benchmark README for the abilities only; the extractor
README and PyPI for version and capabilities. Facts placed in the memory
skill with dates and the vendor label; one scenario case covers the
journey; a fresh-agent trial is in the
[testing record](../testing/memory-sources-alignment-2026-10-23.md).

## Drift corrected

- The memo's summary of consolidation holds; the page also states that
  revisions are enabled by default and can be disabled per request or for
  all requests, which the skill's `disable_memory_revisions` example already
  used without saying what it gives up. It says so now.
- LongMemEval-V2 was not read; the memo names it for experience-built
  memory, left for a later pass.

## Imported, by specialist

- **adk-memory-architecture.** The consolidation and revision paragraph in
  the Memory Bank reference; the five-ability gold structure in retrieval
  strategy; Docling in document ingestion.

## Routed, not copied

Nothing.

## Vendored assets

None; the benchmark data is not imported.

## Left out, with reasons

- Mem0's ADK sample as the contrast the memo describes: not read.
- Docling's chunkers as a retrieval design: the skill's chunking rules
  stand; the extractor is named, not re-taught.

## Limits

Read, not run; the product page is vendor documentation on one day.
