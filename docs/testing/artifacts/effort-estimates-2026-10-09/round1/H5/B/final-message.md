I've written the design, the plan, 20 phase 1 tickets and `REPORT.md`; nothing was implemented. Every user answer is an assumption (A1–A18 at the top of the design), so the design is a **draft** and no decision has been accepted.

**Profile:** production service, because external customers' personal data is involved and the assistant writes to Guidewire ClaimCenter, the system of record.

**The design in brief:**
- **Agents:** one ADK intake agent fills a versioned draft of the claim through three validated tools. A separate model call with no tools turns each photo into structured, editable suggestions.
- **Claim creation:** the agent can never create a claim. A code endpoint does it once the customer confirms a summary rendered from the saved draft.
- **Exactly one claim:** a durable record per submission, an idempotency key, and lookup before any retry protect against duplicates.
- **Hosting:** Cloud Run in Frankfurt (assumed), with Cloud SQL and Cloud Storage.
- **Model:** pinned to `gemini-3.8-flash`. `gemini-3.7-flash` was rejected because its Vertex AI retirement date (2027-01-28) falls before GA.

**Capacity and cut line:**
- **Capacity:** about 2,830 focused hours over 19 working weeks, about 2,120 after a 25 % reserve.
- **Phase 1 (G01–G20, through to GA):** 820–1,400 hours, so it fits even at the high end. The unused margin is deliberate: the schedule risk is waiting on other people, not hours. That means Guidewire sandbox access, the data-protection impact assessment, network allow-listing and the pen test.
- **Phase 2 (G21–G26):** claim status, hand-off to a human, a second market, streaming, analytics and tuning.
- **If hours run high:** the load test and dashboards shrink first; the identity, submission, data-protection, security and budget goals are never cut.

**Open decisions:**
- **O1:** does the Guidewire API support idempotent creates or lookup by an external reference? Without either, uncertain submissions need manual reconciliation.
- **O2:** is the chosen model available in an EU Vertex AI region with enough quota and EU processing terms?
- **O3:** does compliance confirm my reading of the data-protection assessment, EU AI Act and DORA? This is unverified.
- **O4:** must faces in photos be redacted before the model sees them?
- **O5–O8:** launch market, choice of judge model, who runs on-call, and all numeric targets.

**Checks:**
- **Run and passed:** estimate arithmetic, and a script that checks links, skill names and that each ticket's estimate matches the plan.
- **Not run:** any ADK test (none exist and dependencies aren't installed), and every provider or Guidewire lookup, because network access wasn't allowed.

Start G01–G03 this week, because their calendar waits are long. Then give the agent G04, the first goal that needs no outside access:

```text
/adk-engineer Carry out G04 Walking skeleton from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its accepted decisions.
Use adk-workflow-design with adk-release-engineering and adk-agent-instructions.
Work within local code and offline tests, verify the G04 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

Files are in the repo root:
- `docs/architecture/home-claim-intake.md`
- `docs/plans/home-claim-intake.md`
- `docs/tickets/home-claim-intake/` (G01–G20)
- `REPORT.md`