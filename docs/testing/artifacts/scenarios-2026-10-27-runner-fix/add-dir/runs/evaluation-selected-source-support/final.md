I judged all 17 cases and wrote the judgments to `workspace/source-judgments.json`, with a rationale for each. I did not run the scorer, because the expected labels are held back and I made no external calls. The judgments are my own reading of the cases and the rubric.

**Judgments (only `supported` counts as accepted)**

| Case | Source identity | Span completeness | Applicability | Contrary evidence | Support |
|---|---|---|---|---|---|
| s01, s02, s04, s06, s08, s10 | valid | complete | applicable | none | supported |
| s03 | valid | incomplete | applicable | none | unsupported |
| s05 | valid | incomplete | applicable | none | unsupported |
| s07 | valid | complete | applicable | contradiction | contradicted |
| s09, s15 | valid | complete | not_applicable | none | unsupported |
| s11 | valid | complete | applicable | contradiction | contradicted |
| s12 | valid | complete | applicable | contradiction | contradicted |
| s13 | valid | complete | applicable | none | unsupported |
| s14 | valid | complete | applicable | unresolved | unresolved |
| s16, s17 | invalid | unresolved | unresolved | none | unsupported |

- **s03 vs s04:** both cite the access form, but s03 selects only the question and leaves out the answer on the next line.
- **s09, s15:** the quotes are genuine and complete, but they cover a different field (colour, applicant name).
- **s07:** the exception is inside the selected passage, so "without exception" is contradicted.
- **s14:** the two meter records conflict and neither has precedence, so the support is unresolved.

**Questions I could not ask, and the assumptions I used**
1. **Invalid citations (s16, s17):** should the other dimensions assess the supplied text or only authenticated evidence? I assumed only authenticated evidence, so completeness and applicability are `unresolved` and support is `unsupported`. If the supplied text is meant to be assessed, s16 and s17 would show `complete` and `applicable` for completeness and applicability.
2. **Pixel claim (s11):** is the claim "contradicted" or just "unsupported"? I chose contradicted, because the cited "not to scale" text directly negates the claim that pixels establish a width. Unsupported with contrary evidence `none` is the other defensible reading. Either way the observation is rejected.
3. **s05:** the quote omits the rolled-mat exception, and the observation only restates the general rule. I chose `none` for contrary evidence. A reviewer could reasonably choose `contradiction` instead.

**Left undone**
- No scorer run, so there are no agreement figures.
- No human review. The skill says these case labels are provisional and AI-authored, so they should not be used as a quality gate without human review.