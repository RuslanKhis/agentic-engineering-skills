I couldn't write the governance pack, because the Write tool was denied. Claude Code is in "don't ask" mode, so the denial wasn't a prompt I could answer. I haven't tried to get around it with shell redirection or heredocs, because that would sidestep the permission setting. No governance file exists yet.

**Done**
- I read the skill, the three project records and the template and reference files. I also created an empty `docs/governance/customer-agent/` directory with `mkdir`, which was allowed.
- The full regulatory memo was drafted and ready to write. It is the first document in the pack.

**Findings so far**
- **Regimes in scope:** Australia, New Zealand and Singapore. Australia is in scope only through Southgate Labs' own handling in Sydney.
- **Regimes out of scope:** the US, EU, UK and Canada, because the record shows customers only in New Zealand and Singapore. Counsel should confirm no one from those places signs in or is delivered to.
- **Largest risks in the record:** transcripts kept for 12 months and reused to build evaluation sets (D3), and Sydney engineers reading traces that contain CRM fields (D4).
- **Open legal questions:**
  - New Zealand: whether Southgate Labs is only an agent under s 11 of the Privacy Act, or is also an agency for the evaluation sets it builds.
  - Singapore: whether Southgate Labs stays a data intermediary, which basis supports the evaluation reuse, and which transfer mechanism covers Sydney. Counsel has to decide all of these.
- **Gaps the record can't fill:**
  - the model's retirement date and processing region, which I couldn't check without network access
  - the Kowhai–Southgate Labs contract
  - customer notices
  - trace retention
  - a way to search stored data by person
  - screening evidence
  - any measurement of human review
- **Contradiction to resolve:** D5 says no copy of CRM data is kept, but D3 and D4 mean transcripts and traces hold copies.

**Not done**
- The memo, privacy impact input pack, transfer annex, impact assessment, system card and security questionnaire are unwritten.
- The checker hasn't been run.
- I haven't updated the plan with the new waits: privacy officer review, Singapore DPO review and counsel review, all needed before the 2026-11-26 pilot decision.
- Records of processing and government form answers are not needed for this pack, since neither the EU nor the UK is in scope and the client is private.

**How to proceed:** either allow Write for `docs/governance/customer-agent/` (and edits to `docs/plans/customer-agent.md`), or tell me that writing the files through Bash is acceptable. I'll then write the pack and run the checker.