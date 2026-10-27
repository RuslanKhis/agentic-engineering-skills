I've drafted the governance pack for Thamesbridge's two DPOs and the CISO, but I couldn't run the checker. No shell was available, so nothing has been validated. I looked through the drafts for placeholders, uncited SB IDs and uncited dates and found none. Please run this before the drafts go out:

```
python3 -I .claude/skills/adk-governance-pack/scripts/check_governance.py docs/governance/service-assistant/ --source docs/discovery/service-assistant.md --source docs/architecture/service-assistant.md --source docs/plans/service-assistant.md
```

I also had no network access, so every legal fact is copied from the skill's references with their 2026-10-26 check date. Nothing was re-read at a primary source.

## What's in `docs/governance/service-assistant/`
- `regulatory-memo.md` (counsel and both DPOs) covers the jurisdiction screen, roles, the EU classification and 14 counsel questions.
- `privacy-impact-input-pack.md` (both DPOs) is the DPIA input for the UK and the EU, plus the consultancy's own Australian position.
- `processing-records.md` (both DPOs) has the Article 30 rows, one per purpose and regime.
- `transfer-assessment.md` (both DPOs) covers the Sydney access, the EU-to-UK flow and Google.
- `impact-assessment.md` (DPOs, CISO, and Laura Whitfield as risk owner) includes the Consumer Duty rows.
- `system-card.md` (DPOs and CISO) describes build v0.8.0.
- `security-questionnaire.md` (CISO) is the answer bank.

Every draft is `status: draft` with every sign-off `pending`. Every draft is `counsel_required: yes`, because the credit-decision facts force it.

## Regimes in scope
- **Australia:** in scope only through Southgate's own handling. Whether the Privacy Act reaches that handling is `counsel:`.
- **EU:** I propose transparency obligations only (Article 50(1)), not Annex III 5(b), because the assistant relays the decision engine's reason codes and does not score. That is `counsel:`, and the CreditLens engine needs its own classification.
- **UK:** UK GDPR Articles 22A to 22D, the restricted transfer for Sydney access, and Consumer Duty.
- **Left out:** the US, New Zealand, Singapore and Canada, each because the record shows no client, customers or data there.

## Counsel questions that block the 2026-12-03 pilot decision
- Which Thamesbridge entity is controller in each region, and who exports the data to Sydney.
- Whether Article 22 or 22A applies to the engine's declines, and whether Article 22B applies given merchant names that reveal health, religion and union payments.
- Whether explaining a decline is within Annex III 5(b).
- Whether the Privacy Act reaches Southgate's handling of UK and EU customers' data.

## Main gaps
- **Logs and traces:** the pseudonymisation control (C5) covers transcripts only. D4 gives the Sydney engineers logs and traces too, and nothing records them as pseudonymised.
- **Model:** the retirement date and processing region of `gemini-3.5-flash-001` are not recorded, and the lifecycle table isn't installed. Caching and abuse-monitoring settings are also missing.
- **Article 50(1):** the D6 chat-header wording says "the bank's assistant", not that it's an AI, and there is no test for it.
- **No evidence recorded** for retention and erasure, the decline contest route, hand-off time, the complaints route or the rollback owner.
- **Security baseline:** only SB01, SB03 and SB05 are in the design's table, so the questionnaire marks every other control as a gap.
- **Contracts:** the Southgate–Thamesbridge contract and the transfer instruments are not in the record.
- **Measures:** M1 to M3 are synthetic, scripted or staff tests, and M3's 41 % isn't comparable with the 22 % baseline.

## Assumptions I proceeded on
Nobody could answer questions in this session, so these are open:
- Southgate acts as processor only and uses no data for its own purposes.
- Pilot customers are adults.
- The 1,000 Irish customers are resident in Ireland.
- No fine-tuning of the model.
- Support access stays six months, although the pilot runs eight weeks. Consider asking whether engineer access should stop at pilot end.

## Plan changes and waits
I added W3 to W6 to the plan, for counsel review, transfer instruments, prior consultation if the DPIA finds high residual risk, and CISO approval. W5's clock can't finish before 2026-12-03. The plan has no pilot-approval goal, so none of these is attached to a goal's "Depends on". I also added a G06 evidence note saying "drafted, not sent".

## Not done
- Checker not run.
- Drafts not sent to anyone.
- No Google model page, lifecycle table or Cloud compliance pages read.
- Government forms not written, as the client is private.

## Next step
```text
/adk-presenter Prepare the pilot-decision presentation for 2026-12-03 from docs/plans/service-assistant.md; cite docs/governance/service-assistant/system-card.md for limits and oversight, and show the open counsel questions and gaps as risks.
```