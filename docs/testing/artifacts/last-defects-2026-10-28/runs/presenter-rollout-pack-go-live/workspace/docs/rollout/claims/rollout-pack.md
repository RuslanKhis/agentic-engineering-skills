# Rollout pack: claims triage assistant

Go-live: 2026-11-10 · Hypercare: 2026-11-10 to 2026-12-08 (four weeks, plan) · Release: v1.2.0 (assumed, see A2)
Assigned population: 60 triage handlers (Leeds 38, of whom 14 were in the pilot; Dublin 22), 6 team leads (Leeds 4, Dublin 2), 2 claims operations managers
Built from: design [docs/architecture/claims.md](../../architecture/claims.md) (contracts), plan [docs/plans/claims.md](../../plans/claims.md) (evidence, go-live goals), discovery brief [docs/discovery/claims.md](../../discovery/claims.md) (workflow, people plan, counter-metric), operations handover (not yet written, see G1)

## 0. Assumptions and gaps

| Item | Assumption or gap | What depends on it | Who settles it |
| --- | --- | --- | --- |
| A1 | "Two weeks" from today (2026-10-28) is 2026-11-11; the plan records go-live as 2026-11-10 (a Tuesday), so the pack uses the plan's date. | Every date below | Helen Okafor |
| A2 | The go-live build is v1.2.0, the build M2 and M3 were measured on. The plan names no release tag for go-live. M1 was measured on v1.0.3. | Release line; which figures the guide may quote | Tom Reid (Larkspur Digital) |
| A3 | Training dates use the Tuesday and Thursday afternoons the brief allows, in 45-minute sessions (the template default of 90 does not fit the brief). The managers' session on 2026-10-29 is tomorrow and may be too short notice. | Section 4 | Helen Okafor; Aoife Byrne for Dublin |
| A4 | Message senders and send dates are proposals; none is recorded. | Section 5 | Priya Shah (sponsor) |
| A5 | The in-product control uses the scale -1/1 (thumbs down/up) with a category on a thumbs-down. The design (C7) says only that a feedback record is written. | Sections 7, 8 | Tom Reid |
| G1 | No operations handover document yet (G13 in progress). Support tiers below are assumed defaults: tier 1 team lead, tier 2 Fenwick IT service desk, tier 3 Larkspur Digital. | Sections 2, 8, 9 | Fenwick IT lead; Tom Reid |
| G2 | Hypercare exit thresholds are not agreed with Helen Okafor (plan, Hypercare). Section 9 is `Status: proposed`. | Hypercare end on 2026-12-08 | Helen Okafor (Priya Shah as sponsor) |
| G3 | No recorded go-live decision in the plan; it says "planned". | Whether 2026-11-10 holds | Helen Okafor |
| G4 | No measurement for Dublin. M2 and M3 cover Leeds pilot claims only; Irish wordings (D7) have no recorded acceptance result. The guide says so to Dublin staff. | Dublin messaging; first Dublin figures in hypercare | Larkspur Digital; claims MI analyst |
| G5 | Retention period for drafts, notes and feedback is not in the record. Section 2 "Your data" states only what the contracts show. | Your data text | Tom Reid; Fenwick data protection lead |
| G6 | Article 50(2) machine-readable marking of drafts a handler edits and sends: `verify` with counsel. Who is "provider" under the statement of work is not in the record. | Section 6 | Fenwick counsel; Helen Okafor |
| G7 | Whether adoption figures are shown per team only, not per person, is the client's decision and not recorded. Messages assume team level; the manager message asks Helen to confirm. | Manager message | Helen Okafor |
| G8 | Support contacts (names, phone, email) are not in the record and appear as roles. | Quick-reference card | Fenwick IT lead |
| G9 | Exact time stamps for hypercare triage and the weekly "you said, we changed" note owner are not recorded. | Section 8 | Tom Reid |

## 1. What it will and will not do

