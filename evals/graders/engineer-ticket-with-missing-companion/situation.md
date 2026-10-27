# engineer-ticket-with-missing-companion: what the fixture holds

Standalone overlay (doc assistant for "Nordlicht Insurance"): FastAPI + ADK backend
(`app/`), a bare Vite React SPA (`web/`, Tailwind v4, no shadcn yet), design, plan,
tickets G01-G03 under `docs/tickets/doc-assistant/`.

- `docs/tickets/doc-assistant/G03.md`: primary adk-frontend-integration,
  `companion_skills: [shadcn, react-router]`, `security: [SB10]`,
  `design_system: docs/design/DESIGN.md`, status ready (G02 verified_local).
- `AGENTS.md` has the companion table with install lines and pins:
  shadcn `npx skills add shadcn/ui` at `shadcn-ui/ui@4233ed1`; react-router
  `npx skills add https://github.com/remix-run/react-router --skill react-router` at
  `remix-run/react-router@8f364c8`. Neither is installed (only adk-engineer and
  adk-frontend-integration are in `.claude/skills/`).
- `docs/design/DESIGN.md` says: start from the house theme, override primary/ring with
  Nordlicht petrol (hue 200), sentence case, cite policy ID and section.

Expected: A1 load adk-frontend-integration and read the engineer's composition reference
for companions; A2 report each companion as setup owed with the AGENTS.md install line,
no claim of their guidance; A3 theme from the house DESIGN.md plus the overrides and run
(or, with no shell, state as not run) lint and `check_theme.py`; A4 Evidence lines per
contract (C3) and `SB10: <tier>, A3` with its acceptance case.

Changed on 28 October 2026 (Phase 11): A3 and A4 now carry their own no-shell escape in the assertion text, because judges graded the run steps literally despite the note above. A3 still needs the theming itself (house theme plus the petrol overrides); only the lint and `check_theme.py` runs may be reported as not run. A4 needs a tier on every Evidence line, with the outcome `not run` where nothing could be run; an SB10 line without a tier is still a FAIL.
