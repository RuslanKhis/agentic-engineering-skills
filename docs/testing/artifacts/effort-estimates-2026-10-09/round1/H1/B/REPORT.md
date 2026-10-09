# Report: HR policy Q&A proof-of-concept design session

Date: 2026-10-09. This was a design-only session. No code was implemented, and
no network, cloud or install commands were run.

## 1. Skills invoked and reference files opened, in order

Only one skill was invoked: `adk-system-designer`, through `/adk-system-designer`.
No other skill was loaded with the Skill tool. I opened files from sibling
skills only where the designer skill pointed to them.

These are the files I opened, in order:

1. `.claude/skills/adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md` (whole file)
3. `adk-system-designer/references/design-decisions.md` (whole file)
4. `adk-system-designer/references/failure-review.md` (whole file)
5. `adk-system-designer/references/implementation-handoff.md` (whole file)
6. `adk-system-designer/references/gcp-decisions.md` (whole file)
7. `adk-system-designer/assets/ticket-template.md` (whole file)
8. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (whole file; SKILL.md:199 points to it)
9. `adk-model-and-output-contracts/references/compatibility.md` (lines 1–40; SKILL.md:195 points to it)
10. `adk-memory-architecture/references/compatibility.md` (grep for version lines only)
11. `adk-memory-architecture/references/local-document-coverage.md` (lines 1–80)
12. `adk-memory-architecture/references/retrieval-strategy.md` (lines 1–60)
13. `adk-memory-architecture/scripts/local_retrieval.py` (function list only, via grep)
14. `adk-system-designer/references/runtime-and-delivery.md` (lines 1–40, the context-size section)
15. `adk-system-designer/assets/implementation-plan-template.md` (whole file)

I did not open `assets/system-design-template.md`, because the compact form in
`delivery-profiles.md:193-215` replaces it for a proof of concept.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer | Depends on it |
| --- | --- | --- | --- |
| 1 | Which Friday is the demo? Today, 2026-10-09, is a Friday. | Friday 2026-10-16 | Whole plan; open decision O2 |
| 2 | Is the code kept after the demo? | Yes, if the demo goes well | Paths are configured rather than hard-coded; phase 2 is written |
| 3 | How familiar are you with ADK and GCP? | New to ADK; no GCP project setup | Estimates use the ×1.5 new-to-ADK rate; Gemini API key rather than Vertex (D4) |
| 4 | Are the 6 hours two focused blocks or interrupted time? | Two dedicated blocks, so a focus factor of 0.8 | Capacity of 3.6 h after reserve, and the cut line |
| 5 | What can you spend on models? | Under USD 20, on a paid-tier key | Choice of model tier; spend stop |
| 6 | How will leadership see it? | Live `adk web` on your screen, plus a results table | No hosting or login in phase 1 (D5) |
| 7 | Do the PDFs contain employee personal data? | No, only policies | Sensitive-data controls deferred |
| 8 | May internal HR policies be sent to the Gemini API or Vertex AI? | Yes, on a paid tier. This is still an open decision (O1) because it blocks the demo | D4; G02 cannot start until it is settled |
| 9 | Are any PDFs scanned images? | Unknown. G01 measures it (O3) | D3; OCR moved to phase 2 (P2-4) |
| 10 | Are all 30 PDFs the current versions? | Yes | Correctness of cited answers |
| 11 | Should the agent refuse uncovered questions or answer from general knowledge? | Refuse with "not covered, contact HR" | D1; G03's two uncovered cases |
| 12 | Gemini API or Vertex AI? | Gemini API with a key; Vertex costs about 0.5–1 h more if IT requires it | D4; G02 estimate |
| 13 | Is the cut line acceptable? (G03 shrinks to 6 questions if work runs high) | Accepted provisionally | Phase 1 scope |

## 3. Files written or changed, and what was not finished

All of these are new, untracked and uncommitted:

- `docs/architecture/hr-policy-qa.md`: the design and plan in compact proof-of-concept
  form. It is marked **draft**.
- `docs/tickets/hr-policy-qa/G01-extract-policies.md`
- `docs/tickets/hr-policy-qa/G02-agent-answers.md`
- `docs/tickets/hr-policy-qa/G03-checked-questions.md`
- `REPORT.md`, this file.

These parts are not finished:

- There is no implementation, as requested.
- The design document is about 1,780 words. The compact-form target is about
  1,200 (SKILL.md:84, delivery-profiles.md:195). I trimmed it once, but did not
  cut it further.
- Phase 2 goals are in the plan only, with no tickets. The instructions asked for
  tickets for phase 1 only.
- Some decisions stay provisional on O1, O2 and O3.
- Provider facts are not verified: Gemini paid-tier data-use terms, prices and
  quotas. They could not be checked offline. The model lifecycle facts come only
  from the skill's snapshot, checked on 2026-10-08.

## 4. Checks run, and checks not run

These checks were run:

- **Word counts** (`wc -w`): design 1,778 words; tickets 416–533 words each.
- **Estimate consistency**: phase 1 is G01 0.5–1.0 + G02 1.0–1.5 + G03 1.0–1.5
  = 2.5–4.0 h, which matches the plan table. In each ticket, hands-on plus
  review adds up to that ticket's total. Each ticket's total equals its goal's
  estimate in the plan. Result: consistent.
- **Relative links**: the `design:` path in each ticket resolves to the design
  file. Result: OK.
- **`git status`**: only `docs/` is untracked before this report. Result: OK.

