# Qualify the contract before paid inference

Read when document-grounded generation depends on label conventions, dense source
representations, exact excerpts or several validators. Qualify ordinary engineering
contracts offline before spending on model decisions. Preserve meaningful evidence,
authority and spending gates; accepting a misleading reference is not solvability.

## Trace requirements across the actual boundaries

1. Inventory every mandatory output requirement: labels, uniqueness, identity,
   completeness, allowed uncertainty, required controls and size. For each, record
   its authoritative requirement/source, effective prompt instruction, wire-schema
   constraint and application validator. Mark application-only checks explicitly;
   providers cannot enforce every rule. Inspect rendered instructions and serialized
   requests, not just templates.
2. Where practical, derive instructions, schemas and validator configuration from
   one versioned contract. Give deterministic code ownership of known IDs, literal
   spans, hashes and calculations. Verify behavior too: matching requirement names
   in a traceability table can hide disagreeing implementations.
3. Construct valid fixtures independently from authoritative sources before running
   the candidate pipeline. Review substantive interpretation separately from the
   generator/checker under test. Include unsupported meaning, identity mutation,
   omitted qualifications and invalid labels as negatives. Record reviewer and
   source/version; AI-authored expectations remain provisional, not independent
   domain review.
4. Pass source-reviewed valid fixtures through actual schema/native projection,
   semantic validators, orchestration and storage, with effective instructions
   checked against the same contract. Invalid fixtures must fail for the intended
   reason; rejecting everything is not a gate. Missing instructions, ambiguous IDs
   or unrepresentable required outcomes block dispatch as contract preflight
   failures rather than triggering repeated model tuning.

Completion requires honest passing references for consequential outcome classes
and discriminating negatives at intended boundaries, with unexecuted boundaries
explicit. Use [evaluation design](evaluation-design.md) for review outcomes and
[provider compatibility](provider-compatibility.md) for the wire route.

## Exercise representability, not just short prose

| Document shape | Offline qualification |
| --- | --- |
| Nested numbering | Retain hierarchy and document/version/occurrence identity; repeated local clause numbers stay distinct |
| Cross-page clauses | Assemble all operative parts with qualifications and exact physical pages |
| Footnotes | Link notes to operative clauses/cells; retain scope and exceptions |
| Repeated table cells | Use table/row/column/occurrence identity; equal text does not merge independent sources |
| Image-only pages | Preserve page/region and actual governed visual evidence; unsupported/unreviewed visuals stay unresolved |
| Missing neighbours | Detect required missing continuations/qualifications before generation; report incomplete input |
| Dense policy tables | Represent necessary cells, headers and notes under actual limits; splitting/grouping preserves their relationships |

Distinguish physical-page adjacency within a document/version from selected-pack
adjacency. Consecutive pack entries may be physical pages 2 and 8; physical pages
2 and 3 may be separated or reversed in the pack. Resolve source coordinates and
declared links rather than pack positions. Content hashes do not replace occurrence
IDs when identical text appears in different cells.

Measure actual-sized inputs and full result/checkpoint envelopes through configured
write → reopen → reuse without truncation. Use supported lossless compaction or
verified references; otherwise record unsupported shape/size and make a contract
or workload decision. Small fixtures and image placeholders do not prove production
fit or visual handling. Keep model input, provider schema and storage limits separate.

## Separate deterministic binding and model interpretation

Ask the model to select supplied reference IDs and explain relevance, support and
uncertainty. Resolve authoritative literal text and coordinates in code where
appropriate. If exact quotation is required, emit the original bound span server-side;
joining a line-wrap hyphen during regenerated quotation should not become an
unexplained semantic failure.

For paraphrases, allow harmless wording variation where the contract permits it,
with independent support checks. Any normalization is versioned, scoped and tested
to preserve quantities, negations, exceptions and identity. Broad punctuation or
hyphen removal can change meaning. Test identity/content mutations separately from
permissible wording. Exact strings and valid IDs do not independently prove support.

| Layer | Passing establishes |
| --- | --- |
| Pydantic/native validation | Local types/coercions and custom validators actually exercised by the application |
| Provider-enforced JSON Schema | Supported constraints in the actual outgoing schema on the selected provider/model/endpoint |
| Semantic source checks | Completeness, applicability, qualifications, contrary evidence and support under the reviewed rubric |

Local validators may impose rules absent from JSON Schema; adapters may transform
or drop keywords. OpenAI-compatible transport does not establish equivalent schema
enforcement. Inspect the emitted schema and relevant provider capabilities before
a budgeted canary when remote evidence is needed. Structured output alone does
not establish factual correctness.

## Repair the earliest dependency and qualify the normal route

Classify the first defect as retrieval, observation, reconciliation, drafting,
review or evaluator. Compare each stage's actual input/output and source obligations;
a downstream rejection may correctly detect an earlier omission. A reviewer cannot
recover operative policy absent from its inputs. Repair ingestion, selection or
representation at its producer rather than weakening downstream gates.

Bind saved stages to effective inputs, source/parser versions, prompts, schemas,
settings and implementation. Reuse unchanged qualified upstream work, invalidate
affected descendants, count actual sends and preserve failed originals.
[Progressive validation](progressive-validation.md) governs continuation, fresh
cases and final regression; optional workflow guidance details checkpoint reuse.

Drive the normal entrypoint with external access denied and the provider boundary
substituted, preserving real Runner/orchestration, validation and configured storage.
Assert that it invokes the same controls as a correction probe, blocks impossible
contracts before dispatch and reopens complete evidence. Broaden earlier checks for
shared authority, persistence or contract changes. Once staged execution stabilizes,
run authorized fresh end-to-end live cases through that route, then final regression
on the frozen snapshot. A successful correction probe cannot substitute for this.

## Small fail-before/pass-after controls

The [synthetic source pack](../assets/contract-qualification.json) contains nested
clauses, a cross-page exception, footnotes, repeated cells, a dense table and an
unreviewed image placeholder. It has no PDF/image bytes or independent domain review.
The [executable examples](../tests/test_contract_qualification.py) retain deliberately
broken prompt/label, pack-adjacency and regenerated-quote controls. They test a tiny
local JSON route with counted provider substitution and file write/reopen, not ADK,
Pydantic, provider schema enforcement or live quality.

From the installed skill directory, with Python 3.11 or later:

```bash
python -B -I -m unittest discover -s tests -p 'test_contract_qualification.py' -v
```

Adapt those controls to the target's actual boundaries; their toy fixture support
oracle is not a production semantic checker. Keep expected meanings out of generation
input and report synthetic, real-Runner, provider and substantive review evidence
separately.
