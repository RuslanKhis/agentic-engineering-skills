I wrote the design and plan, plus `REPORT.md`. Nothing is implemented, and no tests ran: there's no code yet, and `google-adk` isn't installed here.

**Where things are**
- `docs/architecture/gmail-support-autoreply.md` is marked **draft**. The plan is inside it because the effort is small. It opens with a table of 10 assumed answers to the questions I would have asked you.
- `REPORT.md` covers the six sections you asked for: skills and files read, assumed answers, what was and wasn't finished, checks, friction log, and the next prompt.

**The design in brief**
- **Flow:** a local Python script checks the inbox for unread mail and skips automated senders, so the agent never ends up in a reply loop with a customer's out-of-office. For each remaining email, one ADK agent with no tools reads only that email and decides "answer" or "skip". An answer must cite at least one entry from a short `faq.md` that you write.
- **Code controls the sending:** ordinary code, not the model, sets the recipient and thread and decides whether a reply goes out. A forged or manipulative email can at worst shape the reply text sent back to its own sender. This costs nothing extra in a 4-hour build, so I kept it even though you said not to worry about security. Everything else security-related is listed as deferred.
- **Model:** `gemini-3.8-flash` (stable, no shutdown announced, per the skill's model table checked 2026-10-08).
- **Goals:**
  - G00: your setup (OAuth client, `faq.md`, API key).
  - G01: the full pipeline in draft mode.
  - G02: run it on 30 real emails and count right and wrong answers.
  - G03: turn on sending, limited to an allow-list, and never re-send if a send's outcome is unclear.

**Decisions still open**
- **Q4, the main one:** I narrowed "automatically sends" to **drafts first**. Real sending is a switch that stays off, and limited to an allow-list, until you've reviewed G02's results.
- Whether a short FAQ exists to ground the answers.
- Whether the Gemini API's data-use terms are acceptable for real customer email.
- What "good enough to send" means. I proposed 0 wrong answers among at least 10 answered.
- Which `google-adk` version to pin. I assumed 2.8.0 (the version the skills were checked against); G01 has to confirm it.

I didn't look up Gmail quotas, Gemini prices or provider terms because network access wasn't allowed.

**Next prompt (from the skill):**

```text
/adk-engineer Carry out G01 from docs/architecture/gmail-support-autoreply.md.
```