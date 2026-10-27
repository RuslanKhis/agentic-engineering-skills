I added a checker and tests, but I couldn't run either, because Bash is disabled in this session. Nothing is verified, and I haven't diagnosed your retriever. Any failure in the code or the tests is still undiscovered.

**What was missing from the workspace**
- `document-coverage.json` holds only extracted segments and questions. It has no retained query or hit observations, and there's no retriever code of yours in the directory.
- So I built an offline stand-in. It runs the skill's own FTS5 lexical retriever over your segments, using only the question text. `required_sections` stays evaluator-side.
- This stand-in is not your actual retriever. Its results show how this fixture behaves. They don't show why your retriever misses answers.

**Files added** (nothing existing was edited)
- `tools/check_coverage.py` does two things:
  - It runs the retriever per question at the existing k=4. It then scores the result with the skill's `score_document_coverage.score`, which reports document coverage, operative-section coverage and per-segment diagnoses.
  - It runs a preflight on the inventory, before any query. This flags empty extractions and visual-required pages with no asset. It also flags a table continuation whose page is missing, and a referenced Supplement or Notice that isn't in the inventory.
  - It exits 1 on any missing evidence.
- `tools/test_check_coverage.py` covers six cases:
  - complete spans pass;
  - a main-document-only result fails the supplement question;
  - a partial table fails;
  - a contents-only hit fails;
  - an empty extraction is diagnosed as `empty_extraction`, not `query_miss`;
  - the unviewed visual stays unresolved.

**What I expect from reading the fixture** (a prediction, not a result)
- `closure-status` can never pass. `closure-notice` has an empty extraction and no image, so it's `empty_extraction` plus `unviewed_visuals`.
- `maintenance-route` is where the lexical `query_miss` risk lies. It needs `route-rule`, both table pages and the S1 exception, and k=4 leaves little room for them.

**Questions I couldn't ask, and the assumptions I used**
- Where are your real query and hit logs, and the adapter that records them? I assumed they aren't available, so I used question text as the query and labelled it `manual_golden`. That is not evidence of what your agent actually asks.
- What are the "output limits"? I assumed k=4 and no character cap. `--max-chars` is available to test a cap.

**Left undone**
- Running the checker and the tests. To do that, run `python3 -I tools/check_coverage.py --fixture document-coverage.json` and `python3 -m pytest tools -q -p no:cacheprovider`.
- Diagnosing your real retriever from its own observations.
- Real PDF extraction and visual review of the closure notice. The notice stays unresolved evidence until an authorised image is reviewed.