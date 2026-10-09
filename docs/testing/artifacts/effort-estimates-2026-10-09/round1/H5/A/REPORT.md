# REPORT: home-insurance claim intake agent, design session

This session produced the design, the plan and the ticket files. Nothing was
implemented. The user was unavailable, so every question was answered by
assumption and recorded.

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer` command. `SKILL.md` was loaded by the harness.
2. Directory listing of the repository and of `.claude/skills/` (the repository is greenfield: one commit, no code).
3. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (full)
4. `.claude/skills/adk-system-designer/references/design-decisions.md` (full)
5. `.claude/skills/adk-system-designer/references/failure-review.md` (full)
6. `.claude/skills/adk-system-designer/references/gcp-decisions.md` (full)
7. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (full)
8. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (full)
9. `.claude/skills/adk-system-designer/assets/system-design-template.md` (full)
10. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (full)
11. `.claude/skills/adk-system-designer/assets/ticket-template.md` (full)
12. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
13. `.claude/skills/*/references/compatibility.md`: only the ADK and version lines were grepped (first ≈ 6 matching lines per file), across all 18 specialist skills.
14. `.claude/skills/adk-model-and-output-contracts/references/model-selection.md` (lines 1–40)
15. A grep across `.claude/skills/` for EU and residency guidance. This found hits in `protect-adk-sensitive-data/references/cloud-lifecycle.md` and `model-armor.md`, but those files were not opened in full.

No other skill was invoked. The skill says implementation specialists are for
later goals, and the user said "Do not implement."

## 2. Questions I would have asked, and the answers I assumed

These are also in the design's **Assumed answers** table
(`docs/architecture/home-claim-intake.md`), together with the decisions each one
affects.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | When does work start, when is GA, and can we run a pilot before GA? | Start 2026-10-12, GA 2027-03-12, with 20 working weeks after a holiday break. Staff dogfood from week 11, limited customer pilot from week 16. Development continues after GA. |
| Q2 | How many hours does each person have, and how familiar are they with ADK and GCP? What share of the security reviewer do we get? Who operates the service? | All six (five engineers and the ML engineer) full time at 40 h/week. They know Python and GCP but are new to ADK. Security reviewer at 0.2 FTE. The team runs the service with business-hours on-call, backed by the existing SRE team. |
| Q3 | What is the budget for models and cloud? | Production ≈ €6k/month, non-production €1.5k/month, evaluation €1k/month (provisional). |
| Q4 | Who are the users, how do they sign in, and through which channel? | Existing policyholders, signed in through the portal's OIDC customer identity provider. Web plus the mobile web view. No anonymous filing. |
| Q5 | Which markets and languages? | One EU country, in its local language plus English. |
| Q6 | Which Guidewire product and API, is there a sandbox, is replay supported, and who owns the configuration? | ClaimCenter on Guidewire Cloud, using the Cloud API with draft, documents and submit. A sandbox is available within 3 weeks. Idempotency and lookup are unknown, so G02 must find out. A separate Guidewire team owns the configuration. |
| Q7 | Does the agent decide coverage, payout or fraud? | No. It only collects the claim. Adjusters make every decision. No GDPR Art. 22 automated decision. |
| Q8 | What should happen with the photos? | Attach the originals as evidence. Analyse a minimised copy to check quality and pre-fill damage information. No cost estimate. |
| Q9 | Is strict EU residency required, including model inference? | Yes. Everything runs in EU regions and there is no global endpoint. |
| Q10 | What are the retention rules? | Transcripts 90 days. Photos 30 days after attach or abandonment. Claims follow Guidewire retention. Operation audit records 24 months (I also flagged this for Legal). |
| Q11 | May the agent collect injury (health) details? | No. It records only a yes/no and sends the customer to the phone line. |
| Q12 | What volume and surges should we expect? | About 2,000 claims/month, 1.5 sessions per claim, and 10× on a storm day. |
| Q13 | Is there a fallback channel? | The existing web form and the phone line. A kill switch routes customers there. |
| Q14 | What availability and latency targets apply? | 99.5% chat availability. 99% of claims `SUBMITTED` within 15 min. p95 turn ≤ 8 s. All provisional. |
| Q15 | What platform exists already? | A GCP EU landing zone, Terraform, Cloud Run experience, and private connectivity to Guidewire. |
| Q16 | Who owns the DPIA, the AI-disclosure text and accessibility? | The DPO and Legal. GA is gated on DPIA sign-off. |
| Q17 | Do we need live hand-off to a human at GA? | No. The agent shows the phone number and a callback form. |
| Q18 | Who sends claim acknowledgements? | Guidewire or the communications platform. The agent sends no messages. |
| Q19 | Is there a baseline to compare against? | Yes: form analytics and data on missing-information callbacks. |

The skill would also have had me ask the user to accept two things:

- **The profile.** I assumed it is accepted as "production service".
- **The cut line.** I assumed phase 1 = G01–G20 before GA, with the cut order
  listed in the plan.

Neither was confirmed by the user. Both are marked draft or proposed.

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/home-claim-intake.md`: the system design, status draft (≈ 6,800 words). It contains:
  - the assumed answers
  - depth per concern and deferred controls
  - invariants I1–I10
  - a component diagram and a submission sequence diagram (Mermaid)
  - decisions D1–D10
  - model-facing contracts
  - data and authority
  - the security posture
  - budgets
  - failure and recovery
  - verification
  - open decisions
- `docs/plans/home-claim-intake.md`: the implementation plan (≈ 9,300 words). It contains:
  - capacity and per-role checks
  - the cut line and cut order
  - milestones
  - the implementation map
  - the goal table
  - full G01–G20 sections, each with its own run prompt
  - phase 2 goals P2-01 to P2-08
  - the Later list
  - open decisions
  - a Resume-here section
- `docs/tickets/home-claim-intake/G01-…md` through `G20-…md`: 20 ticket files, one per phase 1 goal, using the ticket template.
  - G01, G02 and G03 are `status: ready`.
  - The other 17 are `status: blocked`, each with `blocked_by` listing the goals it depends on.
- `REPORT.md`: this file.

Nothing outside the current directory was changed. Nothing was committed.

Not finished, or deliberately left open:

- **No user review.** Every decision is *proposed*, and the profile and cut line are unconfirmed.
- **No provider facts were looked up**, because the session had no network. This leaves open:
  - Vertex regional availability of `gemini-3.8-flash`
  - prices and quotas
  - Model Armor and SDP EU endpoints
  - every Guidewire Cloud API behaviour (draft claims, documents, idempotency, lookup by external reference)

  These are labelled as unverified in the design and handed to discovery goals G02 and G03. The cost estimate is a formula only.
- **Legal points are not cited.** These are the EU AI Act transparency obligations, GDPR Art. 9, 22 and 35, and accessibility. They appear as assumptions for Legal and the DPO to confirm.
- **No ADRs were split out.** The decisions live in the design document.
- **No implementation, scaffolding or dependency changes**, as instructed.

## 4. Checks run, and checks not run

Run, all passing:

- **Consistency script** (Python stdlib, run with `python3 -I`, read-only over `docs/`). It checked:
  - every relative Markdown link resolves
  - every backticked skill name exists under `.claude/skills/`
  - there are no leftover template placeholders and no secret-like strings
  - each ticket's frontmatter has all 11 template keys
  - each ticket's primary and supporting skills exist
  - each `blocked_by` ID has a ticket
  - the plan has a section for each of G01–G20

  Result: `problems: none`.
- **Estimate arithmetic.** The generator summed the goal estimates to **1,348–2,104 h**, which matches the plan's phase 1 total. The capacity figures were worked out by hand:
  - total: 2,976 h
  - after a 25% reserve: 2,232 h
  - per role, usable: ML engineer 360 h, security reviewer 72 h, engineers 1,800 h

Not run:

- **No tests.** No application code exists, `google-adk` and the other dependencies are not installed, and tests importing `google.adk` could not run here.
- **No Mermaid rendering or validation** of the two diagrams.
- **No network, cloud, `gcloud`, Terraform or Guidewire calls**, and no lookups of provider documentation or prices.
- **The skill helper scripts were not run.** For example, `adk-model-and-output-contracts/scripts/audit_model_config.py` audits code, and there is no code to audit.

## 5. Friction log

Each entry is marked as uncertain, heavier than needed, or helpful.

- **Helpful.** `adk-system-designer/SKILL.md:119-122` covers runs where the user cannot answer: ask nothing further, put an **Assumed answers** table at the top, and mark the dependent decisions provisional. This matched the headless rule exactly and settled the tension with `SKILL.md:52` ("Let the user answer before treating a material product choice as settled").
- **Uncertain: phase model versus a hard production deadline.**
  - `delivery-profiles.md:128-138` defines phase 1 as what fits capacity and phase 2 as work done "when the team has time".
  - Here the deadline is GA, and the whole 5-month capacity has to deliver GA.
  - I mapped phase 1 to "everything GA needs" (G01–G20) with internal milestones M0–M4, and phase 2 to post-GA hardening.
  - The reference has no example of a production profile with a fixed launch date that uses the whole capacity. The closest is the MVP example at `delivery-profiles.md:187-190`.
- **Uncertain: focus factor for a full-time, multi-month team.**
  - `delivery-profiles.md:104-106` gives 0.6 for part-time or interrupted work and 0.8 for "a dedicated block such as a single afternoon".
  - It gives no figure for full-time engineers over 20 weeks. I used 0.6.
- **Missing: per-role capacity.**
  - `delivery-profiles.md:98-121` checks only the total capacity.
  - In this team the binding constraints are the 0.2 FTE security reviewer and the single ML engineer.
  - I added a per-role table to the plan. The reference could say "check scarce roles separately".
- **Uncertain: tickets for blocked goals.**
  - `SKILL.md:266-267` says to write "one file per ready goal", and `assets/ticket-template.md:12` defaults to `status: ready`.
  - The user asked for tickets for *all* phase 1 goals, and only G01–G03 are ready.
  - I wrote all 20, setting `status: blocked` and `blocked_by` on 17 of them.
- **Uncertain: primary skill for the photo upload pipeline (G06).**
  - The mapping table at `implementation-handoff.md:19-37` has no row for user-uploaded files or artifacts, even though `design-decisions.md:148-149` names artifacts as a data class.
  - I chose `protect-adk-sensitive-data` as primary.
- **Uncertain: goal numbering.**
  - The skill's closing example (`SKILL.md:276`) and the handoff reference (`implementation-handoff.md:105`) both use "Carry out G01" as the next prompt.
  - My first draft had the discoveries as G01 and G02, which need external access, so they were not the next runnable goal.
  - I renumbered so G01 is the local walking skeleton. That took a sed swap over the design document, and one range ("G01–G20") broke and had to be fixed by hand.
- **Helpful.** The dated model-lifecycle snapshot at `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12-27` and the pointer to it at `SKILL.md:195-198` were valuable. They:
  - avoided picking from memory
  - surfaced the Vertex retirements of `gemini-3.6-flash` (2026-11-19) and `gemini-3.7-flash` (2027-01-28), which fall inside or near the plan's horizon
  - gave a dated source for D10
- **Helpful.** The compatibility pins (`*/references/compatibility.md`, for example `adk-model-and-output-contracts/references/compatibility.md:3,24`) gave a consistent ADK 2.8.0 working assumption. They also flagged `FallbackModel` as absent at 2.8.0.
- **Helpful.** `adk-release-engineering/references/compatibility.md:9` notes that `adk eval` exits 0 whatever the results. That shaped G18: the CI gate must parse the results, not rely on the exit code.
- **Heavier than needed.**
  - `SKILL.md:85` says a production design is "as long as its decisions require", with "every template section either filled or marked not applicable".
  - Together with the plan template's per-goal fields (`implementation-plan-template.md:48-69`) repeated for 20 goals, then copied again into 20 tickets, this gave ≈ 16k words of plan and design plus ≈ 6.7k words of tickets.
  - The plan's goal sections and the tickets are near duplicates. I generated both from one data source to keep them consistent. The skill could allow "the plan holds a one-line goal index when tickets exist".
- **Helpful.** The failure-scenario table at `failure-review.md:21-43`, especially "Provider commits, reply is lost" and "One effect succeeds, a later step fails", directly produced:
  - invariants I3 and I4
  - the per-photo document sub-operations
  - the G10 acceptance cases
- **Helpful.** The trifecta guidance at `design-decisions.md:182-196` led to the main structural security decisions:
  - no submit tool for the model
  - a tool-less photo reader
- **Uncertain: provider facts with no network.**
  - `gcp-decisions.md:37-41` says to "consult current official sources and record URL, access date…", but the session forbade network access.
  - `SKILL.md:201-203` covers this case ("keep those decisions provisional and name the exact verification needed"), so I created G03.
  - No skill reference gives Guidewire facts. Every Guidewire API behaviour in the design is an unverified assumption, sent to G02.

## 6. The exact next prompt the skills told the user to type

The skill's template, quoted verbatim from `SKILL.md:276`:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Filled in for this plan, using the plan template's continuation form
(`implementation-plan-template.md:113-119`) and written into the plan's "Resume here" section:

```text
/adk-engineer Carry out G01 (walking skeleton) from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its accepted decisions.
Use adk-workflow-design with adk-model-and-output-contracts.
Work within local-only scope (no cloud, no Guidewire), verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```
