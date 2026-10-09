I've written the design and the implementation plan for the dispute assistant, plus `REPORT.md`. Everything is a draft built on assumed answers (you weren't available), so none of the decisions has been agreed by you yet.

**Files:** the design is in `docs/architecture/card-dispute-agent.md`, the plan in `docs/plans/card-dispute-agent.md`, and the session report in `REPORT.md`. The report covers the skills and reference files used, 17 assumed questions, the checks, a friction log with line pointers, and the next prompt.

**Profile:** production service. It handles regulated customer and payment data, real customers use it, and it writes cases into the core banking system.

**Key design choices:**
- **One agent, read-only plus drafts.** It has five tools, and none of them can create a case or receive a customer ID from the model.
- **Submit is outside the agent.** Only the customer's Submit button creates a case. Code checks that they confirmed the exact summary shown, checks eligibility again, then creates the case once, with a record that prevents duplicates. If the core system's reply is lost, the customer sees "We're confirming your dispute" and a background job finds the outcome.
- **"I didn't make this purchase" goes to the existing fraud process.** A fixed question on the summary screen decides this, not the model.
- **Card numbers never reach the model, the stored conversations or the logs.** They are redacted on the way in; if the redaction service is down, nothing is stored and the customer gets the dispute form.
- **Model and hosting:** `gemini-3.8-flash` on an EU Vertex AI endpoint, pinned. The service runs on Cloud Run in an EU region with Cloud SQL. The ADK version assumed is `google-adk==2.8.0`, to be confirmed in the first goal.

**Capacity and cut line:** I estimate about 2,500 focused hours, or about 2,000 after a 20% reserve. Phase 1 (G00–G13, through to GA) is 1,440–2,180 h, so it fits at the low and middle estimates but not the high end. The plan names four cuts that save about 190 h if work runs high; beyond that, the GA date or the size of the launch group has to move. Please confirm or move this cut line. Phase 2 (G14–G20, 700–1,120 h) waits until after GA: reading uploaded evidence, a second language, an extra prompt-injection screening layer, creating fraud cases, and tuning. The regulatory sign-offs (DPIA, model-risk approval, pen test) are the real critical path, so the plan gives each a target date.

**Still open:**
- Whether the core banking dispute API can safely retry a case creation without duplicating it. G00 is a discovery goal to find out, and it blocks G05.
- Whether the model is available in the EU region, and its retirement date.
- Whether Cloud Run, Cloud SQL and the redaction service are allowed inside the bank's network perimeter.
- How Compliance classifies this under the EU AI Act.
- Retention periods.
- Merchant-only scope at launch.
- Cloud Run versus a GKE platform the bank may require.

**What wasn't done:**
- No provider facts were looked up, since network access wasn't allowed. Those decisions are marked provisional, each with the exact check needed.
- The cost estimate is a formula, not figures.
- No ADK tests were run: there's no code and ADK isn't installed.
- The estimate sums and the links between the documents were checked by script; one total in the plan was wrong and is fixed.

Next prompt, for the first ready goal:

```text
/adk-engineer Carry out G01 from docs/plans/card-dispute-agent.md.
```