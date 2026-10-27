I've drafted the governance papers for the Auckland privacy officer (Aroha Ngata) and the Singapore DPO (Daniel Tan). The skill's checker passes on all six, but that only checks form, not the law. Every sign-off row is `pending`, and nothing has been sent to anyone.

**Files:** `docs/governance/customer-agent/`
- `regulatory-memo.md`
- `privacy-impact-input-pack.md`
- `transfer-assessment.md`
- `impact-assessment.md`
- `system-card.md`
- `security-questionnaire.md`

**Regimes in scope** (all papers carry `counsel_required: yes`):
- **Australia** is in scope only through Southgate Labs' own handling: the Sydney engineers read traces that include CRM fields. The client's own Australian rows are marked n/a.
- **New Zealand** is in scope as the client's home.
  - The main obligations are IPP 5 security, IPP 8 accuracy, IPPs 9 to 11 on reusing transcripts, and Southgate Labs and Google holding data as agents under s 11 of the Privacy Act.
- **Singapore** is in scope because the customers are there.
  - The main obligations are the client's Transfer Limitation Obligation for Sydney hosting and access, and an assessed basis for reusing transcripts to build evaluation sets.
  - Southgate Labs stays a data intermediary only while it stays inside a written contract.
  - The PDPC clock is 3 calendar days.
- **United States, EU, UK and Canada** are left out because the record shows no customers, client or processing there. This is an assumption for counsel to confirm.

**Questions I couldn't ask, and what I assumed:**
- **Pilot start:** I assumed the pilot starts on or after 2026-11-26.
- **Consultancy home:** I assumed Australia, the default.
- **Other jurisdictions:** I assumed no US, EU, UK or Canadian users.
- **Regulation and access:** I assumed Kowhai is not a MAS-regulated or health client, and that engineers reach traces only from Sydney.

**Counsel questions that block the pilot decision of 2026-11-26** (14 in the memo; the main ones):
- Whether Southgate Labs is only an s 11 agent in New Zealand and a data intermediary in Singapore.
- Which mechanism covers Singapore data in Sydney, and whether the contract names Australia.
- Whether reusing transcripts for evaluation is allowed in each country.
- Whether Google's abuse monitoring counts as its own use.
- Whether offering store credit in place of a refund breaches NZ or Singapore consumer law. This pack doesn't cover Singapore consumer law.

**Gaps, each tied to a proposed owner skill in the memo:**
- **Model details:** `gemini-3.5-flash-001`'s retirement date and processing region, plus abuse-monitoring and caching settings. I had no web access, so I assumed neither.
- **Data handling:** retention and erasure for traces and evaluation sets, and where evaluation sets live. D5 says "no copy is kept", but traces keep CRM fields.
- **Contracts and notices:** no written Kowhai–Southgate Labs contract and no customer notice text in the record. There is also no AI-disclosure contract, and no named counsel.
- **Evidence:** no masking or screening evidence, no measured handover time, no adversarial test result.
- **Unrecorded details:** the Salesforce region, and security baseline rules beyond SB01, SB03 and SB05.

**Plan updated:** I added waits W2 (privacy officer review), W3 (DPO review) and W4 (counsel review) to `docs/plans/customer-agent.md`, plus G05 evidence marked "drafted, not sent". The plan has no pilot-approval goal, so I couldn't add them to a goal's dependencies. Please add one.

**Left undone:**
- Contacting reviewers or counsel, or sending anything.
- Re-reading the model page, Google's terms and the laws at their sources. Legal facts come from the skill's references (read 2026-10-26), and dates carry that check.
- Drafting the client's own PIA or DPIA, notice text or contracts.
- Getting Mere Walker to name counsel.

Next step, when you want the deck:
```text
/adk-presenter Prepare the pilot-decision presentation from docs/plans/customer-agent.md; cite docs/governance/customer-agent/system-card.md for limits and oversight, and show the open counsel questions and gaps as risks.
```