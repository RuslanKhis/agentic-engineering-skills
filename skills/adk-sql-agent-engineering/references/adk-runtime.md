# ADK runtime integration

Read this when implementing or diagnosing the ADK boundary. The graph and callback mechanisms below come from the Chapter 10 application tested with ADK **2.8.0**. Keep the target's versions and architecture; verify the installed APIs before adapting the examples. The optional [offline contract probe](../assets/test_adk_contract.py) supplies a runnable synthetic example independent of the book or companion source.

## Connect typed data, routing and final messages

ADK 2.8 accepts Agents and Python functions in `Workflow.edges`. A typed parameter named `node_input` receives the preceding node's output. Return `Event(output=...)` to pass data, `Event(route=..., output=...)` to choose a mapped destination, and `Event(message=...)` to emit final presentation. These are different responsibilities; a router's JSON is not the database answer.

The following is the verified graph pattern. Names such as `router`, `collect_context` and `execute_candidate` are application dependencies, not hidden SDK functions. The probe supplies runnable definitions for its synthetic equivalent.

```python
from google.adk import Event, Workflow

def select_route(node_input: RouteDecision) -> Event:
    known = node_input.template_name in template_library
    route = "FAST_PATH" if node_input.route == "FAST_PATH" and known else "SLOW_PATH"
    return Event(route=route, output=node_input)

root_agent = Workflow(name="sql_workflow", edges=[
    ("START", router, select_route),
    (select_route, {"FAST_PATH": execute_template, "SLOW_PATH": collect_context}),
    (execute_template, format_result),
    (collect_context, {"READY": sql_author, "NO_QUERY": format_result}),
    (sql_author, execute_candidate, format_result),
])
```

The collector validates the selected domain/tables and every requested categorical field before metadata access. Resolve ambiguous values before authoring. Missing metadata returns a controlled failure through `NO_QUERY`; it is not an invitation to invent columns. `READY` carries exact structured metadata, including physical `fully_qualified_name`, logical table identifiers, columns/types, grain, relationships, partition information and resolved values. Preserve those fields without a model summary.

Use public invocation APIs in integration tests. Create a session with the same application/user/session identifiers supplied to `Runner.run_async`, pass a `types.Content(role="user", parts=[types.Part(text=question)])`, and consume the asynchronous event stream through completion. The companion supplies `RunConfig(max_llm_calls=10)`. Its helper keeps the final response while continuing iteration; it does not return immediately on the first intermediate model event. Test the actual formatter's output, not just that some event was labelled final. Project the events appropriate for the audience rather than forwarding internal candidates by default.

Assert the trajectory as well as the answer: reviewed route bypasses metadata/authoring; generated route reaches collection then authoring; refusal and metadata failure bypass execution. Count model, metadata and submission operations separately. Two model stages is a property of this graph, not proof of a particular latency.

## Keep provider and runtime schemas distinct where necessary

The author has no execution tools. Its six output fields are `status`, `explore_name`, `tables`, `sql`, `parameters` and `message`. `READY` requires a usable SQL candidate and domain at the application boundary. A refusal can have null SQL/domain and empty collections.

In the tested ADK 2.8 workflow, null fields are removed before a later validation step. Keep nullable runtime defaults so a valid refusal survives that handoff; independently require those keys in the provider-facing schema. The minimal types below illustrate that distinction, not the full parameter or SQL validation policy.

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict
from google.adk import Agent

class Candidate(BaseModel):
    status: Literal["READY", "NEEDS_CLARIFICATION", "UNSUPPORTED"]
    explore_name: str | None = None
    tables: list[str]
    sql: str | None = None
    parameters: list[dict[str, str]]
    message: str

class ProviderCandidate(Candidate):
    model_config = ConfigDict(json_schema_extra={
        "required": ["status", "explore_name", "tables", "sql", "parameters", "message"]
    })

def require_keys(callback_context, llm_request):
    llm_request.set_output_schema(ProviderCandidate)

# configured_model is supplied by the application's model/credential factory.
author = Agent(
    name="sql_author", model=configured_model,
    instruction="Propose one candidate from the supplied approved metadata.",
    output_schema=Candidate, before_model_callback=require_keys,
    mode="single_turn",
)
```

`set_output_schema` sets the request's schema and JSON MIME type in ADK 2.8. Inspect the GenAI HTTP request after its real serialisation: `generationConfig.responseSchema.required` must include all six fields, and SQL/domain must remain nullable. Then test the return path into a typed Python node. A local `model_json_schema()` check does not establish this wire contract. Nor does a well-formed synthetic answer prove the outgoing schema is correct: the probe deliberately removes the callback and verifies that its required-key assertion fails.

The provider schema is still not an execution policy. Simulate a provider returning `READY` without SQL and verify that the application rejects it before submission. Preserve explicit-null refusals. Require the author to put SQL in `sql`, use physical paths from retrieved metadata in `FROM`/`JOIN`, and distinguish those paths from logical names in `tables`; enforce the needed policy independently.

## Preserve trusted state outside model output

**Production extension; not implemented or live-verified by the companion.** Keep the original question and authenticated authorisation in host-owned invocation state. A model's copied question or selected domain is a proposal. An immutable request record can contain an opaque request identifier, original question, caller policy/version and authorised table/domain sets. A separate collection record contains the validated selection and actual retrieved physical table identities.

Use explicit interfaces such as these; they are design contracts, not claims about automatic ADK state injection:

```text
collect_context(selection, trusted_request, metadata_gateway) -> collected_scope
execute_candidate(candidate, trusted_request, collected_scope, warehouse) -> result

