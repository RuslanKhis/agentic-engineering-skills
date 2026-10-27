---
document: government-form-answers
system: Public enquiries assistant
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: AIAF Accountable Owner at the NSW Trades Licensing Office (agency: to be named)
form: NSW AIAF self-assessment (2024 framework, Excel and offline process)
form_version: The NSW AI Assessment Framework, Digital NSW 2024 (88 pages)
form_url: https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/nsw-ai-assessment-framework
form_checked: 2026-10-26
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md, security-questionnaire.md
---

# Draft answers for NSW AIAF self-assessment: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own order, for the NSW Trades Licensing Office's officers to check and paste into the official tool, where they complete, rate and approve the assessment. Each answer cites the project record, or says who must answer it: `agency:` for what only the agency can answer, `counsel:` for a legal question. Not legal advice.

## Form and version

- **Form:** NSW AI Assessment Framework, Digital NSW 2024, https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/nsw-ai-assessment-framework (checked 2026-10-26).
- **Crosswalk used:** references/au-government-crosswalks.md, verified 2026-10-26 (source: adk-governance-pack reference, read 2026-10-28).
- **Version match:** gap: official page not re-read on 2026-10-28 (no web access); the copy the crosswalk read was a mirror, so its provenance is reported; not confirmed at the source; questions Q14 and Q30 were not recovered; agency: which AIAF version and Excel copy the agency uses.
- **Rating basis the form uses:** the 2024 AIAF rated residual risk; the Operational Policy band is intrinsic (assumption: ratings proposed here are labelled with which one).

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Project sponsor, executive sponsor, technical owner, data governance owner | agency: names; the sponsor and decider is Ruth Abbott (docs/discovery/enquiries.md §5); the records manager is Fiona Lee | gap: other officers not named |
| Approving officer | agency: name and position | gap |
| External suppliers | Southgate Labs as developer; Google as model and cloud provider; Southgate's lead is not a responsible officer | regulatory-memo.md Roles, D1, D6 |

## Draft answers

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| Part 1 | Elevated-risk screen | Proposed elevated risk: generative AI, public-facing, a tool that reads personal information; no administrative decisions or real-world actions; embedded and developed by a consultancy | R2, C2, D1 | agency: classifies |
| Part 2 | Human rights prompts; responsible officers | counsel: human rights; officers agency: | docs/discovery/enquiries.md §5 | counsel: / agency: |
| Info | Name, delivery, phase, contributors, goals, problem, why AI | Pilot of a public enquiries chat assistant; contributors Southgate Labs and the Office; goal fewer calls about status from 17,500 a month; next review is a wait to set (W5) | docs/discovery/enquiries.md §1, §2, §6 | agency: |
| Q1 | Improves on existing approaches against NSW outcome frameworks | Outcome measure is calls about status per month; no pilot result yet | docs/discovery/enquiries.md §2 | agency: |
| Q2 | Non-AI systems considered | gap: not recorded; a login status page is an alternative to record | docs/discovery/enquiries.md §2 | agency: |
| Q3 | Aligns with legislation | PPIP, HRIP, GIPA and State Records Act points are in the memo; counsel: | regulatory-memo.md | counsel: |
| Q4, Q5 | Reversible harms; significant or irreversible harms | H1 disclosure of a third party's status and H2 wrong guidance; handover is the correction path | C4, M1, M2 | counsel: at mid-range or higher |
| Q6 | Secondary or cumulative harms | no memory beyond 90-day transcripts (D3); H3 sensitive disclosures | D3 | agency: |
| Q7, Q8, Q9 | Data selection, availability, quality, representativeness | published guidance and live status data; evaluation set of 400 historical enquiries; gap: representativeness not assessed | M1 | agency: |
| Q10, Q11 | Diversity, inclusion, minority groups | gap: no evaluation by language, accessibility or group | M1 | agency: |
| Q12, Q13 | Performance and fairness targets; monitoring and calibration | 94% correct citation offline, no target recorded; 0 of 250 mismatches; gap: live monitoring and thresholds | M1, M2 | agency: |
| Q14 | Privacy and security by design (text not recovered) | agency: confirm the question; see privacy-impact-input-pack.md and security-questionnaire.md | SB01, SB03, SB05 | agency: |
| Q15 | PIA completed | The input pack supplies facts; the agency's PIA is not done | privacy-impact-input-pack.md | agency: privacy officer (W4) |
| Q16 | Consent or authority for identifiable information | counsel: | privacy-impact-input-pack.md | counsel: |
| Q17 | NSW Cyber Security Policy mandatory requirements | gap: no Maturity Level One evidence; CISO assessment pending | W2, security-questionnaire.md | agency: CISO |
| Q18 | Sensitive information under PPIP s 19 | health and criminal-history disclosures may be typed; no screening | D3, docs/discovery/enquiries.md §3 | counsel: |
| Q19, Q20 | Community consulted; scope and safeguards public | agency: | system-card.md | agency: |
| Q21, Q22 | Appeal route; explanation or reversal | handover to the contact centre; citation shown with answers | C1, C4 | agency: |
| Q23, Q24 | Who is responsible; intervention and over-reliance controls | Accountable Official is the sponsor; gap: stop and rollback owner; no review step | docs/discovery/enquiries.md §5, C4 | agency: |
| Summary | Highest risk per principle | assumption: privacy and security highest (H1, H3); agency: sets | impact-assessment.md | agency: |
| Q25 | Mitigations; independent audits for high risk | see impact-assessment.md Measures | C1, C2, C3, C4 | agency: |
| Q26 | Residual elevated risk and next steps | H3 and H4 high until screening and model-change plan exist | impact-assessment.md | agency: |
| Q27, Q31, Q32 | Treatments as requirements or contract controls; order | planned: screening, AI disclosure, log export, model-change plan (proposed goals) | impact-assessment.md | agency: / counsel: |
| Q28 | Contract clauses sufficient (ICTA Order Form items) | AI module selected; 6.11 at default; model-change notice cannot be met for 2027-02-26; model IDs not in the summary | D1, `docs/contract/order-form-summary.md` | counsel: |
| Q29 | Questions unanswerable because of supplier products | Google model processing region, abuse-monitoring location and data use not recorded | D1, D4 | counsel: / agency: |
| Q30 | Contract framework (text not recovered) | ICTA Customer Contract with Order Form TLO-2026-031 | `docs/contract/order-form-summary.md` | agency: |
| End | Review committee referral, pilot, records, officers' approval | referral within 5 business days if the band is high or critical (W6); pilot decision 2026-12-10 | docs/discovery/enquiries.md §6 | agency: |

## Questions for the agency

- agency: which AIAF version applies, and who are the responsible officers; needed by W5.
- agency: set the band and the review date; needed by W5.

## Questions for counsel

- counsel: human rights alignment (Part 2) and Q3, Q16, Q18; needed by W3.
- counsel: contract sufficiency (Q28): the model-change notice, data location and the model list; needed by W7.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| AIAF Accountable Owner (agency: to be named) | this document | pending | pending |
