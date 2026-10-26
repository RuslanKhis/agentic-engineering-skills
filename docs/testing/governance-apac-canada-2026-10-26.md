# Governance pack: New Zealand, Singapore, Canada and AU government forms

*26 October 2026. Skill: `skills/adk-governance-pack`. Branch:
`governance-apac-canada`, on top of the drafting-aid, sign-off and
law-freshness work (step 1). Research:
[New Zealand](../research/nz-ai-privacy-law-2026-10-26.md),
[Singapore](../research/sg-ai-privacy-law-2026-10-26.md),
[Canada](../research/ca-ai-privacy-law-2026-10-26.md),
[AU government forms and NSW law](../research/au-government-forms-nsw-2026-10-26.md).*

The consultancy is in Sydney, with NSW government work coming and
Commonwealth agencies possible. The owner asked for New Zealand, Singapore
and Canada at screen depth, crosswalks (not copies) for the official
Australian government forms, and deeper NSW state law, and said: "no skill
can substitute a real lawyer being in the company. Those should be only
considered as a supporting tools."

## What changed

- **Screen.** Seven regimes in the order au, us, eu, uk, nz, sg, ca. Canada
  is matched by Canada, Canadian or Quebec, never CA (California).
- **Old four-row screens are now an error.** A memo or POC note whose screen
  names only Australia, the United States, the EU and the UK fails with
  "names no row for New Zealand" (and Singapore, Canada) plus a fix message
  saying the screen now covers seven regimes. Chosen because a regime left
  out without a recorded reason is the failure the screen exists to stop;
  adding three `n/a:` rows is a small fix.
- **References** (each with a verified line): `new-zealand.md`,
  `singapore.md`, `canada.md` (180 days) and `au-government-crosswalks.md`
  (90 days, because forms change faster than laws). `australia.md` gains a
  NSW government clients section; NSW statute wording not read at
  legislation.nsw.gov.au says "re-read the section at the source".
- **Templates.** New `government-form-answers-template.md`. Memo and
  input-pack sections for each new regime (required by the checker); an
  optional "Australia: Government client" memo section and "Australia: NSW
  IPP and HPP check" input-pack section; transfer-annex sections for New
  Zealand (s 11 and IPP 12), Singapore (Transfer Limitation Obligation) and
  Canada (Quebec s 17 and Alberta); optional impact-assessment sections for
  New Zealand, Singapore, Canada and NSW AIAF inputs; system-card and
  questionnaire rows. Every template keeps the banner and sign-off.
- **Transfer annex decisions.** Allowed for eu, uk, nz, sg, ca. New Zealand
  gets an annex because Gemini lists no New Zealand processing region, so
  every design processes offshore and the s 11 facts need a row per party.
  Australian APP 8 and NSW s 19(2) facts stay in the input pack (use or
  disclosure facts in the recipients table, as before).
- **Checker.** `agency:` marker (counted in the summary);
  `government-form-answers` with required sections, `form`, `form_version`,
  `form_url`, a real `form_checked` date, a "not the official form" sentence
  and a warning after 90 days; new date-check references (IPPs, Biometric
  Processing Privacy Code, PDPA, PDPC, Do Not Call, PIPEDA, Law 25,
  Directive on Automated Decision-Making, AIA, PPIP Act, HRIP Act, GIPA,
  DCS-2026-02, ICTA, DTA) and `Act,?\s20\d\d`; new counsel triggers (NSW
  and state agencies, AIAF, AI Review Committee, State contract, NZ and
  Singapore public bodies, Canadian federal departments, AIA level,
  exclusively automated decisions, emotion inference, health information
  custodians, critical information infrastructure).
- **Wiring.** adk-engineer routing, designer governance goal, hand-off and
  scoping question, practice-profile interview menu, README, CHANGELOG
  (Unreleased), refresh runbook. `profile.py` does not restrict
  jurisdiction codes, so only the interview menu changed; the shared
  `references/practice-profile.md` did not change.

## Checks