candidate.domain == collected_scope.selected_domain
parsed_physical_tables <= trusted_request.authorized_tables
parsed_physical_tables <= collected_scope.retrieved_physical_tables
```

Choose a tested host-to-node injection mechanism in the target application. A request-specific workflow factory or explicit invocation dependency may fit; do not treat arbitrary session/model state as authorisation automatically. Keep each invocation's scope separate, restore temporary context in `finally`, and avoid mutable caller scope on shared Agent objects or process-wide environment variables. Give the author only the metadata needed for its task; the authorisation record itself need not become prompt content.

Test two interleaved callers, tampered copied intent, a candidate choosing another globally approved domain, an authorised-but-unretrieved table, and a permission change between requests. Bind reviewed templates to caller policy too. These tests establish only the controls actually implemented; the companion's executor currently checks the domain named by the candidate rather than independently binding it to the router and collected schemas.

## Share credential construction, not caller authorisation

The companion has one optional credential factory consumed by both `bigquery.Client(..., credentials=credentials)` and ADK `Gemini(..., client_kwargs={...})`. Its impersonation branch checks that the runtime service-account name belongs to the configured resource project before calling ADC. It constructs refreshable credentials with a 900-second lifetime and an explicit quota project, then uses the same object for model and warehouse clients. Construction does not itself establish successful refresh or permissions.

For a target that uses this pattern, the version-specific wiring is:

```python
import google.auth
from google.auth import impersonated_credentials
from google.cloud import bigquery
from google.adk.models.google_llm import Gemini
from google.genai import types

# Values below must already come from validated host/deployment configuration.
scopes = ["https://www.googleapis.com/auth/cloud-platform"]
source, _ = google.auth.default(scopes=scopes)
credentials = impersonated_credentials.Credentials(
    source_credentials=source, target_principal=runtime_email,
    target_scopes=scopes, lifetime=900, quota_project_id=quota_project,
)
warehouse = bigquery.Client(project=resource_project, credentials=credentials)
model = Gemini(model=model_name, client_kwargs={
    "enterprise": True, "project": resource_project, "location": model_location,
    "credentials": credentials,
    "http_options": types.HttpOptions(
        timeout=60000, retry_options=types.HttpRetryOptions(attempts=1),
    ),
})
```

This excerpt constructs real credential/client objects and is **not an offline probe or provisioning command**. Adapt it only within the target's authorised configuration; use boundary doubles in ordinary tests. The shared runtime identity is not tenant isolation. The source companion scopes runtime project roles to BigQuery Job User, Vertex AI User and Service Usage Consumer, dataset access to the owned dataset, and operator Token Creator to the owned runtime account. Those are recorded lab choices, not a universal IAM recipe.

Test factory contracts without refresh: both clients receive the same intended credentials; resource/quota settings remain distinct; a wrong-project principal fails before ADC discovery; absent impersonation does not eagerly discover credentials. The companion's default branch returns the model name and lets normal ADK/backend configuration apply. It does not inherit every explicit transport option of the impersonated branch. Separately approved readiness checks mint only a token, with bounded retry for recognised IAM propagation errors; they do not replay model calls or queries.

Configuration lifetime matters. The companion reads its chapter `.env` with existing process variables winning, caches settings, caches runtime credentials/client objects, and constructs Agents from those settings during module initialisation. Configure before constructing the application. A later environment edit does not update existing objects. Test cache invalidation explicitly or restart/rebuild the application. A plan/inspection entry point should avoid imports that initialise runtime credentials; import inside the execution path when necessary.

## Budget and concurrency boundaries

`single_turn` is interaction mode. An output-token limit, a Runner model-call limit, a model HTTP timeout, a query-call timeout and an invocation deadline are separate controls. Specify the relevant budgets explicitly. The historical companion used one model SDK attempt with a 60-second HTTP timeout in its impersonated branch, separate query-call limits, and no complete cumulative invocation deadline.

The inspected ADK 2.8 `FunctionNode` directly calls synchronous Python functions; do not assume it moves blocking BigQuery work to a thread. Before serving concurrent requests, test an unrelated request or event-loop heartbeat while the database boundary is delayed. Use a supported asynchronous adapter or bounded worker strategy where needed, and test cancellation/cleanup semantics: cancelling an await does not prove a thread or provider job stopped. This is an implementation concern identified from source, not a measured companion concurrency regression.

## Run the optional offline contract probe

From the installed skill directory, use the target's existing environment in a **fresh process**:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  python -m pytest -q -p no:cacheprovider assets/test_adk_contract.py
```

Do not install or change dependencies to make this command pass without the target's normal dependency decision. The asset requires ADK 2.8.0 and reports a failing version assertion for another version; adapt and evaluate another version deliberately. It is outside the standard-library helper test directory. It has no imports from the target application or companion repository.

The asset blocks socket connection/DNS operations and ADC discovery, uses `AnonymousCredentials`, disables inherited Google/telemetry configuration within its test fixture, and replaces only the GenAI client's private `async_request` HTTP seam. Unexpected traffic fails locally. The seam is private and version-sensitive; a changed seam is a compatibility failure, not a reason to mock away serialisation. Run in a process without custom startup/exporter code; the guards protect probe execution, not arbitrary code executed before pytest starts. Both client interfaces are closed.

Metadata and query results are synthetic. PASS establishes the exercised graph, serialiser, nullable return path, final-event and refusal/call-count contracts under the observed stack. It does not establish provider acceptance, BigQuery SQL semantics, query safety, live credentials, model quality, streaming transport or latency. The tests intentionally use non-streaming model transport while consuming ADK's asynchronous event stream.

The historical companion used GenAI **2.23.0**, Pydantic **2.13.5** and google-auth **2.58.0**. This portable asset is evaluated separately with the existing repository environment; record its actual versions and command result in the skill verification record. A successful run on another stack does not retroactively rerun the historical campaign.
