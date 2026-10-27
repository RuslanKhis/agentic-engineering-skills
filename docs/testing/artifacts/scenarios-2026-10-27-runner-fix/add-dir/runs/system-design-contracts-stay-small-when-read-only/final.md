I wrote the design and plan to `docs/architecture/travel-policy-bot.md`. It's one page and marked draft, because nobody could confirm the assumptions.

**Design:** This is a proof of concept. It uses one ADK agent with no tools and no sub-agents. The whole policy text goes into the instruction, with `[page N]` markers so answers can cite pages. I chose that over RAG for a single PDF. A keyword search can miss a paraphrase like "lodging cap" versus "hotel limit", and managed RAG costs setup time and money while idle. If the PDF turns out to be over about 60 pages, the fallback is one search tool over page chunks.

**Contracts:**
- Every claim cites a page, or the bot says it can't find the answer.
- The agent reads one fixed file and has no write or browse tools.
- The bot never approves a request or promises an exception.
- Text inside the PDF is treated as data, not instructions.
- Spend is stopped by a quota on the model project. `adk web` doesn't let you set `max_llm_calls`, so the quota has to be set by you.

**Plan (about 4 hours):**
- G01: extract the PDF to page-tagged text and check the layout. This comes first, because a scanned or table-heavy PDF would break the budget.
- G02: build the agent and run it in `adk web` on loopback only, with a pinned model.
- G03: write 8 gold questions, check the answers by eye, and include an approval request and an injected line.
- G04: run the demo through once, with screenshots as a fallback.
- Goals total 1.75–2.75 h against 2.4 h available after the reserve. The low end fits, but the high end overruns by 0.35 h. If you run high, cut G03 to 5 questions, not the safety floor.

**Questions I couldn't ask, and what I assumed:**
- PDF size and layout: I assumed it has a text layer and is under 60 pages.
- ADK experience: I assumed you know ADK basics, so I applied no multiplier. A new-to-ADK multiplier of 1.5 would not fit.
- Model access: I assumed a Gemini key or Vertex project you already have.
- After the demo: I assumed the bot is continued only if the team likes it.

**Left undone:**
- I didn't build anything or install any packages.
- I didn't look up the model ID. G01 picks it from the ADK model-lifecycle table.
- The plan is unreviewed, and I ran no schedule checker. The estimates are summed by hand, as the one-person form allows.
- The workspace was empty, so there was no existing code to inspect.
- I didn't write tickets.

Next prompt:
```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```