| Statement for users | Contract |
| --- | --- |
| Will: draft a triage recommendation for a new home claim (type, urgency, cover position) for you to accept or change. | C3 |
| Will: show you only claims in your own team's queue. | C1 |
| Will: name the policy clause each cover position relies on, from that policy's own wording version, or say "none found". | C2 |
| Will: show urgency "high" only for escape of water, fire and uninhabitable home. | C6 |
| Will: let you report a wrong draft from the draft view. | C7 |
| Won't: change a claim's status or route a claim. You triage; the assistant never writes to the claim. | C3 |
| Won't: show a draft when the cover position has no valid clause check; the draft is withheld and you triage by hand. | C2 |
| Won't: send claim notes to the AI model until personal details are removed; if that step fails, no draft is shown. | C4 |
| Won't: show "high" urgency for any other claim type; the urgency field is left blank for you to set. | C6 |
| Hands over: when a draft is withheld or urgency is blank, you triage by hand as you do today. | C2, C6 |
| Hands over: when drafts are paused for the day (spend cap), the banner says "drafts are paused for today" and you triage by hand. | C5 |
| Hands over: a report about a wrong draft goes to your team lead. | C7 |

Known limits (design, deferred controls):
- Motor claims and commercial policies are not supported; the assistant is for home claims only.
- Claims lodged before 2024 have no claim history.
- Handwritten attachments are not read; the draft says "attachment not read". Read them yourself.
- Settling, paying and contacting customers are out of scope; do those as you do today.

## 2. User guide

### Getting started

The assistant opens from the claims queue on your normal Fenwick sign-in (the service runs behind company identity-aware access). Open a new home claim in your team's queue and read the draft that appears: claim type, urgency, cover position and clause. Accept it, or change it and carry on as you do today. Your first try: take your next new home claim, read the draft before opening the policy, then check the cited clause. (Exact link and sign-in screen: to be added by Larkspur Digital before the guide is distributed; not in the record.)

### Asking well

You do not type questions: the assistant drafts from the claim notification and the policy record. What helps it is a complete notification, so:
- Before you accept, check the claim notes say what happened (for example "burst pipe in kitchen, ceiling down"). If notes are thin, the draft will be thin; add what you know.
- In Dublin, the Irish policy wording is indexed with the UK ones (D7). If the clause cited looks like the wrong country's wording, report it (see below).
- If the draft says "attachment not read", open the attachment yourself.

### Checking its answers

A cover position ends with a policy clause reference. Open that clause in the policy and confirm it says what the draft says. Check urgency against what the notification describes, in particular water, fire and uninhabitable homes, which are the only claim types that get "high". Check the claim type. You decide and you are responsible for the triage you save; the draft is a suggestion. If the draft says "none found" for a clause, work out the cover position yourself.

### When it hands over to a person

When a draft is withheld, urgency is blank, or the banner says drafts are paused for today, triage the claim by hand. Nothing is lost; the claim stays in your queue. If the report you make needs a decision, your team lead gets a message (C7).

### Reporting a problem

Use "report a problem" in the draft view. Choose what went wrong (wrong or made-up answer; could not do the task; too slow; unsafe or inappropriate; something else). Free text is optional; do not put customer names, addresses or policy numbers in it. If you think a customer could be harmed, a claim was changed by the assistant, or personal data was exposed, do not only use the control: also contact your team lead and the Fenwick IT service desk straight away, who log it as an incident (assumed tiers, G1).

### Your data

- Claim notes are de-identified before they reach the AI model (C4).
- The assistant reads the policy record and claim history read-only (C3).
- Do not paste claim details, customer names or policy numbers into other AI tools, such as public chatbots. This assistant is the approved tool for claims triage.
- How long drafts and feedback are stored, and who can see them: not yet confirmed (G5); the final guide will state it.

How well it works (measured): in the September 2026 pilot, median triage time was 13 minutes against a 21-minute baseline, on 1,184 pilot claims in Leeds (M1, v1.0.3). From 1 to 24 October 2026, handlers accepted 71% of 980 drafts without change in Leeds (M2, v1.2.0); this shows how often drafts were kept, not that they were correct. Re-routing after triage was 8.2% against a 9% baseline on 980 pilot claims (M3, v1.2.0). Dublin: not yet measured (G4).

## 3. Quick-reference card

**It will (3):**
1. Draft type, urgency and cover position for a new home claim (C3).
2. Cite the policy clause, or say none found (C2).
3. Show you only your team's claims (C1).

**It won't (3):**
1. Change or route a claim (C3).
2. Show "high" urgency outside escape of water, fire, uninhabitable home (C6).
3. Handle motor claims or read handwritten attachments (design limits).

