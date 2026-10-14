# Report: home-insurance claim assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer`, loaded by the user's `/adk-system-designer`
command. No other skill was invoked. `adk-engineer` is only named in the
handoff prompts.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded with the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/gcp-decisions.md`
6. `adk-system-designer/references/implementation-handoff.md`
7. `adk-system-designer/assets/system-design-template.md`
8. `adk-system-designer/assets/implementation-plan-template.md`
9. `adk-system-designer/assets/ticket-template.md`
10. `adk-system-designer/scripts/check_schedule.py` (read in full, then run)
11. `adk-system-designer/references/runtime-and-delivery.md` (its trigger applied: browser contract, concurrency during storm peaks, release continuity)
12. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. The first 25 lines of every specialist's `references/compatibility.md`. The output was too large and was saved to a file, so I saw only a preview. I then grepped them for the ADK version.
14. `adk-agent-security/references/compatibility.md` lines 1–10 (source of the 2.8.0 working assumption)

I did not open any specialist `SKILL.md` or any other specialist reference.

## 2. Questions I would have asked, and the answers I assumed

These are recorded in full in the design's **Assumed answers** table
(`docs/architecture/home-claim-assistant.md`). Each decision that depends on
them is marked provisional.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | What does "GA in five months" mean: which customers and which date? | All home-insurance customers in one market (Germany) on Mon 2027-03-15. Work finishes by Fri 2027-03-12: 98 working days from 2026-10-19, with 24 Dec–1 Jan off. |
| A2 | Which languages? | German and English. |
| A3 | Which Guidewire product, version and API? | ClaimCenter on Guidewire Cloud Platform, using the Cloud API (REST). A sandbox can be requested. |
| A4 | How do customers sign in? | Through the existing portal, with CIAM issuing OIDC tokens. |
| A5 | How familiar is the team with ADK and GCP, and how many hours do they have? | Experienced with Python and GCP but new to ADK (×1.5 on estimates). 6 focused hours a day. The security reviewer has about 2 hours a day. |
| A6 | What is the budget for models and cloud? | There is a production budget, but no figure. The spend ceiling is open decision O3. |
| A7 | What claim volume and peaks? | Illustrative: 40,000 home claims a year, 25 % through the assistant, storm peaks of about 300 conversations an hour. |
| A8 | May the assistant say whether something is covered, or how much will be paid? | No. |
| A9 | May the claim be created after the customer confirms, without staff review? | Yes. The customer's explicit confirmation is the human approval. |
| A10 | What happens to photo EXIF and GPS data? | Originals go to Guidewire unchanged. The model gets a re-encoded copy with the metadata removed. |
| A11 | Retention periods? | Unsubmitted drafts: 30 days. Sessions: 90 days after submission. Our photo copies: deleted 30 days after transfer. |
| A12 | Is there an existing malware scanner for uploads? | Not known (open decision O5). |
| A13 | Does the call centre need to see drafts at GA? | No. Customers get the phone number and a draft reference. The draft view is phase 2 (G28). |
| A14 | Accessibility standard? | WCAG 2.1 AA. |
| A15 | Is there an existing GCP organisation, and which services are allowed? | An existing organisation and platform team. Cloud Run, Cloud SQL, Cloud Tasks and Vertex AI are allowed. EU location policy is possible. |
| O1 | Is `gemini-3.8-flash` available on Vertex AI in an EU region, and when does it retire there? | Assumed yes, unverified. G14 checks it. |
| O2 | Guidewire replay and idempotency contract, and a searchable external-reference field | Unknown. The design doesn't depend on Guidewire supporting idempotency keys: it searches before re-sending. |
| O3 | What is the monthly model-spend ceiling? | Not given. It blocks the G18 thresholds. |
| O4 | Retention for the audit ledger? | 2 years (assumed). |
| O6 | Does the AI Act transparency duty apply, and is this a high-risk use? | Disclosure applies. Assumed not high-risk; legal review needed. |
| O7 | Confirm or move the cut line. The calendar fits only at the low end. | Not chosen. I offer two tested remedies: the security reviewer at 4 h/day, or GA moved two working days to Tue 2027-03-17. |

## 3. Files written or changed, and what was not finished

Written (all new, uncommitted):

- `docs/architecture/home-claim-assistant.md`: the design (draft, about 5,600 words). It contains the Assumed answers, scope gate, depth table, guarantees I1–I10 and T1–T3, decisions D1–D15, model-facing contracts, data and authority, security posture, budgets, failure table, verification, and open decisions O1–O7.
- `docs/plans/home-claim-assistant.md`: the plan (about 3,450 words, including the YAML schedule block). It contains the summary, capacity, per-person load, schedule block (W1–W6, G01–G27 in phase 1, G28–G33 in phase 2), the helper result, what-if table, implementation map, goals table linking to tickets, phase 2, Later, and Resume here.
- `docs/tickets/home-claim-assistant/G01-…md` to `G27-…md`: 27 phase 1 tickets in the ticket template, about 5,700 words in total.
- `REPORT.md`: this file.

Temporary files: I first wrote the schedule scratch files (`plan.md`,
`gen.py`, `g*.json`) to `/tmp/h5sched/`, which is **outside the current
directory** and against the session rule. I noticed, moved what I needed into
`./.scratch/`, and deleted `/tmp/h5sched/`. I deleted `./.scratch/` (the
schedule and ticket generator scripts) before finishing. No files outside the
working directory remain changed.

Not finished:

- No user has accepted any decision. The design stays **draft**.
- These are not verified: Vertex AI EU availability and quotas, prices, Model Armor regional availability, and the Guidewire API contract. Network access was not allowed. They are recorded as O1–O3 and O5 and as goals G10 and G14.
- The cost estimate is symbolic (token counts only, no prices).
- Design and plan together are about 9,050 words against the skill's production budget of about 8,000. The roughly 300-line YAML schedule block accounts for most of the excess. I did not trim further.
- No implementation, as requested.

## 4. Checks run and not run

Run, all with `/opt/homebrew/bin/python3.12 -I`. The system `python3` is 3.9, and the skill asks for 3.11 or later.

| Check | Result |
| --- | --- |
| `check_schedule.py --plan … --tickets … --days 98 --reserve 0.25` with 6 people at 6 h and the reviewer at 2 h | Phase 1 is 775–1,222 h against 2,793 h of capacity: hours fit. Finish is 66.89–99.67 working days against 98: **low end only, exit 1**. No mismatches between tickets and plan. |
| Same, reviewer at 4 h/day | Finish 72.89–93.56 days. Fits, exit 0. |
| Same, `--days 100` (GA Tue 2027-03-17) | Fits, exit 0. |
| What-if: cut G08 photo analysis (run on a scratch copy of the final schedule, since deleted) | Finish unchanged, still low end only. Cutting scope doesn't help. |
| `--phase 2` | 188–308 h (copied into the plan). |
| About 8 earlier failing runs while restructuring | The plan's "Changes made after earlier failing runs" table lists every change. Each one is true of the work; no dependency was removed and no wait was shortened. |
| Relative-link check of the plan's `../` links | All targets exist. |

Not run:

- Any application test. There is no code, and tests importing `google.adk` can't run here because the dependencies aren't installed.
- Any network, cloud, Guidewire or Vertex lookup.
- Markdown linting.
- The skill's own test suites under `.claude/skills/*/tests/`. They aren't relevant to a design-only task.

## 5. Friction log

- **Unsure: is phase 1 all of GA, or a shorter slice?** `delivery-profiles.md:237-239` defines phase 1 as the goals that "fit the capacity and deliver the profile's 'done'". For a production profile with five months, that makes phase 1 the whole GA programme: 27 goals and 27 tickets. That felt heavy. An "internal pilot" phase 1 would have been the alternative. I followed the text.
- **Unsure: does the focus factor stack with the reserve?** `delivery-profiles.md:178-179` says to give full focused hours to `--person` and let `--reserve` hold back a share. `delivery-profiles.md:213-215` separately describes capacity as people × hours × a focus factor of about 0.6–0.8. I used 6 focused h/day with a 0.25 reserve and no second focus factor. It isn't clear whether both discounts were intended.
- **Unsure: which Python?** `delivery-profiles.md:206-207` asks for Python 3.11 or later. The default `python3` here is 3.9. The script (`check_schedule.py:15-19`) uses nothing 3.11-specific that I could see. I found 3.12 under Homebrew and used that.
- **Unsure: `wait_days` on tickets.** The ticket template's front matter (`assets/ticket-template.md:11-15`) has no `wait_days`, but the helper reads it from tickets (`check_schedule.py:96`). I added `wait_days` only to tickets that have a wait.
- **Unsure: ticket status.** The template hard-codes `status: ready` (`assets/ticket-template.md:17`). Most tickets have unresolved prerequisites, so I used `blocked` for them.
- **Unsure: what a missing Vertex date means.** In `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12`, `gemini-3.8-flash` has no `vertex_retirement` field. It could mean "not on Vertex" or "no date announced". I treated it as unverified (O1).
- **Unsure: which run-prompt form to use.** The skill gives three. `SKILL.md:279-283` has "Carry out G01 from docs/plans/<topic>.md". `assets/implementation-plan-template.md:153-158` has a multi-line form. `assets/ticket-template.md:53-57` has a ticket-path form. I used the ticket-path form in tickets and in the closing prompt.
- **Heavier than needed: the reading budget.** `SKILL.md:87-88` sets about 8,000 words, but the YAML schedule block (`assets/implementation-plan-template.md:46-59`) alone is about 300 lines for 39 entries. It isn't stated whether the block counts.
- **Heavier than needed: the what-if loop.** `delivery-profiles.md:189-201` asks for every remedy and every negative claim to be run as a what-if. That took about 10 helper runs plus restructuring. The discipline was worth it, though: it showed the plan is limited by the dependency chain, not by hours, and that cutting scope wouldn't help.
- **Heavier than needed: the helper's goal count.** The summary counts calendar-wait entries as goals ("33 goals" when there are 27 goals and 6 waits; `check_schedule.py:277`). That is slightly misleading to quote.
- **Helpful: Assumed answers for headless runs.** The instruction at `SKILL.md:124-128` made a headless run straightforward.
- **Helpful: the helper's chain and load output.** `check_schedule.py:213-241`, together with the rule against shortening waits or removing dependencies (`delivery-profiles.md:189-193`), kept the remedies honest.
- **Helpful: the review-ratio check.** `check_schedule.py:170-174` made me vary review effort deliberately: heavier for authorisation and writes, lighter for UI and evaluation.
- **Helpful: the model lifecycle table.** It immediately showed that `gemini-3.7-flash` retires on Vertex on 2027-01-28, inside the plan horizon (`model-lifecycle-2026-10-01.json:13`). That drove D7.
- **Helpful: the trifecta rule.** The trifecta check (`references/design-decisions.md:182-196`) led directly to D1: submission is ordinary code and not a model tool.
- **Helpful: failure-review scenarios.** `references/failure-review.md:23-43` mapped almost row for row onto the design's failure table.
- **Helpful: compatibility notes.** The specialists' notes gave a clear ADK working version (2.8.0) for a greenfield design, as `SKILL.md:197-200` instructs.

## 6. The exact next prompt the skills told the user to type

The skill's instruction (`SKILL.md:279-283`) gives this example, verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

The plan template's continuation form (`assets/implementation-plan-template.md:161-162`), verbatim:

```text
/adk-engineer Continue the next ready goal in <plan path>.
```

Applied to this project, the prompt I give the user for the next ready goal is:

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
