# REPORT: support inbox auto-reply POC design (headless session)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`; SKILL.md loaded by the harness).
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (full)
3. `.claude/skills/adk-system-designer/references/design-decisions.md` (full)
4. `.claude/skills/adk-system-designer/references/failure-review.md` (full)
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (full)
6. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (model choice, per SKILL.md:196-197)
7. `grep` over `.claude/skills/*/references/compatibility.md` for the ADK version (all name `google-adk` 2.8.0; `adk-agent-security/references/compatibility.md:36` gives the ≥2.7.0 CVE floor)
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (goal fields)

No other skills were invoked. Not opened: `gcp-decisions.md` (no service selection beyond the Gemini API; local only), `runtime-and-delivery.md` (no trigger: no streaming, sessions or releases), the design and ticket templates (compact form replaces the design template; no tickets requested).

## 2. Questions I would have asked, and the answer assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Deadline, and is the POC thrown away or continued? | Today, about 4 h; kept and continued if it impresses |
| 2 | Your familiarity with ADK and GCP; do you have admin access to the support mailbox? | New to ADK; has a Google account that can authorise OAuth on the mailbox |
| 3 | Budget for models? | Under USD 10 |
| 4 | Who judges the result and what will they read? | The builder plus a teammate, reading a review table |
| 5 | You asked for automatic sending to real customers. A wrong or manipulated answer would reach a real customer with nobody checking it. Do you accept that risk for the POC? | **No** (not accepted). "Don't worry about security" lowers depth, not the floor (SKILL.md:75-77). Phase 1 proposes replies, phase 2 creates drafts, auto-send is G06 behind written acceptance |
| 6 | Which model backend may receive real customer email: Gemini API free tier, paid tier, or Vertex AI? | Paid Gemini API (free-tier data terms are unsuitable for customer data; Vertex adds about an hour of setup). To be confirmed against current terms |
| 7 | Which mailbox, and how many messages per run? | One support mailbox, 30 newest inbound messages |
| 8 | What counts as a "simple question"? | Five guessed categories (hours, password reset, order-status link, shipping times, contact details), recorded in G02 |
| 9 | Does Workspace policy allow a third-party OAuth app on that mailbox? | Unknown; G01 falls back to a hand-exported 30-email sample |
| 10 | Confirm the cut line: G01–G03 now, G04–G07 later? | Assumed confirmed |

## 3. Files written or changed; what is not finished

- **Written:** `docs/architecture/support-inbox-autoreply.md`: compact POC design and plan in one file (constraints with an Assumed answers table, journey, six decisions, floor/depth table, graduation conditions, phase 1 goals G01–G03 with run prompts, phase 2 goals G04–G07, later list, open decisions).
- **Written:** `REPORT.md` (this file).
- No code, dependencies or config were changed (design-only request).
- **Not finished:**
  - The document is marked **draft**. Every scope answer is assumed, and D1 (no auto-send) and D4 (model backend) wait on the user.
  - The doc is about 1,370 words without table syntax (1,495 by `wc -w`). That is roughly 14% over the "about 1,200 words" target.
  - No separate `docs/plans/` file was written; SKILL.md:244 allows a small effort to keep its plan in the design.
  - No tickets were written (none requested).
  - Gmail scope semantics, paid Gemini API data terms and the ADK 2.8.0 pin were not checked against live documentation because network use was forbidden. They are labelled assumptions in the doc.

## 4. Checks run and not run

Run:
- `wc -w` on the design: 1,495 words; 1,371 with table pipes and rule lines removed. Over target, accepted (see above).
- A secret and personal-data scan of the design (`grep` for API key patterns, `client_secret`, the user's email domain and `password=`). Result: no matches.
- `grep` for `messages.send` / `drafts.send`. They appear only in D1's check column as forbidden calls, not as a planned action.

Not run:
- No tests exist; none were written (design only). Tests importing `google.adk` could not run here anyway, because the dependencies are not installed.
- No Gmail API, Gemini API or official-documentation lookups (network forbidden). This covers the model lifecycle status (taken from the skill's 2026-10-08 snapshot), Gmail scope behaviour and the API data terms.
- No markdown link checker (the design has no relative links).

## 5. Friction log

- **Unsure: headless versus scope gate.** SKILL.md:54-56 says to open with a scope-gate question turn. SKILL.md:119-122 says to ask nothing when the user cannot answer and to use an Assumed answers table instead. The second rule resolved it, but it sits about 50 lines after the instruction to ask. A one-line pointer at line 54 would help.
- **Unsure: assuming "no" to a risk-acceptance question.** delivery-profiles.md:80-83 says nothing visible to an outside person happens without approval "unless the user explicitly accepts that risk after hearing it in one sentence". The headless rule (SKILL.md:119) says to assume answers. It is not stated that a floor-waiving answer can never be assumed. I chose "not accepted" because the floor wording implies it. An explicit line ("never assume acceptance of a floor risk") would remove the doubt.
- **Genuinely helpful.** delivery-profiles.md:24-27 describes almost exactly this request ("A 'POC' that sends email to real customers from a real inbox carries production risk"). The worked example at delivery-profiles.md:170-178 gave the shape of phase 1 and phase 2 directly.
- **Genuinely helpful.** design-decisions.md:182-191 (lethal-trifecta split) led to the cheapest control: the agent has no tools, and code owns Gmail. That is cheaper than any callback or confirmation mechanism.
- **Helpful.** The model lifecycle JSON (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`) showed that the 2.5 models retire on Vertex on 2026-10-20, 11 days from today. A from-memory pick could easily have chosen one.
- **Heavier than needed.** I read design-decisions.md in full (343 lines). Most of it (RAG, analytics at :327-343, shared allowances at :280-289, event-driven updates) has no bearing on a four-hour POC. SKILL.md:95 says to read "the sections its journey touches", but the file has no index, so selective reading means skimming it all anyway.
- **Heavier than needed.** implementation-plan-template.md:48-69 lists 13 fields per goal. That conflicts with the compact form's "four to six lines each" (delivery-profiles.md:160-162). I followed the compact form.
- **Unsure: word budget.** SKILL.md:84 and delivery-profiles.md:146 say about 1,200 words. A compact form with an Assumed answers table, six decision rows and seven goals with run prompts lands near 1,400. It is unclear whether tables count, or whether the Assumed answers table can replace the scope-gate table rather than add to it.
- **Unsure: plan path in the run prompt.** SKILL.md:276 shows `docs/plans/<topic>.md`, but SKILL.md:244 lets a small effort keep the plan in the design. I pointed the run prompt at the design file. The example could show both forms.
- **Unsure: which skill owns G01.** The fetch script is ordinary code, not an ADK tool. The handoff table (implementation-handoff.md:30) puts credentials under `adk-tool-auth-and-secrets`, so I chose that, but no row covers "non-agent ingestion script using user OAuth".
- **Minor.** SKILL.md:194 says to make "confirm against the chosen pin" an acceptance item of the first implementation goal. Here the first goal (G01) does not touch ADK, so I attached it to G02. The rule could say "the first goal that imports ADK".

## 6. Next prompt the skills told the user to type

From SKILL.md:270-276 (closing message with a copyable prompt), filled in for this plan:

```text
/adk-engineer Carry out G01 from docs/architecture/support-inbox-autoreply.md.
```
