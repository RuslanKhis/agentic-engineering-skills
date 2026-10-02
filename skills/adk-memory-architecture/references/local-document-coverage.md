# Check local-document retrieval completeness

Read this when retrieving local PDFs or document bundles with supplementary
authorities, continued tables or image-only pages. A successful search response
and a correct document ID do not establish that the operative evidence arrived.

## Start with an inventory and a question

1. Inventory approved document versions, pages, headings, cross-references and
   required visual material before asking the model to produce claims. Follow
   references to supplements within the authorised corpus. Record a missing
   referenced source as unresolved evidence; keep scope and payload bounds.
2. Retain the extraction result for each page, including an empty string,
   extraction errors, table continuation and visual-review status. Preserve
   headings, qualifiers and links between pages as evidence units.
3. Define expected documents and complete operative sections per question on
   the evaluation side. A contents-page hit counts as a document hit only.
   A table requiring two pages is incomplete when only its first page arrives.
4. Capture the actual query sequence, source filters, selected release, returned
   passages and any post-retrieval truncation from the application adapter.
   Record hand-written golden queries separately. Their success establishes
   retrievability under those queries, not that the agent will formulate them.
5. Score document coverage and operative-section coverage before claim quality.
   Include a question whose answer needs a supplementary exception. A retriever
   returning the main document for every question must fail that case.

Classify failures from retained observations, not from the model's explanation:

| Diagnosis | Observable condition | Next step |
| --- | --- | --- |
| `absent_content` | A required source or segment is missing from the available corpus/ingestion inventory | Reconcile the approved source inventory and ingestion; report unresolved evidence |
| `empty_extraction` | A present page/segment produced no text | Inspect extraction status and the visual-review path; do not infer no relevant provision |
| `query_miss` | Required text exists in extraction but the actual query did not return it | Compare query, source filters and ranking with the required section |
| `section_truncation` | Extraction or returned text omits part of the required operative span | Repair the extraction/chunk or preserve a complete evidence unit within the existing bounds |
| `unviewed_visuals` | A required visual authority has no completed governed review | Review the authorised source image or keep the answer unresolved |

Multiple diagnoses may apply, especially empty extraction and unviewed visuals.
These are missing-evidence states, distinct from a reviewed authority that
contains no applicable provision. Keep irrelevant neighbours out of the coverage
numerator. Increasing retrieval limits requires evidence that the chosen limits
caused the miss and that the new bounds fit the authorised workload.

## Qualify the source representation before generation

Exercise nested numbering, cross-page clauses, footnotes, repeated table cells,
dense policy tables, image-only pages and required missing neighbours. Bind each
unit to document/version, physical page, hierarchy and table/row/column/occurrence
as applicable. Equal text or identical local clause numbers do not merge identities.
Check that all necessary content and qualifications fit the representation; a
fixed one-span/one-row limit can make dense content unrepresentable.

Physical-page adjacency comes from source coordinates within one document/version,
not selected-pack position. Link continued clauses and footnotes explicitly;
splitting/grouping must preserve header, exception and note associations. Missing
required content or unsupported shapes produce a clear preflight disposition before
model dispatch, rather than a copying/model-quality failure. Unreviewed visual
material stays unresolved through the governed branch below.

Keep known IDs, literal spans, hashes and calculations deterministic where practical.
Models can select supplied references and explain relevance/support; resolve exact
source text server-side instead of regenerating extraction-sensitive strings.
Version any permitted normalization and retain original text/coordinates. Joining
line-wrap hyphens in a paraphrase is distinct from mutating an authoritative quote;
quantities, negations and policy qualifications must survive either representation.

Qualify actual-sized input/result persistence and reopen without truncation through
the configured storage path. Parser/extractor versions and representation settings
are checkpoint dependencies: change them at the earliest affected producer and
invalidate descendants while preserving eligible upstream work and failed originals.
A reviewer cannot recover policy text absent from its inputs. Optional evaluation
guidance supplies prompt/schema/validator qualification; independently source-reviewed
valid references and discriminating invalid controls are required at actual boundaries.

## Govern the visual branch

Resolve the original page through the same source/version and entitlement
boundary. Render or open its authorised image, apply the target's protection
controls before any remote model exposure, and preserve the reviewed page
identity and region with the observation. Record the reviewer/tool, completed
review status, legibility and uncertainty; OCR is an extraction aid, not proof
that the relevant visual content was assessed. A written dimension and a value
estimated from pixels are different evidence types.

If the image is absent, unreadable, unreviewed or outside authorised processing,
return unresolved evidence with the missing authority/page. A model assertion
that it reviewed the image is not a review receipt. The resulting disposition
must affect publication or material uncertainty according to the application
contract; it cannot silently count as support.

## Run the synthetic controls

The [fixture pack](../assets/document-coverage.json) supplies authored extracted
page records for a contents page, operative rule, two-page table, supplementary
exception and an image-only placeholder. It contains **no PDF or image bytes**.
Its values are fictional, and its expectations have not received independent
domain review. These controls test bookkeeping and completeness diagnosis, not
PDF parsing, OCR, semantic applicability or answer correctness.

The [scorer](../scripts/score_document_coverage.py) and
[regressions](../tests/test_document_coverage.py) are portable offline examples:

```bash
"$PYTHON" -m pytest "$SKILL_DIR/tests/test_document_coverage.py" -q -p no:cacheprovider
"$PYTHON" "$SKILL_DIR/scripts/score_document_coverage.py" \
  --question maintenance-route --observation /path/to/observation.json
```

Set `PYTHON` to an existing interpreter and `SKILL_DIR` to this installed skill.
The scorer uses only the standard library; the test command uses the target's
existing pytest. CLI exit 0 means complete fixture spans; exit 1 means an
incomplete or invalid retrieval observation. Invalid input raises an error.

The adapter-owned observation has this shape; the deliberately sparse example
fails the supplementary-exception question:

```json
{
  "available_documents": ["main-policy", "supplement-s1", "notice-n1"],
  "extracted_segments": {"route-rule": ""},
  "hits": [],
  "query_origin": "manual_golden",
  "queries": ["raised route maintenance exception"]
}
```

Populate extraction records from the ingestion boundary and each hit as
`{"segment": "route-rule", "text": "the actual returned passage"}`. Segment
IDs map to document/page/section in the evaluator-side fixture. Keep expected
sections and answers out of the retriever/model input. For these small controls,
each required segment must arrive as a complete span; a real adapter can retain
verified offsets to assemble adjacent chunks without losing qualifiers.
Provenance fields are supplied by the trusted recording adapter; the scorer
does not authenticate them or run a query. Preserve actual agent query traces
before using `query_origin: "agent"`; a manual run is not agent evidence.

The image-only case always remains unresolved in this text-only pack, even if
an observation claims a review occurred. To exercise successful visual review,
supply an approved synthetic image/PDF in a separate application fixture and
verify the actual visual path and its receipt. Never convert the placeholder's
metadata into the missing provision.

Completion requires both the honest complete-text control and the failing
main-only, contents-only, partial-table, empty-extraction and unviewed-visual
controls. Then exercise the target's actual extractor and agent query adapter
on representative documents, with its existing versions and limits. Report
those results separately from this deterministic fixture pass.
