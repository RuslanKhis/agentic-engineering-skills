# Web application defaults: stack, layout and companion skills

Read this when the design gives the agent its own web interface or an HTTP API
beyond `adk web`, and again when writing goals for it. These are defaults a
team can extend after handover, not a stack to impose on an existing
application. Preserve what the project already uses, and record each
deviation as a decision.

The designer decides what crosses the browser–server boundary, what is
expensive to reverse and where ADK changes the answer. Companion skills decide
how code is written inside those decisions. Record the decisions in the design
and copy them into each goal as constraints. A companion skill knows its
library; it does not know this application's identity, ownership or security
rules. Generic skills miss ADK's seams: ADK's API server is unauthenticated,
ag-ui-adk reads the user from client input, assistant-ui's direct mode sends
`userId` from the browser, and Vercel's React rules default to SWR and server
components.

## Default stack

| Layer | Default | Decide differently when |
| --- | --- | --- |
| Browser app | Vite, React and strict TypeScript as a single-page application, with React Router in data mode. More pages are added as routes. | Public pages need search indexing or a server-rendered first paint, or the CopilotKit route is chosen: its runtime expects Next.js or a separate Node service. TanStack Router is acceptable when copying the full-stack FastAPI template's layout. |
| Server data in the browser | TanStack Query over a client generated from the API's OpenAPI document (`@hey-api/openapi-ts`, exact version, because it is pre-1.0). Streamed events are validated at run time, for example with zod; a type assertion is not validation. | The project already has another data layer. |
| Components and look | shadcn/ui on Base UI with Tailwind CSS, themed only through tokens from `docs/design/DESIGN.md`, which starts from the house design system. shadcn's chat and agent-trace components for the conversation. Never ship shadcn's default theme. | The organisation has its own design system; the goal's `design_system` points to it. |
| Model output in the page | Text, or markdown with raw HTML disabled, a URL-protocol allowlist and images only from listed hosts (SB10). | — |
| Agent transport | The JSON or SSE contract of `adk-frontend-integration`. AG-UI through ag-ui-adk only when CopilotKit or another AG-UI client is chosen for shared state or generative UI. The goal that builds the run route also builds its stream route and event schema when the UI streams, so no UI goal has to invent one. | — |
| Backend | One FastAPI application (0.138 or later, for `app.frontend()`). It runs the ADK Runner in process behind a verified-principal dependency, serves the domain routes under `/api`, and serves the built SPA. `adk-fastapi-backend` records the tested pins. | Managed Agent Runtime or a separately deployed ADK service is required. The FastAPI application then becomes a gateway in front of it. |
| ADK's own server | Not exposed. `get_fast_api_app` and `adk api_server` only for local development, or as a private upstream behind the gateway. `adk web` only on loopback for a builder-only demo (SB05). | — |
| Identity | Workforce users: IAP with a group allowlist. External users: Identity Platform or Firebase Authentication ID tokens, sent as bearer tokens by `fetch`. Local development: a test principal through a dependency override, never in a deployed build. | An existing SSO already fronts the organisation's tools. |
| Conversation storage | In-memory sessions for a local demo. `DatabaseSessionService` once a conversation must survive a restart, kept apart from application tables (`adk-memory-architecture`). | — |
| Hosting | One Cloud Run service, with the SPA and `/api` on the same origin, running one process (`fastapi run`) with an explicit request timeout and concurrency. A POC runs one instance, so per-user run limits can live in process. | Static assets need a CDN at public scale. Firebase Hosting or Cloud Storage then serve assets only, never run or stream paths: Hosting rewrites stop at 60 seconds (`deploy-adk-on-google-cloud`). |

Versions belong to the specialists' compatibility references. The first goal
confirms each pin.

## Proposed layout

Label this as proposed, and keep the project's own structure where one exists.

