G03 is not finished. Its status is `in_progress`, and no acceptance case is ticked. This session had no packages and no network. Neither companion is installed, and `web/` has no `node_modules`.

**Setup owed.** Install both companions at the pins in AGENTS.md. I did not apply any shadcn or react-router guidance and wrote no code from memory for either.
- `npx skills add shadcn/ui` (pin `shadcn-ui/ui@4233ed1`, and record the shadcn CLI version)
- `npx skills add https://github.com/remix-run/react-router --skill react-router` (pin `remix-run/react-router@8f364c8`)

**Written, in `web/`:**
- **`web/src/lib/sse.ts`** parses the stream and validates each event. A frame split across network chunks is handled.
- **`web/src/lib/message.ts`** sets a message to completed only after a `completed` event. A stream that ends without one is failed. Partial text is kept, and the failed message uses fixed copy instead of the server's raw text.
- **`web/src/lib/safe-content.ts` and `web/src/components/SafeText.tsx`** implement SB10. Raw HTML stays literal text, only `https:` and `mailto:` links are rendered, and images load only from a host allowlist that is currently empty.
- **`web/src/components/ChatColumn.tsx`** posts to `/api/chat` with `session_id` and the message only. It aborts the fetch on unmount.
- **`web/src/lib/chat.test.ts`** has tests for A1–A3, and `web/tsconfig.json` is new.

**Results:**
- **Tests A1–A3:** not run. `vitest` isn't installed.
- **Throwaway check:** the same assertions for the parser, state machine and tokeniser passed in a throwaway Node script outside the repo. That is not the ticket's verification, and it does not cover the React render.
- **Lint and tests:** `npm run lint` and `npm test` did not run.
- **ESLint config:** `npm run lint` would fail anyway, because `web/` has no ESLint config.
- **Theme check:** exits 2 because `index.css` has no theme tokens.
- **G02/A1 baseline:** the Python suite exits 0, but both stream tests were skipped (fastapi and google-adk absent), so G02/A1 was not run.
- **Design contract cells:** I left the C3 and SB10 evidence cells in the design unchanged, since neither is evidenced yet.

**Not done:**
- shadcn init and theming from `DESIGN.md`.
- The router with `/` and `/c/:conversationId`. `App.tsx` is still the placeholder, so no chat page is wired yet.
- `web/index.html` and the ESLint config.
- Your manual check of the page against `DESIGN.md`. I can only record it as owed.

**Assumptions (nobody to answer):**
- **Images:** no image host is allowed until the policy library host is named, so every image renders as text.
- **Sources:** the C2 contract has no sources event, so sources appear only as citations inside the answer text. A separate sources list needs a contract change.
- **Session creation:** `/api/chat` returns 404 for an unknown `session_id` and nothing creates sessions. A first message on a new conversation will show the failed state until a creation route exists. That route is outside this ticket's scope (`app/server.py`).

**Human effort still owed:** about 2–3 hours of Lea's time to finish the items above, then about 1 hour to review in a browser. These notes and the full Evidence are in the ticket, and nothing is committed.

Next prompt: `/adk-engineer Resume docs/tickets/doc-assistant/G03.md from its Progress block.`