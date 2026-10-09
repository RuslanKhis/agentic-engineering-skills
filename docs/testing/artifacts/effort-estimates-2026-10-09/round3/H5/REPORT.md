# REPORT — home-insurance claim intake agent (design and plan only)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer` (the user typed `/adk-system-designer`). I
invoked no other skill: the request was design-only, and the designer says it
"needs no other skills".

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (provided at invocation)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/gcp-decisions.md`
6. `adk-system-designer/references/runtime-and-delivery.md`
7. `adk-system-designer/references/implementation-handoff.md`
8. `adk-system-designer/assets/implementation-plan-template.md`
9. `adk-system-designer/assets/system-design-template.md`
10. `adk-system-designer/assets/ticket-template.md`
11. `adk-system-designer/scripts/check_schedule.py` (read in full before running it)
12. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. I grepped the version lines, not whole files, of `references/compatibility.md` in: `adk-agent-instructions`, `adk-agent-evaluation`, `adk-agent-observability`, `adk-agent-interoperability`, `safe-api-tool-calls`, `deploy-adk-on-google-cloud`, `protect-adk-sensitive-data`, `adk-operational-guardrails`, `adk-agent-security`, `adk-frontend-integration`, `adk-memory-architecture`, `adk-model-and-output-contracts`. This was to find the ADK version to assume (2.8.0). I listed `adk-tool-auth-and-secrets/references/` but did not open it, because it has no `compatibility.md`.
14. `adk-system-designer/tests/test_check_schedule.py` (imports only, to see whether it needs pytest)

## 2. Questions I would have asked, and the answers I assumed

These are recorded in full as the **Assumed answers** table (A1–A18) at the top of
`docs/architecture/home-claim-intake.md`. In short:

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | GA date; continued afterwards? | GA 2027-03-09; continued by this team |
| A2 | Hours and familiarity | 5 engineers and 1 ML engineer full time, new to ADK (×1.5), Python/GCP experienced; security reviewer about 40%; focus 0.6 |
| A3 | Model/cloud budget | ≤ €1,500/month in phase 1, ≤ €6,000/month at GA |
| A4 | Users and judges | Retail home policyholders in the existing portal; handlers read ClaimCenter; claims leadership judges the pilot |
| A5 | Data and effects | Personal and possibly Art. 9 data, photos; one effect: create an FNOL claim with documents; no payments or cover decisions |
| A6 | Guidewire product and interface | ClaimCenter on Guidewire Cloud, Cloud API with OAuth client credentials, sandbox available |
| A7 | Markets and languages | Germany; German and English |
| A8 | Customer identity | Portal OIDC tokens, verifiable, mapped to a policyholder ID |
| A9 | Frontend | Chat widget in the existing portal |
| A10 | Volume | ~1,500 digital home FNOLs/month; 10× storm peaks |
| A11 | Residency | Everything in the EU, including regional model inference |
| A12 | Retention | Transcripts 90 days after submission, drafts 30 days, photo copies 30 days after transfer |
| A13 | Cover guidance allowed? | No |
| A14 | Who resolves uncertain submissions? | Claims operations, within one business day |
| A15 | Availability target | 99.5% monthly; fallback is the web form and hotline |
| A16 | GCP environment | Existing org; platform team provisions via Terraform (wait of days) |
| A17 | Emergencies | Static hotline banner; agent repeats it; no triage |
| A18 | Profile and cut line | Production; phase 1 = G01–G13, phase 2 = G14–G25 |

The design also lists open decisions that need people other than the user:
O1 Guidewire replay contract, O2 EU model availability, O3 baseline metrics,
O4 EU AI Act classification and disclosure wording, O5 retention of the ledger
and transcripts.

## 3. Files written or changed, and what was not finished

Written (none existed before; no other files changed):

- `docs/architecture/home-claim-intake.md` — the system design (draft): journey, Assumed answers, profile and depth table, floor, invariants I1–I7, decisions D1–D12, model-facing contracts, data and authority, security posture, budgets, failure table, open decisions.
- `docs/plans/home-claim-intake.md` — the implementation plan: capacity, load table, YAML schedule block for G01–G25, schedule-check results and cut line, implementation map, full G01–G13 goal entries, phase 2 goals G14–G25 in coarse form, a "later" list, and a Resume-here section.
- `docs/tickets/home-claim-intake/G01-…md` to `G13-…md` — 13 phase 1 tickets in the ticket template. Their front matter matches the plan, as `check_schedule.py` confirmed.
- `REPORT.md` — this file.

One temporary side effect was undone: the `unittest` run created `.claude/skills/adk-system-designer/tests/__pycache__/`, and I deleted it. Nothing is committed.

Not finished, or deliberately left open:

- Every decision is **provisional**: no user confirmed anything, and the design says "draft".
- No provider fact was verified, because network access was not allowed: the Guidewire Cloud API endpoints and replay mechanism (G01), `gemini-3.8-flash` on an EU regional Vertex endpoint, Model Armor and SDP EU regions, and prices (G02). The model choice rests only on the bundled lifecycle snapshot (`checked_on` 2026-10-08).
- The cost per claim is symbolic only (no dated prices).
- ADK 2.8.0 is a working assumption; G03 confirms it.
- Phase 2 goals have no tickets (the user asked for phase 1 only). They have only an estimate, a primary skill and one acceptance check each.
- No implementation, as requested.

## 4. Checks run, and checks not run

Run:

- `python3.12 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/home-claim-intake.md --phase 1 --capacity 690 --days 30 --person …` (Eng A–E and ML at 4.8 h/day, Sec at 1.9)
  - **First run: exit 1.** Fits capacity, but the calendar fit only at the low end: high end 32.4 days against 30, chain G01 → G06 → G13. I also found my hand-written total (287) was wrong; the true figure is 267–418.
  - I fixed it by making G13 depend on G08 instead of G06. The re-check of G06's finished code moved into G14.
  - **Rerun: exit 0.** 267–418 h of 690; chain G01 → G06 → G12 at 16.8–26.0 working days of 30.
- The same script with `--phase 2 --capacity 1540 --days 67`
  - **First run: exit 1.** High end 74.6 days against 67, because G24 depended on G22.
  - I changed G24 to depend on G21.
  - **Rerun: exit 0.** 332–540 h; chain G14 → G21 → G24 at 35.9–61.3 days of 67, about 6 days of margin.
- The phase 1 run again with `--tickets docs/tickets/home-claim-intake/`: **exit 0**. No ticket/plan mismatches.
- `python3.12 -m unittest discover -s tests` in `adk-system-designer`: **8 tests OK**. pytest is not installed, so I used unittest.
- A Python check of every relative Markdown link under `docs/`: no broken links. Anchors were checked by eye, not by script.

Not run:

- Nothing in the application has tests, because there is no code yet.
- No test importing `google.adk` was run (the dependencies are not installed).
- I made no network, cloud, Guidewire or Vertex calls, so every live check named in G01, G02, G05, G07, G10 and G12 is pending.
- I did not run `adk-model-and-output-contracts/scripts/audit_model_config.py`, because there is no model configuration to audit.
- The checker was not run on the default `python3`, which is 3.9.13. I used 3.12 because delivery-profiles asks for 3.11 or later.

## 5. Friction log

**Unsure what to do**

- *Production profile against "phase 1 delivers the profile's done".* `delivery-profiles.md:204-206` says phase 1 delivers the profile's "done", and `:37` defines production "done" as "Agreed SLOs, release gates and recovery are in place and tested". With a five-month deadline that is GA, not a first phase. I made phase 1 an internal staging slice of the production design (6 weeks) and phase 2 the run to the pilot and GA. The skill has no example of a multi-month production plan; its examples at `:246-266` stop at two weeks.
- *A part-time reviewer who reviews other people's work.* The schedule format (`implementation-plan-template.md:37-47`) allows one `owner` per goal, so the security reviewer's review hours on G06 and G08 cannot be charged to them. I made a separate review goal, G13. Its dependency on G06 then broke the calendar; the checker caught this.
- *Headless run against "ask them to confirm or move it".* `SKILL.md:94-95` and `delivery-profiles.md:195-196` ask for confirmation of the cut line. `SKILL.md:122-125` covers headless runs with the Assumed answers table, so I recorded the cut line as A18. This worked, but the two instructions are far apart.
- *Which interpreter to use.* `delivery-profiles.md:173` requires Python 3.11 or later, but the default `python3` here is 3.9. `check_schedule.py` has no version guard. The `$SKILL_DIR` variable in the example command (`delivery-profiles.md:163`) is never defined; I substituted the path.
- *Two run prompts per goal.* The plan's goal entry (`implementation-plan-template.md:93-95`) and the ticket (`ticket-template.md:53-57`) each carry a different prompt for the same work. The closing message (`SKILL.md:276-279`) uses the plan form. I used the plan form for "next prompt".
- *Estimates for production-sized goals.* The starting-point table (`delivery-profiles.md:131-140`) tops out at 16 hours per slice. Goals such as the submission ledger with a Guidewire adapter, or an evaluation set with photo labelling, had no anchor. My 20–60 h figures are my own judgement.
- *What to do with spare capacity.* The resulting phase 1 uses about 60% of capacity after reserve, and the calendar chain is the binding constraint. The skill says what to cut when work does not fit (`delivery-profiles.md:193-197`), but not what to do with a large team that is under-loaded. I added a note to pull G18 and G25 forward.

**Heavier than needed**

- *Plan and tickets duplicate each other.* `SKILL.md:268-271` and `implementation-handoff.md:109-112` ask for full goal entries in the plan and the same content again in tickets. For 13 goals that is about 26 near-duplicate blocks. Generating the tickets from one data source kept them consistent, but a hand-written pass would drift.
- *An assignment-only section in the production template.* `system-design-template.md:123-127` ("Name the deliverable the evaluator will judge … regenerated") applies to assignments. The production rule "every template section either filled or marked not applicable" (`SKILL.md:85-87`) forced an N/A paragraph for it.

**Genuinely helpful**

- *`check_schedule.py`* (`delivery-profiles.md:157-174`). It caught my arithmetic error and two calendar overruns that the hours totals hid. It also confirmed the tickets match the plan. This was the most valuable piece.
- *The model lifecycle table* (`SKILL.md:198-202` pointing to `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`). It ruled out `gemini-3.6-flash` and `gemini-3.7-flash`, which retire on Vertex before GA, and made the choice of `gemini-3.8-flash` traceable without network access.
- *The greenfield version rule* (`SKILL.md:194-197`), with every specialist's `compatibility.md` recording 2.8.0. This made the version assumption quick and defensible.
- *The lethal-trifecta guidance* (`design-decisions.md:182-196`) and the failure scenarios (`failure-review.md:21-43`). Together they led directly to D6, which keeps the ClaimCenter write out of the model's reach, and to the "provider commits, reply is lost" row that shaped D5.
- *The rule for calendar waits* (`delivery-profiles.md:122-126`). Separating waits from hours made the critical-path findings visible: Guidewire, the platform team, the DPIA and the penetration test.

## 6. The exact next prompt the skills told the user to type

The skill's own template, verbatim from `adk-system-designer/SKILL.md:279`:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Filled in for this plan. This is the first line of the plan's "Resume here"
continuation prompt, which then names the skills, scope and acceptance cases
to use:

```text
/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md.
```
