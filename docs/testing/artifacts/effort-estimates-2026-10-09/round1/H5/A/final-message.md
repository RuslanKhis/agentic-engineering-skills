I've written the design, the plan and 20 ticket files for phase 1. Nothing was implemented or committed. Every scope question was answered by assumption (Q1–Q19, listed at the top of the design), so the whole design is marked **draft** and none of it has your approval yet.

**Profile:** a production service. It serves external EU customers, handles personal data and writes to Guidewire, which is the official record.

**Recommended design:**
- **One agent** gathers the claim. It has four narrow tools and fills in a versioned claim draft.
- **Photos** are read by a separate step that has no tools and only returns structured findings. The agent never sees the images themselves.
- **Submission** happens only when the customer presses Submit on a specific version of the draft. The model cannot trigger it.
- **Exactly-once filing:** each submission gets a lasting record of the operation. A background worker sends it to Guidewire and, if Guidewire's reply is lost, checks before trying again.
- **Hosting** is Cloud Run with Cloud SQL, all in one EU region.
- **Model:** `gemini-3.8-flash`, pinned, chosen from the skills' dated model-retirement table (checked 2026-10-08).

**Capacity and cut line:**
- About 2,976 focused hours over 20 working weeks, or about 2,232 after a 25% reserve.
- Phase 1 is G01–G20, everything needed for GA. It is estimated at 1,348–2,104 h, so it fits even at the high end.
- The tightest constraint is the security reviewer: about 72 usable hours against a demand of 48–68.
- If work runs long, the plan lists what to cut first. It starts with dropping photo pre-fill and keeping only the quality check, then moving English as the second language to after GA. Identity, the exactly-once submission and the data, security and budget controls are never cut.
- Phase 2 (P2-01 to P2-08, after GA) and a "later" list are written into the same plan.

**Decisions still open:**
- **Guidewire:** whether it supports idempotency or lookup by our own reference. No Guidewire behaviour in the design is verified; G02 finds out.
- **Login:** how a customer's login maps to their Guidewire account.
- **EU region:** whether `gemini-3.8-flash` is available there, plus quotas and prices. No network was allowed, so the cost estimate is only a formula; G03 checks.
- **Photo metadata:** whether original photos go to Guidewire with their metadata (including location). The DPO needs to decide.
- **Budget figures and the reviewer's time allocation.**

**Checks:** a local script checked links, skill names, ticket fields, dependencies and goal coverage, and found no problems. No tests were run: there is no code, and `google-adk` isn't installed. The Mermaid diagrams weren't rendered or validated.

`REPORT.md` covers the skills and references I used, the assumed answers, a friction log with file:line pointers into `.claude/skills/`, and the exact next prompt quoted verbatim.

Next ready goal (fully local):

```text
/adk-engineer Carry out G01 (walking skeleton) from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its accepted decisions.
Use adk-workflow-design with adk-model-and-output-contracts.
Work within local-only scope (no cloud, no Guidewire), verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

G02 and G03 can run alongside it once someone has Guidewire sandbox access and an approved GCP project.

Files are in `docs/`:
- architecture/home-claim-intake.md
- plans/home-claim-intake.md
- tickets/home-claim-intake/G01-walking-skeleton.md to G20-pilot-and-ga-readiness.md

The report is `REPORT.md`, in the repository root.