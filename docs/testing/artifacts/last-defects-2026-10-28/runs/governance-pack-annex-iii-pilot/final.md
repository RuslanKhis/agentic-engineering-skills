I drafted the full pack for Kestrel's counsel and DPO in `docs/governance/shortlisting/`, but I could not run the checker because Bash is disabled in this session. Every draft is `status: draft`, `counsel_required: yes` and has `pending` sign-off rows. Please run this before anything is sent:

```
python3 -I .claude/skills/adk-governance-pack/scripts/check_governance.py docs/governance/shortlisting/ --source docs/discovery/shortlisting.md --source docs/architecture/shortlisting.md --source docs/plans/shortlisting.md
```

**What I wrote**
- **Seven papers:** `regulatory-memo.md`, `privacy-impact-input-pack.md` (the DPIA inputs), `processing-records.md`, `transfer-assessment.md`, `impact-assessment.md`, `system-card.md` and `security-questionnaire.md`.
- **Plan edits:** `docs/plans/shortlisting.md` now has W3 (legal review), W4 (transfer mechanism for Sydney access), W5 (Article 36 consultation, only if triggered) and a G06 evidence note. G06 stays `ready` and is marked "drafted, not sent". W3, W4 and W5 are added to G07's dependencies.
- **Regimes in scope:** Australia, and only through Southgate Labs' own handling from Sydney (D5). The EU, through Kestrel's establishment and the applicants. The US, UK, New Zealand, Singapore and Canada are out, because no applicant or entity in the record is there.
- **EU classification (counsel to confirm):** high-risk under Annex III point 4 (ranking applicants), and it profiles people, so no Article 6(3) derogation is proposed. Annex III duties apply from 2 December 2027 (checked 2026-10-26), but GDPR applies to the pilot now.
- **Australia (counsel to confirm):** Kestrel's own APP 1.7 duty is n/a. The open question is whether the Privacy Act reaches Southgate reading EU applicants' data from Sydney.

**Blocking facts and questions**
- **Adverse impact (M3):** the ratio is 0.71 for applicants aged 50 and over. C7 says "pilot paused" on failure, but the design records no threshold and no decision. I reported the figure as recorded and drew no conclusion.
- **Main counsel questions:**
  - Annex III classification, GDPR Article 22 and equality law on the 0.71.
  - Controller roles of the two Kestrel entities.
  - Basis for reusing the 1,400 past applications (D6).
  - Whether incident I1 needed GDPR breach notification.
  - Works council rights (W1).
  - Whether the Sydney access is a restricted transfer (W4).
  - The Privacy Act question above.
  - Dutch, German, Polish and Romanian law not covered by the skill's references.

The full list of 14 is in the memo.

**Gaps and who should own them**
- **Evaluation:** no review or override rate, and no measure of nationality, health or family status (`adk-agent-evaluation`). C4 does not remove health or family status, although R5 bars them.
- **Mitigation:** no plan goal addresses the age disparity.
- **Model:** retirement date and processing region for `gemini-3.5-flash-001` were not read, because there was no network access and no lifecycle table (`adk-model-and-output-contracts`).
- **Data stores:** no retention, erasure or log-sink decision, and no coverage figure for the C4 redaction step (`protect-adk-sensitive-data`).
- **Security:** the baseline table covers only SB01, SB03 and SB05, and no security reviewer is named. The ADK runtime hardening (SB05) is deferred until production even though the pilot uses real applicant data (`adk-agent-security`).
- **Missing documents or goals:** no applicant notice, no recruiter AI-literacy training goal, no Article 25(4) or processor agreement in the record, and no goals for technical documentation, conformity assessment or registration before December 2027.

**Assumptions I proceeded on**
- Southgate's home is Australia, and Kestrel is a private company.
- No applicants are in the US, UK, New Zealand, Singapore or Canada.
- Law dates were copied from the skill's references (checked 2026-10-26) and not re-read at the source.

**Waits to schedule:** W1 has no date against the 2026-11-20 decision. W3 and W4 have no dates either. W5 applies only if the DPIA records a high residual risk.

**Not done:** the checker run, and nothing was sent to anyone. No government form answers were drafted, because Kestrel is a private client.

Next step:
```text
/adk-presenter Prepare the pilot-decision presentation from docs/plans/shortlisting.md; cite docs/governance/shortlisting/system-card.md for limits and oversight, and show the open counsel questions and the 0.71 adverse-impact result (M3) as risks.
```