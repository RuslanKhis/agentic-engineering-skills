# Web application security baseline

Read this when the design has a web interface or an HTTP API, after the
component layout is known and before writing goals. The designer is the only
skill that sees every component. It assigns each component the rules below,
sets their depth from the delivery profile and cites them in goals. The named
skills implement them.

The rules are written in this toolkit's words, as checks. The OWASP column
gives labels for coverage and reporting:

- **OWASP Top 10:2025** (`A01`–`A10`) covers the web application.
- **The Top 10 for LLM Applications 2025** (`LLM01`–`LLM10`) and **the Top 10
  for Agentic Applications 2026** (`ASI01`–`ASI10`) cover the agent.
  `adk-agent-security` treats these in depth.

The Top 10 is an awareness list, not a test standard, so the later tiers adopt
OWASP ASVS 5.0, Level 1 and then Level 2. Cite OWASP identifiers and titles
only; keep rule wording your own, because the OWASP texts are share-alike.

## Assign the rules

1. List the components the design creates: browser app, `/api` routes, agent
   run and stream routes, ADK runtime, application records, uploads, routes or
   tools that fetch a URL, tools with external effects, and deployment.
2. Take the tiers that apply to the profile (see [depth by
   profile](#depth-by-profile)). Tiers are cumulative.
3. A rule whose component is absent is recorded as `n/a: <reason>`.
4. Record every rule once, in the design's *Web security baseline* table:
   depth now (Build, Minimal or Defer) and either the goal acceptance that
   proves it (`G04/A3`), `n/a: <reason>` or `deferred: <trigger>`. In the
   compact form, the same facts fit one line in *Floor, depth and deferred*.
5. Cite the rule IDs in each goal that creates or changes the component
   (`security: [SB01, SB03]`), and name the rule beside the contract in the
   acceptance item that proves it: `A3 … (C2, SB03)`.
6. The last goal of a handed-over proof of concept repeats each rule's status
   in its evidence, so the next team starts from the deferred list.

`scripts/check_schedule.py --design` reports a Build or Minimal rule that no
goal cites and a goal that cites a rule the table lacks; a goal cites a rule
through its `security` list or an acceptance item's parentheses. The compact
form has no table, so the helper cannot check rule coverage even when it runs
for several people: check by reading that every rule of the applied tiers is
cited by a phase 1 goal or named in the section 4 line as `n/a` or deferred.

## Rules

| ID | Component | Rule | OWASP | Check | Implemented by |
| --- | --- | --- | --- | --- | --- |
| SB01 | `/api` routes | All API routes live under one prefix (default `/api`), behind one verified-principal dependency that rejects requests when no verifier is configured. Static SPA assets and a health check stay public. | A01, A07 | With the verifier unset, every `/api` route returns 401. | `adk-fastapi-backend` |
| SB02 | Identity | Managed sign-in only: IAP for workforce users; Identity Platform or Firebase Authentication for external users. The provider's library verifies signature, audience, issuer and expiry. With IAP, identity comes only from the signed assertion, never from the unsigned identity headers. The first goal that uses IAP confirms the audience for its set-up (load balancer or directly on Cloud Run) against a captured token. | A07 | Expired, wrong-audience and forged-header requests are rejected. | `adk-fastapi-backend`; the principle is `adk-tool-auth-and-secrets` |
| SB03 | Agent routes | The principal comes from the verified token, never from the request. The server overwrites `user_id` on every ADK call, and ignores AG-UI `context` and assistant-ui `userId` as identity. A session ID only locates a conversation. | A01; ASI03 | A forged user ID runs in the caller's own scope. Another user's session returns the same 404 body as an unknown one, with no model call. | `adk-frontend-integration` |
| SB04 | Records and the tools that touch them | Every route that reads, lists, updates or deletes records filters by owner. Administrative actions are checked on the server by role. A tool that reads or changes records takes the principal from trusted session state, never from model arguments. | A01; ASI03 | A two-user test per resource type. A tool call whose arguments name another user's record finds nothing. | `adk-fastapi-backend` (routes); `adk-tool-auth-and-secrets` (tools) |
| SB05 | ADK runtime | ADK's own routes (`/apps/…`, `/run`, `/run_sse`, `/run_live`, `/list-apps`, the development UI and builder) are never reachable from a browser or the internet. The Runner runs in process, or as a private service behind the gateway. The only exception is `adk web` on loopback for a builder-only demo. | A01, A02 | At the deployed URL, each path returns no ADK data and causes no model call. Under the SPA's client-routing fallback, the HTML shell is an acceptable answer. | `adk-frontend-integration`; `deploy-adk-on-google-cloud` |
| SB06 | API configuration | Same origin by default. Otherwise an explicit origin allowlist, never `*` with credentials. CORS is not access control. | A02 | A preflight from an unlisted origin receives no allow header. | `adk-fastapi-backend` |
| SB07 | API configuration | In deployed environments: debug is off; interactive docs and the OpenAPI schema are not served (the client is generated from an offline dump); a `Content-Security-Policy` sets `default-src 'self'`, `object-src 'none'` and `frame-ancestors 'none'`, plus the identity provider's documented origins; `X-Content-Type-Options: nosniff`, a `Referrer-Policy` and HSTS are sent. | A02 | Deployed `/docs`, `/redoc` and `/openapi.json` return neither the docs UI nor the schema. A header test passes on the served build. | `adk-fastapi-backend` |
| SB08 | Browser credentials | Bearer tokens are sent by `fetch`, never in URLs or query strings. Native `EventSource` is not used, because it cannot send them. If cookies are chosen, they are `HttpOnly`, `Secure` and `SameSite`, with a CSRF token or Origin check on every state-changing request, including streamed runs. | A01 | No request carries a token in its URL. Under cookie auth, a cross-site POST without proof is rejected. | `adk-frontend-integration` |
| SB09 | API inputs | Every body has a bounded request model. Body and message size are limited, and identifiers are validated before use. Queries use the ORM or parameters only. No `eval`, shell or `pickle` on client data. | A05, A08 | Oversize and malformed bodies get 413 or 422. A lint or grep finds no string-built SQL or unsafe deserialisation. | `adk-fastapi-backend` |
| SB10 | Browser app | Model and tool output is untrusted: rendered as text, or as markdown with raw HTML disabled and a URL-protocol allowlist; images only from listed hosts, because an image URL can carry data out; never through `dangerouslySetInnerHTML`; links open with `rel="noopener noreferrer"`. | A05; LLM05 | A scripted reply containing an `<img onerror>` payload, a `javascript:` link and an image from an unlisted host renders inert and loads nothing. | `adk-frontend-integration` |
| SB11 | Uploads | Type and size are allowlisted on the server. Files are stored privately, never served inline from the app's origin, and never executed. Their content reaches the agent as untrusted data. | A05, A06; LLM01 | A disallowed type and an oversize file are rejected. An uploaded HTML file is not rendered by the app. | `adk-fastapi-backend`; `adk-agent-security` |
| SB12 | Outbound fetch | A route or tool that fetches a URL supplied by a user or the model resolves the host and refuses private, loopback, link-local and metadata ranges (`169.254.169.254`, `metadata.google.internal`) and redirects to them; refuses non-HTTPS schemes unless listed; and allowlists destinations where the product permits. This is the same rule as `adk-agent-security`'s fetch-tool rule, applied to routes as well. | A01 (SSRF); ASI02 | Requests to the metadata address and name, and a redirect to them, are refused. | `adk-agent-security` (tools); `adk-fastapi-backend` (routes) |
| SB13 | Errors | One exception handler returns a generic body with a request ID. No stack trace, SQL or provider message reaches the browser. An error inside an authorisation check denies. | A10 | A forced exception returns a generic 500, and a verifier outage denies. | `adk-fastapi-backend` |
| SB14 | Logging | Sign-in failures, denied access and approval decisions are logged with principal, route and request ID. Prompts, replies, tokens and personal data stay out of logs unless the sensitive-data policy allows them. | A09; LLM02 | A test asserts the denied-access log line and the absence of message content. | `adk-fastapi-backend`; `protect-adk-sensitive-data` |
| SB15 | Supply chain | Lockfiles are committed, and pre-1.0 tools are pinned exactly. Python and JavaScript dependency audits run in `make check`, failing on high or critical findings, with exceptions recorded. Companion skills and MCP servers are pinned. No run-time scripts or fonts load from third-party CDNs. | A03; LLM03, ASI04 | `make check` runs both audits; the built page requests nothing from another origin except the identity provider. | `adk-fastapi-backend`; `adk-release-engineering` once it gates CI |
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

- SB18 and SB19's spend cap restate floor items in
  [delivery profiles](delivery-profiles.md#keep-the-floor-at-every-profile).
- SB17 restates the proof-of-concept depth "break the
  untrusted-input-plus-write combination".
- They are listed so coverage sits in one table. SB19's per-user run limit is
  the one new mechanism among them; the rest of SB01–SB16 and SB20–SB25 are new
  to the designer.

## Depth by profile

Tiers are cumulative. SB02, SB07, SB15 and SB17 appear twice, at rising depth.

| Tier | Rules | Applies to |
| --- | --- | --- |
| 1. Always | SB01, SB03, SB05, SB09, SB10, SB13, SB16, SB17, SB18, SB19 | Every profile with a browser UI or HTTP API, including a local demo |
| 2. When the component exists | SB04 (records), SB08 (cookies), SB11 (uploads), SB12 (outbound fetch) | Every profile. Each is cheap, and the harm (another user's records, the metadata server) cannot be undone. |
| 3. Reachable at a URL, or handed over | SB02 minimal (IAP with a group, or Firebase with an allowlist); SB06; SB07 minimal (docs and schema not served, `nosniff`, `frame-ancestors`); SB15 minimal (lockfiles and one recorded audit) | A proof of concept that leaves the builder's machine |
| 4. Internal tool | SB02 with the organisation's SSO; SB07 complete; SB14; SB15 in CI; SB17 checked per agent by `adk-agent-security` | Internal tool and above |
| 5. MVP or pilot | SB20, SB21, SB22 | MVP or pilot and above |
| 6. Production | SB23, SB24, SB25 | Production |

A rule in a tier above the profile is recorded as `deferred: <trigger>`, the
trigger being the profile or event that raises it (internal-tool depth, a CI
pipeline, external users).

## After handover

The design's table records every rule's status, and the final goal's evidence
repeats it. A team extending the application raises depth one tier at a time,
adopting that tier's rules and its ASVS level, rather than starting a separate
security plan.

## Sources

Read 23 October 2026. OWASP texts are CC BY-SA 4.0, so they are cited, not
copied.

- [OWASP Top 10:2025](https://top10.owasp.org/2025/): A01 Broken Access
  Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures,
  A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07
  Authentication Failures, A08 Software or Data Integrity Failures, A09
  Security Logging and Alerting Failures, A10 Mishandling of Exceptional
  Conditions. [A01](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/)
  maps CWE-918 (SSRF) and CWE-352 (CSRF).
- [OWASP ASVS 5.0.0](https://asvs.owasp.org/), published 30 May 2025, with
  Levels 1 to 3.
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/):
  LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply
  Chain, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System
  Prompt Leakage, LLM10 Unbounded Consumption (the identifiers used here).
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/),
  the published document (December 2025): ASI01 Agent Goal Hijack, ASI02 Tool
  Misuse and Exploitation, ASI03 Identity and Privilege Abuse, ASI04 Agentic
  Supply Chain Vulnerabilities.
- [ZAP baseline scan](https://www.zaproxy.org/docs/docker/baseline-scan/):
  `zap-baseline.py` in the `ghcr.io/zaproxy/zaproxy:stable` image.
- The ADK and Google Cloud facts behind SB01–SB08 are verified, with sources,
  in the implementing skills' references (`adk-fastapi-backend`,
  `adk-frontend-integration`, `deploy-adk-on-google-cloud`).
