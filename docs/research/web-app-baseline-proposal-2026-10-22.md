# ADK web app baseline: change proposal

**Status:** draft for review, 22 October 2026, revised after an independent review the same day. Nothing here has been applied to the repository. Paths name where each change would go in `RuslanKhis/agentic-engineering-skills`, read at commit `8554a96` (16 October 2026). This proposal builds on the research report *FastAPI and React agent skills* (22 October). Where they disagree, this document takes precedence.

**What it does.** It gives `adk-system-designer` two new references:
- **`web-app-defaults.md`:** default stack, layout, handover fundamentals and companion skills.
- **`security-baseline.md`:** testable rules tagged with OWASP identifiers, assigned to the components the design creates, in cumulative tiers by delivery profile.

Small template changes carry companion skills and security rule IDs from the designer to `adk-engineer`. The proposal also specifies one thin new skill, `adk-fastapi-backend`, for the HTTP application around the agent. There is no first-party React or UI skill. The frontend is built by `adk-frontend-integration` and pinned upstream skills, inside constraints the designer writes.

---

## 1. Decisions

| # | Decision | Why | Supersedes |
|---|---|---|---|
| D1 | The designer decides and companion skills build. The designer owns choices that cross the browser–server boundary, are expensive to reverse, or where ADK changes the answer, and copies them into each goal as constraints. Companion skills decide library syntax and UI craft inside those constraints. | Generic skills don't know ADK's seams. ADK's API server is unauthenticated; ag-ui-adk reads the user from client input; assistant-ui's direct mode sends `userId` from the browser; Vercel's React rules default to SWR and server components. Specifying component-level detail in the designer would duplicate faster-moving upstream skills. | — |
| D2 | One thin first-party skill, `adk-fastapi-backend`. No first-party React or UI skill. | The backend has many ADK-specific traps, and they are security traps. Nothing owns ordinary backend work today: domain routes, app data and migrations, the public contract, the identity dependency. Developers extending a handed-over POC need a skill that activates on "add an endpoint". On the frontend, `adk-frontend-integration` already owns the ADK part, and the rest is generic. | Restates the FastAPI report's recommendation, which was briefly dropped in the 22 October discussion |
| D3 | A single-page app by default: Vite, React and TypeScript with client-side routing. More pages are added as routes. Next.js only for public pages that need server rendering, or for CopilotKit's standard runtime, which expects Next.js or a separate Node service. | An internal agent app needs no server rendering. Client routing gives real URLs from day one. A FastAPI-served SPA keeps one origin and one identity owner. | — |
| D4 | The security baseline lives in the designer. Rules are written as checks and tagged with OWASP Top 10:2025 for the app, and with the LLM Top 10 (2025) and the Top 10 for Agentic Applications (2026) for the agent. Later tiers adopt OWASP ASVS 5.0. | Only the designer sees every component. OWASP calls the Top 10 an awareness document, so it serves as labels and a coverage frame, not as the checklist. | — |
| D5 | A POC anyone reaches at a URL gets managed sign-in and the URL tier of the security baseline. A POC that will be handed over also gets the generated typed client and the handover fundamentals. | You want POCs that developers can extend. A hand-typed fetch helper and deferred identity make the second phase a rewrite. | The FastAPI report's "a proof of concept stops after G04, with a hand-typed fetch helper in place of G02", and the POC rows for frontend and identity in `delivery-profiles.md` |
| D6 | Ticket front matter stays flat: skill names and rule IDs only. Install lines and pins are written once: proposed in the plan, then moved by the first goal into the project's `AGENTS.md`, which the plan links to. Each security rule's depth and status are written once, in the design. | `check_schedule.py` parses front matter with one level of nesting (`parse_mapping`), so a nested list of mappings would be mangled. It also follows the designer's rule, "write each fact once". | The nested `companion_skills` and `reference_patterns` YAML in the FastAPI report |

---

## 2. Change map

| File | Change | Section |
|---|---|---|
| `skills/adk-system-designer/references/web-app-defaults.md` | **New** | §3 |
| `skills/adk-system-designer/references/security-baseline.md` | **New** | §4 |
| `skills/adk-system-designer/SKILL.md` | Scope question; two pointer sentences; goal fields | §5.1 |
| `skills/adk-system-designer/references/delivery-profiles.md` | Scope-gate row and sentence fix; four depth rows; one floor item; compact-form allowance | §5.2 |
| `skills/adk-system-designer/references/implementation-handoff.md` | Three routing rows; one paragraph | §5.3 |
| `skills/adk-system-designer/assets/system-design-template.md` | Web security baseline table under *Security posture* | §5.4 |
| `skills/adk-system-designer/assets/implementation-plan-template.md` | Companion table; three goal lines; one schedule key | §5.5 |
| `skills/adk-system-designer/assets/ticket-template.md` | Three flat fields; Constraints section; run prompt | §5.6 |
| `skills/adk-system-designer/scripts/check_schedule.py` and tests | Security-rule coverage; a fix for an existing parser bug | §5.7 |
| `skills/adk-engineer/SKILL.md`, `references/composition.md` | Companions, design system and rules; router rows; composition trigger and row | §6 |
| `skills/adk-fastapi-backend/` | **New skill** (spec only here) | §7 |
| `evals/activation.json`, `evals/scenarios.json` | Cases for the new skill and the changed scopes | §7.6 |
| `adk-frontend-integration`, `deploy-adk-on-google-cloud`, `adk-memory-architecture`, `adk-tool-auth-and-secrets` | Description, version and reference changes | §8 |

---

## 3. Draft: `skills/adk-system-designer/references/web-app-defaults.md`

*Headings are shown two levels lower than they would be in the file. Other skills are named in code spans, not linked: the package validator rejects links that leave the skill's directory.*

### Web application defaults: stack, layout and companion skills

Read this when the design gives the agent its own web interface or an HTTP API beyond `adk web`, and again when writing goals for it. These are defaults a team can extend after handover, not a stack to impose on an existing application. Preserve what the project already uses, and record each deviation as a decision.

The designer decides what crosses the browser–server boundary, what is expensive to reverse and where ADK changes the answer. Companion skills decide how code is written inside those decisions. Record the decisions in the design and copy them into each goal as constraints. A companion skill knows its library; it does not know this application's identity, ownership or security rules.

#### Default stack

