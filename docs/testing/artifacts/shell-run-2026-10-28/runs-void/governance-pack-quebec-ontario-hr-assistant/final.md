The pack is not done. I wrote one draft, the regulatory memo, and then Bash and Write were both denied, so I stopped. I did not try another route around the denial.

**Where the file is.** I ran `mkdir` and `cat >` from the wrong directory, so the memo is at `.claude/skills/adk-governance-pack/docs/governance/hr-assistant/regulatory-memo.md`. It belongs in `docs/governance/hr-assistant/`. I tried to move it, and that and a second write to the right path were both denied, so the stray copy is still there. Please move it and remove the empty `docs/` folders it created inside the skill directory.

**Direct answer for counsel (`counsel:`, from the memo's Summary).**
- Law 25 likely applies to Érable's handling of Montréal staff data. Érable's head office is in Montréal and 1,150 staff work there (brief §1).
- Section 12.1 is likely engaged for auto-approved requests from Quebec staff. A code rule decides, the approver is recorded as "HR assistant" with no human review (C3, C4, D5), and replay shows 64% of pilot-shape requests would be decided that way (M2).
- It is likely not engaged for requests routed to the manager (C5).
- Two points decide it. First, whether a deterministic rule counts as "automated processing". Second, whether an approval counts as a decision under s 12.1. The wording of s 12.1 is "reported; not confirmed at the source on 2026-10-26", so I kept that marking.
- The s 3.3 assessment and s 17 assessment duties apply whatever s 12.1 means. Three flows leave Quebec: Toronto hosting (D2), US model processing (D1) and Sydney log access (D4).
- Ontario staff have no general private-sector privacy statute. The Ontario electronic monitoring policy and human rights duties are the questions for counsel there.

**What is in the memo.**
- **Regimes in scope:** Australia (only through Southgate Labs' own Sydney access) and Canada (Quebec and Ontario).
- **Regimes out:** the US, EU, UK, New Zealand and Singapore, each with its reason in the screen table.
- **Questions and assumptions:** 12 questions for counsel and the assumptions I proceeded on.
- **Sign-off:** all sign-off rows are left `pending`.

**Not done.**
- Not drafted: the privacy impact input pack, transfer annex, impact assessment, system card and security questionnaire. No processing records, because the EU and UK are out.
- The checker was never run, so the memo has not passed `check_governance.py`.
- I did not add waits W2 to W6 to `docs/plans/hr-assistant.md`. The memo cites them, and the checker would fail on them until they exist. They are W2 counsel review, W3 Quebec privacy impact assessment (s 3.3), W4 s 17 assessment and written agreement, W5 Montréal union consultation (if required), and W6 Ontario monitoring policy update (if required). I also did not fill G05's evidence.
- I did not re-read the model page, because I had no network access. The model's retirement date is a `gap:`, and the US processing fact is cited from D1 (read 2026-09-10).

**Main gaps in the record.** None of these is in the docs, so I flagged them rather than filling them in.
- No employee notice.
- No contract or written agreement for Google or Sydney access.
- No route for staff to have an auto-approval reviewed or explained.
- No screening of leave reasons that may mention health.
- No evaluation split by language or site.
- No test of whether a prompt can manipulate the extracted dates.

**How to continue.** Grant write access (or Bash) for `docs/governance/hr-assistant/` and `docs/plans/hr-assistant.md`, then re-run the skill. I'll move the memo, draft the other five documents, add the waits, run the checker and finish.