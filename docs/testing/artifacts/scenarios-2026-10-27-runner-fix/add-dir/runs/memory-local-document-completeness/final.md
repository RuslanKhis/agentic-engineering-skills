I added offline controls for the retriever's missing-evidence cases, but I haven't run them. Bash is disabled in this session, so none of the expected results below are confirmed.

**What I did**
- **Files read:** the workspace `document-coverage.json`, the skill's `local-document-coverage.md` and its `score_document_coverage.py`.
- **New file:** `workspace/coverage_controls.py` builds adapter-style observations from the fixture and scores each one with the skill's scorer. It checks the pass/fail result, document coverage, section coverage and the exact set of (segment, diagnosis) pairs. It uses only the standard library. Expected sections stay in the fixture's `questions` block, so the retriever never sees them.

**Controls, with the expected result for each**

| Control | Expected result |
| --- | --- |
| Complete text (honest control) | Pass, 2/2 documents, 3/3 sections |
| Main policy only | Fail, 1/2 documents; the supplement is a `query_miss` |
| Contents only | Fail; the contents hit counts as a document hit only, 0/3 sections |
| Table, continuation page never returned | Fail; `query_miss` |
| Table, continuation extraction cut short | Fail; `section_truncation` |
| Supplement extracted as empty text | Fail; `empty_extraction` |
| Supplement missing from the corpus | Fail; `absent_content` |
| Empty image page | Fail; `empty_extraction` and `unviewed_visuals` |
| Image page with a claimed review | Still unresolved |

To run it: `python3 -I coverage_controls.py <skill>/scripts/score_document_coverage.py`.

**Diagnosis**
I couldn't diagnose your actual retriever. No retriever code, query trace or extraction output exists in the workspace, only the fixture. The controls show what each failure would look like in your retained observations. Your real misses still need to be classified from those observations.

**Assumptions and open questions**
- Which retriever adapter and extractor should be recorded? I assumed none are available here, so the controls only cover the scoring side.
- I used `manual_golden` as the query origin, so nothing here counts as evidence of how the agent formulates queries.
- I read the fixture's expected sections as authoritative. They haven't had independent domain review.

**Left undone**
- Running the controls, and any fixes if one of them fails.
- Running your real extractor and agent query adapter on representative documents.
- Reviewing the closure notice's image. The fixture has no image bytes, so the Route Cedar closure question stays unresolved.
- Checking whether your retrieval limits caused any miss. I changed no limits or output bounds.
- The skill's `tests/test_document_coverage.py` is referenced in its documentation but is not in the skill directory.