| Layer | Default | Decide differently when |
|---|---|---|
| Browser app | Vite, React and strict TypeScript as a single-page application, with React Router in data mode. More pages are added as routes. | Public pages need search indexing or a server-rendered first paint, or the CopilotKit route is chosen. Its runtime expects Next.js or a separate Node service. |
| Server data in the browser | TanStack Query over a client generated from the API's OpenAPI document (`@hey-api/openapi-ts`, exact version). Streamed events are validated at run time; a type assertion is not validation. | The project already has another data layer. |
| Components and look | Tailwind CSS with shadcn/ui on Base UI, themed only through tokens from `docs/design/DESIGN.md`. shadcn's chat and agent-trace components for the conversation. | The organisation has its own design system; the goal's `design_system` points to it. |
| Model output in the page | Text, or markdown with raw HTML disabled, a URL-protocol allowlist and images only from listed hosts (SB10). | — |
| Agent transport | The JSON or SSE contract of `adk-frontend-integration`. AG-UI through ag-ui-adk only when CopilotKit or another AG-UI client is chosen for shared state or generative UI. | — |
| Backend | One FastAPI application (0.138 or later, for `app.frontend()`). It runs the ADK Runner in process behind a verified-principal dependency, serves the domain routes under `/api`, and serves the built SPA. | Managed Agent Runtime or a separately deployed ADK service is required. The FastAPI application then becomes a gateway in front of it; `adk-frontend-integration` describes the gateway in its JSON-API reference. |
| ADK's own server | Not exposed. `get_fast_api_app` and `adk api_server` only for local development, or as a private upstream behind the gateway. `adk web` only on loopback for a builder-only demo. | — |
| Identity | Workforce users: IAP with a group allowlist. External users: Identity Platform or Firebase Authentication ID tokens, sent as bearer tokens. Local development: a test principal through a dependency override, never in a deployed build. | An existing SSO already fronts the organisation's tools. |
| Conversation storage | In-memory sessions for a local demo. `DatabaseSessionService` once a conversation must survive a restart, kept apart from application tables (`adk-memory-architecture`). | — |
| Hosting | One Cloud Run service, with the SPA and `/api` on the same origin, running a single process (`fastapi run`) with an explicit request timeout and concurrency. A POC runs one instance, so per-user run limits can live in process. | Static assets need a CDN at public scale. Firebase Hosting or Cloud Storage then serve assets only, never run or stream paths: Hosting rewrites stop at 60 seconds. |

Versions belong to the specialists' compatibility references. The first goal confirms each pin.

