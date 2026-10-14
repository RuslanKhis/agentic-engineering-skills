I've written the design and plan in one file, `docs/architecture/travel-policy-bot.md`, plus `REPORT.md`. The design is marked draft because you weren't available, so every answer it depends on is an assumption, and each one is recorded.

**What it proposes:** a proof of concept with one ADK agent and no tools. The policy PDF is turned into text once, with a page marker on each page, and the whole text goes into the agent's instructions. No search index or database is needed for one document. Answers cite the page they came from, and a question the policy doesn't cover gets "the policy doesn't cover this". The model is pinned to `gemini-3.8-flash`, chosen from the skill's dated model list (checked 2026-10-08), not from memory. Because `adk web` runs the agent itself, you can't set a call limit in code, so the spend cap is a daily request quota on your Google Cloud project plus a limit on answer length.

**Plan for the afternoon:** about 4 hours, of which roughly 2.4 are usable after a 25% reserve.

| Goal | What it delivers | Estimate |
| --- | --- | --- |
| G01 | The bot answers from the PDF in `adk web` | 0.75–1.25 h |
| G02 | 4 hand-checked test questions | 0.25–0.5 h |
| G03 | Quota set, one dry run, backup screenshots | 0.25–0.5 h |

That's 1.25–2.25 h in total, which fits. I cut the test questions from six to four to get there. If time runs short, do G01, then G03, then G02. Running the bot for real users, a larger evaluation set and a policy-version owner are written up as phase 2 for if the demo lands.

**Checks:** the skill's schedule checker passes with the four-question version. It also found two problems along the way, both now fixed: the original six-question plan only fit at the low end, and one test was counted for two different failures. Nothing involving ADK was run, because it isn't installed here. The model ID and ADK version (assumed 2.8.0) are unverified; G01 includes checking them.

**Questions for you:**
- Do you have a Gemini API key? Using Vertex AI instead would add about half a day of setup.
- Is the PDF real text rather than a scan? A scanned PDF needs a different way of reading it.
- Is the cut line acceptable?

`REPORT.md` covers the rest. One gap: the document is about 1,500 words against the skill's target of about 1,200. The report also notes where the skill's instructions contradict each other, mainly on whether to run the schedule checker.

Next prompt:

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```