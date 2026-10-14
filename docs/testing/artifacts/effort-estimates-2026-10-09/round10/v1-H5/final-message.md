I've written the design, the plan and 25 ticket files for phase 1. Phase 1 fits the team's hours easily but fits the five-month calendar only if things go well. Nothing was implemented, and you weren't available, so every answer in the design is an assumption and all decisions are drafts.

**Documents**
- Design: `docs/architecture/home-claim-intake.md`. It opens with an assumed-answers table (18 questions), then covers decisions D1–D14, the guarantees, a failure grid for every external system, and open decisions O1–O6.
- Plan: `docs/plans/home-claim-intake.md`, including the schedule, the remedies I tested, phase 2 and a later list.
- Tickets: `docs/tickets/home-claim-intake/G01–G25`, one per phase 1 goal.
- `REPORT.md`: the six sections you asked for, including the friction log with pointers into the skill files.

**The design in brief.** I treated this as a production service. One ADK agent collects the claim details, and a separate model call with no tools describes the photos. The agent cannot write to Guidewire at all. The claim is created only when the customer presses Submit on a summary built from the stored draft. Each confirmed draft gets a durable record so it creates at most one claim. A scheduled job resolves cases where Guidewire may have created the claim but the reply was lost. Everything runs in one EU region; the model is pinned to `gemini-3.8-flash`, chosen from the skill's model lifecycle table.

**Cut line**
- **Hours:** phase 1 (everything up to GA) needs 702–1070 hours of the 2,280 available after a 25% reserve. Nobody is more than half loaded.
- **Calendar:** finishing takes 70.6–106.7 working days against the 95 available, because external waits and an invite-only pilot sit on one long chain. Moving GA to 107 working days (about end of March 2027 instead of mid-March) fits even the high end. Giving the security reviewer more hours made no difference.
- **To get there,** I changed four dependencies, each because the work doesn't actually need the wait (listed in the plan's change table):
  - The confirmation and claim-record logic is built against a fake Guidewire, so it doesn't wait for sandbox access.
  - The evaluation set is split so the photo work can start earlier.
  - The security review is split into two smaller reviews.
  - The pilot runs during the external pen test, which needs your security team's approval (O3). Without it, GA moves by about 12 working days.
- **Phase 2:** a feedback loop from production claims into the evaluation set, a second EU market, the mobile app, cost tuning and a model migration rehearsal.

**Decisions still open**
- **Region (O1):** whether the model is served from an EU regional endpoint, and which region. The first ticket checks this before anything else depends on it.
- **Guidewire (O2):** whether its API safely handles a repeated create, or we must rely on looking claims up by our own reference field.
- **Pilot during the pen test (O3):** as above.
- **Assumed answers:** confirm them, especially the Guidewire setup, claim volumes, strict EU residency for model calls, and retention periods.

**Checks**
- The skill's schedule checker found no mismatch between the plan and the tickets. It reports "fits at the low end only" at 95 days and passes at 107 days.
- The checker's own 14 unit tests pass.
- Every relative link in the plan resolves; links inside the design and tickets weren't checked.
- Nothing that imports `google.adk` was run, and nothing touched the network.

**Requests to send on day 1:** Guidewire non-prod access, the login-provider client registration, the GCP projects, legal review of the AI notice wording, and a Guidewire load-test window. Book the pen-test vendor too. The security reviewer can start the DPIA pack (G15) now, alongside G02.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```