#### Proposed layout

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
AGENTS.md  CLAUDE.md  Makefile
```

#### What a handed-over application contains

A proof of concept that others will extend needs these fundamentals and no more. Each is cheap, and each makes later work additive rather than a rewrite.

| Fundamental | Check |
|---|---|
| The browser reaches the API only through the generated client. | `make check` regenerates the client from an offline `app.openapi()` dump and runs `git diff --exit-code`. |
| Configuration comes from environment settings, with a `.env.example` that holds no values. | The application imports and dumps its OpenAPI document in a job with no credentials. |
| A verified-principal dependency covers every `/api` router and fails closed (SB01). | With no verifier configured, a request to `/api` returns 401. |
| Application tables are kept apart from ADK's session tables, and migrations run as a job. Only when the POC has application data. | `alembic check` is clean, and ADK's tables are untouched. |
| Components are themed from DESIGN.md tokens. | The DESIGN.md lint passes, and a grep finds no raw colours outside the theme file. |
| `make dev`, `make check` and `make e2e` exist. | All three run from a fresh clone after the documented setup. |
| One browser journey covers sign-in, sending, the streamed answer with tool progress, and approving or rejecting an action. | A Playwright journey passes against the real API with the model replaced. |
| An `AGENTS.md` names the commands, constraints and companion skills with install lines and pins, with a one-line `CLAUDE.md` containing `@AGENTS.md`. | Under about 200 lines. It is the only home of the companion pins once the first goal has written it. |
| Handover notes list the deferred security rules and their triggers. | The final goal's evidence gives each SB rule as evidenced, not applicable or deferred. |

#### Companion skills

Companion skills install into the application project, not into this toolkit. The plan proposes the table below, adapted. The first goal writes it into `AGENTS.md`, and the plan then links to it. Goals name companions by name. A proof of concept uses the first six rows at most. Add others only when a goal needs them, because more companions compete to trigger on the same request.

| Companion | Use for | Source and install | Scope notes for goals |
|---|---|---|---|
| `fastapi` | Routes, dependencies, SSE, `app.frontend()`, settings | Bundled in the FastAPI package: `uv sync && uvx library-skills`. Follows the locked FastAPI version. | Idioms only. Identity, ownership and process shape follow this design. |
| `react-router` | Routing | `npx skills add https://github.com/remix-run/react-router --skill react-router` | Data mode. Docs come from `node_modules` for the installed version. |
| `vercel-react-best-practices` | Re-renders, bundle size, request waterfalls | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices`, pinned by commit | In a SPA, skip the `server-` rules and Next.js advice. Use TanStack Query, not SWR. |
| `shadcn` | Components, theming from DESIGN.md, chat and trace patterns | `npx skills add shadcn/ui` | Semantic tokens only. An approval is its own prompt, not a trace line. |
| `frontend-design` | One visual direction at the start | `anthropics/skills`, skill `frontend-design` | Use once per new direction, not on every UI change. |
| `playwright-cli` | Writing and debugging browser tests | `playwright-cli install --skills` | Role-based locators. Never wait for network idle on a streaming page. |
| `impeccable` (optional) | Critique and polish after a UI change | `npx skills add pbakaus/impeccable` | It downloads a detector binary on first run; approve that as setup. Record the critique; don't gate on it. |
| `copilotkit`, `copilotkit-cli` (CopilotKit route only) | Provider set-up, verification | CopilotKit monorepo `skills/` | `copilotkit verify --round-trip` is an acceptance check. |
| aimock `write-fixtures` (browser tests) | Replaying Gemini responses | `CopilotKit/aimock` | Start with a fixture smoke test on the real agent. |

When guidance conflicts:
- This toolkit's specialist decides identity, ownership, security rules and the stream contract.
- A companion decides library syntax for its pinned version.
- DESIGN.md decides between UI companions, including copy case, where Vercel's guidelines and `frontend-design` disagree.

A companion's advice that conflicts with a goal's constraints loses, and the agent notes the conflict in Evidence.

---

## 4. Draft: `skills/adk-system-designer/references/security-baseline.md`

*Headings are shown two levels lower than they would be in the file.*

### Web application security baseline

Read this when the design has a web interface or an HTTP API, after the component layout is known and before writing goals. The designer is the only skill that sees every component. It assigns each component the rules below, sets their depth from the delivery profile and cites them in goals. The named skills implement them.

The rules are written in this toolkit's words, as checks. The OWASP column gives labels for coverage and reporting:
- **OWASP Top 10:2025** covers the web application.
- **The LLM Top 10 (2025) and the Top 10 for Agentic Applications (2026)** cover the agent. `adk-agent-security` treats these in depth.

The Top 10 is an awareness list, not a test standard. The later tiers therefore adopt OWASP ASVS 5.0, Level 1 and then Level 2. Cite OWASP identifiers and titles only, and keep the rule wording your own.

#### Assign the rules

1. List the components the design creates: browser app, `/api` routes, agent run and stream routes, ADK runtime, application records, uploads, routes or tools that fetch a URL, tools with external effects, and deployment.
2. Take the tiers that apply to the profile. Tiers are cumulative.
3. A rule whose component is absent is recorded as `n/a: <reason>`.
4. Record every rule once, in the design's web security baseline table. In the compact form, use the line in *Floor, depth and deferred*. Each rule records its depth now and either the goal acceptance that proves it, `n/a: <reason>`, or `deferred: <trigger>`.
5. Cite the rule IDs in each goal that creates or changes the component (`security: [SB01, SB03]`), and name the rule beside the contract in the acceptance item that proves it: `A3 (C2, SB03)`.
6. The last goal of a handed-over proof of concept repeats each rule's status in its evidence, so the next team starts from the deferred list.

#### Rules

| ID | Component | Rule | OWASP | Check | Implemented by |
|---|---|---|---|---|---|
| SB01 | `/api` routes | All API routes live under one prefix (default `/api`), behind one verified-principal dependency that rejects requests when no verifier is configured. Static SPA assets and a health check stay public. | A01, A07 | With the verifier unset, every `/api` route returns 401. | `adk-fastapi-backend` |
| SB02 | Identity | Managed sign-in only: IAP for workforce users; Identity Platform or Firebase Authentication for external users. The provider's library verifies signature, audience, issuer and expiry. With IAP, identity comes only from the signed assertion header, never from unsigned identity headers. Confirm the header and audience format for the chosen IAP set-up (load balancer or direct on Cloud Run) in the first goal that uses it. | A07 | Expired, wrong-audience and forged-header requests are rejected. | `adk-fastapi-backend`; the principle is `adk-tool-auth-and-secrets` |
| SB03 | Agent routes | The principal comes from the verified token, never from the request. The server overwrites `user_id` on every ADK call, AG-UI `context` and assistant-ui `userId`. A session ID only locates a conversation. | A01; ASI03 | A forged user ID runs in the caller's own scope. Another user's session returns the same 404 body as an unknown one, with no model call. | `adk-frontend-integration` |
| SB04 | Records and the tools that touch them | Every route that reads, lists, updates or deletes records filters by owner. Administrative actions are checked on the server by role. A tool that reads or changes records takes the principal from trusted session state, never from model arguments. | A01; ASI03 | A two-user test per resource type. A tool call whose arguments name another user's record finds nothing. | `adk-fastapi-backend` (routes); `adk-tool-auth-and-secrets` (tools) |
| SB05 | ADK runtime | ADK's own routes (`/apps/…`, `/run`, `/run_sse`, `/run_live`, the development UI and builder) are never reachable from a browser or the internet. The Runner runs in process, or as a private service behind the gateway. The only exception is `adk web` on loopback for a builder-only demo. | A01, A02 | At the deployed URL, each path returns no ADK data and causes no model call. Under the SPA's client-routing fallback, the HTML shell is an acceptable answer. | `adk-frontend-integration`; `deploy-adk-on-google-cloud` |
| SB06 | API configuration | Same origin by default. Otherwise an explicit origin allowlist, never `*` with credentials. CORS is not access control. | A02 | A preflight from an unlisted origin receives no allow header. | `adk-fastapi-backend` |
| SB07 | API configuration | In deployed environments:<br>• debug is off;<br>• interactive docs and the OpenAPI schema are not served (the client is generated from an offline dump);<br>• a `Content-Security-Policy` sets `default-src 'self'`, `object-src 'none'` and `frame-ancestors 'none'`, plus the identity provider's documented origins;<br>• `X-Content-Type-Options: nosniff`, a `Referrer-Policy` and HSTS are sent. | A02 | Deployed `/docs`, `/redoc` and `/openapi.json` return neither the docs UI nor the schema. A header test passes on the served build. | `adk-fastapi-backend` |
| SB08 | Browser credentials | Bearer tokens are sent by `fetch`, never in URLs or query strings. Native `EventSource` is not used, because it cannot send them. If cookies are chosen, they are `HttpOnly`, `Secure` and `SameSite`, with a CSRF token or Origin check on every state-changing request, including streamed runs. | A01 | No request carries a token in its URL. Under cookie auth, a cross-site POST without proof is rejected. | `adk-frontend-integration` |
| SB09 | API inputs | Every body has a bounded request model. Body and message size are limited, and identifiers are validated before use. Queries use the ORM or parameters only. No `eval`, shell or `pickle` on client data. | A05, A08 | Oversize and malformed bodies get 413 or 422. A lint or grep finds no string-built SQL or unsafe deserialisation. | `adk-fastapi-backend` |
| SB10 | Browser app | Model and tool output is untrusted:<br>• rendered as text, or as markdown with raw HTML disabled and a URL-protocol allowlist;<br>• images only from listed hosts, because an image URL can carry data out;<br>• never through `dangerouslySetInnerHTML`;<br>• links open with `rel="noopener noreferrer"`. | A05; LLM05 | A scripted reply containing an `<img onerror>` payload, a `javascript:` link and an image from an unlisted host renders inert and loads nothing. | `adk-frontend-integration` |
| SB11 | Uploads | Type and size are allowlisted on the server. Files are stored privately, never served inline from the app's origin, and never executed. Their content reaches the agent as untrusted data. | A05, A06; LLM01 | A disallowed type and an oversize file are rejected. An uploaded HTML file is not rendered by the app. | `adk-fastapi-backend`; `adk-agent-security` |
| SB12 | Outbound fetch | A route or tool that fetches a URL supplied by a user or the model does three things:<br>• resolves the host and refuses private, loopback, link-local and metadata ranges (`169.254.169.254`, `metadata.google.internal`), and redirects to them;<br>• refuses non-HTTPS schemes unless listed;<br>• allowlists destinations where the product permits. | A01 (SSRF); ASI02 | Requests to the metadata address and name, and a redirect to them, are refused. | `adk-agent-security` (tools); `adk-fastapi-backend` (routes) |
| SB13 | Errors | One exception handler returns a generic body with a request ID. No stack trace, SQL or provider message reaches the browser. An error inside an authorisation check denies. | A10 | A forced exception returns a generic 500, and a verifier outage denies. | `adk-fastapi-backend` |
| SB14 | Logging | Sign-in failures, denied access and approval decisions are logged with principal, route and request ID. Prompts, replies, tokens and personal data stay out of logs unless the sensitive-data policy allows them. | A09; LLM02 | A test asserts the denied-access log line and the absence of message content. | `adk-fastapi-backend`; `protect-adk-sensitive-data` |
| SB15 | Supply chain | Lockfiles are committed, and pre-1.0 tools are pinned exactly. Python and JavaScript dependency audits run in `make check`, failing on high or critical findings, with exceptions recorded. Companion skills and MCP servers are pinned. No run-time scripts load from third-party CDNs. | A03; LLM03, ASI04 | `make check` runs both audits. | `adk-fastapi-backend`; `adk-release-engineering` once it gates CI |
| SB16 | Secrets | Secrets come from Secret Manager or the environment. Nothing secret appears in `VITE_` or `NEXT_PUBLIC_` variables, the built bundle or system prompts. A secret scan runs in `make check`. A Firebase web API key is a public identifier that ships in the bundle: allowlist it in the scan and restrict the key in the console. | A04, A02; LLM07 | The secret scan is clean apart from allowlisted identifiers. | `adk-fastapi-backend`; `adk-tool-auth-and-secrets` |
| SB17 | Agents with tools | No agent both reads untrusted content and holds an unconfirmed write or egress tool. | A06; LLM01, ASI01 | A scripted-model test: an instruction injected into a document does not cause the forbidden call. | `adk-agent-security` |
| SB18 | Tools with external effects | A human approves any external effect. Rejecting the action runs the tool zero times. | A06; LLM06, ASI02 | Approve runs the tool once; reject runs it zero times. | `adk-operational-guardrails` |
| SB19 | Cost and abuse | `max_llm_calls`, a model spend cap, one active run per user and conversation, and SB09's size limits. A process-local run lock is enough only while the service runs one instance; beyond that it needs a shared store. | A06; LLM10 | The cap stops a looping run, and a second concurrent run is refused. | `adk-operational-guardrails` |
| SB20 | Identity | Token revocation is checked before sensitive actions, and session lifetime is set. | A07 | A revoked token is refused on a sensitive action. | `adk-fastapi-backend` |
| SB21 | Deployment | A ZAP baseline scan runs against staging, and its findings are triaged. | A02, A05 | The scan report is recorded, with each finding fixed or accepted. | `adk-release-engineering` |
| SB22 | Whole application | A review against ASVS 5.0 Level 1. | All | The review is recorded, with gaps as goals. | The team; `adk-agent-security` for the agent |
| SB23 | Whole application | A review against ASVS 5.0 Level 2, plus the threat model and adversarial suite of `adk-agent-security`. | All | The review and suite results are recorded. | The team; `adk-agent-security` |
| SB24 | Whole application | A penetration test before external users. | All | Findings are fixed or accepted by an owner. | An outside party |
| SB25 | Public endpoints | Cloud Armor rate limiting and WAF rules in front of public endpoints. | A02, A06; LLM10 | Rules are deployed and a rate-limit test triggers them. | `deploy-adk-on-google-cloud` |

What is new and what restates:
- SB18 and SB19's spend cap restate floor items.
- SB17 restates the POC depth row "Minimal: break the untrusted-input-plus-write combination".
- They are listed so coverage sits in one table. SB19's per-user run limit is the one new mechanism among them.

#### Depth by profile

Tiers are cumulative. SB02, SB07, SB15 and SB17 appear twice, at rising depth.

| Tier | Rules | Applies to |
|---|---|---|
| 1. Always | SB01, SB03, SB05, SB09, SB10, SB13, SB16, SB17, SB18, SB19 | Every profile with a browser UI or HTTP API, including a local demo |
| 2. When the component exists | SB04 (records), SB08 (cookies), SB11 (uploads), SB12 (outbound fetch) | Every profile. Each is cheap, and the harm (another user's records, the metadata server) cannot be undone. |
| 3. Reachable at a URL, or handed over | SB02 at minimal depth (IAP with a group, or Firebase with an allowlist); SB06; SB07 at minimal depth (docs and schema not served, `nosniff`, `frame-ancestors`); SB15 at minimal depth (lockfiles and one recorded audit) | A proof of concept that leaves the builder's machine |
| 4. Internal tool | SB02 with the organisation's SSO; SB07 complete; SB14; SB15 in CI; SB17 checked per agent by `adk-agent-security` | Internal tool and above |
| 5. MVP or pilot | SB20, SB21, SB22 | MVP or pilot and above |
| 6. Production | SB23, SB24, SB25 | Production |

#### After handover

The design's table records every rule's status, and the final goal's evidence repeats it. A team extending the application raises depth one tier at a time, adopting that tier's rules and its ASVS level, rather than starting a separate security plan.

Sources (read 22 October 2026):
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/); [A01:2025](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/) lists SSRF (CWE-918) and CSRF (CWE-352) among its notable CWEs.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).
- The LLM and Agentic identifiers as recorded in `adk-agent-security`'s sources reference.

---

## 5. Edits to existing designer files

### 5.1 `SKILL.md`

In the scope-gate list (the bullets that open **Conduct the design conversation**), after the "Who uses or judges it" bullet, add:

> - Does it need its own web interface, who can reach its URL, and will other developers continue it? (Default: `adk web` for the builder only; not handed over.)

In **Make the recommendation implementable**, after the paragraph about the seven cross-framework specialists, add:

> When the design gives the agent its own web interface or an HTTP API, read [web application defaults](references/web-app-defaults.md) for the default stack, layout and companion skills, and record each deviation as a decision. Then read [the security baseline](references/security-baseline.md), list the components the design creates and record each rule's depth and status once in the design.

In **Deliver and hand off**, extend the goal-field list ("Each goal needs a stable ID, phase, estimate, …") with:

> …and, for a goal that creates or changes a web component, its companion skills (by name), the design system it follows and the security rule IDs its acceptance proves.

In the closing-message paragraph, add: "For a web application, also say which security rules are deferred and what raises them."

### 5.2 `references/delivery-profiles.md`

**Scope gate.** Insert after the "Who uses or judges it" row:

| Question | Default | Why it changes the design |
|---|---|---|
| Does it need its own web interface, who can reach its URL, and will other developers continue it? | `adk web` for the builder only; not handed over | Frontend depth, identity, the handover fundamentals and the security-baseline tier |

The default matches the existing judge default ("The user, reading the design"). A team whose POCs are usually handed over can change both defaults together; see open question 3.

**Fix an existing sentence.** "The last row decides the risk" now points at the presentations row, not the data row. Change it to "The data row decides the risk".

**Depth table.** Replace two rows and add two:

| Concern | POC | Internal tool | MVP or pilot | Production |
|---|---|---|---|---|
| User identity and per-user data scope | Defer for a builder-only local demo. Minimal when reachable at a URL: managed sign-in with an allowlist, principal from the token (SB02). | Build: existing SSO, users see their own records | Build | Build |
| Frontend | `adk web` on loopback for a builder-only demo. Otherwise Build: the baseline SPA from web-app defaults, one journey. | Build | Build | Build |
| API contract and typed client *(new)* | Build when handed over: generated client and drift check | Build | Build, with a breaking-change check | Build, with a breaking-change gate |
| Web security baseline *(new)* | Tiers 1–2; also tier 3 when reachable at a URL or handed over | Tiers 1–4 | Tiers 1–5 | Tiers 1–6 |

**Floor.** Add one bullet:

> - Nothing reachable at a URL without sign-in: ADK's own server routes are never exposed, and the application's routes fail closed when no verifier is configured.

*Rationale:* it costs minutes. Once ADK's server is exposed, anyone can read or delete sessions and spend the model budget, which a demo cannot undo.

**Compact form.** Add to its section list:

> For a web application, section 4 gains one security line: the tiers applied, rules marked `n/a` with a reason, and deferred rules with triggers. Each phase 1 goal gains one line naming its companions and rule IDs. Allow about 250 more words: about 1,450 in total, or 1,850 with the failure grid. A ticket may add a one-line Constraints section (about 30 words) to its 120-word body.

### 5.3 `references/implementation-handoff.md`

Add three rows to the routing table:

| Need | Concrete implementation route to assess | Infrastructure responsibility | Primary skill |
|---|---|---|---|
| HTTP API beyond the agent route | Domain routes under `/api` behind the shared verified-principal dependency; records filtered by owner; application tables and migrations kept apart from ADK's; the public OpenAPI contract and generated client; one error handler; CORS and headers; the single-process Cloud Run shape | Database for application data; Cloud Tasks for work that must outlive the response | `adk-fastapi-backend` |
| Visual design and agent UI states | shadcn components themed from DESIGN.md tokens; agent events mapped to UI states; screenshot and accessibility checks at the profile's depth | None | `adk-frontend-integration`, with companions `shadcn` and `frontend-design` |
| Web security baseline | Rules from the security baseline, recorded once in the design and cited in goals and acceptance | As each rule's owner needs | The rule's *Implemented by* skill |

After "Name one primary skill and only the supporting skills the slice needs.", add:

> A goal that creates or changes a web component also names its companion skills, its design system and the security rule IDs it proves. Companions install in the application project. A missing companion is a setup step, not a claim that its guidance was applied.

Under **Continue the work**, add: "`adk-engineer` also reads a goal's companion skills, design system and security rules."

### 5.4 `assets/system-design-template.md`

Under **Security posture**, after the trifecta table, add:

```markdown
#### Web security baseline

