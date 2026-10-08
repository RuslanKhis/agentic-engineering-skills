# Fresh-session before/after measurement · 9 October 2026

This replaces the reconstructed friction logs in the
[usage journey record](usage-journeys-2026-10-09.md) with first-hand ones, and
measures whether the product pass of 9 October (commit `73599b5`) reduced
friction compared with the skills one commit earlier (`a1fe2d5`).

## Method

- **Real installs, fresh hosts.** For each condition the skills were installed
  with the real installer (`npx skills@latest add <source> --skill '*' -a
  claude-code`) into twelve fresh copies of the
  [fixture app](artifacts/journeys-2026-10-09/fixture/), one per journey and
  condition. Each journey then ran in a new headless Claude Code session
  (`claude -p`, Claude Code 2.1.294, model Opus 5.5) with
  `--setting-sources project`, so only the project's installed skills were
  visible. The [runner](artifacts/before-after-2026-10-09/run.sh) and the
  shared [prompts](artifacts/before-after-2026-10-09/prompts.tsv) and
  [session rules](artifacts/before-after-2026-10-09/friction.txt) were
  identical across conditions.
- **Journeys.** The greenfield design brief (J1, the corpus's designer
  scenario) and the five maintenance tickets (T-101 to T-105), each started
  with the same `/adk-system-designer` or `/adk-engineer` prompt as the earlier
  trial. Each agent wrote its own friction log in REPORT.md.
- **Permissions.** Headless sessions cannot answer permission prompts, so they
  ran with permission checks disabled, inside scratch copies only, with network,
  cloud and package installs forbidden by the prompt.
- **Blind grading.** A separate agent graded each pair, labelled A and B with
  the condition randomised per task, on five 1 to 5 dimensions: outcome,
  correctness, completeness, next-step clarity and user friction. The mapping
  was revealed only after grading
  ([grades](artifacts/before-after-2026-10-09/grades.json),
  [mapping](artifacts/before-after-2026-10-09/blind_mapping.json)).

## Discovery in a fresh host

A fresh session with project-only settings discovered all twenty skills with
their current descriptions. With default settings on the maintainer's machine,
it also discovered twenty, but the twelve skills that also existed in an older
user-level install were served **from that older copy**: the user-level skill
takes precedence over the project copy of the same name. The README now warns
about this and says how to check which copy a session loaded.

## Results

The blind grader preferred the after condition in all six tasks.

| Task | Before (of 25) | After (of 25) | Most important difference, per the grader |
| --- | --- | --- | --- |
| J1 design | 19 | 23 | After pinned current models from the dated lifecycle table and overrode ADK's default judge, which retires in 11 days |
| T-101 wrong tool | 16 | 21 | After made the package importable without the SDK so its tests ran (13 passed) and dropped the forced-tool instruction |
| T-102 MCP servers | 17 | 20 | After put the MCP tools on a separate read-only agent instead of the root agent that can send email |
| T-103 model retiring | 17 | 21 | After added a real eval gate (eval set, strict checker, "not run" fails) beyond the model swap |
| T-104 security review | 19 | 21 | After wrote the review and then made the structural fixes with tests; before wrote the review only |
| T-105 prose output | 18 | 21 | After's contract tests did not need the SDK and ran (11 passed) |
| **Total** | **106** | **127** | |

| Dimension (sum over six tasks, max 30) | Before | After |
| --- | --- | --- |
| Outcome | 22 | 25 |
| Correctness | 23 | 25 |
| Completeness | 21 | 30 |
| Next-step clarity | 21 | 26 |
| User friction | 19 | 21 |

Structural checks, read from the artefacts:

| Check | Before | After |
| --- | --- | --- |
| Ticket agents that announced their specialist before editing | 3 of 5 | 5 of 5 |
| Ticket agents that recorded evidence back in the ticket file | 0 of 5 | 5 of 5 |
| Design plan goals with their own run prompt | 0 of 5 | every goal |
| Design closed with a copyable prompt for the next goal | yes | yes |

Effort across the six sessions: before 105 turns, 24 minutes; after 120 turns,
28 minutes. Token use, expressed as the CLI's `total_cost_usd` estimate at public
API prices, was 6.63 before and 8.61 after, about 30 percent more. No API key was
used and nothing was billed per run: the sessions ran under a claude.ai
subscription login and drew on that plan's usage allowance. The after runs did
more of the requested work (completeness rose most), which accounts for most of
the extra token use.

## Friction that remained, and what was changed

From the after condition's own friction logs:

| Friction | Change |
| --- | --- |
| Helpers scanned the installed skills in `.claude/skills/` as if they were project code, producing tens of kilobytes of irrelevant findings and failing on unrelated skill files | Every project inspector now skips coding-agent skill folders (`.claude`, `.agents`, `.codex`, `.gemini` and others) and `.adk-evidence`; regression test added. The model audit fell from 30 KB to 4 KB of output on the fixture |
| Validation references wrote evidence to `/tmp`, which sandboxes forbid or clear | Evidence now goes to a gitignored `.adk-evidence/` folder at the project root |
| The designer had no pattern for a user who cannot answer | An **Assumed answers** table at the top of the design, with dependent decisions marked provisional |
| A single ticket ended with no useful next prompt | When no next ticket exists, the router ends with the prompt for the verification still owed or the new ticket the change uncovered |

Frictions the grader listed that came only from the before runs (the bare
`tomllib` traceback on Python 3.9, missed `tools.fn` references) were already
fixed in the after version.

## What this establishes and what it does not

It establishes, for one fixture, one brief, one model and one run per task,
that the product pass produced work a blind grader preferred in every task,
mainly by completing more of what was asked and telling the user what to do
next. It does not establish a general effect size: six pairs are a small
sample, each task ran once per condition, the grader was a model rather than a
person, and the user's answers in J1 were supplied by the agent. The remaining
frictions above were fixed after this run and have not themselves been
re-measured.
