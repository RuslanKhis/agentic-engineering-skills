# Release channel and plan health · 25 October 2026

Branch `release-and-plan-health`. Two parts of the improvement plan agreed on
25 October 2026: a release channel so installed skills can follow tagged
releases, and checks that keep a multi-ticket build tied to its design while
it runs. A field trial on the `field-feedback` branch also found a gap in the
`adk-agent-instructions` linter, which is fixed here.

## What changed

| Area | Change |
| --- | --- |
| Release | `metadata.version: "2026.10.25"` in every `SKILL.md`; `scripts/release.py` (`stamp`, `prepare`, `tag`, `show`) with `tests/test_release.py`; `CHANGELOG.md`; a CONTRIBUTING section |
| Package check | `scripts/validate_skills.py` fails when skills or versioned manifests carry different versions, when one is missing while others have one, or when a marketplace entry repeats the version |
| Plugins | `.claude-plugin/marketplace.json` and `plugin.json` (Claude Code), `gemini-extension.json` (Gemini CLI), root `plugin.json` (Antigravity, name and description only, as its schema allows) |
| Engineer | A once-per-session version comparison and a new-release notice from [updates.md](../../skills/adk-engineer/references/updates.md); a [ticket lifecycle](../../skills/adk-engineer/references/ticket-lifecycle.md) reference (resume from `Progress:`, finish, checkpoint routing, parallel worktrees); `actual:` in Evidence |
| Designer scripts | `plan_files.py` (shared reader), `plan_status.py` (roll-up, `--gate`, `--weekly`), `check_tickets.py` (lint and context budget), a journey rule and `type`/`status` passthrough in `check_schedule.py`; a fixture of a plan in progress and `tests/test_plan_status.py` |
| Designer instructions | Journey goal before each review of built work; `check_tickets.py` after writing tickets; a checkpoint section; templates gain `type`, `status`, `actual:` and `Progress:` (nothing removed) |
| Instruction linter | Follows one `from <module> import NAME` to a string constant in another project file, so the `prompt.py` → `agent.py` layout is linted; records `instruction_from` |
| Evals | 8 scenario cases and 2 activation cases (designer checkpoint positive, next-ticket near miss) |

## Checks run

- `scripts/check_repo.py`: passes (23 packages, 0 errors; every helper suite
  OK; optional SDK checks skipped as before).
- `tests/test_release.py`: 6 tests, also run with `HOME=/nonexistent` and no
  system git config to confirm they need no global git identity (CI has none).
- `claude plugin validate .` and `--strict` (Claude Code 2.1.306): pass. The
  only warnings come from the plugin directory profile (no icon, and two
  untracked `.DS_Store` files that are not committed).
- Plugin install into a throwaway `CLAUDE_CONFIG_DIR`: `claude plugin
  marketplace add <checkout>` then `claude plugin install
  agentic-engineering@agentic-engineering-skills`; `claude plugin details`
  lists all 23 skills at version 2026.10.25, about 4,000 tokens always on.
- `plan_status.py`, `check_tickets.py` and `check_schedule.py` on the
  plan-in-progress fixture: the expected checkpoint items (a contract delta,
  an open ruling, a 6 h overrun on a 2-3 h estimate, a phase that no longer
  fits 10 h), the stale design cells, the interrupted ticket, the overlap
  between two ready tickets, and the lint errors. Two defects were found and
  fixed while doing this: a resource line after `Rulings:` was read as a
  ruling, and a contract that no goal cites was hidden from the orphan check
  when a phase was selected.
- Instruction linter on the field trial's fixture (`pkg/prompts.py` imported
  into `pkg/agent.py`): before the fix, only `instruction_unresolved_reference`;
  after it, `unresolved_placeholder: tier` with `instruction_from:
  pkg/prompts.py`. A regression test covers absolute, relative and
  out-of-project imports.

Not verified: Gemini CLI and Antigravity installs (neither CLI is on this
machine), and Codex's plugin format, whose documentation is ambiguous; Codex
users keep the Skills CLI with a pinned tag. The `stable` branch and the first
tag do not exist until the maintainer runs `release.py tag` and pushes them,
so the plugin install commands in the README work only after that.

## Fresh-agent trials

Each trial agent got a scratch project under
`/private/tmp/claude-501/plan-health-trials/`, the path of the skill to follow
and the user's request, with no expected answer.

**A. Resume an interrupted ticket** (`/adk-engineer Resume
docs/tickets/support/G02.md from its Progress block.`). Passed. The agent
checked the uncommitted files the block named and reran its re-verify
command. It confirmed G01 was finished and compared the installed versions
(all 2026.10.25). It wrote the A2 and A3 tests first and saw five fail, then
fixed `final_state`. It set `verified_local`, removed the Progress block and
wrote `actual: not reported`, asking the person for hours. It updated only
C3's design Evidence cell, honestly as `offline` where the design had planned
`local`, and recorded a new ruling (an error followed by done counts as
failed). It ran `plan_status.py` and ended with the designer's checkpoint
prompt and its four items, not with the next ticket. Friction: none that
needed a change.

**B. Designer checkpoint** ("Checkpoint docs/plans/support.md. G01 … took me
about six hours. Phase 1 has 10 hours in total. I'm fine with forget being a
soft delete … but I don't want to drop the failed-state work."). Passed, with
one defect found in the script. The agent ran `plan_status.py` and took its
CHECKPOINT lines as the agenda:
- It revised C2 in place, so forget also clears the session-state copy, and
  added C6 (value purged within 30 days, a content-free audit record kept),
  deferring the purge with its trigger.
- It recorded the soft delete as proposal D4 and marked G01's ruling
  `settled: D4`.
- It updated the C1, C2 and SB01 Evidence cells.
- It added the A2 and A3 that G02's Progress block implied, and acceptance
  items for the empty journey goal G04.
- It made G03 wait on G02 because both write `Message.tsx`.
- It computed three cut-line options with the scripts, proposing to move the
  review presentation to phase 2, and left the choice to the user.
- It flagged the fixture's undefined decision D3.
- `check_tickets.py` ended with 0 errors.

**Defect:** a finished ticket's overrun stayed a checkpoint trigger after the
checkpoint, so the plan would keep asking for one. A finished overrun is now
reported under "Above estimate (finished)" and in the weekly RAID log. Its
consequence still triggers a checkpoint through the phase fit, as does an
unfinished ticket already past its estimate. Rerun on the trial's output, the
only item left was the cut-line decision it had handed to the user.

**C. Designer writes tickets from a plan with no journey goal** ("Turn the
ready goals in docs/plans/support.md into ticket files under
docs/tickets/support/."). Passed.
- `check_schedule.py` rejected the plan because the review presented built
  work with no journey goal before it. The agent added G04 (type journey,
  every earlier acceptance item in `pass_to_pass`) and made the review depend
  on it.
- It made G03 wait on G02 because G03's file sits inside G02's `touches`.
- It added acceptance items for SB01's own check and for C3's third end state.
- It wrote five tickets with `type`, `touches` and `pass_to_pass`.
- `check_tickets.py` reports 0 errors and 0 warnings. Estimated tokens of
  named skills and docs per ticket range from about 3,700 to 14,000, under
  the 30,000 budget.
- It also found that the fixture design omits floor security rules (SB03,
  SB05, SB10 and a spend stop). It recorded this as an open decision blocking
  G02 and G03 instead of writing tickets around it.

Friction: none that needed a change. The lint and the journey rule were found
and used from the designer's instructions alone.
