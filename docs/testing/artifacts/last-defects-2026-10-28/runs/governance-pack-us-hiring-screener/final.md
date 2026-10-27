I drafted the five governance papers for the applicant screener, but I could not run the checker because Bash is disabled in this session. The drafts follow the template structure, but I haven't confirmed they pass its checks. Before they go to Monica Alvarez, run this from the project root:

```bash
python3 -I .claude/skills/adk-governance-pack/scripts/check_governance.py docs/governance/screener/ \
  --source docs/discovery/screener.md --source docs/architecture/screener.md --source docs/plans/screener.md
```

**Files:** `docs/governance/screener/` holds `regulatory-memo.md`, `privacy-impact-input-pack.md`, `impact-assessment.md`, `system-card.md` and `security-questionnaire.md`. All are `status: draft`, `counsel_required: yes`, with sign-off `pending` and Monica Alvarez as the reviewer. I did not draft a processing-records or transfer annex, because EU and UK GDPR are out of scope. I also added waits W2 to W5 and a "drafted, not sent" note under G05 in `docs/plans/screener.md`.

**Can we use it in New York City? (counsel:)** Not yet, and not on the current record.
- **Design scope:** the design puts the New York warehouses out of scope.
- **Audit gap:** NYC Local Law 144 needs an independent bias audit with impact ratios by sex, race and ethnicity. The record has only sex (0.91, M3), nothing on race or ethnicity, and no audit.
- **Notice gap:** the law also needs a candidate notice 10 business days before use, and no alternative-process route is designed.
- **Open for counsel:** whether the tool "substantially assists or replaces" a decision, since recruiters usually bulk-reject the "not recommended" group.
- **Age:** the 0.74 age ratio is outside the audit categories but a separate exposure; federal and state age-discrimination law and New York State and City human rights law are not in my reference, so they are listed as questions, not described.

**Regimes in scope:**
- **Australia:** in scope only through Southgate's own handling, because Sydney engineers read real applications (D4, D5). The client's own APP 1.7 duty is n/a. Whether the Privacy Act reaches US applicants' data is a counsel question.
- **United States:** in scope. The main obligations are:
  - a California risk assessment before pilot processing;
  - California rules on automated hiring tools from 1 January 2027, which an 8-week pilot decided on 2026-11-18 runs past;
  - California's automated-decision regulations on hiring bias (FEHA);
  - Title VII and ADA disparate impact, where 0.74 is below the 0.8 four-fifths line.
- **Out of scope:** EU, UK, New Zealand, Singapore and Canada. Applicants are in California and New York only (brief §3). I assumed any applicants from elsewhere are incidental, which counsel should confirm.
- **EU classification:** none, since the EU is out of scope.

**Facts in the record that are in tension:**
- Recruiters rejecting in bulk (M4: 6% of "not recommended" applications opened) undercuts the claim that a recruiter makes every rejection (R4). It also bears on whether the human review counts as meaningful.
- C4 removes age, but M2 infers age from work-history length. I could not tell whether work-history length feeds the score.

**Gaps and the goal each needs:**
- **Model details:** the model's retirement date, processing region and data-use terms were not read because there is no network. This is a goal for adk-model-and-output-contracts.
- **Measurement:** ratios by race, ethnicity and disability, a threshold for M1 and M4, and the M4 denominator are missing. This is a goal for adk-agent-evaluation.
- **Design:** nothing enforces reading before rejecting, and there is no accommodation route or applicant appeal route. This is a goal for adk-engineer.
- **Facts only Redwood can supply:**
  - revenue and applicant counts for the California privacy-law threshold;
  - applicants' states of residence;
  - contracts with Southgate and Google;
  - retention, log contents and who approves the assessment.

**Blocking questions:** 17 questions are in the memo, numbered so the ones that must close before the pilot can be told apart.

**Waits to schedule:**
- **W2:** General Counsel sign-off, needed before 2026-11-18, so request it the day the drafts go out.
- **W3:** the California risk assessment and approver.
- **W5:** the pre-use notice and opt-out or appeal route, before 1 January 2027.
- **W4:** the NYC bias audit and notice, only if New York use is decided.
- The plan has no pilot-approval goal for these to block. I did not invent one.

**Left undone:** I did not send anything to anyone, fill any sign-off, re-read the law at its source (all dates are "checked 2026-10-26" from the skill references), or draft the client's own documents (the bias audit, the California risk assessment and the pre-use notice).

**Next step:**
```text
/adk-presenter Prepare the California pilot-decision briefing from docs/plans/screener.md; cite docs/governance/screener/system-card.md for limits and oversight, and show the open counsel questions as risks.
```