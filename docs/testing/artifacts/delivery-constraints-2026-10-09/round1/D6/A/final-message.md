I've written the design and plan in `docs/architecture/support-inbox-poc.md` and the session report in `REPORT.md`. Nothing is implemented. Every decision is provisional because you weren't available to answer questions.

**The big change from your request: no automatic sending in this POC.** The agent drafts replies, and a person checks each one and presses Send. Your request was automatic replies to real customers from the real inbox, which the skill treats as production risk however the project is labelled. It only allows automatic sending if you accept that risk explicitly, and I couldn't ask you. Drafts still save the typing, which is most of the time spent today. Automatic sending is phase 2: first you see how often it wrongly marks a question as simple, then you decide.

**How it works:**
- **One agent with no tools.** It reads one email plus your FAQ and returns a structured result: `simple` with a reply, or `not_simple`. Ordinary code handles everything else (fetching mail, deciding what happens, any Gmail write).
- **Why no tools:** an email that contains hostile instructions can at worst produce a bad draft, which the person reviewing it throws away. It can't trigger any action.
- **Gmail access:** read-only for most of the afternoon. Gmail drafts need a broader permission that would also allow sending, so the guarantee that nothing gets sent comes from the code having no send call, not from the permission.
- **Model:** pinned to `gemini-3.8-flash`, the newest stable model in the skill's model list (no retirement date announced as of 2026-10-08). It runs on a paid-tier Gemini API key so customer mail isn't used for training.
- **Spend:** capped at 3 model calls per message and 25 messages per run.

**Fitting it into 4 hours:** about 3.2 focused hours, leaving roughly 2.4 hours of work after a reserve for setup surprises and the demo.

| Goal | What it delivers | Estimate | Phase 1? |
| --- | --- | --- | --- |
| G01 | Agent drafting replies to sample emails, demoed in `adk web` | 0.75–1 h | Yes |
| G02 | Reading the real inbox, read-only | 0.75–1 h | Yes |
| G03 | Run over 25 real messages, review table, 10–15 labelled, wrong-"simple" count | 0.5–0.75 h | Yes |
| G04 | Drafts created inside the Gmail threads | 0.5–0.75 h | Stretch, cut first |

Phase 1 is G01–G03, about 2–2.75 hours. Each goal still works on its own if time runs out. Phase 2 (G05–G08) covers deciding on automatic sending, guarded sending, a scheduled cloud run and a regression test set.

**Still open:**
- Does your Workspace admin allow an OAuth app to read the support mailbox? Check this in the first 15 minutes; only G01 works without it.
- Do you accept automatic sending, once you've seen the G03 numbers?
- Is there a written FAQ, and who owns it? It defines what a correct reply is.
- Is the Gemini API key on the paid tier?

**Checks:** each goal has its required fields, the document has no secrets in it, every skill it names exists, and the chosen model is in the skill's model list. No tests were run: none exist, and the ADK packages aren't installed. Nothing that needed the network was checked, so the Gmail permission behaviour and the model's status should be re-checked before building.

`REPORT.md` also covers which files I read, the friction log, and the next prompt. The design came out at about 3,600 words, over the skill's ten-minute-read target.

Next step:
```text
/adk-engineer Carry out G01 from docs/architecture/support-inbox-poc.md.
```