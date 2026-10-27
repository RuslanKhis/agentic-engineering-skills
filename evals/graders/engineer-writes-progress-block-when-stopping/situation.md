# engineer-writes-progress-block-when-stopping: what the fixture holds

Workspace = support-assistant + support-plan bases, G01 implemented and
`verified_local` (copied from the resume scenario's overlay), the web chat under
`web/`, and AGENTS.md naming the worktree-per-ticket convention (`../wt-G02`, branch
`g02-stream`).

`docs/tickets/support/G02.md` (base) is ready with three acceptance items:
A1 completed event after text, A2 failed and no completed after a Runner exception,
A3 client disconnect stops the run and records interrupted. The user says they leave
in ten minutes, so only A1 fits.

Expected: implement A1 (app/stream.py SSE adapter, tests/test_stream.py), then write a
`Progress:` block at the head of G02's Evidence (done items with checks, item in hand,
next step, uncommitted files with the worktree, re-verify commands), leave
`status: in_progress`, end with `/adk-engineer Resume docs/tickets/support/G02.md from
its Progress block.` The agent has no shell, so test commands are written but not run;
reporting them as not run is correct.
