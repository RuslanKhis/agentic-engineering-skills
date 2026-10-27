I judged all 17 cases on the five dimensions and wrote them, each with a rationale, to `.adk-evidence/source-judgments.json`. I did not run the scorer, because the expectations file is held back. I also didn't validate the JSON shape with a script.

**Supported (6):** h02, h04, h05, h08, h11, h13.

**Not supported:**
- **Unsupported (6):**
  - h01: the quote is only the form question, not the answer.
  - h09: the log field reads "[not recorded]".
  - h10 and h17: the quote is real but about a different field.
  - h06 and h16: the cited source ID is wrong or doesn't resolve, so `source_identity` is invalid.
- **Contradicted (4):**
  - h03: the log says 62 C, not 58 C.
  - h07: the selected sentence leaves out the temporary event notice exception, which applies to this party.
  - h12: the sketch is "not to scale" and no pixel scale is given.
  - h15: "without exception" is wrong because the quoted rule includes an exception.
- **Unresolved (1):** h14, where the two boiler records conflict and neither has precedence.

**Questions I couldn't ask, and the assumptions I used:**
1. **Invalid citations (h06, h16):** I assessed the other dimensions on the text as supplied and set `support` to unsupported, since the citation can't be authenticated.
2. **h12:** I treated the claim as "the pixel line establishes 4.5 m", which is a method claim and so contradicted. The other reading is unsupported with `contrary_evidence` none. I'm least sure of this one.
3. **h07:** I marked it applicable, because it is the right rule, but incomplete, because the exception was dropped.

**Left undone:**
- No scoring against the expectations.
- No second rater or human review.
- Everything was judged from the case pack and the sketch only, with no external calls.