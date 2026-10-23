# googleapis/mcp-toolbox compared with this toolkit — 22 October 2026

## Scope and snapshot

A file-level review of [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox)
(MCP Toolbox for Databases, formerly genai-toolbox) at commit `3581e0a`
(2026-10-21), latest tag v1.14.0, cloned on 22 October 2026 into its own
directory and read, never run. Licence: Apache-2.0, no NOTICE file, no
per-folder licences. Files read: `README.md`, `CHANGELOG.md`,
`docs/en/documentation/configuration/security/read-only.md`,
`.../configuration/security/model-armor.md`,
`.../configuration/tools/_index.md` (parameters, template parameters, secure
parameters), `docs/en/integrations/bigquery/tools/bigquery-execute-sql.md`,
`docs/en/integrations/postgres/tools/postgres-sql.md`,
`docs/en/documentation/connect-to/toolbox-sdks/python-sdk/adk/index.md`.
The memo also named ADK's `DataAgentToolset`; its page
(https://adk.dev/integrations/data-agent/) and `tools/data_agent/config.py`
at adk-python main `ed76f94` were read the same day, as was the ADK Model
Armor plugin (`integrations/model_armor/_plugin.py`, `_config.py`) because
the Toolbox Model Armor page raised the question of who screens tool
results.

**Conclusion.** Toolbox is the executor this toolkit's SQL specialist has
been describing generically. Its read-only document is the clearest
statement anywhere of why a prompt or a `SELECT` check is not a control and
what an engine-level lock looks like, so the SQL skill now carries a Toolbox
branch checklist that maps its four boundaries onto Toolbox configuration,
plus the three bypass statements as deterministic fixtures. Secure parameters
give the auth skill a concrete mechanism for keeping the tenant id out of the
model. Two memo claims did not survive verification and are recorded below.

## Method

Each named document was read in full; each candidate item was classified
(fact, routing line, method, asset, spike, or do not import), checked against
the specialist that already covers the decision, and written at that
decision with the citation `(MCP Toolbox for Databases v1.14.0, <file>, read
2026-10-22; vendor documentation)`. One scenario case and one fresh-agent
trial cover the changed journey (see the
[testing record](../testing/mcp-toolbox-alignment-2026-10-22.md)). Nothing
was executed: the Toolbox server, its SDK and a database were all absent.

## Drift corrected

- The memo said the Toolbox Model Armor document "screens tool results
  flowing back to the model" and fills the ADK plugin's gap. The page's ADK
  sample screens with `before_model_callback` and `after_model_callback` and
  explicitly skips tool-result turns; only its LangChain middleware screens
  tool data, and the gateway and floor-setting paths screen outside the
  agent. Recorded as such in the sensitive-data skill.
- The ADK plugin's gap itself closed in 2.12.0: commit fdda17c adds an
  `after_tool_callback` that screens tool output against a separate
  template, chunked at 65,536 characters (source-verified on main; absent at
  tag v2.8.0). The sensitive-data skill's "skips function responses" sentence
  is now version-conditional. This is a Phase B row 4 fact that the Toolbox
  question surfaced.
- The memo said secure parameters "require MCP protocol 2026-07-28". The
  documentation says a client that has not negotiated the feature is refused
  with `-32021` on 2026-07-28 and with `-32602` on earlier revisions, so the
  requirement is negotiation, with a different error before that revision.

## Imported, by specialist

- **adk-sql-agent-engineering.** A "MCP Toolbox for Databases as the
  executor" checklist in the acceptance-and-extensions reference: read-only
  at the source (DSN lock `cloudsql_session_read_only=locked` or
  `alloydb_session_read_only=locked`, MySQL `read_only_connection=true`,
  BigQuery `dryRun` statement-type check; why `COMMIT;` chaining and pooler
  poisoning do not apply), the BigQuery flags (`readOnly` defaults
  `writeMode` to `blocked`, `protected` for session temp tables, conflicting
  settings rejected at startup, `allowedDatasets` analysis with its
  authorized-view and fully-qualified-name rules and the operations it cannot
  analyse), the prebuilt free-form tool's own "shouldn't be used for
  production agents" note, basic parameters over template parameters with
  the documentation's injection warning and the `allowedValues`, `escape`,
  `minValue`/`maxValue` mitigations, secure parameters for tenant and user
  ids with the wire and error semantics, and the three bypass fixtures.
  `DataAgentToolset` facts (read-only by default, the modification flag,
  the 50-row default, the 60-second modification timeout, the experimental
  credentials base) on the governed-data-agent row. The entry skill points to
  the checklist; the execution-safety reference carries the three fixtures
  for the application's own parser path; the compatibility reference records
  the sources.
- **adk-agent-interoperability.** The selection row and the toolset notes
  now carry the client's default protocol (2026-07-28) and the `protocol=`
  pin, the seven credential strategies with the `openid` requirement for the
  user-identity flow, and the `credentials: CredentialConfig | None`
  signature on adk-python main.
- **adk-agent-security.** The annotations row says a server you operate can
  make `readOnlyHint` true, with the DSN lock as the control.
- **protect-adk-sensitive-data.** The version-conditional tool-output
  screening in the ADK plugin, and the two Google paths that screen tool
  traffic outside the agent (Agent Gateway ingress and egress templates;
  project-wide floor settings for supported Google Cloud MCP servers, with
  their limits).
- **adk-tool-auth-and-secrets.** Tenant and customer ids as secure
  parameters bound in code, database credentials in the source configuration,
  and the client-to-server strategies.

## Routed, not copied

No routing line: Toolbox is a server and a client library, not a skill, and
the repository's `skills/maintainer/` folder maintains Toolbox itself.
Deploying the server and provisioning its sources stay with
deploy-adk-on-google-cloud and the database product skills already mapped.

## Vendored assets

None.

## Left out, with reasons

- The prebuilt `bigquery-execute-sql` tool as a production default: its own
  page says not to.
- Template parameters for user-supplied values: the documentation calls them
  prone to injection; they are allowed only behind `allowedValues` and a
  reviewer, as the checklist says.
- The Toolbox ADK page's `toolbox_identity()` strategy outside local
  development: no authentication.
- Toolbox's own evaluation harness (`evals/`), its Looker, Firestore, Spanner
  and other source tools, and the 1.14.0 authorized-view feature beyond the
  one sentence the checklist carries: no decision in this toolkit changes.
- A spike against a running Toolbox server: no server, database or
  credentials in this session; the checklist's live steps are written as
  planned verification.

## Limits

Read, not run. The DSN lock and the dry-run rejection are the vendor's
statements of their own mechanism and were not exercised; the checklist asks
the ticket to prove the three bypass fixtures fail closed on the installed
server. The `-32021` and `-32602` codes and the SDK method names are as
documented at v1.14.0 and `toolbox-adk` 1.4.0 and may move. The ADK Model
Armor plugin's tool-output screening was read in source, not executed.
