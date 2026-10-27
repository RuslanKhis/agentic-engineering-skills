G03 is only partly built, and I ran nothing: `web/` has no `node_modules` or lockfile, and I couldn't install packages here. The ticket is set to `in_progress`. I used `adk-frontend-integration` as the primary skill, as the ticket names it.

**Missing companions.** Neither `shadcn` nor `react-router` is installed, so I didn't use their guidance and don't claim it. Install lines at the AGENTS.md pins:
- `npx skills add shadcn/ui`, pinned to `shadcn-ui/ui@4233ed1`; also record the shadcn CLI version.
- `npx skills add https://github.com/remix-run/react-router --skill react-router`, pinned to `remix-run/react-router@8f364c8`.

**Written** (all under `web/src/lib/`, none of it executed):
- `stream.ts`: reads the `/api/chat` stream. It validates each event, drops malformed or unknown ones, and ends in exactly one of completed or failed. A stream that closes without `completed` or `failed` counts as failed. No user ID is sent from the browser.
- `safe-text.ts`: the SB10 renderer. Model text becomes plain text nodes, so an `<img onerror>` payload is inert. Only `https:` links are kept, and an image loads only from a listed host. The host list is empty for now, so no image loads.
- `chat.test.ts`: vitest cases for A1, A2 and A3.

**Not done:**
- `shadcn` init and theming from `docs/design/DESIGN.md`, and `web/components.json`.
- The router with `/` and `/c/:conversationId`, and the chat column component.
- `web/` config: `react-router` isn't in `package.json`, and there is no tsconfig, eslint config or vite config. Lint, test and build can't run until these exist.
- The theme check, and the Python tests for G02/A1.
- The C3 evidence cell in the design file is left as `planned`.

**Open questions I wrote into the ticket's Evidence section**, each with the assumption I used:
- **Sources:** the stream sends only `text`, `completed` and `failed`, and C3 names no `sources` event. I didn't build sources. Should C2/C3 gain a `sources` event, or should citations be parsed from the text?
- **Logo:** `web/public/nordlicht-mark.svg` still has to come from the brand team.

Lea still has to do the manual check against DESIGN.md. Remaining effort is about 2–3 hours to finish the build once setup is done, plus about 1 hour to review and verify.

The `Progress:` block in the ticket lists the next steps. To resume after setup, run: `/adk-engineer Resume docs/tickets/doc-assistant/G03.md from its Progress block.`