Only when the design has a web interface or HTTP API. One row per rule from
the designer's security baseline; this table is the rule's only status record.

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
```

### 5.5 `assets/implementation-plan-template.md`

After **Implementation map**, add:

```markdown
## Web stack and companion skills

Only when the design has a web interface or HTTP API. Deviations from
web-app defaults link their decision. The first goal writes this table into
the project's AGENTS.md; afterwards keep only the link.

| Companion | Source and install | Pin | Load when | Scope notes |
| --- | --- | --- | --- | --- |
```

Add three lines to each goal entry:

```markdown
- **Companion skills:** <names, or none>
- **Design system:** <path to DESIGN.md for UI goals, or none>
- **Security rules:** <SB IDs this goal proves, each cited by an acceptance item>
```

Add one key to the schedule block:

```yaml
  security: [SB01, SB05]
```

Keep list lines free of trailing comments until the parser fix in §5.7 lands.

### 5.6 `assets/ticket-template.md`

Front matter, after `contracts:`:

```yaml
companion_skills: [<names, or empty>]
security: [<SB IDs this ticket proves, or empty>]
design_system: <path to DESIGN.md for UI tickets, or none>
```

Body, after **Scope**:

```markdown
## Constraints

<One line: the decisions this ticket must not change (identity source,
transport, stack), by reference to AGENTS.md and the design.>
```

Acceptance items cite rule IDs beside contracts, for example:

```markdown
- [ ] A3 Another user's session returns the unknown-session 404, with no model call (C2, SB03)
```

Run prompt:

```text
/adk-engineer Carry out <path to this ticket>. Read its design and plan,
use its primary and supporting skills and its companion skills at the pins
in AGENTS.md, keep its constraints and security rules, run its verification
locally, fill in the Evidence section and set status. Leave changes uncommitted.
```

### 5.7 `scripts/check_schedule.py`

**An existing parser bug comes first.** `parse_scalar` reads `[a, b]` as a list only when the line has no trailing comment. With a comment, `[a, b]  # note` comes back as the text `"[a, b]"`, and `normalise` splits it on commas into `['[a', 'b]']`.

