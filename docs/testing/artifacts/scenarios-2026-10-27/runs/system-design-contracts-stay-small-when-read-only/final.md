I wrote a short design and plan, about 1,100 words, to `docs/architecture/travel-policy-bot.md`. It is a draft, and no one has reviewed it.

**Design:** I treated this as a proof of concept you may keep, with one `LlmAgent` and one tool, `search_policy`. You extract the PDF once into page-tagged chunks and rank them locally with BM25. The tool returns passages with page numbers, and the bot answers with a page citation. If the policy doesn't cover the question, or the question is about a personal exception, it says so and points to the travel team. There is no vector database or cloud resource, so nothing keeps costing money and no teardown is needed.

**Plan, about 1.5–2.25 hours of work against 2.4 available after a 25% reserve:**
- **G01 (0.75–1h):** ingest the PDF and write the search tool. It should return a clear error if the chunk file is missing.
- **G02 (0.5–0.75h):** build the agent and run 8 hand-checked questions in `adk web`. Six should be answerable and two shouldn't. I assumed the hours at 1.5 times a normal ADK estimate in case you're new to it.
- **G03 (0.25–0.5h):** pick the demo questions and do a dry run.
- **If time runs short:** cut the extra demo questions first, then trim the gold set to 5. Don't cut the spend cap or the "not found" behaviour.

**Questions I couldn't ask, and what I assumed:**
- **Deadline and afterwards:** the demo is this afternoon, and the bot is continued if the team likes it.
- **Builder:** one developer with 4 hours, and ADK experience unknown.
- **Spend:** a small allowance.
- **Audience:** the team, watching a live demo.
- **Access:** `adk web` on localhost only.
- **Data:** one public PDF and no personal data.
- **Extras:** no statement of work, and no lock-in concern.

**Left undone or open:**
- **Model and ADK pin:** I didn't pick a model ID or ADK version. The model lifecycle table the skill refers to isn't in this workspace. G01 should pin them against what you have installed.
- **The PDF:** it isn't in the workspace, so I haven't seen its size, or whether it's text or a scan. A scan would need OCR and break the estimates. If it's under about 30 pages, pasting it into the prompt may be simpler than search.
- **Spend cap:** `adk web` won't let you set a call limit, so set a spend cap on the model project yourself before the demo.
- **Citation enforcement:** the citation rule lives in the prompt, so I can't guarantee it. The 8 gold questions are the only check on it.
- **Not done:** I didn't write tickets or run the schedule checker. A one-person plan doesn't need them.

Next step:
```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```