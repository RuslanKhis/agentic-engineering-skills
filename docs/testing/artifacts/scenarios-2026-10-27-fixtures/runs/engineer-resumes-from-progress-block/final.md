I stopped without making any changes, because I couldn't reach the code G02 needs. Nothing was edited and no tests were run.

**What I checked**
- The plan's first unfinished goal is G02, not G03, so "next ready goal" means resuming G02 from its Progress block.
- G02 is blocked only by G01, and G01 is `verified_local` with all three acceptance cases ticked. That blocker is clear.
- G02's Progress block is current. A1 is done, A2 is in hand, and the next step is to stop the generator in `app/stream.py` on the first exception and then add the A2 test. A3 is untouched.

**Why I couldn't continue**
- `app/stream.py` and `tests/test_stream.py` are uncommitted in the worktree `../wt-G02`, which is outside the current directory. Reading it was denied, and there is no copy of those files in this checkout.
- This session has no shell, so I couldn't run the re-verify command (`python -m unittest tests.test_stream`) or the `pass_to_pass` tests, or check `git status` in the worktree.
- Rewriting `app/stream.py` from the ticket's description would have risked overwriting the uncommitted A1 work, so I didn't.
- G03 has the same problem. Its worktree `../wt-G03` would have to be created outside the current directory, and building it needs a shell to run tests. I also didn't want to start it while G02 is open.

**Question and assumption**
- **Question:** may this session work in `../wt-G02`, or should the uncommitted files be copied into this checkout?
- **Assumption I proceeded on:** the Progress block is still accurate and the worktree is untouched.

**Left undone**
- G02: the A2 fix and test, A3, the `web/src/chat/` reader, the Evidence update and the status change.
- G03: not started.
- Human effort owed: none new yet. G02's 2–4 h estimate still stands.

**Next prompt**, run from a session that can reach `../wt-G02` and run Python:
`/adk-engineer Resume docs/tickets/support/G02.md from its Progress block.`