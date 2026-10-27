The pack is drafted in `docs/governance/enquiries/` and the checker passes on all seven documents. That only checks form and citations, not the law. Every document is `status: draft` and `counsel_required: yes`, and every sign-off is `pending`.

**Documents**
- `regulatory-memo.md`: for the Accountable Official and agency counsel.
- `privacy-impact-input-pack.md`: for the privacy officer.
- `impact-assessment.md`: for the Accountable Official, with sign-off rows for the privacy officer and CISO.
- `system-card.md`: for the Accountable Official and privacy officer.
- `security-questionnaire.md`: for the CISO.
- `government-form-answers-nsw-aiaf-registration.md` and `government-form-answers-nsw-aiaf-assessment.md`: draft answers for the agency's officers, not the official forms.

**Regimes in scope:** Australia only, through a NSW agency client and NSW applicants. The US, EU, UK, New Zealand, Singapore and Canada are out of scope: there are no such clients or data subjects on the record. That rests on an assumption that visitors from those countries are incidental, which counsel should confirm. Australia has no AI Act, so there is no EU classification. The main obligations are:
- The PPIP and HRIP Acts apply, including the s 19(2) rule for recipients outside NSW.
- The agency registers the use case on the AIAF Platform.
- ICTA clause 6.11 sets the model-change notice.

**Model-change notice:** the answer I propose to counsel is that it does not fit. Gemini is pinned to retire on 2027-02-26, and six months' notice before that fell on 2026-08-26, before the Order Form was signed on 2026-09-08. Notice given today would run to 2027-04-28, and the contract runs to 2027-09-14. The summary does not show whether the Order Form lists the model IDs.

**Blocking questions for counsel** (10 in the memo; the main ones):
- Can the model-change notice be waived or shortened, or the replacement model approved now?
- Do the Brisbane support access, Google's abuse monitoring and the model's processing region count as a use or a disclosure outside NSW, and which s 19(2) or HPP 14 ground applies? Order Form item 14 says Australia, not NSW.
- Does s 7B(5) cover all of Southgate's acts, and is Southgate bound by the HRIP Act for health details typed into chat?
- Does the contract meet the IPC's minimum for recipients outside NSW? The contract text is not in the record.
- Which AIAF band applies? I propose medium, which the agency sets.

**Gaps and the goal each needs**
- Model processing region and Google's data use: `adk-model-and-output-contracts`. I could not re-read the model page (no network), so the 2026-10-20 retirement date is cited as not re-read.
- Screening of free text, since transcripts may hold health and criminal-history details: `protect-adk-sensitive-data`.
- Security baseline rules beyond SB01, SB03 and SB05; no incident process; no recorded encryption or log retention: `adk-agent-security` and `adk-agent-observability`.
- Export of transcripts to the agency's recordkeeping system, and the 90-day retention against its disposal authority: `adk-memory-architecture`.
- No AI disclosure contract, no stop or rollback owner, no bias, accessibility or live evaluation: `adk-agent-evaluation`.
- No model-retirement release path: `adk-release-engineering`.
- No staff training goal for contact-centre staff.

**Waits:** I added W3 to W7 to `docs/plans/enquiries.md` (counsel review, privacy officer's PIA, AIAF registration, conditional AI Review Committee referral, customer approval of the model replacement). Start all of them now for the 2026-12-10 pilot decision. The plan has no pilot-approval goal for them to block, so I proposed a G06 but did not add it. G05 is marked "drafted, not sent".

**Questions I could not ask, with the assumptions I proceeded on**
- Is the Accountable Official being also the sponsor and decider intended? I flagged it for the agency and left acceptance as a gap.
- Which AIAF version does the agency use? I drafted answers to the 2024 framework and the registration baseline, neither re-read at source.
- Is the `gemini-3.5-flash-001` retirement date correct? I took it from the design record without re-reading.

**Not done:**
- No processing records or transfer annex: the EU and UK, the only regimes that require them, are out of scope.
- No agency forms, PIA or review committee referral: those are the agency's.
- No web re-reads of any source.

Next step:
```text
/adk-presenter Prepare the pilot-approval presentation for the 2026-12-10 executive board from docs/plans/enquiries.md; cite docs/governance/enquiries/system-card.md for limits and oversight, and show the open counsel questions and the model-retirement conflict as risks.
```