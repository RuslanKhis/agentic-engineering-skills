I've written the design and plan as one file at `docs/architecture/travel-policy-bot.md`. It is a draft: nobody could answer questions, so every answer in it is an assumption.

**Design.** One `adk web` agent with one read-only tool, `search_policy`. The tool searches a `pages.json` file built once from the PDF, with the text split by page so every answer can cite a page. There is no vector database and no cloud resource, so nothing charges while idle. The model words the answer and the code decides what can be retrieved. If the policy doesn't cover the question, the bot says so and doesn't answer from general knowledge.

**Contracts.** There are five:
- **C1:** every claim cites a returned page. The model's compliance is tested, not enforced.
- **C2:** the agent has that one tool only.
- **C3:** a model-project quota caps spend, and the server stays on localhost.
- **C4:** no match means an explicit "can't find it".
- **C5:** every PDF page is covered, or listed as a gap.

**Plan.** About 3 h of the 4 h available, leaving a 1 h reserve:
- **G1:** ingest the PDF and check page coverage (0.75 h).
- **G2:** build the agent and tool (0.75 h).
- **G3:** run a 15-question check, including 3 questions outside the policy (0.75 h).
- **G4:** set the spend quota and prepare a 5-minute demo script (0.5 h).
- **G5:** stop the server and record results (0.25 h).

If G1 overruns, G3 shrinks to 8 questions. The spend cap and the refusal behaviour stay.

**Assumed answers**, for the questions I would have asked:
- The PDF is text-based and under about 60 pages.
- The demo is the only review.
- There is no deadline beyond today, and no continuation afterwards.
- There is no spend cap yet, and the team's cloud project is available for one.

**Left undone**
- The PDF isn't in the workspace, so I haven't checked it for scanned pages or tables. G1 does that first.
- The model ID is unpinned. The lifecycle table the design calls for isn't installed here, and I installed nothing and made no network calls.
- I haven't written any code, created tickets, or run the schedule checker. For a one-person plan, the estimates are added by hand.

The next step is:

```text
/adk-engineer Carry out G1 from docs/architecture/travel-policy-bot.md.
```