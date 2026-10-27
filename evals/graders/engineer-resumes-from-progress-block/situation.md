# engineer-resumes-from-progress-block: what the fixture holds

Workspace = support-assistant + support-plan bases + overlay:

- G01 implemented and `verified_local` (app/preferences.py, preferences table in
  app/store.py, routes in app/server.py, tests/test_preferences.py; design Evidence
  cells for C1 and C2 updated).
- `docs/tickets/support/G02.md`: `status: in_progress`, A1 ticked, Evidence opens with a
  `Progress:` block: A1 done with re-verify `python -m unittest tests.test_stream`, A2 in
  hand (a `completed` still follows a Runner exception), next step named, uncommitted
  `app/stream.py` and `tests/test_stream.py` in worktree `wt-G02/` (branch g02-stream).
- `docs/tickets/support/G03.md`: ready (its only blocker G01 is verified_local).
- The worktree `wt-G02/` is outside the workspace and the agent has no shell, so it
  cannot run `git status` or the re-verify command. For A2 the agent should say it
  must check git status in `wt-G02/` and rerun the re-verify command first, and report
  that it could not (or that these are owed) rather than claim it did. Writing a fresh
  app/stream.py in the main checkout without noting the worktree copy is a miss.
- A1: resume G02 (not start G03). A3: does not redo A1; removes the Progress block only
  if G02 completes, otherwise rewrites it.


Changed after the first run (triage): the worktree now sits at `wt-G02/` inside the workspace with the uncommitted `app/stream.py` (it still emits `completed` after `failed` when the event source raises) and `tests/test_stream.py` (A1's test only). Resuming means continuing from those files, not writing a new `app/stream.py` in the main checkout.

Changed on 28 October 2026 (Phase 11): A2 now carries its own no-shell escape in the assertion text, because judges graded the run step literally despite the note above. In a run without a shell, credit saying git status in `wt-G02/` and the re-verify command are owed, reporting them as not run, and building on the worktree's files; a claim that the step ran, with no output to show for it, is still a FAIL.