The current plan template's schedule block has two such lines:
- `contracts: [C1, C3]    # design contracts…`. A plan that keeps this comment always fails `--design` with "G01 cites [C1, which is not in the design's contracts table" (exit 1). The goal's prose usually names C1 and C3, so the coverage half may still pass.
- `mentions_only: []      # IDs…`, which becomes `['[]']`.

This was checked by running the functions on 22 October. The existing tests don't catch it, because their `contracts:` lines carry no comments. **Fix:** strip the comment before the list check, and add a regression test that uses the template's commented lines verbatim.

**Then add security coverage:**
- Read a `security` list per goal, from the schedule block and from ticket front matter, the same way as `contracts`.
- With `--design`, read the design's *Web security baseline* table.
- Report each rule at depth Build or Minimal that no goal cites, unless its row records `n/a:` or `deferred:`.
- Report each goal that cites a rule the table lacks.
- Both are exit-1 findings, matching contracts.
- Add tests mirroring the contract-coverage tests.

Compact-form POCs don't run the helper; their coverage is checked by reading the section 4 line against the goals' rule IDs.

---

## 6. Edits to `adk-engineer`

### 6.1 `SKILL.md`

In **Understand the request**, after "If it names a `Primary skill` … use them;", add:

> If it names companion skills, load each at the pin recorded in the project's `AGENTS.md` (or the plan's companion table before the first goal has written it). A missing companion is reported as setup, with its install line, and the work continues without claiming its guidance. Follow its design system for UI work. Treat its security rule IDs like contracts: evidence records one line per rule, with the tier reached and the acceptance cases that showed it.

