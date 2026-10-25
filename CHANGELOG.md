# Changelog

One section per tagged release, newest first. Pin a release with
`npx skills@latest add RuslanKhis/agentic-engineering-skills#v<version> --skill '*'`.

## 2026.10.25 · 25 October 2026

First tagged release. Earlier changes are recorded in the README under
Compatibility & Checks.

- **Releases and updates.** Every skill carries `metadata.version`.
  `scripts/release.py` stamps a release, writes this changelog and tags it.
  The validator fails when skills or manifests disagree. `adk-engineer`
  reports a mixed installation or a newer release in one line and never
  updates anything itself. Plugin manifests for Claude Code, Gemini CLI and
  Antigravity follow the `stable` branch.
- **Plan health during the build.** The designer's `plan_status.py` reads
  ticket evidence back into the plan: contract and security-rule coverage,
  contract deltas and rulings waiting for a decision, the ready and
  interrupted tickets, safe parallel groups, hours spent and remaining
  against capacity, a phase-exit gate (`--gate`) and a weekly status update
  with a RAID log (`--weekly`). `check_tickets.py` lints tickets after they
  are written. `check_schedule.py` requires a journey goal before a review of
  built work. The designer gains a checkpoint mode. The engineer gains a
  ticket lifecycle covering resume from a `Progress:` block, checkpoint
  routing and parallel worktrees. The ticket and plan templates gain `type`,
  `status`, `actual:` and `Progress:`; nothing was removed.
- **Instruction linter.** `adk-agent-instructions`' linter now follows an
  instruction imported from the prompt module into `agent.py`, which a field
  trial showed it had silently skipped.