**How to check:** open the cited clause; check type and urgency against the notification; you decide.
**How to report:** "report a problem" in the draft view; for harm, a changed claim or exposed data also call your team lead and the service desk.
**Who to call:** team lead first; Fenwick IT service desk second; Larkspur Digital hypercare contact third (names and numbers to be added, G8).
**Remember:** it is an AI assistant and can make mistakes.

## 4. Training plan

| Session | Audience | Minutes | Objectives | Practice on | Trainer | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Managers and champions | 6 team leads (Leeds 4, Dublin 2), 5 Leeds champions, Aoife Byrne, 2 operations managers | 45 | Coach the first week; answer the top questions; read the weekly figures; handle reports | Their team's real claims; the will/won't table | Larkspur Digital trainer with Helen Okafor | 2026-10-29 |
| Dublin handlers | 22 Dublin handlers | 45 | Use, check, hand over, report | Own Irish-policy claims | Aoife Byrne, with Larkspur Digital | 2026-11-03 |
| Leeds handlers, new | 24 Leeds handlers not in the pilot | 45 | Use, check, hand over, report | Own claims | Leeds champions | 2026-11-05 |
| Leeds pilot handlers | 14 pilot handlers | 45 | What has changed since the pilot (urgency table, report a problem, Dublin) | Own claims | Leeds champions | 2026-11-05 |

Train managers and champions first. Attendance is recorded (AI literacy, EU AI Act Article 4); owner: Larkspur Digital trainer, kept with the plan. Industry surveys associate more training time with regular use; this plan has 45 minutes a person, and whether that is enough is a hypercare question, not a promise. If the Leeds 24 need a second slot, Tuesday 2026-11-10 is go-live day: raise with Helen Okafor.

## 5. Rollout messages

### Sponsor

Briefing to the sponsor (from Helen Okafor, 2026-10-30, by email and 15-minute call with Priya Shah): Why now: the pilot cut median triage time to 13 minutes from 21 (M1) and Dublin is ready (G11 done). Measure: median triage time per claim, monthly, against 21 minutes. Counter-metric: re-routing rate after triage, 8.2% in October (M3) against 9% baseline; if it exceeds 9% in any month the urgency field is paused until the cause is found. Success at the end of hypercare: the exit test in section 9, once you and Helen agree it (G2). Your visible action: use your own login to look at the monthly figures, and mention the assistant in your next leadership meeting in the week of 2026-11-09.

Announcement the sponsor sends (sender: Priya Shah, 2026-11-05, email to all triage handlers, team leads and claims operations in Leeds and Dublin):

> From 10 November, home-claims triage in Leeds and Dublin gets an AI assistant. It drafts a claim type, urgency and cover position, with the policy clause it relies on. You decide; it never changes or routes a claim. In the pilot, median triage time fell from 21 to 13 minutes in Leeds, and we are watching that re-routing does not rise. It can make mistakes, so check the clause before you accept. Training is booked with your team lead; report anything wrong from the draft view. This is the approved tool for claims; please do not put claim details into other AI tools. — Priya

### Middle managers