Widen the trigger for reading `references/composition.md` from "agents-cli … or another collection already supplies the development workflow" to also cover "or a ticket names companion skills".

In the router table, amend one row and add one:

| Request concerns | Specialist skill |
|---|---|
| Browser interfaces and the agent's run and stream API: JSON or SSE contracts, AG-UI, CopilotKit, agent UI states | `adk-frontend-integration` *(amended)* |
| HTTP routes beyond the agent's run and stream API: domain data and migrations, the API contract or generated client, errors, CORS or headers in an ADK web application | `adk-fastapi-backend` *(new)* |

### 6.2 `references/composition.md`

In the existing row "User hands over a ticket or plan goal written by `adk-system-designer`", change "No other collection is needed." to "No other collection is needed unless it names companion skills (next row)." Then add:

| Situation | How to proceed |
|---|---|
| A ticket or goal names companion skills (FastAPI's bundled skill, shadcn, Vercel's React rules, `playwright-cli` and others) | Load them for library syntax and UI craft inside the ticket's constraints. This toolkit's specialist decides identity, ownership, security rules and the stream contract. DESIGN.md decides between UI companions. A companion's advice that conflicts with a constraint or rule loses and is noted in Evidence. |

---

## 7. Spec: `skills/adk-fastapi-backend`

### 7.1 Purpose and size

The skill owns the HTTP application around a Python ADK agent: the parts no specialist owns today, where ADK or Google Cloud changes the answer. It is thin by design. FastAPI idioms come from FastAPI's bundled skill, which tracks the installed version. `SKILL.md` runs to about 150–250 lines, with detail in references.

### 7.2 Package files

- **`SKILL.md` front matter:**

  ```yaml
  name: adk-fastapi-backend
  description: Build, adapt or review the FastAPI application around a Python Google ADK agent - the in-process Runner or gateway topology, the verified-principal dependency for IAP or Identity Platform, owner-filtered domain routes, application data and migrations beside ADK's session tables, the public OpenAPI contract and generated client, error handling, CORS and security headers, and the Cloud Run process shape. Use for backend routes, data or API-contract work in an ADK web application. Do not activate for the agent's run and stream contract (adk-frontend-integration), tool credentials or delegated OAuth (adk-tool-auth-and-secrets), hosting and IAM (deploy-adk-on-google-cloud), or FastAPI work unrelated to an ADK application.
  license: MIT
  ```

- **`LICENSE`:** as in the other packages.
- **`agents/openai.yaml`:**
  - `display_name: "ADK FastAPI Backend"`;
  - `short_description: "Build the FastAPI backend around an ADK agent"` (45 characters; the validator requires 25–64);
  - a `default_prompt` that invokes `$adk-fastapi-backend`, as the validator requires;
  - `allow_implicit_invocation: true`.

### 7.3 Boundaries

| Concern | Owner |
|---|---|
| Agent run, stream and session endpoints, event translation, UI states | `adk-frontend-integration` |
| The shared verified-principal dependency used by every router, and the concrete IAP and Firebase verifier facts | **`adk-fastapi-backend`**. The agent routes consume the dependency. |
| The identity principle (one internal principal; verify signature, issuer, audience and expiry; outage versus invalid credential), tool credentials, Secret Manager, delegated OAuth | `adk-tool-auth-and-secrets`. Its `identity-and-output.md` already holds the principle. |
| Domain routes, application data, migrations, OpenAPI contract and client, errors, CORS and headers, process shape, work after the response | **`adk-fastapi-backend`** |
| Hosting, ingress, IAM, revisions | `deploy-adk-on-google-cloud` |
| Session storage choice and memory | `adk-memory-architecture` |
| FastAPI syntax and idioms | FastAPI's bundled skill (companion) |

`adk-frontend-integration`'s JSON-API procedure currently says "Reuse the app's verified authentication dependency". It would name `adk-fastapi-backend` as where that dependency is built.

### 7.4 `SKILL.md` outline

1. **Inspect.** Record versions of FastAPI, Starlette, Pydantic, google-adk and ag-ui-adk. Build the feature matrix:
   - `EventSourceResponse` needs 0.135 or later;
   - `app.frontend()` needs 0.138 (dependencies 0.139);
   - native OpenTelemetry arrived in 0.142, and from 0.143 automatic exporter set-up is opt-in.

   Inspect existing auth, routers, database and migrations, and whether ADK's server routes are mounted. A read-only helper, `scripts/inspect_backend.py`, reports this. It may start from a copy of `adk-frontend-integration`'s `inspect_project.py`; packages don't share code.
2. **Choose the topology.**
   - In-process Runner (the default).
   - Gateway to a private ADK service.
   - Backend-for-frontend in front of Agent Runtime.

   ADK's own warning decides it. On a non-loopback bind it says that "any client that can reach it can read, modify, and delete any user's sessions".
3. **Identity dependency.**
   - One `Principal`, from the IAP signed assertion, a Firebase or Identity Platform ID token, or a test override.
   - It fails closed.
   - Synchronous verifiers run off the event loop.
   - An invalid credential and a verifier outage both deny; only the first suggests signing in again.
4. **Domain routes and ownership.** Records are filtered by owner. Pick one behaviour for other users' records (404 recommended) and keep it consistent. Roles are checked on the server.
5. **Data and migrations.**
   - Use a separate database or schema, or an Alembic `include_object` filter that excludes ADK's five tables (`sessions`, `events`, `app_states`, `user_states`, `adk_internal_metadata`).
   - Prefix application tables.
   - Run migrations as a job, not at instance start.
   - Use async drivers.
