I've written the design and plan in `docs/architecture/travel-policy-bot.md` and the session report in `REPORT.md`. No code was written, since you asked for a design and plan. It's marked **draft** because you weren't available to confirm the assumptions behind it.

**Profile:** proof of concept. That's one builder for about 4 hours, a live `adk web` demo, one public PDF, answers only.

**Design:**
- **One agent, no tools, no search.** A single ADK agent gets the whole policy text in its prompt, with `[page N]` markers so answers can cite pages. With one short document nothing can be missed by a search step, and a turn can't loop.
- **Text loaded through a function.** The PDF text is read once at startup with `pypdf` and passed in through a function rather than a plain string. A plain string would break the agent if the PDF contains `{...}` text, because ADK treats braces as variables.
- **Model pinned to `gemini-3.8-flash`.** It's stable with no shutdown date. I ruled out `gemini-2.5-*` (Vertex retirement on 2026-10-20) and `gemini-3.6-flash` (2026-11-19).
- **Key and spend.** The API key lives in a gitignored `.env`. The spend cap is a budget alert on the key's Google project, because `adk web` doesn't let you set a per-run call limit.

**Plan and cut line:** three steps, 1.5–2.5 h against 2.4 h usable (4 h × 0.8 focus, minus a 25 % reserve).

| Goal | What it delivers | Estimate |
| --- | --- | --- |
| G01 | Local agent answering from the PDF, with an offline test for the PDF loader | 0.75–1.25 h |
| G02 | Six test questions, two of them about things the policy doesn't cover | 0.5–0.75 h |
| G03 | Demo dry run | 0.25–0.5 h |

The low end fits; the high end is about 0.1 h over. If G01 runs long, G02 drops to three questions. Phase 2, if the team wants to keep it:
- a 20+ case evaluation set;
- hosting on Cloud Run with sign-in;
- better handling of tables in the PDF.

**Still open:**
- your hours and familiarity with ADK;
- Gemini API key or Vertex AI;
- whether the PDF is text-based and under about 60 pages (a scanned PDF changes how the text is loaded);
- the citation format;
- the policy owner's name the bot should point people to;
- the budget alert, which needs your own console access.

**Checks:** I checked the plan's sums with a quick calculation and they match. No tests were run, because none exist yet and google-adk isn't installed. The skill's schedule checker wasn't run either; its own guidance says a one-person POC adds up estimates by hand. I skipped the independent plan review, which the skill also skips for a one-person POC.

The design is about 1,630 words against the skill's target of about 1,200. The assumptions table, the failure table and the deferred-controls table take up the extra, and I kept them. `REPORT.md` covers this and the other places where the skill's instructions disagree with each other.

Next prompt to type:

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```