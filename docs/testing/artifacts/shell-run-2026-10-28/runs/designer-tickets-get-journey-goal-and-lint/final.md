I wrote the two ready tickets, but the lint still reports 4 errors, all about skills that aren't installed here. I'm leaving them rather than swapping skills, because that would contradict the plan.

**Tickets written** in `docs/tickets/claims/`:
- `G01-triage-draft.md` covers C4, is owned by Dev A, and has no blockers.
- `G03-handler-queue.md` covers C1 and SB01, is owned by Dev B, and has no blockers. It carries the Cloud SQL resource line from the plan, with the cleanup command and the owner of its lifetime.

G01 and G03 touch different paths, so both are `parallel_safe: yes`.

**Lint result** (`check_tickets.py`):
- **Errors:** `protect-adk-sensitive-data`, `adk-model-and-output-contracts`, `adk-fastapi-backend` and `adk-tool-auth-and-secrets` aren't in `.claude/skills/`. Only four skills are installed: evaluation, engineer, presenter and system-designer. The plan names these four, and I can't install packages in this run. Because they're missing, I couldn't cite `docs` references from them, so `docs: []` in both tickets.
- **Warning:** the `react-router` pin is "to be chosen" in the plan. I made G03 choose and record the pin in AGENTS.md.

**Left undone:**
- **G02** is blocked by W1 (the policy API credential) and G01.
- **G04** and **G05** are still `proposed` in the plan, not ready. I'll write G02 once W1 arrives, G04 once it's promoted to ready, and G05 for `adk-presenter` after G01–G04 finish.
- The plan has no detail entry for G03 beyond the stub, so I wrote its scope and A3 and A4 (tool-hop recheck, delete script) myself.

**Assumptions I proceeded on** (nobody could answer):
- "Ready" means the plan's state column reads `ready`, which is G01 and G03 only.
- I added extra acceptance items beyond the plan's own:
  - G01 A3: if de-identification fails, the draft is withheld.
  - G01 A4: the model is the pinned one and no secret sits in code (floor).
  - G03 A3: the tool refuses a claim outside the caller's team.
  - G03 A4: the delete script exists and its dry run names the instance (floor).
- Creating the Cloud SQL instance needs the owner's go-ahead. Tests use a local or in-memory database.
- The plan's name for each acceptance item is kept, so G01's A1 and A2 are unchanged from the plan.

**Open decisions:** the production approval review date (from the plan) and which skills will be installed for the engineer.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/claims/G01-triage-draft.md.
```