<!--
The one evidence vocabulary for every skill's report, ticket Evidence line and
design Evidence cell. Base tiers are adk-engineer's (offline, local, live,
release); specialist distinctions are bracketed qualifiers on a base tier, never
new tiers. Edit here, then run scripts/sync_shared.py.
carriers: adk-engineer, adk-agent-evaluation, adk-agent-instructions, adk-agent-interoperability, adk-agent-observability, adk-agent-security, adk-fastapi-backend, adk-frontend-integration, adk-memory-architecture, adk-model-and-output-contracts, adk-operational-guardrails, adk-release-engineering, adk-sql-agent-engineering, adk-tool-auth-and-secrets, adk-tool-interface-design, adk-workflow-design, deploy-adk-on-google-cloud, optimise-adk-on-google-cloud, protect-adk-sensitive-data, safe-api-tool-calls
-->

## Evidence labels

Every result in a report carries the tier it reached and its outcome. The same
words fill a ticket's Evidence lines and a design's Evidence cells.

| Tier | What ran |
| --- | --- |
| `offline` | No ADK SDK: this skill's helpers, static reads of source or saved exports, and policy, schema and tool functions called directly on recorded or duck-typed inputs |
| `local` | The real Runner, framework or library on this machine, with a scripted model, a provider double, or a local backend or emulator |
| `live` | An authorised call to a real model, provider or cloud service, made in this session |
| `release` | The promoted build in its target environment |

Outcomes: `pass`; `fail`; `blocked` (a prerequisite, credential or approval is
missing: name it); `not run` (written or planned but not executed here: say why
and what would run it); `inconclusive` (the observations leave a threshold
open); `n/a` (the check does not apply to this change).

When a distinction matters to the reader, qualify the tier in brackets rather
than inventing a tier:

| Qualifier | Meaning | Example |
| --- | --- | --- |
| `(source read)` | Read in the installed or pinned package source; nothing executed | `offline (source read)` |
| `(rendered)` | A prompt or template rendered with fixture state; no model call | `offline (rendered)` |
| `(mocked)` | A double stood in for the model, provider or service; proves the exercised code path only | `local (mocked)` |
| `(provider)`, `(browser)`, `(hosted)` | Which live surface was exercised | `live (browser)` |

Three labels mark material that is not this session's evidence and never counts
toward a status: `historical` (an earlier session, campaign or this skill's own
validation; give its date, versions and build), `vendor-measured` (a figure or
threshold a vendor published) and `guidance` (a production principle taken from
documentation and never executed here).

A stand-in for the SDK proves only the function it was passed to; a hand-built
imitation of the Runner, the flow or the confirmation protocol is never a pass.
A skipped job, a missing score, an empty result set, a zero-case run and a bare
successful exit are `not run`. A fixture response is fixture evidence; a live
provider result and a human reviewer's decision each need their own observation.

Ticket statuses build on the tiers: `verified_local` when every acceptance case
that can run offline or local has passed here; `in_progress`, with the owed run
named in Evidence, when SDK-tier cases are written but the SDK is absent in this
session; `verified_live` after the authorised live run; `done` when the owner
accepts; `blocked` only for a decision or dependency outside the ticket.
