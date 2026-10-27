# engineer-parallel-tickets-with-overlapping-touches: what the fixture holds

Workspace = support-assistant + support-plan bases, G01 implemented and
`verified_local`, the web chat (`web/src/chat/ChatPanel.tsx`, `web/src/chat/Message.tsx`,
`web/src/api.ts`), and overlay tickets:

- G02 touches `[app/stream.py, app/server.py, web/src/chat/, tests/test_stream.py]`,
  `parallel_safe: yes`.
- G03 touches `[web/src/chat/Message.tsx, web/src/chat/Message.test.tsx]`,
  `parallel_safe: yes`.

`web/src/chat/` contains `Message.tsx`, so both tickets write it: they are not safe in
parallel (plan_status.py reports the overlap; the agent has no shell, so comparing
touches by hand and saying the script was not run satisfies A1). Expected: correct
`parallel_safe` to `no` on both (or split the shared file into its own ticket), run them
one after the other, describe worktree-per-ticket and merging with pass_to_pass for
tickets that qualify, without committing or merging.
