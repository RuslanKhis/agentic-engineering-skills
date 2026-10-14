# Report: advertiser campaign assistant design session

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer` (by the user's slash command). No other
skill was invoked. Specialist files were read only as references.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md` (full)
3. `adk-system-designer/references/design-decisions.md` (full)
4. `adk-system-designer/references/failure-review.md` (full)
5. `adk-system-designer/references/implementation-handoff.md` (full)
6. `adk-system-designer/references/gcp-decisions.md` (full)
7. `adk-system-designer/assets/system-design-template.md` (full)
8. `adk-system-designer/assets/implementation-plan-template.md` (full)
9. `adk-system-designer/assets/plan-review-prompt.md` (full)
10. `adk-system-designer/scripts/check_schedule.py` (lines 1–200, then 222–262 to see how grid citations are matched)
11. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
12. `adk-model-and-output-contracts/references/compatibility.md` (first 40 lines), plus a grep for the ADK version across all `*/references/compatibility.md`
13. `adk-system-designer/references/runtime-and-delivery.md` (first 30 lines only; its triggers did not apply)
14. `safe-api-tool-calls/SKILL.md` (first 80 lines, to check the write and confirmation guidance)
15. `safe-api-tool-calls/references/writes-and-confirmation.md` (grep only)

Not opened: `assets/ticket-template.md`, because no tickets were requested.

## 2. Questions I would have asked, and the answers I assumed

The same rows are in the design's **Assumed answers** table, with the
decisions that depend on each.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | When must the pilot start, and is the code kept afterwards? | End of week 3 (15 working days) is wanted; the date can move by about a week if the plan shows it must; the code is kept |
| Q2 | Who builds it: hours, and familiarity with ADK and GCP? | One engineer, full time, about 6 focused hours a day; knows Python and GCP; new to ADK (1.5× multiplier) |
| Q3 | What is the model and cloud budget? | A small pilot allowance (about USD 300/month or less) in a new GCP project |
| Q4 | Which protocol does the IdP speak, and what identifies an advertiser? | OIDC, with an organisation claim; no brand data in the IdP |
| Q5 | What do owner, brand and channel mean in the rights system, and is there an API? | A record grants a brand the use of an owner's asset on a channel; read REST API; asset descriptions are free text from media owners |
| Q6 | Does booking have read APIs for price and inventory? Is pricing per advertiser? | Yes, read APIs plus a staging environment; prices are advertiser-specific and confidential |
| Q7 | May the assistant create orders directly during the pilot? | Not until replay and status lookup are known. Booking ops enter confirmed requests within one business day |
| Q8 | Who triggers payment and delivery? | Those teams, from the booking system, as today |
| Q9 | Is there an existing frontend? | No; a minimal page is acceptable |
| Q10 | Is there personal or regulated data, residency or retention rules? | Business-confidential data only; IdP email and name; 90-day conversation retention |
| Q11 | Who signs off go-live, and who reconciles orders? | A business owner and the booking-operations lead; booking ops reconcile |

## 3. Files written or changed, and what was not finished

Written:

- `docs/architecture/campaign-assistant.md`: the design (draft). It contains the assumed answers, the journey, depth and deferred controls, invariants I1–I5, decisions D1–D9, model-facing contracts, data and authority, security posture, budgets, both coverage grids, cross-cutting failure scenarios and open decisions.
- `docs/plans/campaign-assistant.md`: the phased plan. It contains the summary, the schedule block (waits W1, W2a, W2b, W3, W4 and goals G01–G15), the implementation map, full entries for phase 1 goals G01–G10, outlines for phase 2 goals G11–G15, the later list, the schedule-change and what-if tables, and the resume prompt.
- `REPORT.md`: this file.

No other files were changed and nothing was committed.

Not finished, or open:

- **The plan does not fit three weeks at the high end.** Go-live lands in 11.67–20.67 working days. The plan states this and recommends committing to 21 working days. The user still has to accept that or choose another remedy.
- Every decision is provisional on Q1–Q11. The design is marked **draft**.
- Model lifecycle, Vertex prices, the ADK pin and service availability were not checked against live sources, because network access was not allowed. G01/A1 and G08/A9 carry these checks.
- No tickets were written (not requested). Phase 2 goals are outlines, as the skill directs.

## 4. Checks run, and checks not run

Run:

