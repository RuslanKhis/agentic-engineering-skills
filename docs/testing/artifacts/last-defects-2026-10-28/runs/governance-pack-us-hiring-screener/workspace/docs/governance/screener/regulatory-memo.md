---
document: regulatory-memo
system: applicant screener (build v0.5.2)
version: design accepted 2026-09-02; build v0.5.2 (docs/plans/screener.md M1)
status: draft
jurisdictions: [au, us]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Monica Alvarez, General Counsel, Redwood Freight Inc.
sources: docs/discovery/screener.md, docs/architecture/screener.md, docs/plans/screener.md
---

# Regulatory memo: applicant screener

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Redwood Freight's counsel. It records which regimes the jurisdiction
screen found in scope, the facts the design records, and the provisions that
appear relevant in Australia and the United States, neither of which has an AI
Act or assigns a risk tier. Conclusions are proposals for counsel; not legal
advice. Law was taken from the skill references read 2026-10-26 and not re-read
at the primary source in this session (no network access); re-read anything a
decision rests on.

## Summary

- **Regimes in scope:** Australia (only through Southgate Labs' own handling) and United States (Jurisdiction screen below; counsel: confirm the screen).
- **Direct answer, can we use it in New York City?** counsel: Proposed answer: **not yet, and not on the current record.** The design puts the New York warehouses out of scope (docs/architecture/screener.md Scope gate), and NYC Local Law 144 would require, before any use on NYC candidates, an independent bias audit within a year before use with impact ratios by sex, race and ethnicity and their intersections, a published summary, and notice 10 business days before use (checked 2026-10-26, United States reference). The record holds an impact ratio by sex only (M3, 0.91), none by race or ethnicity (gap), and no audit, notice or alternative-process route (gap). Whether the tool "substantially assists or replaces" discretionary decisions is counsel's call; the facts point toward yes (ranks and labels R2, C3; recruiters usually reject "not recommended" in bulk, source: requester (Southgate Labs), 2026-10-28; M4 6% opened). The age ratio of 0.74 (M2) is outside what the audit categories cover in the reference, but is a separate exposure counsel must clear before any use (see Questions for counsel).
- **Main obligations in the other regimes:** United States: California risk assessment before the pilot processing begins (CPPA §7150(b), from 1 January 2026, checked 2026-10-26); automated decision-making technology (ADMT) duties from 1 January 2027 (checked 2026-10-26), which an 8-week pilot decided 2026-11-18 straddles (docs/discovery/screener.md §6, docs/architecture/screener.md Scope gate); California FEHA automated-decision system regulations in force 1 October 2025 (checked 2026-10-26); Title VII and ADA disparate impact with the four-fifths rule (29 CFR 1607.4(D)), against which the age ratio 0.74 (M2) is below 0.8. Australia: APP duties of Southgate Labs for the evaluation set and logs its Sydney engineers read (D4, D5); the client's own APP 1.7 duty is n/a.
- **Proposed roles:** Redwood as CCPA business and the employer; Southgate Labs as service provider or contractor and possibly an FEHA "agent"; Southgate as an APP entity in its own right for its Sydney handling (Roles below; counsel: confirm).
- **Proposed readiness:** counsel: the California pilot should not start until the gating items in Questions for counsel 1 to 6 close; the bulk-rejection pattern (M4) is the largest single fact against treating review as meaningful.
- **Blocking questions:** counsel: 17 questions, listed under Questions for counsel.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes (gap: Southgate Labs' turnover and contract terms not in the record) | Two Southgate engineers in Sydney read the evaluation set of real past applications and logs (D4, D5); consultancy home Australia, assumption: consultancy home Australia (default) | The consultancy's own handling only; counsel: whether the Privacy Act reaches US applicants' data read from Sydney. The client's own APP 1.7 and sector rows are n/a: client is US-established and applicants are in California and New York (docs/discovery/screener.md §1, §3) |
| United States | yes | Delaware corporation headquartered in Oakland, California; applicants in California and New York; six California and two New York City warehouses (docs/discovery/screener.md §1, §3) | Client is established and does business in the US; applicants are US residents; employment use |
| EU | no | Applicants are in California and New York (docs/discovery/screener.md §3); no EU establishment or EU output use | n/a: no EU client, data subject or output use; assumption: job-board applicants from the EU are incidental; counsel: confirm |
| United Kingdom | no | Same facts (docs/discovery/screener.md §1, §3) | n/a: no UK client, data subject or output use; assumption: UK applicants are incidental; counsel: confirm |
| New Zealand | no | Same facts (docs/discovery/screener.md §3); Southgate staff are in Sydney only (D4) | n/a: no NZ client or data subject; no NZ data accessed from Australia on the record |
| Singapore | no | Same facts (docs/discovery/screener.md §3) | n/a: no Singapore client or data subject |
| Canada | no | Same facts (docs/discovery/screener.md §3) | n/a: no Canadian client, data subject or province recorded |

- **Processing locations:** Cloud Run in us-west1 (Oregon) and BigQuery for scores (docs/architecture/screener.md Scope gate, D2); Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in us-west1 (D1); model processing region and retirement date gap: not read from the model page (no network access in this session), proposed goal for adk-model-and-output-contracts; logs, backups and BigQuery region gap: not recorded; Southgate access from Sydney (D4).
- **Government client:** private client, Redwood Freight Inc. (docs/discovery/screener.md §1); n/a: no Commonwealth, NSW or other agency client, so no government form answers are drafted.

## System and intended purpose

- **What it does:** scores each application 0-100 against the role's requirements, ranks per requisition and labels scores under 40 "not recommended" (R1, R2, C3).
- **Who uses it and who it affects:** 11 recruiters in Oakland and 3 in New York use it; it affects applicants for warehouse associate and forklift operator roles, about 9,000 applications a month across Redwood (docs/discovery/screener.md §1, §2, §5). The pilot is California warehouses for 8 weeks; New York use is not decided (docs/architecture/screener.md Scope gate, docs/discovery/screener.md §6).
- **What the model decides and what code or people decide:** the model produces the score and the requirements evidence (C1); code applies the under-40 label (C3) and removes age, date of birth, graduation years and photos before scoring (C4); a recruiter makes every rejection (R4), the screener never changes an application's stage in Greenhouse (C2).
- **Effects it can cause:** writes a score, rank and label to a Greenhouse custom field and BigQuery (D2); recruiters see "not recommended" applicants in a collapsed group they can open (D3). It does not reject or message applicants (docs/architecture/screener.md Scope gate).
- **Human review of decisions about people:** a recruiter makes each rejection (R4, C2). Recruiters usually reject "not recommended" applicants in bulk (source: requester (Southgate Labs), 2026-10-28), and M4 records 6% of "not recommended" applications opened before rejecting (shadow trial of 410 applications, 2026-10-06 to 2026-10-17, build v0.5.2). gap: the denominator of M4 (all 410, or only those rejected) and whether the trial included New York recruiters.

## Roles

- **Facts:** Redwood commissions it, runs it in its Greenhouse and decides (Kevin Ortiz, sponsor and decider, docs/discovery/screener.md §5); Southgate Labs built it and its engineers in Sydney read the evaluation set and logs during the build and a three-month support period (D4). gap: contract between Redwood and Southgate, whose Google Cloud project and billing hold the stack (docs/architecture/screener.md Scope gate does not say), and any contract with Google.
- **Australia, Privacy Act:** Southgate Labs may be an APP entity in its own right if its turnover is above $3 million; the employee-records exemption does not cover unsuccessful applicants or recruitment providers working under contract (australia reference, checked 2026-10-26); gap: Southgate's turnover (counsel: confirm; also whether the Act reaches information of US applicants read from Sydney, which the reference leaves to counsel).
- **United States:** Redwood is the CCPA business if it meets a threshold (gap: revenue and consumer counts not in the record; 9,000 applications a month suggests 100,000 or more a year, assumption: not verified, docs/discovery/screener.md §1); Southgate and Google as service providers or contractors (counsel: confirm; no contract in the record); under the California FEHA regulations an agent acting for the employer, including through an automated-decision system, is itself an employer (§11008(a), checked 2026-10-26), so Southgate's liability as agent is counsel's question; that a vendor can be liable as the employer's agent is tested in *Mobley v. Workday*, reported; not confirmed at the source on 2026-10-26.

## Australia: Privacy Act and APPs

Scoped to Southgate Labs' own handling in Sydney only (D4, D5); the client's own APP duties are n/a: Redwood is US-established with US applicants (docs/discovery/screener.md §1, §3).

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed, and obligations come from the laws screened here (checked 2026-10-26).
- **APPs engaged:** APP 3 and 3.3 (free text in applications may reveal age, disability, national origin, docs/discovery/screener.md §3), APP 5, APP 6 (evaluation use of past applications, D5), APP 8, APP 10, APP 11, APPs 12 and 13 for the evaluation set and logs (privacy-impact-input-pack.md; D4, D5).
- **Overseas disclosure (APP 8, s 16C):** the stack runs in us-west1, outside Australia (docs/architecture/screener.md Scope gate, D1); Sydney access is staff reading data held in the US (D4); gap: model processing region, abuse-monitoring storage and support access not read from the model page; counsel: use or disclosure, and whether Southgate or Redwood is the disclosing entity.
- **Notifiable data breaches:** gap: no breach contract term or owner in the record; counsel: which entity assesses within 30 days and notifies if Southgate is an APP entity (security-questionnaire.md; checked 2026-10-26).
- **Pending, not law:** the tranche 2 exposure draft (Privacy Amendment (Personal Data Protection) Bill 2026) is not law (checked 2026-10-26).

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| n/a: Southgate Labs makes no decision about a person; the hiring decisions are Redwood's, a US employer with US applicants, so APP 1.7 is not Redwood's duty on the record | n/a: client outside the Privacy Act on the record | M4 for the US workflow (6%; denominator gap:) | n/a: not assessed under APP 1.7 | n/a | R4, M4; counsel: confirm the n/a, noting APP 1.7 commences 10 December 2026 (checked 2026-10-26) |

- **Privacy policy inputs (APP 1.8):** n/a: client's own APP 1.7 row is n/a; the system card's automated-decision disclosure supplies the facts to Redwood's US notices (system-card.md; C1, C3).

## Australia: Sector, state and government AI policy

- **Sector laws:** n/a: no Australian client, workplace surveillance, health, financial or consumer-facing use (docs/discovery/screener.md §1); counsel: confirm no Australian-law employment angle for Southgate's own staff reviewing real applications.
- **Government AI policy:** n/a: private client, not a Commonwealth or NSW agency (docs/discovery/screener.md §1).

## United States: Preemption status and FTC claims

- **Federal preemption:** no federal statute preempts the state laws screened below; EO 14365 preempts nothing by itself; a federal court order of 27 April 2026 stops enforcement of Colorado's SB 24-205 pending rulemaking and *X.AI v. Weiser* (all checked 2026-10-26; United States reference). No Colorado applicants are recorded (docs/discovery/screener.md §3).
- **FTC Act Section 5:** any public claim about accuracy, fairness or "bias-free" needs competent and reliable evidence (Workado order, checked 2026-10-26). The only measure is M1, 78% agreement with recruiter advance decisions in a backtest of 6,000 past applications; it measures agreement with past human decisions, not accuracy or fairness. gap: no public claim recorded; none should be made beyond M1 as defined. The FTC said on 7 August 2026 it will not bring disparate-impact claims under Section 5; disparate treatment, private plaintiffs and states are unaffected (checked 2026-10-26).

## United States: Automated decisions and state AI laws

- **CPPA ADMT and risk assessment:** California treats an applicant as a consumer and hiring as a "significant decision"; assessments are required before new in-scope processing from 1 January 2026 and ADMT duties (pre-use notice, opt-out or human appeal, access) apply from 1 January 2027 (all checked 2026-10-26). The pilot decision is 2026-11-18 and 8 weeks later is at the earliest 2027-01-13 (docs/discovery/screener.md §6, docs/architecture/screener.md Scope gate; assumption: the pilot starts on the decision date). The human-review exclusion needs a reviewer who can interpret the output (C1 shows requirements met and missed), reviews it with other information (M4 suggests not for "not recommended" applicants, 6% opened) and has authority to change it (R4, C2). counsel: ADMT or not, and whether notices are needed from the pilot's first day.
- **Colorado SB 26-189 and other state AI laws:** consequential decisions from 1 January 2027 (checked 2026-10-26) apply only to Colorado consumers; none recorded (docs/discovery/screener.md §3); gap: applicants' states of residence beyond California and New York, since the careers site and job boards are open (docs/discovery/screener.md §1). Illinois HB 3773 is reported; not confirmed at the source on 2026-10-26: screen it for any Illinois applicant (counsel:).
- **Chatbot and companion laws:** n/a: no conversational interface, no applicant messaging (docs/architecture/screener.md Scope gate, R1 to R4).

## United States: Privacy, sector and employment laws

- **State privacy laws:** California's CCPA applies to applicants only if Redwood meets a business threshold (gap: revenue and counts, docs/discovery/screener.md §1); other states' thresholds are reported; not confirmed at the source on 2026-10-26 and need counsel if applicants reside there (gap: residence data).
- **Employment AI rules:** (a) NYC Local Law 144, enforced since 5 July 2023 (checked 2026-10-26): see the Summary answer; needs an independent auditor, a published summary, notice 10 business days before use, and the route to an alternative process (none designed, gap); whether New York-resident applicants to California roles count is counsel's question, and the evaluation set's mix of warehouses is not recorded (D5; gap). (b) California FEHA regulations in force 1 October 2025 (checked 2026-10-26): anti-bias testing, its quality, recency, scope, results and response, is evidence for or against a claim (§11009(f)), and selection criteria and ADS data are kept four years (§11013(c)); the screener's retention is a gap (privacy-impact-input-pack.md Retention). (c) Title VII and ADA: disparate impact is statute and the four-fifths rule is codified (29 CFR 1607.4(D), checked 2026-10-26); the age impact ratio is 0.74 for "recommended" (M2, sample 6,000, window 2026-09-22 to 2026-10-03, build v0.5.2), below 0.8; M2's method infers age from work-history length where no date of birth exists, so the screener's own age removal (C4) does not show that work-history length has no effect (gap: whether work-history length or tenure is a scoring input). Sex ratio 0.91 (M3). No ratio by race or ethnicity, national origin or disability (gap), and no accommodation route (gap). (d) Federal and state age-discrimination law, New York State and City human rights law and state breach-notification statutes are not covered by the skill reference, so they are named only as questions (counsel: see Questions for counsel 8 and 17).
- **Sector statutes:** n/a: no health, credit, children or biometric data in the design; FCRA question: the screener reads only Greenhouse application data and adds no third-party information (docs/discovery/screener.md §3; counsel: confirm FCRA does not apply).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| United States | CPPA risk assessment before new in-scope processing | 1 January 2026 (CPPA section 7150, checked 2026-10-26) | Needed before pilot processing, W3 |
| United States | CPPA ADMT duties for significant decisions | 1 January 2027 (checked 2026-10-26) | The pilot runs past this date; notice and opt-out or appeal route, W5 |
| United States | California FEHA automated-decision regulations | 1 October 2025 (2 CCR section 11008 et seq., checked 2026-10-26) | In force now; testing and four-year records |
| United States | NYC Local Law 144 | 5 July 2023 (checked 2026-10-26) | Gates any New York use, W4 |
| United States | Colorado SB 26-189 consequential-decision duties | 1 January 2027 (checked 2026-10-26) | Only if Colorado applicants exist |
| United States | CPPA first risk-assessment submission and attestation | 1 April 2028 (checked 2026-10-26) | Later; Redwood to calendar |
| Australia | APP 1.7 automated-decision transparency | 10 December 2026 (checked 2026-10-26) | n/a: not Redwood's or Southgate's decision |

- **AI literacy (EU AI Act Article 4) and staff training:** n/a: EU not in scope; gap: no recruiter training or guidance goal in docs/plans/screener.md, proposed goal for adk-engineer on guidance for recruiters about reviewing "not recommended" applicants.
- **Documents the client's own process produces:** NYC bias audit by an independent auditor with published summary and candidate notice, W4 (conditional on New York use); California CPPA risk assessment with approver, W3; California ADMT pre-use notice and opt-out or appeal, W5; update of Redwood's applicant privacy notice (gap: current notice not in the record).

## Open questions and assumptions

Questions that would have been put to the requester; none could be answered in this non-interactive run, so each proceeds on the stated assumption.

- Question: Does Redwood meet a CCPA business threshold? Assumption: yes (9,000 applications a month, docs/discovery/screener.md §1; revenue not recorded).
- Question: Whose Google Cloud project and contract hold the stack? Assumption: Redwood's, with Southgate acting under its instructions (gap, not recorded).
- Question: Does Southgate keep a copy of the evaluation set in Sydney or read it remotely? Assumption: remote access to a Redwood-controlled store (D4 says "read"; gap).
- Question: Do the 6,000 evaluation applications include New York warehouses or New York residents? Assumption: unknown (D5, gap); treated as possibly yes for the NYC answer.
- Question: Pilot start date? Assumption: 2026-11-18, the decision date (docs/discovery/screener.md §6).
- Question: Southgate's home. Assumption: consultancy home Australia (default).

## Questions for counsel

- counsel: 1. Is Redwood a CCPA business, and does California treat the screener's output as ADMT for a significant decision given M4 and the bulk-rejection pattern; regime United States; facts at R4, C2, M4; needed before W3.
- counsel: 2. Must the §7150 risk assessment be complete, and its approver named, before pilot processing starts; regime United States; facts at D1, D2, D5; needed before W3.
- counsel: 3. Are ADMT pre-use notice, opt-out or human appeal and access responses needed from the pilot's first day or only from 1 January 2027; regime United States; needed before W5.
- counsel: 4. Does the age ratio 0.74 (M2) on 6,000 past applications, below the four-fifths rule of thumb, bar the pilot, require remediation first or only monitoring; what remediation is acceptable under Title VII, ADA and FEHA; regime United States; needed before W2.
- counsel: 5. Is bulk rejection of "not recommended" applicants "meaningful" human review for ADMT and FEHA purposes, and should D3's collapsed group or the rejection workflow change; regime United States; facts at D3, M4; needed before W2.
- counsel: 6. Is Southgate Labs an FEHA "agent" and thus an employer, and what contract terms does Redwood need (service provider terms, assistance with assessments, audit); regime United States; needed before W2.
- counsel: 7. Is anti-bias testing by Southgate (M2, M3) sufficient evidence under FEHA §11009(f), and how long must selection criteria and ADS data be kept (§11013(c)); regime United States; needed before W3.
- counsel: 8. What federal and state age-discrimination law, and New York State and City human rights law, apply to the age ratio and to any New York use (not covered by the reference); regime United States; needed before W4.
- counsel: 9. NYC Local Law 144: does the screener "substantially assist or replace" discretionary decisions, does it reach New York-resident applicants to California roles, who is an independent auditor (Southgate cannot be), and what alternative process route is acceptable; regime United States; needed before W4.
- counsel: 10. Which other states' laws attach to applicants from outside California and New York (Colorado, Illinois, Connecticut, Texas), once Redwood supplies residence data; regime United States; needed before W2.
- counsel: 11. May past applicants' data be used for the 6,000-application evaluation set (D5) under the notices they saw, and is the removal of names and contact details enough de-identification given free text; regime United States and Australia; needed before W2.
- counsel: 12. Is Southgate an APP entity, does the Privacy Act reach US applicants' information read from Sydney, and is that handling a use or a disclosure under APP 8 and s 16C; regime Australia; needed before W2.
- counsel: 13. Who notifies a breach affecting the evaluation set or logs, and what US state breach-notification statutes apply (not covered by the reference); regime Australia and United States; needed before W2.
- counsel: 14. Which public claims, if any, may Redwood make about the screener beyond M1 as defined; regime United States; needed before W2.
- counsel: 15. Does FCRA apply to an agent that scores applications from Greenhouse data only; regime United States; needed before W2.
- counsel: 16. Is a disability accommodation route required in the screening workflow (ADA) and what must it be; regime United States; needed before W2.
- counsel: 17. Should the pilot proceed at all on the current record, and on what conditions, the decision being Kevin Ortiz's on 2026-11-18 (docs/discovery/screener.md §2, §6); regime United States; needed before W2.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Monica Alvarez, General Counsel, Redwood Freight | this document | pending | pending |