These checks were not run:

- No tests. No code exists, and `google-adk` and `pypdf` are not installed, so
  any test importing `google.adk` could not run here.
- No live model calls and no `adk web`.
- No checks of provider documents or prices, because network access was not
  allowed.
- The bundled tests in `adk-memory-architecture/tests/` were not run. They are
  not part of this design's evidence.

## 5. Friction log

**Unsure: which focus factor to use.**
`delivery-profiles.md:153-155` gives 0.6 for part-time or interrupted work and
0.8 for a dedicated block. "About 6 hours spread over two days" fits either
reading. I chose 0.8 and recorded it as assumption 4. With 0.6, capacity would
be 2.7 h after reserve, and even the low end of phase 1 (2.5 h) would be tight.

**Unsure: the estimate table made phase 1 impossible as first designed.**
`delivery-profiles.md:131` gives retrieval over a small document set as 3–6 h.
`delivery-profiles.md:138` multiplies that by 1.5 for a team new to ADK, which
gives 4.5–9 h. That exceeds the whole capacity. This was genuinely helpful: it
pushed me to D2 (whole-document reads from a catalogue, with no index), and that
change made phase 1 fit. My G01–G03 ranges are below what the table implies,
which I justified by the small corpus and the absence of a search index. A
reviewer may still disagree with that judgement.

**Unsure: the cut line when only the low end fits.**
`delivery-profiles.md:161-163` says that when only the low end fits, I should
say so and name what moves. I did that. However, the rule says phase 1 "fits"
only when the high end fits, so it is unclear whether a plan where only the low
end fits is acceptable to hand over.

**Unsure: an assumed-answers table, or answers folded into the scope gate?**
`SKILL.md:122` asks for an **Assumed answers** table at the top.
`delivery-profiles.md:201-202` (compact form) folds the assumed answers into the
scope-gate table, one line each. I followed the compact form and marked each
answer U or A. The full list of questions is in this report.

**Unsure: where the plan goes, and what `plan:` points to.**
`SKILL.md:246` says a small effort can keep its plan in the design. The ticket
template's `plan:` field (`ticket-template.md:5`) and the handoff examples
(`SKILL.md:278`, `implementation-handoff.md:105`) assume a separate
`docs/plans/<topic>.md`. I pointed `plan:` at the design's §5 anchor.

**Unsure: which run prompt to give.**
`SKILL.md:278` shows the plan-style prompt (`Carry out G01 from
docs/plans/...`). `ticket-template.md:53-57` gives a ticket-style prompt. I used
the ticket prompt because no separate plan file exists.

**Heavier than needed: reading all of design-decisions.md.**
`design-decisions.md` is 343 lines, and most of it covers writes, OAuth, approvals,
SQL and budgets that a read-only proof of concept does not touch. `SKILL.md:97`
says "Every design reads" it "for the sections its journey touches". Since it is
one file, I read all of it. Only lines 26-61 (proportionality), 126-147 (RAG),
182-196 (the trifecta) and 296-313 (pinning and structured output) were used.

**Heavier than needed: the 1,200-word target.**
`SKILL.md:84` and `delivery-profiles.md:195` set about 1,200 words. Six decision
rows in four columns, a depth table, three goals, phase 2 and the later list
together came to about 1,800 words even after trimming. The target felt tight
for the required sections, `delivery-profiles.md:201-212`.

**Heavier than needed: the failure review.**
`failure-review.md` has a scenario table with 20 rows. For a single-user,
read-only demo, only three rows applied. `failure-review.md:4-5` ("give a
reason for cases that do not apply; do not invent write machinery") and
`delivery-profiles.md:214-215` permitted a short table, which helped.

**Genuinely helpful: the model lifecycle table.**
`SKILL.md:197-201` sends me to the lifecycle table
(`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:21-23`).
It showed that `gemini-2.5-*` retires on Vertex on 2026-10-20, four days after
the demo. Without the table I might have chosen that model from memory.

**Genuinely helpful: the floor list.**
`delivery-profiles.md:70-86` gave a concrete floor list. Its note on `adk web`
("put the cap on the model project instead", lines 79-80) settled the spend
stop for a host I do not configure.

**Genuinely helpful: a phase 2 retrieval path that already exists.**
`adk-memory-architecture/references/retrieval-strategy.md:11-14` and
`scripts/local_retrieval.py` give a ready local FTS5 path for phase 2 (P2-1).
That gave a credible phase 2 without designing an index now.

**Genuinely helpful: the ADK version assumption.**
`SKILL.md:193-197` (record the specialists' ADK version and confirm it in the
first goal) gave a clean answer to "which ADK version" without network access.
I used 2.8.0, from `adk-model-and-output-contracts/references/compatibility.md:3`.

**Unsure: which goal confirms the ADK version.**
`SKILL.md:196-197` asks for "confirm against the chosen pin" as an acceptance
item of the *first* implementation goal. Here, the first goal (G01, PDF
extraction) does not use ADK. I put the check in G02's acceptance instead.

**Unclear trigger: when to read runtime-and-delivery.md.**
`SKILL.md:180-184` says to read it "when requirements depend on context limits".
D2 does depend on context size, so I read the first section. It added little
for a read-only local demo, and the trigger was borderline.

## 6. Next prompt the skills told the user to type

The design document ends with this prompt, and so does the G01 ticket's "Run this
ticket" block. Its form comes from `ticket-template.md:53-57`, as directed by
`SKILL.md:268-283`:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-policies.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