6. **Contract.** Every route has a response model. Operation IDs are stable (`generate_unique_id_function`). The OpenAPI document is dumped offline, and a client drift gate runs in `make check`. A breaking-change check (oasdiff) is added from MVP.
7. **Errors, CORS, headers and limits.** SB06, SB07, SB09 and SB13 as code.
8. **Run-time shape.**
   - Single process with `fastapi run`; Cloud Run concurrency no higher than the application admits; explicit request timeout.
   - Under request-based billing, Cloud Run gives no CPU after the response, so work the user must not lose goes to Cloud Tasks, not `BackgroundTasks`.
   - One owner for the telemetry exporter, because ADK's exporter and FastAPI's can duplicate spans.
9. **Validate and report.** The tests in §7.5, evidence per contract and SB rule, and controls deliberately deferred.

**References:**
- `compatibility.md` (version and feature matrix)
- `topology.md`
- `identity.md` (the only home of the IAP and Firebase verifier facts)
- `data-and-migrations.md`
- `contract-and-client.md`
- `runtime-shape.md`
- `validation.md`
- `sources.md`

### 7.5 Tests the skill asks for

The application is driven with its lifespan running, because the Runner and session service are created there. Use FastAPI's `TestClient` in a `with` block, or `httpx.AsyncClient` with an ASGI transport inside `asgi-lifespan`'s `LifespanManager`. The model is replaced.

- With no verifier configured, every `/api` route returns 401.
- Missing, expired and wrong-audience tokens return 401.
- A forged `user_id` runs in the caller's own scope.
- Two users with the same record or session ID: the other user gets the same 404 body as an unknown ID, with no model call.
- ADK's own paths return no ADK data.
- The OpenAPI dump runs with no credentials, and regenerating the client leaves no diff.
- `alembic upgrade head` on an empty database, then `alembic check`, is clean, and ADK's tables are untouched.
- A forced exception returns a generic body.
- Security headers are present, and docs and schema are not served in the deployed configuration.
- Oversize bodies are rejected.
- From MVP: Schemathesis over the non-agent routes finds no 5xx.

Per `CONTRIBUTING.md`, the package also needs:
- tests for `inspect_backend.py`;
- the exact tested versions, with runtime contract tests for any SDK recipe it ships.

### 7.6 Evaluation cases

`evals/activation.json` cases carry `skill` and `should_trigger`:

| Skill | Request | `should_trigger` |
|---|---|---|
| `adk-fastapi-backend` | "Add an endpoint so users can list and delete the documents they uploaded to our ADK assistant." | true |
| `adk-fastapi-backend` | "Set up migrations for our app tables; the agent already stores sessions in the same Postgres." | true |
| `adk-fastapi-backend` | "Generate a typed TypeScript client for the React app from our FastAPI backend and keep it in sync." | true |
| `adk-fastapi-backend` | "Stream tool progress into the chat UI while the agent runs." | false |
| `adk-fastapi-backend` | "Each user should connect their own Google Drive for the agent's tool." | false |
| `adk-fastapi-backend` | "Build a FastAPI CRUD service for our inventory system." (no agent) | false |

The routing expectations between skills (the second request goes to `adk-frontend-integration`, a Cloud Run deployment request to `deploy-adk-on-google-cloud`) go in `evals/scenarios.json` with `available_skills`, as that file's existing cases do.

`adk-frontend-integration`'s existing near-miss ("larger border radius … mobile spacing") stays `false` under the description change in §8, because an isolated styling tweak is still excluded.

---

## 8. Related changes in existing specialists

These come from the FastAPI report's section *Existing skills take references and version corrections*, and from its thirteen ticket rules.

| Skill | Change |
|---|---|
| `adk-frontend-integration` | **Description.** Replace "Do not activate for ordinary React styling" with wording that covers agent UI states and setting up an ADK interface's design system with the named UI companions, while still excluding isolated styling tweaks. That is what makes it a fitting primary skill for G03-style goals.<br><br>**References:**<br>• `ag-ui.md`: `user_id_extractor` receives the client's `RunAgentInput`, so bind identity through `add_adk_fastapi_endpoint(..., dependencies=[...])` and request state.<br>• `compatibility.md`: ag-ui-adk 0.11.0 (the recorded pin is 0.7.0) and the Vite 8 gap.<br>• New `agent-ui-states.md` (ADK and AG-UI events to UI states).<br>• New `frontend-quality.md` (lint, strict types, client drift, axe, screenshots, streaming-UI rules).<br>• `json-api.md`: name `adk-fastapi-backend` for the authentication dependency. |
| `deploy-adk-on-google-cloud` | **New `frontend-hosting.md`:** the same-service default; Firebase Hosting for static assets only, because of the 60-second limit; stream timeout and heartbeat; no `Content-Length` or compression on `text/event-stream`.<br><br>**`cloud-run.md`:** one process per container; the `"*"` origin in the adk-docs example flagged as non-production. |
| `adk-memory-architecture` | ADK's five session table names, its `create_all` behaviour, and `adk migrate session` versus application migrations. |
| `adk-tool-auth-and-secrets` | No duplicated facts. One sentence in `identity-and-output.md` names `adk-fastapi-backend` for the verifier code of a web application. |

---

## 9. Worked example: a POC that will be handed over

**Brief.** An internal document-Q&A assistant with one write action, filing a ticket. Two developers have about 30 hours. A client team continues it, and the URL is shared with a pilot group.

**Profile and tiers.** Proof of concept, handed over and reachable at a URL, so tiers 1 to 3 apply.
- **Not applicable:** SB04 (no application records), SB08 (bearer tokens, no cookies), SB11 (no uploads), SB12 (no outbound fetch).
- **Deferred:** SB14, until internal-tool depth; SB15's CI form, until a CI pipeline exists; SB20 to SB22, until MVP.

