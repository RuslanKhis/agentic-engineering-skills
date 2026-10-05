# Retrieve by issue with a local index

Read this when a document-grounded agent misses operative policy text, treats
an unresolved policy number as a "gap" instead of a lookup, or runs a fixed set
of one-shot searches that come back truncated. It gives the retrieval technique
that [governed RAG](rag.md) §3 serves and [local-document coverage](local-document-coverage.md)
measures: how to chunk, formulate, follow references, fuse rankings and tell the
next stage what was and was not found. Everything here runs locally with the
standard library; a cloud retrieval service is a later, separately justified choice.

The bundled [script](../scripts/local_retrieval.py) and
[gold fixture](../assets/retrieval-gold.json) demonstrate every step on a
synthetic plan. They are controls for the mechanism, not evidence about a
target corpus.

## Chunk by operative unit

Index the unit a decision cites: a policy heading to the next heading, a table
with its notes, an appendix section. Keep the physical page span on each unit so
citations stay checkable, and let a unit continue across a page break until the
next heading. Screen contents, cover, monitoring and index pages at index time
and record what was screened, so a hit on a contents entry can never pass as a
hit on the policy it points to.

```python
pages = [{"document": "local-plan", "page": 2, "text": extracted_text}, ...]
units = chunk_by_heading(pages)            # heading → next heading, across pages
kept, screened = screen_units(units)       # screened units are listed, not lost
conn = build_index(kept)                   # SQLite FTS5 bm25() over heading + text
```

Adapt `DEFAULT_HEADING` to the corpus's heading grammar; a fixed character
window or a page is the fallback only when the documents have no usable
headings, and then the coverage pack's section-truncation diagnosis applies.

## Formulate queries by issue

Write one query per material issue the case review raised, in the corpus's
vocabulary: "visibility splay classified road gate", not the applicant's
sentence. Then resolve every named reference in code: policy codes, tables,
figures, appendices and supplementary documents that the case, the issue or a
retrieved passage names. A named reference is a deterministic lookup by heading
or document identity, never a ranked guess and never something the model is
asked to remember.

```python
hits = search_lexical(conn, "visibility splay classified road gate", k=4)
for reference in resolve_references(hits[0]["text"]):   # e.g. "Table 2", "Design SPD"
    units = lookup_reference(conn, reference)            # exact heading/document match
```

`retrieve_for_issues` combines both: ranked search per issue, lookups for every
reference the issue or its passages name, and the self-citation shortcut when a
retrieved unit is itself the referenced policy.

## Run one bounded second round

After the first round, three conditions justify more retrieval: an issue with no
operative unit, a reference no lookup could resolve, and a hit list that was
exactly `k` long (truncated). Run exactly one further round for those issues,
within a call budget declared before the run: the next page for a truncated
list, or a reformulated query that adds the unresolved reference terms. Stop
when the budget is spent and say so; a third round is a new design decision,
not a retry.

```python
report = retrieve_for_issues(conn, issues, k=4, call_budget=4 * len(issues))
report["second_round_ran"], report["budget_exhausted"], report["calls_run"]
```

## Fuse a local hybrid index

When the corpus is small enough to embed locally, keep the lexical index and
add a dense ranking from any embedding function, then fuse the two rankings by
reciprocal rank fusion:

```text
score(unit) = Σ over rankings r of 1 / (k + rank_r(unit)),   k = 60
```

RRF uses ranks only, so the two scorers need no calibration, and a unit present
in both lists outranks one that is first in only one. The combination is the
common production shape because lexical and dense retrieval miss different
things: exact codes and numbers versus paraphrase ([Denser, hybrid search for
RAG](https://denser.ai/blog/hybrid-search-for-rag/); [Supermemory, hybrid search
guide](https://supermemory.ai/blog/hybrid-search-guide/); both reviewed 6 October 2026).

```python
hits = search_hybrid(conn, query, k=4, embed=embed, unit_vectors=vectors)
```

`embed` is any callable returning a vector; `unit_vectors` maps unit IDs to the
vectors computed at index time. A cross-encoder reranker over the fused top
candidates is optional and is measured on the gold set like any other change.

## Emit retrieval sufficiency as a stage output

The retrieval stage returns, per issue, the operative units found with their
page spans or the literal value `none_found`, plus the references it could not
resolve, the queries it ran and whether the second round ran. This report is the
coverage output the reconciliation and drafting stages receive, so drafting can
decline an issue or attach an explicit unresolved reference instead of reasoning
from memory.

```python
problems = sufficiency_problems(report)
# ["splay: unresolved reference Appendix Z", "noise: none_found",
#  "parking: truncated search without a second round"]
```

An empty problem list is the admission condition for drafting. A non-empty list
is data for the next stage, not a reason to raise `k` on the spot.

## Measure recall on a gold set before drafting

For each development case, record the operative units a competent reviewer
would cite. Keep that gold set with the evaluator, never in retriever or model
input. Run the retriever and score recall per question before any drafting
work, and again after every retrieval change:

```bash
"$PYTHON" "$SKILL_DIR/scripts/local_retrieval.py" --k 4
"$PYTHON" "$SKILL_DIR/scripts/local_retrieval.py" --k 4 \
  --issues '["visibility splay for a gate on a classified road"]'
"$PYTHON" -m pytest "$SKILL_DIR/tests/test_local_retrieval.py" -q -p no:cacheprovider
```

Set `PYTHON` to an interpreter whose SQLite includes FTS5 and `SKILL_DIR` to
this installed skill. The first command retrieves the fixture's own questions
and prints the sufficiency report, problems, recall, precision and the listed
irrelevant hits; exit 1 means invalid input. Raising `k`, the page cap or the
call budget requires this measurement to show the current bounds caused a miss,
consistent with the coverage pack.

Measure precision and the hand-listed irrelevant units beside recall, because
recall alone hides ranking noise that fills the drafting context with off-topic
policy. A reranker or a tighter query is judged on both numbers, and an
irrelevant hit is reported, never counted as a sufficiency failure. The fixture
itself shows the gap: recall is 1.0 on every question, while the splay question
at `k=4` also returns the parking policy and the SPD cover unit as irrelevant
hits, so that 1.0 is not a clean ranking.

## Maintainer test

Given a case whose Local Plan policy cites an SPD table, the retriever must
return the SPD table or record an explicit unresolved reference. Four truncated
searches with no second round must fail the acceptance case; the fixture test
`test_four_truncated_searches_without_a_second_round_fail` encodes that
observation shape.

## Completion

Retrieval work is complete when units carry page spans, named references are
resolved in code, one bounded second round exists with a declared budget, the
sufficiency report reaches the next stage, and gold-set recall is recorded for
the development cases before and after the change. Recall on the synthetic
fixture establishes the mechanism only; the target corpus needs its own gold set.