```text
backend/
  app/main.py          # FastAPI app, lifespan, /api routers, app.frontend()
  app/settings.py      # pydantic-settings; .env.example without values
  app/principal.py     # verified-principal dependency; fails closed
  app/agent_routes.py  # run, stream and session routes (adk-frontend-integration)
  app/routes/          # domain routes, each filtered by owner
  app/errors.py        # one handler, generic bodies, request ID
  agent/               # the ADK agent package
  migrations/          # application tables only; ADK tables excluded
  tests/
frontend/
  src/client/          # generated; never edited by hand
  src/routes/
  src/components/ui/   # shadcn components
docs/design/DESIGN.md
AGENTS.md  CLAUDE.md (one line: @AGENTS.md)  Makefile (dev, check, e2e)
```

## What a handed-over application contains

A proof of concept that others will extend needs these fundamentals and no
more. Each is cheap, and each makes later work additive rather than a rewrite.

| Fundamental | Check |
| --- | --- |
| The browser reaches the API only through the generated client. | `make check` regenerates the client from an offline `app.openapi()` dump and runs `git diff --exit-code`. |
| Configuration comes from environment settings, with a `.env.example` that holds no values. | The application imports and dumps its OpenAPI document with no credentials. |
| A verified-principal dependency covers every `/api` router and fails closed (SB01). | With no verifier configured, a request to `/api` returns 401. |
| Application tables are kept apart from ADK's five session tables, and migrations run as a job. Only when the POC has application data. | The migration check is clean, and ADK's tables are untouched. |
| A theme from the house or client DESIGN.md. | The DESIGN.md lint passes, no raw colours appear outside the theme, and no shadcn default tokens remain. |
| `make dev`, `make check` and `make e2e` exist. | All three run from a fresh clone after the documented setup. |
| One browser journey covers sign-in, sending, the streamed answer with tool progress, and approving or rejecting an action. | The journey passes against the real API with the model replaced. |
| An `AGENTS.md` under about 200 lines names the commands, constraints and companion skills with install lines and pins, with a one-line `CLAUDE.md` containing `@AGENTS.md`. | It is the only home of the companion pins once the first goal has written it. |
| Handover notes. | The final goal's evidence lists each security rule as evidenced, not applicable or deferred with its trigger. |
| Demo-ready, when stakeholders will see it: the Must items in `adk-frontend-integration`'s demo readiness, including an activity view when the agent acts. | `make demo-reset && make demo-replay` runs the golden path with no model calls, and the screenshots come from the current build. |

## Design system

`adk-frontend-integration` ships the house design system as
`assets/design/DESIGN.md`: a restrained enterprise look in Google's open
DESIGN.md format. The first UI goal copies it to `docs/design/DESIGN.md`. A
client brand overrides only the surface that file names (accent ramp, fonts
if licensed, logo, optionally radius); everything else stays fixed. When the
client's brand cannot be used yet, the same skill ships fictional demo brands
that apply through the same surface. Record the choice of house, client or
demo brand as a decision.

## Companion skills

Companion skills install into the application project, not into this toolkit.
The plan proposes the table below, adapted. The first goal writes it into
`AGENTS.md` with the pins it resolves, and the plan then links to it. Goals
name companions by name. A proof of concept uses the first six rows at most.
Add others only when a goal needs them, because more companions compete to
trigger on the same request.

Install lines and the last-known pins were checked on 23 October 2026; the
first goal confirms them on the day. Pin GitHub-hosted skills by commit,
because they carry no version of their own.

