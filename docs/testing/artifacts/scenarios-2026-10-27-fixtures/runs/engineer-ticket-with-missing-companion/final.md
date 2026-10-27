G03 is partly built and set to `in_progress`. I ran nothing: this session has no shell, and `web/` has no `node_modules`. The A1–A3 tests are written but not run, and the pass-to-pass baseline (G02/A1) was not run either.

Specialist: `adk-frontend-integration`.

**What I built (uncommitted):**
- **`web/src/lib/stream.ts`:** an SSE parser that checks each event at run time and drops malformed ones.
- **`web/src/lib/chat.ts`:** message state. Text only becomes final on `completed`, `failed` keeps the partial text, and a stream that closes without either event counts as failed. Sources are the policy citations (for example "HR-04 §2.3") found in the completed answer.
- **`web/src/lib/safe.ts`:** the SB10 rules. There is no raw HTML. Links must be `https:` or `mailto:`. Images load only from a host allowlist, which is empty for now.
- **`web/src/Chat.tsx`, `App.tsx`, `main.tsx`:** the chat column, with routes `/` and `/c/:conversationId`. The browser sends no user ID.
- **`web/src/lib/chat.test.ts`:** vitest cases for A1, A2 and A3.

**Not done:**
- **Companions:** `shadcn` and `react-router` are not installed, so I applied none of their guidance. Setup lines, from `AGENTS.md`:
  - `npx skills add shadcn/ui`, pinned at `shadcn-ui/ui@4233ed1`, with the CLI version recorded.
  - `npx skills add https://github.com/remix-run/react-router --skill react-router`, pinned at `remix-run/react-router@8f364c8`.
- **`react-router` dependency:** it is not in `web/package.json`, and I did not guess a version. The build fails until it is added.
- **shadcn and theming:** no shadcn init, no `components.json`, no DESIGN.md tokens in `index.css`, no theme check. Theme check would fail on the default `index.css`.
- **Missing G02 test file:** `tests/test_stream.py`, which G02 cites as its evidence, is not in `tests/`. Check it wasn't lost.
- **Manual check:** Lea's browser check against DESIGN.md is owed.
- **Contract and rule evidence:** no tier is claimed for C3 or SB10, and I did not update the design's Evidence cells.

**Assumptions to check** (also recorded in the ticket):
1. `/api/chat` returns 404 for an unknown session and no route creates sessions. I assumed that gets fixed separately, so the UI shows the failed state on a 404. This needs a designer ruling before G04.
2. The stream carries no sources event, so sources come from citation text in the answer.
3. Answers render as plain text with links and images only, not full markdown.

**Estimate:** the ticket's 3–4 h holds. I put the remaining work at roughly 1–2 h hands-on plus 1 h review.

Next prompt: `/adk-engineer Resume docs/tickets/doc-assistant/G03.md from its Progress block.`