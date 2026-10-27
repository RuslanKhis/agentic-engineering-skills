# Triage: spread group (batch spread1)

Eight scenarios, one per otherwise unmeasured skill. Skill files read per run (agent.json):
frontend ag-ui.md; fastapi data-and-migrations.md; deploy cloud-run.md, frontend-hosting.md,
production.md; sql acceptance-and-extensions.md (+ interop mcp-consumption.md); optimise
context-window.md; instructions routing-and-descriptions.md, adk-instruction-mechanics.md;
tool-interface none (SKILL.md only); privacy none (no skill loaded at all).

| Scenario | A# | Votes | Class | Evidence | Proposed action |
| --- | --- | --- | --- | --- | --- |
| frontend-agui-approval-contract-declared | A1 | FPF | c | ag-ui.md:56-64 names both contracts and the `INTERRUPT_RESUME_REQUIRED` rejection; agent read it, named both contracts but said the code "should not cause the refusal". | none |
| frontend-agui-approval-contract-declared | A2 | FFF | c | ag-ui.md:80 "sends a tool-message answer and asserts `INTERRUPT_RESUME_REQUIRED`"; agent's test only asserts the flag is False. | none |
| frontend-agui-approval-contract-declared | A3 | FFF | c | ag-ui.md:94-113 `ADKAgent.from_app(app)` with `ResumabilityConfig`, stripping app:/user: keys; read, not applied. | none |
| frontend-agui-approval-contract-declared | A4 | FFF | c | ag-ui.md:102 "the decision is permission, not completion, and the backend gate ..."; not stated. | none |
| web-backend-app-migrations-beside-adk-sessions | A1 | FFF | c | data-and-migrations.md:32 "Prefix application tables (`app_documents`)"; filter done, prefix skipped. | none |
| web-backend-app-migrations-beside-adk-sessions | A3 | FFF | b | data-and-migrations.md:41 gives the `alembic check` test; writing it is possible, but the fixture has no Alembic and no shell, and SQLAlchemy tests skip offline; the agent wrote none. Mostly (c); the run cannot execute it. | flag: grade on the test written, not on it passing |
| web-backend-app-migrations-beside-adk-sessions | A4 | FFF | c | adk-fastapi-backend SKILL.md:108 "404 with the same body as an unknown ID is the default"; agent noticed the missing filter, did not fix it. | none |
| web-backend-deploy-routes-to-deploy | A3 | FFF | a | The Cloud Run IAP audience form `/projects/PROJECT_NUMBER/locations/REGION/services/SERVICE_NAME` is only in adk-fastapi-backend/references/identity.md:75; deploy's frontend-hosting.md topology A row (:12) says nothing about the audience and :16 names only the backend-service form for topology E; no "first live run confirms it" wording in the deploy skill. Agent read the three deploy references. | deploy frontend-hosting.md: state the Cloud Run audience form for topology A and that the first live run confirms it, or link identity.md:75 |
| sql-toolbox-read-only-and-secure-tenant | A2 | PPF | c | passed by majority; justification did not cite the developer-assistant note. | none |
| sql-toolbox-read-only-and-secure-tenant | A3 | FFF | c | acceptance-and-extensions.md:329 names the `secureInputSchema` split and the secure-in-arguments error; agent bound tenant_id client-side. | none |
| sql-toolbox-read-only-and-secure-tenant | A4 | FFF | c | :329 lists all three fixtures (CTE-DELETE, writing UDF, COMMIT chaining); agent left the UDF fixture out of the loop and implemented assertion verification itself instead of handing it to adk-tool-auth-and-secrets. | none |
| optimise-compaction-atomic-groups-three-points | A2 | FFF | c | context-window.md:336-342 "The three compaction points, mapped to ADK" with a test per point; agent read the file, named two. | none |
| optimise-compaction-atomic-groups-three-points | A3 | FFF | c | context-window.md:59-70 retained-history accounting and the static prefix (:33-51); not applied. Measuring needs a shell, but "keeps the static prefix intact" did not. | none |
| privacy-with-observability | A1 | FFF | a+c | No skill loaded (no Skill call, no file read). protect-adk-sensitive-data's description excludes "telemetry pipelines and alerts (adk-agent-observability)" (SKILL.md:11) and never names prompt content leaving through trace export or completion uploads, so a "prompts uploaded through telemetry" request reads as observability; observability was not loaded either and google-agents-cli-observability is absent. | description: name "prompt or completion content leaving through traces, uploads or analytics exporters" as in scope |
| privacy-with-observability | A2 | FFP | c | Without the skill the agent fixed the upload path and only noted the analytics plugin; SKILL.md:91 "inspect SDK and exporter capture separately". | none |
| privacy-with-observability | A4 | FFF | c | No canary-per-sink test; the skill's boundaries guidance was never read. | none |
| privacy-with-observability | A6 | FFF | c | Same root cause (skill not loaded). | none |
| instructions-routing-and-templating-repair | A2 | FFF | c | adk-instruction-mechanics.md:12, :52-56 explain identifier-like braces before 2.10.0 and recommend an `InstructionProvider`; agent read it, used optional placeholders, never explained. | none |
| instructions-routing-and-templating-repair | A3 | FFF | b+c | A scripted-model transfer check needs the SDK (absent); writing it and reporting not run was possible but not done; the render test mirrored the regex instead of the SDK's injector. | none (flag only the SDK part) |
| instructions-routing-and-templating-repair | A4 | FFF | c | Hand-off to adk-agent-evaluation not stated. | none |
| tool-interface-wrong-tool-diagnosis | A1 | FFF | b | "Runs the read-only linter and dumps the live declarations" needs a shell (and the SDK for declarations); no escape in the assertion. | flag the assertion |
| tool-interface-wrong-tool-diagnosis | A3 | FFF | c | adk-tool-interface-design SKILL.md:102 says not to return a bare string; agent read no reference and left `search_help`'s string return. | none |
| tool-interface-wrong-tool-diagnosis | A4 | FFF | c | Retry/idempotency hand-off to safe-api-tool-calls not stated; the skill's description names that boundary. | none |

## Suspected skill defects

1. **deploy-adk-on-google-cloud, references/frontend-hosting.md:12 and :16:** topology A (one Cloud
   Run service behind IAP) gives no IAP audience form; the Cloud Run form lives only in
   adk-fastapi-backend/references/identity.md:75, and nothing says the first live run confirms
   the audience. (web-backend-deploy A3)
2. **protect-adk-sensitive-data, description (SKILL.md:3-12):** excludes "telemetry pipelines"
   and does not name prompt content leaking through trace export, completion uploads or analytics
   exporters, so a privacy request phrased around tracing loaded no skill at all.
   (privacy-with-observability A1, and A2/A4/A6 downstream)

## Fixture or assertion defects

- **tool-interface-wrong-tool-diagnosis A1:** running the linter and dumping live declarations
  needs a shell and the SDK; flag it (shell-dependent, no escape).
- **web-backend-app-migrations-beside-adk-sessions A3:** an `alembic check` test can be written
  but not run here; grade the test written. Flag.
- **instructions-routing-and-templating-repair A3 (part):** the scripted-model transfer check
  needs the SDK; the assertion should accept a written test reported as not run.

No fixture files were changed.