| Goal | Primary (supporting) | Companions | Security | Key acceptance |
|---|---|---|---|---|
| G01 Scaffold, fail-closed principal, AGENTS.md | `adk-fastapi-backend` (`adk-frontend-integration`) | fastapi, react-router | SB01, SB05, SB13, SB15, SB16 | `make check` passes with no credentials and runs the audits and secret scan; with no verifier configured, `/api` returns 401; ADK paths return no ADK data; a forced exception returns a generic body |
| G02 Contract and typed client | `adk-fastapi-backend` | fastapi | SB09 | Regenerating leaves no diff; an oversize body gets 413 or 422 |
| G03 UI shell and DESIGN.md | `adk-frontend-integration` | shadcn, frontend-design | — | DESIGN.md lint passes; no raw colours; no overflow at 375 and 1280 px in light and dark |
| G04 Streamed answer, tool progress, approval for filing | `adk-frontend-integration` (`adk-operational-guardrails`, `adk-agent-security`) | vercel-react-best-practices, shadcn | SB03, SB10, SB17, SB18, SB19 | First frame arrives before completion<br>Injected HTML, a `javascript:` link and an unlisted image render inert<br>A forged user ID runs in the caller's scope<br>An instruction injected into a document cannot file a ticket without approval<br>Approve files once; reject files zero times<br>A second concurrent run is refused, and the call cap stops a loop |
| G05 Sign-in and Cloud Run | `deploy-adk-on-google-cloud` (`adk-fastapi-backend`, `adk-tool-auth-and-secrets`, `adk-agent-observability`, `adk-release-engineering`) | — | SB02, SB06, SB07 | Signed out is denied at the URL; deployed docs and schema are not served; headers are present; one instance and one process with an explicit timeout |
| G06 Browser journey and handover notes | `adk-frontend-integration` (`adk-agent-evaluation`) | playwright-cli | — | The journey passes with the model replaced; axe finds no serious violations on the main view; evidence lists every SB rule as evidenced, not applicable or deferred |

The six companions are the first six rows of the companion table. G05 is the first goal in a shared environment, so it carries `adk-agent-observability` and `adk-release-engineering`, as `implementation-handoff.md` requires.

G04 as a ticket's front matter, complete as `check_schedule.py` reads it (parsed with `read_tickets` on 22 October):

```yaml
goal: G04
title: Users see the answer stream in, watch tool progress and approve filing a ticket
design: docs/architecture/doc-assistant.md
plan: docs/architecture/doc-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-operational-guardrails, adk-agent-security]
blocked_by: [G01, G03]
contracts: [C1, C2, C4]
companion_skills: [vercel-react-best-practices, shadcn]
security: [SB03, SB10, SB17, SB18, SB19]
design_system: docs/design/DESIGN.md
phase: 1
profile: proof of concept
estimate:
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev A
status: ready
```

In the compact form the design file holds the plan, so `design` and `plan` point to the same file.

---

## 10. Before merging

**Repository checks.**
- `scripts/check_repo.py` passes. This includes package validation of the new skill, which needs `LICENSE`, `agents/openai.yaml` and links that stay inside its directory.
- The `check_schedule.py` parser fix and the security-coverage tests are in place.
- `git diff --check` is clean.

**Behaviour, in fresh sessions** (`CONTRIBUTING.md` asks for evidence of behaviour, not just package validity):
1. Run the designer on a brief like §9's and check five things:
   - it asks the new scope question;
   - it reads both new references;
   - it records each SB rule once in the design;
   - it lists companions once;
   - the compact design stays near 1,450 words.
2. Run `adk-engineer` on the G04 ticket with and without a companion installed, and check the Evidence lines per contract and rule.
3. Run the activation and scenario cases in §7.6, plus the existing frontend near-miss after the description change.

**Facts to re-verify when writing the files.**
- Companion pins and install lines as of the merge date: `frontend-design`'s exact install line wasn't confirmed.
- Whether shadcn's chat components render markdown with raw HTML disabled and images restricted; SB10's check settles it either way.
- Whether `app.frontend()` serves the HTML shell for unknown GET paths, as SB05's check assumes.
- The origins Firebase Authentication needs in a CSP.
- The IAP header and audience format for IAP directly on Cloud Run.
- ag-ui-adk 0.11's identity binding on the pinned version.
- The scope of the ADK 2.12 changelog line about user IDs from authenticated principals. Until it is traced, SB03 and SB05 stand as written.
- The Agentic Top 10 titles. `adk-agent-security`'s sources note they came from secondary summaries.

**Size.** The two new references come to about 3,500 words (1,430 and 2,120, measured on the drafts above). The designer reads them only for web designs. A POC's own documents grow by about 250 words, as allowed in §5.2, because they cite rule IDs instead of restating rules.

---

## 11. Open questions for you

1. **Skill name.** `adk-fastapi-backend` names the framework, which helps activation on "FastAPI" requests but ties the skill to it. `adk-web-backend` is the neutral alternative.
2. **Router default.** React Router (official, version-matched skill) or TanStack Router (matches the full-stack FastAPI template, a good layout reference)? This proposal uses React Router.
3. **Defaults for your team.** The new scope question defaults to "builder only, not handed over", to match the toolkit's existing defaults. If most of your POCs are handed over, flip both this default and the judge default together.
4. **Floor addition.** Should "nothing reachable at a URL without sign-in" join the floor, as proposed in §5.2?
5. **Reviews.** Should `adk-agent-security`'s review mode also report SB IDs, so one review covers both the app and the agent?

---

**Sources:**
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/) (read 22 October 2026)
- [OWASP Top 10:2025 A01 Broken Access Control](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/) (read 22 October 2026)
- [What's new in ASVS 5.0 (SoftwareMill)](https://softwaremill.com/whats-new-in-asvs-5-0/)
- [FastAPI bundled skill](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills/fastapi)
- [FastAPI: one process per container](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md)
- [Cloud Run CPU allocation and billing](https://docs.cloud.google.com/run/docs/configuring/cpu-allocation)
- [ADK `fast_api.py` warning](https://github.com/google/adk-python/blob/main/src/google/adk/cli/fast_api.py)
- [ADK `DatabaseSessionService`](https://github.com/google/adk-python/blob/main/src/google/adk/sessions/database_session_service.py)
- [ag-ui-adk `adk_agent.py`](https://github.com/ag-ui-protocol/ag-ui/blob/main/integrations/adk-middleware/python/src/ag_ui_adk/adk_agent.py)
- [IAP signed headers](https://docs.cloud.google.com/iap/docs/signed-headers-howto)
- [Firebase: verify ID tokens](https://firebase.google.com/docs/auth/server/verify-id-tokens)
- [Firebase Hosting with Cloud Run](https://firebase.google.cn/docs/hosting/serverless-overview?hl=en)
- [MDN: EventSource](https://developer.mozilla.org/docs/Web/API/EventSource/EventSource)
- [Repository at `8554a96`](https://github.com/RuslanKhis/agentic-engineering-skills)
- Detailed citations for every version and behaviour claim are in the *FastAPI and React agent skills* report.
