I drafted five governance papers for the Privacy Officer and Head of Security, but I could not run the skill's checker because this session had no shell. They are drafts only: every sign-off row is `pending`, `counsel_required: yes` is set on all five, and nothing has been sent to the reviewers. They need a checker run (command at the end) before they go out.

**Where the files are:** `docs/governance/hr-assistant/`
- `regulatory-memo.md` and `privacy-impact-input-pack.md` are for the Privacy Officer (and counsel for the memo).
- `impact-assessment.md` is for both reviewers.
- `system-card.md` is for the Privacy Officer.
- `security-questionnaire.md` is for the Head of Security.

I also added waits W3 to W6 to `docs/plans/hr-assistant.md` and made G05 depend on W2 to W6.

**Regimes in scope:** Australia only. The US, EU, UK, New Zealand, Singapore and Canada are each out with a reason in the memo's screen table. That rests on an assumption that no staff are located in those countries. Sentry holding data in the US does not bring US law in; it is an APP 8 (overseas disclosure) question.

**Main obligations, all for counsel:**
- **Automated decisions:** APP 1.7 to 1.9 privacy-policy entries start on 10 December 2026. The manager attendance summary before a performance conversation (D6) is the likely trigger.
- **Overseas disclosure:** APP 8 and s 16C apply to the Sentry US flow and to any Gemini processing outside Australia.
- **Sensitive information and security:** APP 3.3 and APP 11 apply to union and medical text that masking misses.
- **Workplace surveillance:** NSW notice of at least 14 days before prompt logging, if counsel treats it as computer surveillance.
- **Consultation:** consultation with the SDA under the enterprise agreement.

**Findings the reviewers should see first:**
- **Sentry:** error bodies, including request and response bodies, go to a US-region Sentry project (D4). The record does not say whether masking (C4) covers that path, or what Sentry's retention or contract is. It contradicts the "logs in Sydney" reading of D2.
- **Masking:** only 82% of 150 synthetic prompts were masked (M2), and engineers read the logs (D5).
- **Manager summaries:** 95% of 60 matched Workday (M3). Nothing records how often a manager checks them, and the summarised person has no route to contest one.
- **Model:** I could not read the model page, so the retirement date and processing region of `gemini-3.5-flash-001` are `gap:` lines.
- **Baseline controls:** the design's baseline table lists only SB01, SB03 and SB05, so most questionnaire rows say `gap`.

**Counsel questions that block the 2026-11-27 pilot decision:**
- Does the employee records exemption (s 7B(3)) cover Wattle's use of the assistant and APP 1.7?
- Is Southgate Labs an APP entity in its own right?
- Is the manager summary caught by APP 1.7?
- Is the Sentry flow a use or a disclosure, and what contract is needed?
- Is holding union and medical information in logs a collection needing consent?

The remaining questions (surveillance, SDA consultation, Victoria and Queensland, breach notifier) are in the memo.

**Questions I could not ask, and the assumptions I used:**
- Southgate's and Wattle's turnover is above $3 million. Neither is recorded.
- C4 masking does not cover Sentry.
- Wattle has no staff outside Australia.
- Wattle's counsel is not named in the record, so the memo's sign-off row has no name.

**Gaps and the goal each needs:**
- **adk-model-and-output-contracts:** the model page check, and whether the summary returns leave reasons.
- **protect-adk-sensitive-data (G04):** masking threshold and Sentry scrubbing.
- **adk-agent-evaluation (G05):** manager guidance, checking rate, the answers-marked-wrong counter-metric, and bias.
- **adk-agent-observability:** Sentry and log retention, and per-person access and erasure.
- **adk-release-engineering:** kill switch and rollback owner.

**Waits to schedule (new, unnumbered in the record before I added them):**
- W3 surveillance notice: its needed-by date depends on a pilot start date the record doesn't give.
- W4 SDA consultation.
- W5 privacy policy update before 10 December 2026.
- W6 counsel review, to be requested the day the drafts go out.

**Left undone:**
- The checker run. Run it from the project root:
  `python3 .claude/skills/adk-governance-pack/scripts/check_governance.py docs/governance/hr-assistant/ --source docs/discovery/hr-assistant.md --source docs/architecture/hr-assistant.md --source docs/plans/hr-assistant.md`
- Model page and provider terms, because I made no network requests.
- No government forms, which don't apply to a private client, and no records of processing or transfer annex, which apply only to EU or UK data.

**Next step:**
```text
/adk-presenter Prepare the pilot-decision presentation from docs/plans/hr-assistant.md; cite docs/governance/hr-assistant/system-card.md for limits and oversight, and show the open counsel questions and the Sentry and masking gaps as risks.
```