I added a set of offline checks that expose missing evidence, but I couldn't run them, because Bash is disabled in this session. The file is `checks/coverage_controls.py`. Its expected results come from reading the scorer by hand, so treat them as unverified until you run `python3 -I checks/coverage_controls.py`.

I did not change the retriever, so its `k`, call budget and output limits are as they were.

**What the checks do**
- They build adapter-style observations from the skill's synthetic fixture (`document-coverage.json`) and score each with the skill's `score_document_coverage.py`.
- The expected diagnoses and coverage counts sit in the check file, on the grader side. The retriever never sees them.
- One honest control (complete text) must pass: the full maintenance route question, and the full two-page table.
- Eight controls must fail with a specific diagnosis:

| Control | Expected result |
| --- | --- |
| Main policy only | `query_miss` on the supplement exception, with 1 of 2 documents covered |
| Supplement not ingested | `absent_content` |
| Contents page only | Counts as a document hit but 0 operative sections, all `query_miss` |
| Table first page only | `query_miss` on the continuation page |
| Table continuation returned but cut short | `section_truncation` |
| Rule page extracted to an empty string | `empty_extraction` |
| Image-only notice page | `empty_extraction` and `unviewed_visuals` |
| Same image page with a claimed "completed" review | Still `empty_extraction` and `unviewed_visuals`, since the text-only pack can't show a real review |

- Every run is marked `manual_golden`, and the checks fail if one is counted as agent evidence.

**Not done**
- Nothing was executed, so there are no pass or fail results to report.
- I did not run the real `local_retrieval.py` against this fixture to record its actual queries and returned passages. Its fixture format is different (`pages` and `questions`), and I couldn't test a conversion. Without that run, the actual cause of the original misses is not diagnosed. The checks only show the scorer can tell each failure kind apart.
- Real PDF extraction and visual review are not exercised, as the fixture allows.
- I did not check that the workspace `document-coverage.json` matches the copy in the skill's `assets` folder. It is the one the checks read by default.

**Questions I couldn't ask, and what I assumed**
- Where should the checks live? I assumed a new `checks/` folder in the workspace, leaving the skill's files untouched.
- Should the retriever's real query trace be captured? I assumed that is a follow-up once someone can run the retriever.