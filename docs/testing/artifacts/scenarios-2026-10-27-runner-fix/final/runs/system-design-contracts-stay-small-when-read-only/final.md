I wrote the design and plan to `docs/architecture/travel-policy-bot.md`. It's a draft that nobody has reviewed, and I haven't built or run anything.

**Design**
- **Profile:** proof of concept, about 1,200 words.
- **Shape:** one ADK agent with one read-only tool, `search_policy`. The PDF is split into one chunk per page and searched by keyword, with no vector store. It runs locally with `adk web`.
- **Behaviour:** answers cite the page number. If the policy doesn't cover a question, the bot says so. It has no write, send or network tools.
- **Contracts:** four, C1–C4, each with a check.
  - **C1:** every claim carries a real page citation.
  - **C2:** no match means "not in the policy", with no guessing.
  - **C3:** the agent has no write, send or network tool.
  - **C4:** a tool failure shows a plain error message.

**Plan** (3.75 of about 4 hours, so tight)
- **G1, ingest the PDF:** 0.75 h.
- **G2, agent and search tool:** 1.25 h.
- **G3, 12-question gold set and fixes:** 1.25 h.
- **G4, demo rehearsal and runbook:** 0.5 h.

If the PDF turns out to be scanned or table-heavy, cut the gold set from 12 questions to 8 and keep the contract checks. No cloud resources are created, so there is no teardown step. Phase 2 and later ideas are listed in the file.

**Questions I couldn't ask, and what I assumed**
Each is in the file's assumed-answers table, and the decisions that depend on it are provisional.
- **Team and money:** one developer with moderate ADK familiarity, and a small model-API allowance.
- **Audience and exposure:** a live demo for colleagues, on localhost only.
- **Data:** a public, text-based PDF of under about 100 pages.
- **Model access:** you already have a working Gemini key or Vertex access.
- **Review and lock-in:** the demo is the only review, with no SOW and no lock-in concern.

**Left undone**
- **Model ID and ADK version:** I didn't check the model ID or the ADK version, because lookups were off-limits here. G2 confirms both against current docs.
- **PDF check:** I never saw the PDF, so whether it's short and text-based is only assumed. G1 checks it.
- **Independent review:** I skipped it, since this is a single-person proof of concept. The file says it's unreviewed.

Next prompt:
```text
/adk-engineer Carry out G1 from docs/architecture/travel-policy-bot.md.
```