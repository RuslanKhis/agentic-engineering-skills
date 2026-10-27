I judged all 17 cases and saved the judgments, each with a rationale, to `.adk-evidence/source-judgments.json`. I didn't run the scorer, so nothing has been checked against the expectations. I made no network calls and read no expectations or scorer files.

| Case | Judgment | Why |
|---|---|---|
| s01, s02, s04, s06, s08, s10 | supported | The selection is complete and on point. s02 is a valid paraphrase. s04 includes the answer. s06 includes the exception. s10 asks only for the written width. |
| s03 | unsupported | Only the form question is quoted, not the answer. |
| s05 | unsupported | The selection leaves out the rolled-mat exception, which is this case's situation. |
| s07 | contradicted | The selected passage contains the exception, which contradicts "without exception". |
| s09, s15 | unsupported | The quote is valid and complete but about something else (colour, applicant name). Applicability is `not_applicable`. |
| s11 | contradicted | "Not to scale" and a null scale mean the pixels can't establish 3.2 m. |
| s12 | contradicted | The selected record says 12 litres and the observation says 15. |
| s13 | unsupported | The reading field is blank. |
| s14 | unresolved | Two equally authoritative records disagree (12 and 15 litres). |
| s16 | unsupported | The `missing-p1` ID doesn't resolve to any source. |
| s17 | unsupported | `roof-p1` resolves, but the quoted text isn't on that page. |

**Questions I couldn't ask, and the assumptions I used**
- **Invalid citations (s16, s17):** Should the other dimensions judge the supplied text or only authenticated evidence? I used authenticated evidence only. So `span_completeness` is `unresolved`, `contrary_evidence` is `none`, and support is `unsupported`. For s17 I set applicability to `not_applicable`, because the real `roof-p1` content is about the roof.
- **Pixel claim (s11):** Is this an unsupported value or a contradicted method claim? I treated it as a contradicted method claim. The alternative (`none` / `unsupported`) is noted in the rationale.
- **Omitted exception (s05):** Is this unsupported or contradicted? The observation is a verbatim statement of the general rule, so I chose `unsupported` and noted the stricter alternative in the rationale.

These three choices are the ones most likely to disagree with the expectations. Review the convention rather than rerunning the judge until it agrees.

**Left undone**
- I didn't run `scripts/check_source_support.py --judgments .adk-evidence/source-judgments.json`. That step should happen after this judging pass.
- No human domain review was done. The reference says the bundled expectations are provisional, so any disagreement still needs human review.