I wrote the design and plan as one file, plus three phase 1 tickets. I haven't implemented anything. I also couldn't run `check_tickets.py`, because this session has no shell tool. I wrote the tickets to the linter's rules by reading its source, so run it before relying on them:

```bash
python3 <skills>/adk-system-designer/scripts/check_tickets.py --tickets docs/tickets/hr-policy-agent
```

**Files**
- `docs/architecture/hr-policy-agent.md` holds the design and plan together. It's marked draft and has an assumed-answers table at the top.
- `docs/tickets/hr-policy-agent/G01-ingest-and-coverage.md`, `G02-grounded-search-agent.md` and `G03-gold-check-and-demo.md`.

**Design and cut line**
- **Profile:** proof of concept, with code meant to be kept.
- **Shape:** one ADK agent with one tool, `search_policies`. It searches a local page-level index with BM25 and answers with `[title, p. N]` citations. If nothing matches, it says the policies don't cover the question and refers the user to HR. There's no vector database or cloud resource, so no teardown goal.
- **Contracts:** five of them, covering citations, not-found, coverage of every PDF, read-only scope, and a spend and search cap. The spend cap has to be set by you on the model key; `adk web` owns the Runner, so the code can't set it.
- **Phase 1 effort:** G01 ingest takes 1.0–1.5h, G02 agent and tool 1.25–1.75h, G03 gold-question check plus demo run-of-show 1.0–1.25h. That sums to 3.25–4.5h of your 6h, and the 1.5h reserve is the only cushion, so it fits with nothing spare. I applied ×1.5 for being new to ADK and added the hours by hand.
- **If time runs short:** the order that stays useful is G01, then G02, then G03. Shrink G03 first.
- **Phase 2:** OCR, embeddings, sign-in with hosting, and an HR-verified question set, written without tickets.

**Assumptions and questions nobody answered** (the first three are the ones that matter)
1. I assumed the PDFs are mostly text-based. Scanned pages would be reported, not read, since OCR is deferred. G01's coverage report will show how many there are, so it runs first.
2. I assumed the PDFs may be sent to a hosted model and contain no employee personal data.
3. I assumed your six hours are focused. If they're interrupted time, only G01 and G02 at their low ends fit.
4. I assumed Gemini through an API key. I couldn't check the model ID or the ADK 2.8.0 pin, because the dated model table isn't installed here, so G01 and G02 confirm both.
5. Can an HR person give you 5–10 real questions with the answering page by Thursday? I assumed not, so you write the gold set and the demo says it isn't HR-verified.
6. I wrote no presentation goal, because `adk-presenter` isn't installed. The live demo is covered by G03's run-of-show, so there's no deck.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01-ingest-and-coverage.md.
```