| Companion | Use for | Source and install | Last-known pin | Scope notes for goals |
| --- | --- | --- | --- | --- |
| `fastapi` | Routes, dependencies, SSE, `app.frontend()`, settings | Bundled in the FastAPI package: `uv sync && uvx library-skills --claude` (it scans the project's `.venv`, so install dependencies first) | Follows the locked FastAPI version | Idioms only. Identity, ownership and process shape follow this design. |
| `react-router` | Routing | `npx skills add https://github.com/remix-run/react-router --skill react-router` | `remix-run/react-router@8f364c8` | Data mode. Docs come from `node_modules` for the installed version. |
| `vercel-react-best-practices` | Re-renders, bundle size, request waterfalls | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices` | `vercel-labs/agent-skills@063bee9` | In a SPA, skip the `server-` rules and Next.js advice. Use TanStack Query, not SWR. |
| `shadcn` | Components, theming from DESIGN.md, chat and Trace patterns | `npx skills add shadcn/ui` | `shadcn-ui/ui@4233ed1`; record the `shadcn` CLI version used | Semantic tokens only. An approval is its own prompt, not a trace line. |
| `frontend-design` | A new visual direction beyond the house theme | Claude Code: `/plugin install frontend-design@claude-plugins-official`; other hosts: `anthropics/skills`, `skills/frontend-design` (Apache-2.0) | `anthropics/skills@41bbe19` | Only when the client wants a direction neither the house theme nor its brand gives. |
| `playwright-cli` | Writing and debugging browser tests | `npm i -g @playwright/cli@0.1.22`, then `playwright-cli install --skills` | `@playwright/cli` 0.1.22 | Role-based locators. Never wait for network idle on a streaming page. |
| `impeccable` (optional) | Critique and polish after a UI change | `npx impeccable install` | Release `skill-v4.7.0` | It downloads a detector binary on first run; approve that as setup. Record the critique; don't gate on it. |
| `copilotkit`, `copilotkit-cli` (CopilotKit route only) | Provider set-up, verification | `npx skills add CopilotKit/CopilotKit/skills` | `CopilotKit/CopilotKit@a191436` | `copilotkit verify --round-trip` is an acceptance check. The CLI it runs is proprietary: run it, never copy it. |
| aimock `write-fixtures` (browser tests) | Replaying Gemini responses | `CopilotKit/aimock`, `skills/write-fixtures` | aimock 1.46.0 | Start with a fixture smoke test on the real agent. |

Do not adopt Vercel's `ai-elements`: its README announces deprecation at the
end of November 2026 in favour of shadcn's AI components.

When guidance conflicts:

- This toolkit's specialist decides identity, ownership, security rules and
  the stream contract.
- A companion decides library syntax for its pinned version.
- DESIGN.md decides between UI companions, including copy case, where Vercel's
  guidelines and `frontend-design` disagree.

A companion's advice that conflicts with a goal's constraints loses, and the
agent notes the conflict in Evidence.

## Sources

Read 23 October 2026.

- FastAPI bundled skill: [`fastapi/.agents/skills/fastapi`](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills/fastapi),
  present in the 0.161.1 wheel; [library-skills](https://pypi.org/project/library-skills/) 0.0.19.
- [react-router skill](https://github.com/remix-run/react-router/blob/main/.agents/skills/react-router/SKILL.md);
  [vercel-react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)
  (70 rules, still SWR-based); [shadcn skill](https://github.com/shadcn-ui/ui/tree/main/skills/shadcn).
- [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache-2.0);
  [playwright-cli](https://github.com/microsoft/playwright-cli) (Apache-2.0);
  [Impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0 with NOTICE).
- [CopilotKit skills](https://github.com/CopilotKit/CopilotKit/tree/main/skills) (MIT; the
  [`copilotkit` CLI](https://www.npmjs.com/package/copilotkit) 4.29.0 is proprietary);
  [aimock](https://github.com/CopilotKit/aimock) (MIT).
- [vercel/ai-elements README](https://github.com/vercel/ai-elements): "This project will be
  deprecated at the end of November 2026 and replaced by AI Elements from shadcn/ui."
- [`@hey-api/openapi-ts`](https://www.npmjs.com/package/@hey-api/openapi-ts) 0.99.0.
- The research behind the defaults: `docs/research/fastapi-react-skills-2026-10-22.md`
  and `docs/research/web-app-baseline-proposal-2026-10-22.md` in the toolkit repository.

Not verified: the `npx skills add` forms for `frontend-design` and
`impeccable`, which their upstreams do not document, and aimock's plugin
install line.
