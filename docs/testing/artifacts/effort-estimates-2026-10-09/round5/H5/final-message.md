I've written the design, the plan and 28 phase 1 tickets. Phase 1 fits easily in hours, but the GA date of 2027-03-09 only holds if nothing runs long. At the high end it needs either a later date or more of the security reviewer's time. Nothing was implemented, and no cloud, Guidewire or network calls were made.

**Profile:** production service, because it serves external customers, handles personal data and writes to Guidewire. Phase 1 is everything needed for GA in one EU market (G01–G28). Phase 2 (P2-01 to P2-06) covers post-GA work, and a Later list holds deferred items with what would bring each forward.

**Core design:**
- **One agent, no write tool.** A single ADK agent collects the loss details and keeps a versioned claim draft. Photos are read by a separate model call that has no tools and returns structured observations, so text inside a photo can't trigger anything.
- **The claim is created by ordinary code, not the model.** It happens only when the customer clicks confirm on the exact summary they saw. A stored submission record makes sure each confirmed draft creates at most one claim, even if a reply from Guidewire is lost.
- **Hosting and model:** Cloud Run in an EU region, with the model pinned to `gemini-3.8-flash` on Vertex AI in the EU. The two other recent Flash models retire on Vertex before GA.

**Capacity and cut line** (from the skill's schedule checker, with the 28 tickets matching the plan):

| Option | Finish (working days) | Fits? |
| --- | --- | --- |
| As stated: reviewer one day a week, GA 2027-03-09 (95 days) | 71–106 | Only if nothing runs long |
| Reviewer two days a week, same GA date | 66–98 | 3 days short at worst |
| Reviewer two days a week, GA moved to 2027-03-12 | 66–98 | Yes |
| Reviewer unchanged, GA moved to 2027-03-25 | 71–106 | Yes |

- **Hours are not the problem:** phase 1 needs 462–696 of about 2,650 available hours. The date is set by external waits: the Guidewire sandbox, the external pen test, a 2–3 week pilot and the canary rollout, plus the part-time reviewer.
- **My recommendation:** ask for two reviewer days a week and commit to GA on 2027-03-12.
- **Fallback:** if the date can't move, open GA on 2027-03-09 to the pilot group only and finish the rollout the following week.
- Every goal on the critical path is a minimum safety requirement, so cutting scope doesn't bring the date in.

**Questions I couldn't ask:** you weren't available, so I assumed 13 answers; they're listed at the top of the design. The ones that matter most:
- the market (Germany, German and English);
- Guidewire Cloud APIs, and whether they deduplicate a repeated create request (I assumed a header name from memory);
- whether `gemini-3.8-flash` is available with image input in the EU;
- retention periods and the AI Act classification, which need DPO and legal sign-off.

Each of these has a goal that checks it.

**Checks:** the skill's own tests passed (10 of 10, run with Python 3.12 because the default `python3` here is 3.9). No application tests exist yet, since there is no code and google-adk isn't installed.

Files are in `docs/`:
- architecture/home-claim-intake.md
- plans/home-claim-intake.md
- tickets/home-claim-intake/
- REPORT.md (in the working directory; it has the friction log and the full list of assumptions)

Next prompt to type:

```text
/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its decisions.
Use adk-workflow-design with adk-tool-interface-design and adk-memory-architecture.
Work locally only (no cloud, no Guidewire), verify the acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

G02 (Guidewire access requests), G03 (DPIA and legal review) and G04 (EU cloud setup) can start the same day with other owners.