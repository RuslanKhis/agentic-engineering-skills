# run-0412: are documents being cut up or lost?

Evidence tier: **offline, hand-traced** from saved files (extract/records.jsonl, the four
run-0412 envelopes, review_app/grouping.py). Bash was unavailable, so nothing was executed:
`analysis/audit_run.py` is written but **not run**, and the unit tests were **not run**.
No model calls, no network, no changes to app code. The PDFs and page images were not
available, so nothing here is checked against the source documents.

Answer: yes, both. The extract looks intact (52 records, matches manifest). The damage is
in the pack (retrieval) and, mostly, in `review_app/grouping.py`.

## Findings (each traced against the saved group envelope)

| # | Where | What happens | Effect in run-0412 |
|---|-------|--------------|--------------------|
| 1 | grouping `unit_key` | Key is `document:label`; labels `(a)`/`(b)` repeat under 4.2 and 4.3 and ignore `clause_path`. | 4.2(a)+4.3(a) merged into `DMP:(a)`; 4.2(b)+4.3(b) merged into `DMP:(b)`. Reviewer: "contains two provisions". |
| 2 | grouping `continues` branch | Continuation is appended to `last_key` (whatever unit came before in score order), not to the record named in `continues`. | r006 (4.2(b) tail, Conservation Area 2.5 m) went onto `DMP:(a)` because r008 preceded it. `DMP:(b)` ends "except where". Its `record_ids` omit r006, and pages get a duplicate (`[14,15,15]`). |
| 3 | grouping `seen_cells` | Table cells de-duplicated on `(table_id, text)`, so equal values in different rows/columns vanish. | 7 of 26 cells dropped: r026, r027, r028, r031, r032, r033, r035. r035 is the 500–800 m² footprint "30 m2". `row`/`col` are never rendered, so the text is a flat run with no row structure. |
| 4 | grouping `split_unit` | Fixed 160-char cut, ignoring words, numbers and record boundaries. Each part copies the whole unit's `record_ids` and `pages`. | `eave|s`, `35|0 to 500 m2`. No part can be traced to the record or page it holds. |
| 5 | grouping `SKIP_KINDS` | Footnotes and page images dropped silently. | r006 ends "2.5 m.7" with footnote 7 (r011) absent; r052 (Inset 3 map, `unreviewed`) is not surfaced as unresolved. |
| 6 | pack order | Pack is in score order, not document order, which is what makes 2 harmful. | — |
| 7 | retrieval pack | 35 ids returned though `top_k` is 40. Never selected: r007, r010, r011 and r039–r052 (all of page 17: table continuation, rows 800–1200 and over 1200, notes a/b, and the page-18 image). | The 900 m² plot's row (r040–r044) never reached the writer. |

Why the reviewer's three complaints happen: depth = #1; eaves = #2 (and #4); outbuilding =
#3, #4 and #7.

## Consequence for the answer (from the extract records, unverified against the PDF)

- Eaves: site is in a Conservation Area, r006 gives 2.5 m, proposal is 2.9 m. The writer
  said "within 3 m", so the finding is probably wrong.
- Outbuilding: 900 m² falls in the 800–1200 m² row, 40 m² footprint (r041), note a only.
  The writer used 30 m² and said 36 m² exceeds it; probably wrong. Note a (not living
  accommodation) is not answerable from the question.
- Depth 3.8 m vs 4 m looks fine, but it cited a unit mixing 4.2(a) and 4.3(a).
- The reviewer was right to reject. Do not read these corrections as a passed review;
  no re-run is authorised.

## Remedies (not implemented; audit only) and tests to add

1. Key units by `(document, tuple(clause_path))`. Test: 4.2(a) and 4.3(a) give different units.
2. Resolve continuations through `continues`/`continued_by` record IDs, independent of pack
   order, and append the record ID and page. Test: pack order r005, r008, r006 keeps r006 in 4.2(b).
3. Drop the cell de-dup; render tables by row/col with headers (and continuation rows). Test: the
   500–800 row keeps its "30 m2".
4. Split only at record boundaries; if a record exceeds the budget, split at whitespace and keep
   per-part `record_ids`/`pages`. Test: concatenated parts equal the source text, no word cut.
5. Surface skipped footnotes (linked by `footnote_refs`) and unreviewed page images as
   explicit "unresolved evidence" units, not silent drops.
6. Retrieval: expand a hit to its table's continuation (`continued_by`) and referenced footnotes;
   sort the pack into document order; investigate why 35 < top_k.
7. Add a coverage check at the group stage: every pack record is either in a unit's
   `record_ids` or listed as skipped with a reason; fail loudly otherwise. The existing tests
   cover only the happy path (one continuation in pack order, no collisions, no tables).

## Questions I could not ask, and assumptions I proceeded on

- Is `MAX_UNIT_CHARS = 160` a real writer per-source budget? Assumed unknown; storage has no
  size limit and reopens full-size envelopes, so the envelope store is not a reason to split.
- Is 35 < top_k=40 deliberate (score threshold)? Assumed unexplained.
- Extraction fidelity (e.g. fused "m.7" marker, table row 4/5 boundaries) cannot be verified
  without the PDFs; page 18 Inset 3 stays unresolved, not assumed.
