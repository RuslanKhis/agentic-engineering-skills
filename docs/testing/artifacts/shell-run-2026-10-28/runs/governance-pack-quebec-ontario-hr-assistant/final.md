The pack is drafted and the checker passes on all six documents, with no warnings. Nothing has been sent, and every reviewer's sign-off is `pending`.

Everything is in `docs/governance/hr-assistant/`:
- `regulatory-memo.md`
- `privacy-impact-input-pack.md`
- `transfer-assessment.md`
- `impact-assessment.md`
- `system-card.md`
- `security-questionnaire.md`

I also edited `docs/plans/hr-assistant.md`. I added W2–W6, a G06 "Pilot approval" row that depends on them, and a G05 evidence note marked "drafted, not sent". G06's hours and primary skill are placeholders, so check them. I did not draft processing records because they only apply under GDPR or UK GDPR.

**Does Law 25 apply to the leave decisions? Proposed answer: yes, for Montréal staff. This is counsel's call.**
- Érable is headquartered in Montréal with 1,150 Montréal staff, and Law 25 covers an enterprise's Quebec employees.
- The assistant approves leave under two days by rule, with no human review (C3, C4, D5). That is what s 12.1 (decisions based exclusively on automated processing) addresses.
- s 12.1 would require a notice, an explanation on request and a route to a staff member who can review the decision. None of these exists in the design.
- Law 25 also brings in a Quebec privacy impact assessment (s 3.3) and a s 17 assessment for each flow leaving Quebec: Toronto hosting, US model processing and Sydney log access.
- Two points are unsettled. Our reference gives the s 12.1 wording as reported, not confirmed at the source, and does not say whether it covers a favourable decision like an approval. It also does not settle whether Law 25 reaches Toronto staff data held by a Quebec enterprise.

**Regimes in scope**
- **Australia (yes, counsel flag):** only for Southgate Labs' own Sydney log access. The question is whether the Privacy Act reaches it.
- **Canada (yes, counsel flag):** Quebec and Ontario.
- **United States, EU, United Kingdom, New Zealand, Singapore (out):** there is no client, staff or data-subject link in the record. US processing of the model call is a transfer fact, not a US trigger.

**Counsel questions that block the 2026-11-24 pilot decision**
1. Does s 12.1 apply, and what does a compliant notice, explanation and review route look like?
2. Does s 17 adequate protection hold for Toronto, the US and Australia, and is Google's cloud agreement plus a Southgate contract the written agreement?
3. Is express consent needed for leave reasons that may mention health or family matters?
4. Does the Montréal collective agreement require union notice? The references don't cover this, so I only raised it as a question.
5. Does the Charter of the French Language apply? Also uncovered by the references.
6. Does logging prompts with employee IDs mean Toronto's electronic monitoring policy needs updating now?

The memo lists 14 questions in total.

**Gaps, and who should own them**
- **s 12.1 notice, explanation and review route:** adk-operational-guardrails.
- **Screening leave reasons before they reach Gemini, and pseudonymising employee IDs in logs:** protect-adk-sensitive-data.
- **Model retirement date and current processing region:** I couldn't read the model page without network access, so both are `gap:` lines. The design uses the global endpoint, so adk-model-and-output-contracts should also check a regional endpoint.
- **Bias and language split, pilot review share, and confirmation of extracted dates:** adk-agent-evaluation. M3's 1.6% extraction error feeds an unreviewed approval.
- **Kill switch, rollback, incident owner and encryption:** adk-release-engineering.
- **Missing from the record:** the Google, Southgate and UKG contracts, UKG's hosting country, how Sydney staff access logs, and the pilot headcount.
- **Assumption I made:** I assumed Southgate Labs is based in Sydney, which is the skill's default home for the consultancy, supported by the brief.

**Waits to schedule**
- None has a needed-by date within 14 days.
- W2 is counsel's review.
- W3 is Érable's Quebec privacy impact assessment (EFVP).
- W4 is the s 17 assessments and written agreements.
- W5 is union notice, only if counsel requires it.
- W6 is the Ontario monitoring policy update, only if counsel requires it.
- W3–W6 are all needed before the pilot starts.

I did not re-read any law at its source, so every legal date carries the references' `checked 2026-10-26`.

Next step:
```text
/adk-presenter Prepare the pilot-approval presentation from
docs/plans/hr-assistant.md; cite docs/governance/hr-assistant/system-card.md
for limits and oversight, and show the open counsel questions as risks.
```