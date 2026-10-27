I judged all 17 cases and saved the judgments, with a rationale for each, to `source-judgments.json` in the workspace. I didn't run `check_source_support.py`. The expectations are held back, and the task said no external calls.

**Judgments (support label)**
- **Supported:** s01, s02, s04, s06, s08 and s10. The selected span states the answer and contains its qualifiers.
- **Unsupported:** these have no stated answer.
  - s03: the quote is only the form question.
  - s09 and s15: valid but unrelated fields.
  - s13: the field is blank.
  - s16 and s17: the citation is invalid.
- **Contradicted:**
  - s05: the selection omits the exception.
  - s07: it claims "without exception" when the passage contains one.
  - s11: the claim is that pixels establish a width on a sketch marked "not to scale".
  - s12: the selected record says 12 litres, not 15.
- **Unresolved:** s14, where two equally authoritative meter records conflict.

**Assumptions** (nobody was available to answer, so I proceeded on these)
1. For invalid citations (s16, s17), I scored the secondary dimensions on the supplied text as if it were authentic. Support is still never "supported". The alternative is to mark those dimensions "unresolved".
2. For s11, I read the claim as one that a measurement method is valid, which the "not to scale" note contradicts. The other reading is "unsupported" with no contrary evidence.
3. For s05, I treated the application to the 3 m rolled mat as contradicted by the exception on the same page. The sentence is literally true as a general rule, so "unsupported" is also defensible.
4. I used the full cited page only to expose incomplete selections. For s12 I did not use `meter-copy-p1`, because it isn't listed as case evidence.

I didn't have the diagram rendered. I read the SVG source, which shows only the written width, the unscaled line and the "not to scale" note.