- `check_schedule.py` with `/opt/homebrew/bin/python3.12 -I`. The default `python3` is 3.9.13, below the helper's 3.11 floor.
  - First run: exit 1. Every grid citation was reported as missing, because the acceptance items were written inline on one line. After reformatting, the grid check passed.
  - After the first fixes: 45–67 h of 67.5 h, finish 10–14.89 days, exit 0.
  - **Final, after the independent review: phase 1 is 48.5–71.5 h against 67.5 h, finish 11.67–20.67 working days, "low end only", exit 1 at `--days 15`. At `--days 21` it fits, exit 0.** The grid citation check passes, and the phase 2 sum is 27.5–43.5 h.
  - What-ifs were run on copies through stdin (results are in the plan's table). 20 days: no. 21 days: yes. A read-only pilot finishes in 9.56–17.56 days: no. An engineer who knows ADK finishes in 8.78–16.45 days: no. Team commitments on the waits give 11.67–15.89 days: no.
- **Independent plan review** by a subagent with a fresh context, using `assets/plan-review-prompt.md`. It found 8 missing prerequisites, 2 unsupported claims and 9 coverage-grid problems. All were settled in the plan's change table. The biggest effect was turning "fits" into "low end only".

Not run:

- No Python or ADK tests: there is no code yet, and google-adk is not installed.
- No network, cloud or package-install commands, so no live provider, price or model-lifecycle verification.
- The specialist skills' own helper scripts (for example `safe-api-tool-calls/scripts/inspect_project.py`): there is no project code to inspect.

## 5. Friction log

| Moment | Kind | Pointer |
| --- | --- | --- |
| The **Assumed answers** rule made a headless run clear: no further questions, a table at the top, and decisions marked provisional | Helpful | `.claude/skills/adk-system-designer/SKILL.md:125` |
| It was unclear whether to run the independent review. The rule covers "several people or a production service" and exempts "a single-person proof of concept". A single-person pilot that takes money from external users is neither. I ran it, and it found the problems that changed the verdict | Unsure, then genuinely helpful | `.claude/skills/adk-system-designer/SKILL.md:249-255`; `.claude/skills/adk-system-designer/assets/plan-review-prompt.md:7-35` |
| The plan template asks for acceptance as one inline field ("numbered A1, A2 ..."). The helper only recognises an item that starts a line, so my first run failed every grid cell. The reference does not mention the line-start requirement | Unsure, cost one rerun | `.claude/skills/adk-system-designer/assets/implementation-plan-template.md:100`; `.claude/skills/adk-system-designer/scripts/check_schedule.py:254`; `.claude/skills/adk-system-designer/references/failure-review.md:29-34` |
| The default `python3` is 3.9. The skill says to report the schedule as unchecked if 3.11 is missing, but it does not say to look for another interpreter. I found 3.12 under `/opt/homebrew/bin` | Unsure | `.claude/skills/adk-system-designer/references/delivery-profiles.md:223-224` |
| The helper's approval regex flagged "credentials from env/Secret Manager" in G02's prose as an outside approval. I settled it with `mentions_only: wait` | Slightly heavy | `.claude/skills/adk-system-designer/scripts/check_schedule.py:31-34` |
| Giving waits their own schedule entries, plus the rule "do not shorten a wait to make it fit", made the honest conclusion unavoidable: waits, not hours, set the date | Helpful | `.claude/skills/adk-system-designer/references/delivery-profiles.md:124-127, 190-202` |
| "Offer only remedies that close the gap" and "run every remedy as a what-if" forced five what-ifs and removed two remedies I had first written (later onboarding; an ADK-experienced engineer with direct ordering) | Helpful, somewhat heavy | `.claude/skills/adk-system-designer/references/delivery-profiles.md:197-202` |
| The profile says an MVP or pilot plan is "two to four pages per phase". The plan template's 14-field goal entry for 10 phase 1 goals produced a plan of about 5,600 words. I kept the fields because "cut waste, never substance" forbids dropping acceptance items | Heavier than needed / conflicting guidance | `.claude/skills/adk-system-designer/references/delivery-profiles.md:36` vs `.claude/skills/adk-system-designer/assets/implementation-plan-template.md:86-110` |
| Choosing the model from the dated lifecycle table, rather than from memory, steered away from `gemini-3.6-flash`, whose Vertex retirement date falls inside the pilot | Helpful | `.claude/skills/adk-system-designer/SKILL.md:198-205`; `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` |
| The coverage-grid rule ("enumerate, don't recall") plus the reviewer's coverage check caught wrong n/a reasons: OIDC callback replay, and injected text replayed from stored sessions | Helpful | `.claude/skills/adk-system-designer/references/failure-review.md:7-37` |
| The trigger for the runtime-and-delivery reference was unclear for a five-advertiser pilot. I skimmed it and did not apply it | Unsure | `.claude/skills/adk-system-designer/SKILL.md:183-186` |
| The scope gate expects a conversation, but this session was headless. Five scope-gate questions turned into eleven assumed rows, because the domain added its own questions | Neutral | `.claude/skills/adk-system-designer/SKILL.md:54-68` |

## 6. Next prompt the skills told the user to type

The skill's instruction gives this example form, quoted verbatim from
`.claude/skills/adk-system-designer/SKILL.md`:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated for this plan (also in the plan's summary and "Resume here"):

```text
/adk-engineer Carry out G01 from docs/plans/campaign-assistant.md.
```

---

# Revision 2: rights also depend on territory, flight dates and creative modification

Same session rules applied: files were changed only inside this directory,
and there were no network, cloud or package-install commands.

## R2.1 Skills invoked and files opened, in order

No new skill was invoked; the work continued under `adk-system-designer`.
Files opened during this revision:

1. `docs/architecture/campaign-assistant.md`, re-read in full after the on-disk change note. The content matched my last write.
2. `.claude/skills/adk-system-designer/SKILL.md:249-260`, the review and revision rules: compare with the previous version and list everything removed or weakened.
3. `.claude/skills/adk-system-designer/assets/plan-review-prompt.md`, reused for the second independent review.
4. `.claude/skills/adk-system-designer/scripts/check_schedule.py`, run only. Its source was not re-read.

No other references were re-read. The decisions from revision 1's reading
of `design-decisions.md` and `failure-review.md` still applied.

## R2.2 New questions I would have asked, and the answers I assumed

These are also rows Q12–Q15 of the design's Assumed answers table.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q12 | What does "the creative may be modified" mean, and who declares the intent? | A yes/no flag per rights record. The planner states the intent, and the assistant never assumes it |
| Q13 | Which territory is checked, and in which codes? | The booked inventory's market, as ISO 3166 codes. Region groups are expanded from a rights-team table, and an unknown code counts as not covered |
| Q14 | How are rights windows compared with flight dates? | Inclusive calendar dates in the market's time zone. The whole flight must be covered; a partly covered asset is shown with its gaps but cannot be ordered |
| Q15 | Can several rights records combine to cover one flight? | Yes, when owner, brand, channel and territory match, the modification flags allow the intent, and the windows join without a gap |
| Q1 (updated) | Can the go-live date move by about six weeks rather than one? | Not assumed. This is now an explicit decision for the user |

## R2.3 Files changed, and what is not finished

- `docs/architecture/campaign-assistant.md` (revision 2):
  - Q12–Q15 and the user's update in the status line.
  - Journey and model-versus-code updated.
  - I1 reworded; new I6 (an order request's terms are exactly the licensed terms).
  - D2 and D4 changed (required terms; quote terms must match the request).
  - D5 binds the terms to the proposal.
  - New D10: `rights_coverage`, a pure function in code, with a rule table the rights team confirms.
  - Tool contracts, data rows, grid citations, three new failure scenarios and new open decisions.
- `docs/plans/campaign-assistant.md` (revision 2):
  - New goals: G00 (day-1 requests, a human task) and G16 (rule corrections after the rights review).
  - New waits: W2c (rights semantics), W5 (rights team confirms the rules), W6 (pilot planners available), W7 (booking-ops staging session).
  - 15 new acceptance items and 7 strengthened ones.
  - Re-estimated G01, G02, G04, G05, G06, G07.
  - Rewritten summary, schedule result, change tables, what-if table and resume prompt.
- `.revision-snapshot/` (new): copies of the design, plan and report as they stood after revision 1, kept so the "removed or weakened" check can be repeated. It is safe to delete.
- `REPORT.md`: this section was appended. Sections 1–6 above describe revision 1 and were not edited.

Not finished:

- **The revised plan does not fit three weeks, even at the low end.** Phase 1 is 57.5–86 h against 67.5 h. Go-live lands in 16–28.56 working days, so a committed date needs 29 working days (about six weeks). The user must accept that or choose another date.
- No tested remedy closes the gap alone. A read-only pilot, an ADK-experienced engineer, or the teams committing to shorter waits each still miss 15 days. All three together fit, but that drops buying and assumes a different engineer, so it is not recommended.
- The rights semantics (Q12–Q15) are assumptions until the rights team answers W2c and confirms the rule table in W5.
- Live checks are still not done: model lifecycle, prices and the ADK pin.

## R2.4 Checks run, and checks not run

Run:

- `check_schedule.py` with `/opt/homebrew/bin/python3.12 -I`:
  - After the first revision 2 edits: 54.5–79.5 h, finish 12.78–22.11 days, low end only at 15 days; fits at 23.
  - **After settling the review: 57.5–86 h, finish 16–28.56 working days. At 15 days it does not fit (exit 1); at 28 days, low end only; at 29 days it fits (exit 0).** The coverage-grid citation check passes, and phase 2 is 27.5–43.5 h.
- What-ifs through stdin on copies: the results are in the plan's revision 2 what-if table.
- A mechanical comparison against `.revision-snapshot/`:
  - All 81 acceptance items, 63 grid cells, cross-cutting scenario rows, waits and the floor text are still present.
  - No grid citation was dropped.
  - 15 items were added and 7 reworded.
- **A second independent plan review** by a fresh subagent with the plan-review prompt, focused on revision 2. It returned 21 findings:
  - Missing prerequisites: W3 needed G09; the waits started before the requests were sent in G01; W2a was overloaded; no hours for rework after W5; G05 needed W5; and outside people and test data had no waits.
  - Unsupported claims, including my "removed or weakened: none".
  - Coverage gaps, including per-brand partial failure, a quote's market against the search territory, ops keying different dates, inverted flight dates and overlapping windows.

  All findings are settled in the plan's change table, rows "Review R2-…". Together they moved the committed date from 23 to 29 working days.

Not run: no tests, as before (no code, and google-adk is not installed); no network or cloud commands.

## R2.5 Friction log

| Moment | Kind | Pointer |
| --- | --- | --- |
| The revision rule (compare with the previous version; nothing leaves silently) made me snapshot revision 1 before editing. Without the copy, I could not have checked the claim at all | Helpful | `.claude/skills/adk-system-designer/SKILL.md:257-260` |
| My mechanical comparison counted items and citations, but it could not see a reworded failure outcome (I1 merged "rights unavailable" into "not covered") or a narrowed assertion (G02/A1 covered only `usable`). The reviewer caught both. The rule says to list items "weakened", but the skill gives no way to detect weakening beyond reading | Unsure; a counting check gives false confidence | `.claude/skills/adk-system-designer/SKILL.md:257-260` |
| It was unclear whether to rerun the independent review for a revision. The skill requires review "before handing over a plan", not after each revision. I reran it because the change touched an authorization rule; it moved the date by six working days | Unsure, then genuinely helpful | `.claude/skills/adk-system-designer/SKILL.md:249-255`; `.claude/skills/adk-system-designer/assets/plan-review-prompt.md:7-35` |
| The reviewer showed that "day-1 requests" written inside a goal do not start on day 1 in the schedule: they start when that goal finishes. The reference says to give waits their own entries, but not that the request-sending itself needs to be a goal the waits follow | Missing guidance | `.claude/skills/adk-system-designer/references/delivery-profiles.md:124-127` |
| "Stable IDs" meant adding G00 and G16 rather than renumbering, which leaves phase 1 IDs out of numeric order. That is acceptable, but nothing says which way to choose | Unsure | `.claude/skills/adk-system-designer/references/implementation-handoff.md:69` |
| The "don't shorten a wait to fit" rule kept the new rights waits at their real assumed lengths, which turned "low end only" into "does not fit". That is uncomfortable but honest | Helpful | `.claude/skills/adk-system-designer/references/delivery-profiles.md:190-196` |
| The plan has grown to about 8,000 words, with the design at about 4,900, for one engineer. Change tables for two revisions plus two reviews are now a large part of it. The "one row per change" rule kept them from growing further, but the profile's "two to four pages per phase" is far exceeded | Heavier than needed | `.claude/skills/adk-system-designer/references/delivery-profiles.md:36, 316-317` |

## R2.6 Next prompt the skills told the user to type

Unchanged form from `.claude/skills/adk-system-designer/SKILL.md`:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated. First, send the day-1 requests in G00 yourself; that is a
human task with no prompt. Then:

```text
/adk-engineer Carry out G01 from docs/plans/campaign-assistant.md.
```
