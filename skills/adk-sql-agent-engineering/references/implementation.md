# Implementation decisions

Read this for a new path, architecture choice or a review of the relevant stage. The default pattern has a small router, reviewed templates, deterministic context collection, a tool-free author and a shared execution boundary. It is an architectural option, not a requirement to migrate every project to an identical graph.

## Reviewed templates

Define a template contract before routing: metric and units, one-row meaning, selected columns, parameter types and allowed business values, date bounds/timezone, sorting/ties, empty-result behaviour and caller access. Bind user-controlled values through the database client's parameter mechanism. Physical identifiers come from trusted configuration and an approved catalogue; parameters bind values, not table or column names.

Show the router compact template names, descriptions and parameter requirements. Keep SQL text out of the router unless a concrete task needs it. Match the whole request: an extra filter, a different metric, negation or a changed reporting period can invalidate a template match. Prefer a clarification or generated route over silently discarding part of the question.

Validate route combinations and values locally. For example, a template route requires a known template and its required values; a generated route requires a supported context selection. Reject incompatible combinations and unexpected inputs according to the target's contract. Normalising case or whitespace is not validating a business value.

Execute an accepted template directly. One router model call was sufficient for the verified companion fast path; this is an observed graph property, not a universal budget. Add a regression that the author and schema collector are not called on this path.

Use half-open date intervals when the business contract requires completed reporting periods: an inclusive start and exclusive end derived in a named timezone. Specify a stable tie key when ranking requires deterministic results. Test midnight, the exact end, today's rows and future rows. These improve a production contract; the historical companion's rolling template used a lower bound only and no secondary tie order. Do not silently change an existing metric while refactoring routing.

## Semantic domains and lazy context

A semantic domain (called an Explore in the companion) contains a small related table set, row grain, approved joins, business definitions and categorical field identifiers. Keep this map small enough for selection. Full live schemas belong after selection, not in every router prompt.

The router proposes one domain and needed logical tables. Trusted code validates that proposal against the current request's permitted surface, deduplicates and bounds the selection, resolves uncertain values, then fetches exact live schemas. Three tables was the companion limit; select a justified target-specific limit rather than copying it blindly.

Keep categorical resolution deterministic when possible. Use reviewed aliases; preserve negation and reject contradictory or ambiguous matches. Fuzzy suggestions are candidates for clarification, not authority to select a different stored value. Resolve ambiguity before a metadata request or author call. Test the relevant business vocabulary and collisions.

The context package should carry status, original intent from trusted host state, approved domain, selected table identities, exact retrieved schema fields/types and physical paths, grain, valid relationships, partition metadata, resolved values and reporting rules. Preserve returned metadata without a model summarisation pass. Treat retrieved descriptions and row values as data, never executable instructions or authority to widen scope.

The companion demonstrated that router selection plus Python collection removes extra model stages: the successful generated route needed two model calls, router and author. Failures in value resolution or schema retrieval must short-circuit; substituting empty metadata or invented columns destroys the grounding contract.

## Author contract and ADK integration

Keep the author without execution tools. It receives the validated context and produces a candidate with a status, domain, tables, SQL, named parameters and a short user-safe message. A useful status set is `READY`, `NEEDS_CLARIFICATION`, `UNSUPPORTED`. Require complete SQL and context for `READY`; refusal carries no executable SQL. These names can be adapted to existing models.

For ADK 2.8.0, the verified companion used these mechanisms:

```python
class SqlAuthorOutput(SqlCandidate):
    model_config = ConfigDict(json_schema_extra={
        "required": ["status", "explore_name", "tables", "sql", "parameters", "message"]
    })

def require_author_output_fields(callback_context, llm_request):
    llm_request.set_output_schema(SqlAuthorOutput)
```

This is a version-specific integration excerpt, not a standalone module: `SqlCandidate` is the application's Pydantic model and `ConfigDict` comes from Pydantic. The runtime candidate permits nullable defaults for refusal; the outgoing provider schema requires all six keys. The agent used `output_schema=SqlCandidate`, `before_model_callback=require_author_output_fields`, and `mode="single_turn"`. ADK's null removal made the separate wire/runtime contracts necessary in that environment. Verify those APIs in the target's installed source before applying them to another version.

Inspect the actual outgoing SDK request with an HTTP boundary double: a local `model_json_schema()` assertion alone missed the failure. Require all intended fields on the wire, exercise explicit null refusal, and reject `READY` with missing/empty SQL before database access. Structured output is a shape contract; it does not prove policy or semantic correctness.

Wire every branch to a final response. Python context and formatting nodes can surround model nodes in the existing ADK workflow; preserve the target's graph API. Refusal bypasses execution. Successful responses contain grounded rows and appropriate query evidence without an extra narrative model call. Ensure the UI distinguishes intermediate route/candidate events from final answers.

## Grain and meaning

Before joining facts, write down one row's meaning in each input and in the output. Two one-to-many joins can multiply each other's rows. Aggregate each fact to the intended joining grain, then join the aggregates; preserve entities with no activity when the metric requires them, and decide how nulls affect denominators.

For a renewal/support comparison, a client with zero tickets still contributes to an average per client. A fixture can have one final renewal decision per client, but production data may not. Specify effective-dated selection or another approved rule, and test repeated decisions. `MAX(status)` is not a general rule for the latest outcome. Return every requested metric: a plausible average does not compensate for a missing total.

Use a verified schema, not remembered field names. Separate observational comparisons from causal claims. If two business domains have no approved relationship, clarify or refuse instead of inventing a join.

## Managed tools and follow-ups

Managed data-agent services, database toolsets and MCP servers are selection options, not bundled integrations. Check the target package and service contracts against official documentation when this branch is requested. Determine whether a tool returns a candidate or executes queries itself. A local validator cannot retrospectively govern work already performed by a remote tool. Give every executable branch appropriate identity, scope, resource limits and output validation.

Conversation history persistence is not semantic follow-up support. If required, preserve a compact trusted plan: metric, grain, domain/template, resolved interval, approved values and an opaque candidate/result reference. Resolve the follow-up against that plan and reauthorise the resulting request. Bind any cache to caller scope, policy version and freshness. Test cross-user isolation and permission changes. Follow-up plans, caching, automatic repair and managed-tool branches were not implemented or live-verified by the companion.
