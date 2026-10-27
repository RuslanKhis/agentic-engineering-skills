# Doc assistant: working on this repository

Internal assistant that answers staff questions from the policy library. Python 3.12,
google-adk 2.12.0, FastAPI serving the SPA from `web/dist` and `/api` behind IAP.

## Commands

- Python tests: `python -m unittest discover -s tests -t .`
- Web: `cd web && npm ci && npm run lint && npm test && npm run build`
- Theme check (UI tickets): the frontend specialist's `scripts/check_theme.py` against
  `web/src/index.css` and `docs/design/DESIGN.md`.

## Constraints

- Identity only from the verified IAP principal (`app/auth.py`); the browser never sends
  a user ID.
- Model and tool output is untrusted in the browser (design SB10).
- Do not upgrade pinned dependencies in a feature ticket.

## Companion skills

Written by G01 from the plan's companion table. Install into this project, at these pins.

| Companion | Source and install | Pin | Load when |
| --- | --- | --- | --- |
| `fastapi` | `uv sync && uvx library-skills --claude` | follows the locked FastAPI version | routes and dependencies |
| `react-router` | `npx skills add https://github.com/remix-run/react-router --skill react-router` | `remix-run/react-router@8f364c8` | routing in `web/` |
| `shadcn` | `npx skills add shadcn/ui` | `shadcn-ui/ui@4233ed1`; record the shadcn CLI version | components and theming |
| `playwright-cli` | `npm i -g @playwright/cli@0.1.22`, then `playwright-cli install --skills` | 0.1.22 | browser tests (G04) |