Sender: Helen Okafor · Date: 2026-10-29 (after the managers' session) · Channel: email to the 6 team leads and 2 operations managers

> What changes: your handlers will see an AI draft on every new home claim from 10 November. The handler still decides. In week one: sit with each handler for one claim, ask them to open the cited clause, and note anything odd. Coach on checking, not on acceptance: 71% of drafts were kept unchanged in the Leeds pilot (M2) and that is not a target. Reports about wrong drafts reach you (C7); review changed drafts weekly. Harm, a changed claim or exposed data go to the Fenwick IT service desk as well. You will see team-level figures: triage time, re-routing rate, weekly active share. Please confirm with me whether figures are team-only, not used to rank individuals; I will confirm before 2026-11-05 (G7). Dublin: no figures yet for Irish policies, so tell us early what you see (G4).

### Frontline users

Sender: team leads (Leeds: Leeds team leads; Dublin: Aoife Byrne) · Date: 2026-11-05, forwarding Priya Shah's announcement · Channel: team email and team meeting

> From Tuesday 10 November you will see a draft triage on new home claims. It saves you re-reading policy wordings; it does not replace you. What does not change: you decide claim type, urgency, cover and routing, and you are responsible for what you save. What it will not do: change or route a claim, contact a customer, or handle motor claims. How to check: open the clause it cites; check urgency against what the customer described. "High" urgency appears only for escape of water, fire and uninhabitable homes. If a draft is withheld, triage as you do now. Use "report a problem" for anything wrong, and tell me if you are worried about how it will be used; we will answer in the session. Please do not put claim details into any other AI tool. Training: your session is booked on the date in your invitation.

## 6. AI disclosure

Status: applies (Dublin handlers are EU users; the Leeds users use the same service). Provider and Article 50(2) marking: verify (G6).
Text: "You are using an AI assistant. It drafts a triage recommendation and can make mistakes. Check the cited policy clause and the urgency before you accept; you decide."
Shown: on the first screen before the first draft is shown, as a permanent label above the draft in the draft view, and on the about page. No voice channel.

## 7. Adoption metrics

| Metric | Definition | Source | Target | Window |
| --- | --- | --- | --- | --- |
| Assigned population | Users given access, by team | access list | 60 handlers (Leeds 38, Dublin 22) | at go-live |
| Active user | A distinct opaque user_id with at least 1 completed invocation (a final response, not an error or abandoned turn) | analytics table (G07 usage reporting) | proposed 80% of assigned (not agreed, G2) | 7 days rolling |
| Weekly active rate | Active users ÷ assigned population | analytics table | proposed 80% | 7 days rolling |
| Activation | Share of assigned users with a first completed invocation within 14 days of access | analytics table | proposed 90% | 14 days |
| Outcome measure | Median triage time per claim (claims MI report), against 21 minutes | claims MI report | below 21 minutes; pilot value 13 (M1) | monthly |
| Counter-metric | Re-routing rate after triage, threshold 9%; above it in any month pauses the urgency field | claims MI report | at or below 9% (M3: 8.2%) | monthly |
| Negative feedback share | Thumbs-down ÷ rated invocations | feedback table | proposed at or below 15% | last 2 weeks |

Handlers use it for every claim, about 30 a day each (brief), so a week is the right active-user window. Figures reported go into the plan as measurement records (M4 onward). Log-ins, messages and conversation counts are vanity counts: appendix only, not reported here. Targets marked proposed are not in the record and need agreement (G2).

## 8. Feedback channel

Record: the observability feedback record (session_id, invocation_id, score, category, optional de-identified free text). Scale assumed -1/1 (A5).

| User action | Record category | Route | Owner | Response |
| --- | --- | --- | --- | --- |
| Wrong or made-up answer | wrong_answer | "report a problem" → feedback record → feedback table; message to team lead (C7) | Team lead; Larkspur Digital triages | Daily triage in hypercare; weekly "you said, we changed" note |
| Could not do the task | tool_failed | same route | Larkspur Digital | same |
| Too slow | too_slow | same route | Larkspur Digital | same |
| Unsafe or inappropriate | unsafe | same route, and also service desk as an incident | Fenwick IT service desk; Larkspur Digital tier 3 (assumed, G1) | same working day, assumed |
| Something else | other | same route | Team lead | weekly |

## 9. Hypercare exit test

Status: proposed. Not yet agreed with Helen Okafor or Priya Shah (G2). Every figure below other than the 9% counter-metric is a proposal, not a record.

| Criterion | Threshold | Window | Source | Owner |
| --- | --- | --- | --- | --- |
| Severity 1 or 2 incidents open | 0 | 10 consecutive working days | incident log | Larkspur Digital hypercare lead |
| Weekly active rate | ≥ 80% of assigned | last 2 weeks | analytics table | Larkspur Digital |
| Counter-metric (re-routing rate) | ≤ 9% | last 4 weeks | claims MI report | claims MI analyst |
| Negative feedback share | ≤ 15% of rated invocations | last 2 weeks | feedback table | Larkspur Digital |
| Tickets resolved by client tiers | ≥ 70% | last 2 weeks | service desk | Fenwick IT lead |
| Operations handover acceptance | passed | at exit | handover document (G13) | Fenwick IT lead |

If the test fails on 2026-12-08: extend by two weeks with the named fix, or take the rollback decision to Helen Okafor; hypercare does not end silently.
