I wrote two tickets, G01 and G03. I couldn't run `check_tickets.py` because Bash is disabled in this session, so the tickets are unlinted.

**Tickets written** (the only two goals the plan marks `ready`):
- `docs/tickets/claims/G01.md`: Dev A, contract C4, `blocked_by: []`.
- `docs/tickets/claims/G03.md`: Dev B, contract C1 and SB01, `blocked_by: []`. It carries the Cloud SQL resource line, with the cost, the cleanup command and how absence is verified. It also has the shadcn and react-router companions and `docs/design/DESIGN.md`.

Both are `parallel_safe: yes` because their `touches` paths don't overlap.

**Left undone:**
- **Lint:** from the project root, run `python3 -I .claude/skills/adk-system-designer/scripts/check_tickets.py --tickets docs/tickets/claims` and fix any errors. I expect it to flag `protect-adk-sensitive-data` and `adk-fastapi-backend` as not installed. Only the ADK system-designer, engineer, presenter and evaluation skills are present in `.claude/skills`.
- **G02, G04 and G05:** G02 is blocked on W1, and G04 and G05 are only `proposed` in the plan. G02 and G04 also have no goal entries yet, and G05 has none either. I wrote no tickets for them.
- **Independent plan review:** not run, because this was a single non-interactive session.

**Assumptions and open questions:**
- **Fields I filled in:** the plan's G01 and G03 entries lack some ticket fields. I assumed `profile: MVP or pilot`, wrote the G01 and G03 `touches` lists myself, and added a G01 `(floor)` acceptance item A3 for the pinned model and no secrets in code. Please confirm or correct these.
- **Chosen react-router pin:** the plan leaves it as "to be chosen". I made G03 choose it and record it in AGENTS.md.
- **Paid cloud action:** I flagged creating `fm-claims-pilot-sql` in G03 as needing explicit authorisation. Local tests use a double.
- **C1 tool-hop recheck:** the design says the tool rechecks the claim's team, but the plan's G03 acceptance only covers the API. Should an acceptance item cover that recheck? I added only a helper to the scope.
- **SB03 proof:** the design cites `G02/A3` for SB03, but G02 has no goal entry or A3 in the plan. That needs fixing when G02 is detailed.
- **Production approval review date:** it is still open and sits with the plan owner.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/claims/G01.md.
```