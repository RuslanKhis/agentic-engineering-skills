I've written the design and plan in one file, `docs/architecture/travel-policy-bot.md`. It's still a **draft**: you weren't available, so I assumed the answers to my questions and recorded each one in an "assumed" table at the top. No code was written, since you asked for a design and plan.

**The design:** one ADK agent with no tools, run locally with `adk web`. When it starts, it reads the PDF once, adds `[page N]` markers and gives the whole text to the model. It answers only from the policy, cites the page, and says "not covered by the policy" when the PDF is silent.

**Choices worth knowing about:**
- **Policy text goes in `static_instruction`, not the normal `instruction`.** ADK treats `{...}` in a normal instruction as a variable and crashes on any brace in the PDF.
- **Model: `gemini-3.8-flash`**, pinned, from the model table dated 2026-10-08. I avoided the `gemini-2.5-*` models because their Vertex retirement date is 2026-10-20.
- **Spending:** with no tools, each question makes exactly one model call. Add a budget alert on the API key's project, because `adk web` ignores the usual per-run call limit.

**Profile:** proof of concept. I assumed one developer new to ADK with about 4 hours. That gives roughly 3.2 focused hours, or **2.4 h** after a 25% reserve.

**Cut line:** the three goals (G01 skeleton, G02 answers from the PDF, G03 eight test questions and a dry run) add up to **2.0–3.0 h**. That fits at the low end but not the high end. If time runs short, cut G03 to three questions; after G02 alone the demo already works. Phase 2 (a larger test set, hosting for colleagues, policy versioning) and the deferred items are written into the same file.

**Open decisions:**
- **U1 – PDF length:** I assumed under about 50k tokens. If it's longer, you'll need search over the document instead of putting it all in.
- **U2 – tables or scanned pages:** if the text doesn't extract cleanly, the fallback is to send the PDF file itself to the model.
- **U3 – API key or Vertex AI:** I assumed a Gemini API key. Vertex would add about half a day.
- **U4 – model table date:** re-check the model table before the demo.

**Checks:**
- **Not checked by the script:** the skill's script can't check the failure table without a schedule block, which the short format leaves out. I checked its references by hand and they're all valid.
- **Script tests passed:** the script's own tests passed (16).
- **Not run:** the bot itself, since google-adk isn't installed and there's no PDF here.
- **Over length:** the document is about 1,600 words against the skill's target of about 1,200.

`REPORT.md` has the files I read in order, all nine assumed questions, the checks, and notes on where the skill's instructions were unclear or contradicted each other.

Next prompt:

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```