| Layer | Result |
| --- | --- |
| Checker suite (`skills/adk-governance-pack/tests`) | 62 tests pass on Python 3.9 (`python3 -I`) and 3.11 |
| Package validation | 25 packages, 0 errors, 0 warnings; governance `SKILL.md` 440 lines, description 1,017 characters |
| Full `scripts/check_repo.py` (scratchpad Python 3.12 virtual environment from `requirements-dev.txt`; the worktree has no `.venv`) | Passed: 1,022 tests run, 59 optional SDK checks skipped |
| Evaluation cases | 4 activation positives and 4 scenarios appended; structure valid, model activation not run |
| Legal facts | Only items a note marks primary are stated as fact, with `checked 2026-10-26`; secondary items say "reported; not confirmed at the source on 2026-10-26" or are left out |

## Trials

Three fresh general-purpose subagents (model inherited from the coordinator,
Claude Opus 5.5), each given only the skill's `SKILL.md` path, a project
directory with a synthetic brief, design and plan, and one request. No web
access, no practice profile. Fixtures and outputs are in the session
scratchpad under `governance-trials-2/`, outside the repository.

| Trial | Fixture (sha256 prefix: brief, design, plan) | Request | Expected screen |
| --- | --- | --- | --- |
| T1 | `nsw-chatbot`: `7776665d`, `e8d14dcb`, `b1736909` | Fictional NSW agency's public grants chatbot; status lookup; Gemini retiring 2027-02-26 under an ICTA Order Form with the default notice; abuse-monitoring location unknown; error bodies to a US tracker; one support engineer in Melbourne | `[au]`, NSW material |
| T2 | `nz-sg-retail`: `2c340f0a`, `d5bff81e`, `a045fdf7` | Auckland retailer with a Singapore subsidiary; automatic store credit; Sydney trace access; evaluation sets reused across the consultancy's clients; no Singapore contract | `[au, nz, sg]` |
| T3 | `qc-on-hr`: `75cf592d`, `2ceace20`, `6c477524` | Montréal employer with Ontario staff; leave under two days approved with no review; Toronto hosting, US model processing, Sydney log access; prompts logged with employee IDs | `[au, ca]` |

### Outcomes, inspected by the coordinator

