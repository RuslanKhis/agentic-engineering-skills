I wrote the design and plan and five phase 1 tickets, but I couldn't run the ticket checker because Bash is disabled in this session. I checked the ticket fields and acceptance items against its rules by reading them. Run `python3 .claude/skills/adk-system-designer/scripts/check_tickets.py --tickets docs/tickets/hr-policy-agent` before you start building. I also didn't run the schedule helper, since a one-person plan adds the hours by hand.

## What I did
- **Design and plan:** `docs/architecture/hr-policy-agent.md` holds both. It is a draft, in the compact one-file form for a proof of concept.
- **Shape:** one ADK agent with a single `search_policies` tool. The tool does BM25 keyword ranking over page-level text from the PDFs. There is no vector database, no hosting and no cloud resource, so nothing charges while idle and no teardown goal is needed. It runs in `adk web` on your laptop for the demo.
- **Contracts C1–C5:**
  - **C1:** every citation must match a page the tool actually returned, or the answer is replaced with "not found".
  - **C2:** answers come only from the approved PDF list.
  - **C3:** every PDF page has a recorded extraction, and empty pages are listed.
  - **C4:** questions about a named person or legal or eligibility decisions get general policy plus a referral to HR.
  - **C5:** a cap on model calls per question, a provider spend quota, and no API key in source.
- **Tickets:** G01 to G05 in `docs/tickets/hr-policy-agent/`.
  - **G01:** ingest the PDFs and report per page.
  - **G02:** build the search tool and 10 gold questions.
  - **G03:** the agent in `adk web`, with the citation check and call cap.
  - **G04:** run the gold questions and hand-review the answers.
  - **G05:** demo script, dry run and a fallback transcript.
- **Phase 2 and later:** phase 2 is outlined in the design, not ticketed: labelling with an HR reviewer, OCR for scans, hybrid retrieval, Cloud Run with sign-in.

## Does it fit?
The phase 1 estimate is 3.5 to 5.5 hours. Usable time is 4.5 hours (6 hours minus a 25% reserve), so **only the low end fits**. G01–G03 and G05 alone come to 4.75 hours at their high ends. G04 is the goal that shrinks, in three steps:
- **3.0 hours or less used after G03:** G04 runs as written.
- **Between 3.0 and 4.0 hours:** G04 runs on 5 of the 10 gold questions.
- **Over 4.0 hours:** G04 drops to a hand read of the answers during the G05 rehearsal, and the demo says answer quality isn't measured yet.

Please confirm or move that cut line.

## Questions I couldn't ask, and what I assumed
- **Model provider approval (W1):** I assumed you can send the policy text to the model provider, but that isn't confirmed. It blocks G03, so request it today. If it's refused, the plan needs a local-model route.
- **PDF quality:** I assumed the 30 PDFs are current versions with extractable text. G01 will show any scans, and OCR is deferred.
- **Your hours and experience:** I assumed the 6 hours are focused time on Wed 28 and Thu 29 Oct, and that you're new to ADK. The ADK-specific estimates include a 1.5× allowance for that.
- **Spend:** I assumed at most USD 10 of model spend, capped by a quota you set on the model project.
- **Model and ADK version:** the model ID is provisional because the dated model lifecycle table isn't in this workspace. G03 pins it. ADK 2.8.0 is the working assumption, and G01 confirms it.
- **Presentation skill:** `adk-presenter` isn't installed, so G05 is a demo-readiness goal carried by `adk-engineer`, not a slide deck.

## Left undone
- No code, installs, network calls or cloud work, as requested.
- C4 has no deterministic screen; the design records that as an accepted gap for the proof of concept.

## Next prompt
```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01-corpus-ingestion.md
```