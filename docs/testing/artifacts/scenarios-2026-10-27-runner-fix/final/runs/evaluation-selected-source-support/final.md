I judged all 17 cases and wrote them to `.adk-evidence/source-judgments.json`. I didn't run the scorer because the expectations file is held back. I also didn't check the file against the scorer's validator, so its format is untested.

**Judgments**
- **Supported (6):** s01, s02, s04, s06, s08, s10.
  - s02 is a faithful paraphrase of the Monday 09:00 opening.
  - s04 and s06 are supported because the selection keeps the answer or the exception.
- **Unsupported (7):** s03, s05, s09, s13, s15, s16, s17.
  - s03: question only, no answer line.
  - s05: stops before the exception that governs a rolled flexible mat.
  - s09 and s15: valid, complete spans about something else (colour, applicant name).
  - s13: blank field, and missing evidence is not contradiction.
  - s16 and s17: citation identity fails.
- **Contradicted (3):** s07, s11, s12.
  - s07: "without exception" against an explicit exception.
  - s11: pixels against "not to scale".
  - s12: 12 litres against 15 litres.
- **Unresolved (1):** s14, two equally authoritative meter records that disagree.

**Assumptions** (no one was available to ask, so I proceeded on these)
- **s16 and s17 (invalid citations):** I assessed the secondary dimensions on authenticated evidence only, not on the supplied text. That gives `unresolved` for completeness, and `unresolved` applicability for s16 and `not_applicable` for s17. A rubric that scores the supplied text would label these differently.
- **s11:** I labelled the claim that the pixels establish 3.2 m as contradicted, not merely unsupported. It is a claim about a measurement method, and the selected "not to scale" note contradicts it.
- **s05:** I labelled it unsupported rather than contradicted. The observation is only the general rule, though that rule is incomplete for this mat.
- I treated the full text of a selected source page as available context, but nothing outside the selected and additional sources.

**Left undone**
- No scoring against expectations, as above.
- No human review of the borderline labels (s05, s11, s16, s17).