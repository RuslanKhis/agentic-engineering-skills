I wrote the checks but couldn't run them. Bash is disabled in this session, so nothing here has been executed, and I haven't diagnosed your real retriever.

**What I added**

`coverage_checks/run_controls.py` is stdlib-only and offline. It loads the skill's scorer, `document-coverage.json` and `local_retrieval.py`.

- **Controls:** it builds ten adapter-style observations from the fixture. For each, it compares the scorer's diagnoses and pass/fail against expectations held in the grader script, not the retriever.
  - **Passing controls:** an honest complete-text control for `maintenance-route`, and one for `complete-table`.
  - **Failing controls:** main-policy-only, main available but the exception not returned, contents-only, first table page only, truncated table extraction, empty text page, empty image page, and an image page with a claimed review.
- **Contents-only check:** it also asserts that this case gets document credit but zero section credit, so a contents hit can't count as operative evidence.
- **Retriever replay:** it runs the fixture's page text through the existing chunking, screening and FTS5 search at their default limits, then scores what came back. The retriever never sees sections or questions. Limits are unchanged.
- **Exit codes:** 0 when every control behaves as expected, 1 when one doesn't, 2 on unreadable input.

**Predictions, from tracing the scorer by hand**

| Control | Predicted diagnosis |
| --- | --- |
| Main-policy-only | `absent_content` for the S1 exception |
| Contents-only | `query_miss` on all four segments |
| First table page only | `query_miss` on the continuation |
| Truncated table | `section_truncation` |
| Empty image page | `empty_extraction` and `unviewed_visuals` |
| Image page with a claimed review | `unviewed_visuals` only |

I expect the retriever replay to expose a real weakness. In `local_retrieval.py`, `DEFAULT_HEADING` treats a whole single-line page such as "Table 1. … Continued on page 4." as a heading with empty body text. I haven't observed what happens downstream.

**Assumptions**
- I assumed the workspace `document-coverage.json` matches the skill's copy, since both have 47 lines. The script uses the skill's copy.
- The replay's `query_origin` is `fixture_question_replay`, so it isn't agent evidence.
- I used the fixture's question text as the query. No agent trace was available.

**Left undone**
- Running the script. Start with `python3 -I coverage_checks/run_controls.py`.
- Any real extractor, real PDFs, visual review or agent query traces. The image-only case stays unresolved by design.
- Any fix to the retriever. I made no changes until the replay confirms a miss.
- The `tests/test_document_coverage.py` file that the reference doc mentions isn't in the workspace.