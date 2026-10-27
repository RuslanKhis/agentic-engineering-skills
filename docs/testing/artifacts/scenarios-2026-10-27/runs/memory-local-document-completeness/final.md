I added offline checks that expose the missing-evidence cases, but I haven't run anything. Bash was disabled for the whole session, so neither the new tests nor the retriever probe has been executed.

**What I added** (in `coverage_checks/`; I changed nothing in the skill or the fixture)
- **`test_coverage_controls.py`** uses the skill's `document-coverage.json` and `score_document_coverage.py`. Its observations are authored adapter records, not real retriever output. I checked each expected result by reading the scorer, and the cases are:
  - **Complete-text control:** passes with document coverage 2/2 and section coverage 3/3.
  - **Main-policy only:** the supplement exception is a `query_miss`, with document coverage 1/2.
  - **Main-policy only, supplement missing from the corpus:** reported as `absent_content`.
  - **Contents-only hit:** counts as a document hit, with 0/3 sections.
  - **Incomplete table:** first page only gives a `query_miss`. A truncated continuation gives `section_truncation`, whether the cut is in the returned passage or in the extraction.
  - **Empty text page:** `empty_extraction`.
  - **Empty image page:** `empty_extraction` plus `unviewed_visuals`.
  - **Claimed visual review:** a claim of review, or a hit on the image page, cannot resolve the image page.
  - **Hit text not in the extraction:** invalid.
  - **Irrelevant neighbours:** don't raise coverage.
  - **Manual or empty-query runs:** don't count as agent evidence.
  - **Expected sections:** stay on the grader side.
- **`probe_retriever.py`** runs the unchanged `local_retrieval.py` with its default `k=4` and default call budget over the fixture pages. It prints which units the real retriever returns per question.

To run them from the workspace root:
- Tests: `python3 -I -m unittest discover -s coverage_checks -p 'test_*.py'`
- Probe: `python3 -I coverage_checks/probe_retriever.py .claude/skills/adk-memory-architecture/scripts .claude/skills/adk-memory-architecture/assets/document-coverage.json`

**Diagnosis**
I couldn't diagnose your actual retriever from retained observations, because none were available to read. The probe is how to get them. The `Table 1…` page lines also match the retriever's heading pattern, so those pages may chunk into heading-only units. Check that first when you run the probe.

**Assumptions** (no one to ask)
- Q: Is the root `document-coverage.json` the same as the skill's asset copy? I assumed so and didn't compare them. The tests use the asset copy.
- Q: Should limits change? I assumed no. I changed no limits, and nothing here shows that the limits caused a miss.

**Left undone**
- Running anything, including the tests and the probe.
- Real PDF extraction.
- Visual review. The image-only case stays unresolved by design.
- Any check of the agent's actual query traces.
- The skill's referenced `tests/test_document_coverage.py` doesn't exist in the skill folder.