| Assertion | T1 | T2 | T3 |
| --- | --- | --- | --- |
| Screen picks the right regimes in order, seven rows, a reason for each left out | Pass: `[au]`; US tracker treated as a flow outside NSW, not a US trigger | Pass: `[au, nz, sg]`; Zendesk US storage a transfer fact, not a US trigger | Pass: `[au, ca]`; US model processing an s 17 and PIPEDA fact |
| Regime sections only for regimes in scope | Pass: no annex or records; NSW sections and two form answers documents | Pass: annex with New Zealand and Singapore sections | Pass: annex with the Canada section |
| Government forms | Pass: AIAF registration and 2024 AIAF answers with form, version, URL and checked date, "not the official form", officer fields `agency:` (12 and 19 agency questions) | n/a | n/a |
| Key judgements | Gemini retirement inside the six-month ICTA notice window raised as a gap and a counsel question; s 19(2) per flow (Melbourne, Sentry, abuse store); s 7B(5), GIPA s 121, State records, ML1 | Reuse of evaluation sets across clients flagged as possibly breaking the s 11 agent and data intermediary roles; no Singapore contract a gap and a wait; NRIC in free text a gap | Automatic leave approval a likely s 12.1 decision, answered in the Summary as `counsel:`; s 3.3 PIA and s 17 per flow; Ontario monitoring policy and union consultation waits |
| Banner, sign-off, no reviewer decision filled | Pass: all drafts `status: draft`, every decision and date `pending` | Pass | Pass |
| Final checker | Exit 0 | Exit 0 | Exit 0 |
| Ease (agent's score) | 3 of 5 | 3 of 5 | 3 of 5 |

After the fixes below, the coordinator reran the final checker on all three
packs unchanged: all 19 drafts still pass.

## Friction log and what changed

| # | Friction (trial) | Change |
| --- | --- | --- |
| 1 | APP sections required for a NSW agency, whose own handling is under the PPIP and HRIP Acts (T1) | SKILL.md and template comments: for a NSW agency the APP sections cover the consultancy's handling outside s 7B(5) and give `n/a:` for the agency's |
| 2 | No impact-assessment home for NSW AIAF inputs (T1) | New optional "Australia: NSW AIAF inputs" section; the DTA section keeps only DTA forms |
| 3 | No offline fallback for form pages, and no rule for a version that cannot be read (T1) | Crosswalks, template and SKILL.md: take version and checked date from the crosswalk and write the re-read as `gap:`; the 90-day warning tracks the true age |
| 4 | Registration questions R1 to R4 read as design IDs (T1) | Renamed "Reg 1" to "Reg 4"; rule that question numbers never look like R, C, M or D IDs |
| 5 | Which NSW assessment version to draft (T1) | Crosswalks: draft the 2024 AIAF and ask the agency which it uses (`agency:`) |
| 6 | Several reviewers, one `for:` (T1, T2) | Crosswalks: who signs each document for a government client; extra sign-off rows |
| 7 | Conditional waits and "before production" waits without a production goal (T1) | SKILL.md hand-over rule |
| 8 | Memo template had no home for the documents the client produces (T3) | Bullet under Applicable dates |
| 9 | Canada reference asks for a per-flow law table the template lacked (T3) | Table added to "Canada: Privacy laws and roles" |
| 10 | Unanswered Canadian questions: Quebec Act and Ontario staff, s 12.1 and favourable decisions, French language law, monitoring policy updates (T3) | Added to `canada.md` as counsel questions, never described |
| 11 | Recipients table said "processor", against the Canadian wording rule (T3) | Heading now names processor, service provider, agent or data intermediary "in the regime's own word" |
| 12 | Model processing region recorded in the design with a date, unclear whether citable (T2, T3) | SKILL.md: cite it through the design's ID with its date and "not re-read" |
| 13 | Ontario human rights checklist only under federal AIA inputs (T3) | Adverse impact section gains regime checklists (Ontario, New Zealand, Singapore) |
| 14 | `australia.md` is long and mostly NSW when Australia is in only through the consultancy (T2, T3) | "Which sections to read" pointer at the top; the s 5B reach question named as `counsel:` |
| 15 | Input pack's own New Zealand row fired the biometrics trigger (T2) | Row reworded; naming the Biometric Processing Privacy Code does not trigger; test |
| 16 | "Store credit decisions" fired the credit trigger (T2) | `credit decision` no longer matches after "store"; test |
| 17 | A "reported; not confirmed at the source on <date>" line failed cite-or-flag (T2) | Counted as a dated flag; a bare "reported" still fails; test |
| 18 | Intra-group transfer had no annex prompt; unclear whether the annex lists `au` (T2) | Example row for a subsidiary's data in the parent's systems; comment: same codes as the other drafts |
| 19 | Checker docstring still said "four regimes" (T1) | Fixed |

Not changed, with reasons:
- **Source triggers for an unreviewed small money decision, a guest chat with
  no age check, or health details in free text** (T2): these are judgement
  calls the SKILL already tells the drafter to make; a phrase list that
  fired on them would fire on most retail chat agents.
- **Workplace surveillance as a counsel trigger** (proposed in the NSW
  note): not a clear high-stakes case, and "Workplace Surveillance Act" in a
  row that then says `n/a:` would fire. It stays a screen row and a counsel
  question.
- **NRIC as a counsel trigger** (proposed in the Singapore note): collecting
  an identity number is not by itself high-stakes; it stays a necessity line
  and a masking contract.
- **Bare "health information" as a trigger** (proposed in the NSW note):
  too broad for free-text chat agents; the HRIP Act, HIPC, PHIPA custodians
  and personal health information trigger instead.
- **Missing `docs/` files in front matter `sources:`** are not warned on
  (T3): harmless, and the body citation already warns.
- **New Zealand and Singapore consumer law beyond the Fair Trading Act**
  (T2): not researched; drafts name it as a counsel question.
- **Reading load** (all three): references are read by section; the
  `australia.md` pointer is the first step. Splitting references further
  was not done in this change.

## Limits

The trials checked form and judgement on synthetic records, not the law. No
counsel reviewed the drafts. Quebec section wording, the Directive on
Automated Decision-Making text, NSW statute text and the NZ Biometric Code's
own text were not read at the source and are marked so. The AIAF Platform's
question set is not public; the crosswalk uses the published baseline
questions and the 2024 framework.
