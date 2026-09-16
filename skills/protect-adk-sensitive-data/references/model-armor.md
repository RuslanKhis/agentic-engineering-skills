# Model Armor at explicit boundaries

Read for prompt injection/content screening, ADK model callbacks and answer
release. Pair it with SDP when policy permits PII replacement. Neither service
decides who may access an order, document or destination.

## Direct versus native integration

| Boundary | Integration and purpose |
| --- | --- |
| User input before session/history | Direct prompt screening after SDP; reject or use an explicitly allowed transformation |
| Model input/output | Native ADK plugin as another model boundary on the recorded compatible version |
| Tool arguments and public tool results | Explicit application hooks; native screening does not cover every structured part |
| Complete public response | Direct response screening after event projection, before JSON/SSE release |

The multiple calls are intentional boundaries with separate costs. Count them
when budgeting. Removing a call to reduce latency needs a data-flow proof and
regression coverage showing the remaining control runs before every relevant
sink; do not silently collapse them.

## Native ADK 2.8.0 contract

The recorded imports are `ModelArmorConfig` and `ModelArmorPlugin` from
`google.adk.integrations.model_armor`. Configure trusted full
`prompt_template_name` and `response_template_name`, static
`input_blocked_message` / `output_blocked_message`, and
`block_on_screening_failure=True`. Attach the plugin once to `App.plugins` after
the argument-protection plugin. Inspect the pinned source and callback tests
before applying this ordering on another version.

At this tested version the native plugin screens the latest user text and model
text, skips function responses, and does not screen function-call arguments as
text. It blocks `MATCH_FOUND`; it does not substitute advanced SDP transformed
text. `block_on_screening_failure=False` changes screening-error behaviour; it
is **not** a shadow/observe-only switch. A native plugin alone therefore does
not establish protection before user-event persistence, complete-history
screening or safe tool payloads. Historical source and regression provenance:
[compatibility.md](compatibility.md), E4–E6.

The native plugin accepts `client=...`, but its calls supply no explicit timeout
or retry arguments and have no semaphore. It closes its internal lazy client,
not a supplied client. Its failure path also logs provider exceptions. When
bounding native calls or suppressing sensitive diagnostics, use the facade and
ownership guidance in [implementation-recipes.md](implementation-recipes.md).
Direct-client limits and log filtering do not automatically cover this path.

## Direct client and verdicts

Own one regional `modelarmor_v1.ModelArmorAsyncClient`, reuse it, close its
transport, and apply semaphore, RPC and overall limits. In the recorded API,
call `sanitize_user_prompt` with `SanitizeUserPromptRequest(name=...,
user_prompt_data=DataItem(text=...))`, or `sanitize_model_response` with
`SanitizeModelResponseRequest(name=..., model_response_data=DataItem(text=...),
user_prompt=...)`. The optional prompt context must already be protected.

Templates use `projects/{project}/locations/{location}/templates/{id}`. Match
the client endpoint `modelarmor.{location}.rep.googleapis.com` to the template
location; do not use the global endpoint for sanitisation. Model generation
location is a separate decision. [Model Armor endpoint documentation](https://docs.cloud.google.com/model-armor/data-residency).

Map provider results to these explicit application decisions:

| Decision | Required handling |
| --- | --- |
| `ALLOW` | Required invocation/filter checks completed successfully with no disallowed match; continue with the accepted text |
| `TRANSFORM` | Input policy explicitly permits it, the only matching filter is the relevant SDP de-identification, all required checks completed, transformed text exists and passes limits/schema; continue with that text |
| `BLOCK` | Any disallowed match, including generated-output PII under block-only policy; withhold action/answer |
| `INDETERMINATE` | Missing/unknown verdict, partial execution, skipped required filter, malformed result, timeout, API error or unsupported modality; withhold action/answer |

Inspect the response `sanitization_result`, invocation state, filter match state
and the relevant filter-result oneofs. Do not interpret an empty response as
allow, a transformed-text field as approval by itself, or successful HTTP status
as successful screening. Validate the configured required filter set on all
paths, including aggregate no-match results (**production hardening beyond the
historical aggregate no-match shortcut**). Add recorded SDK-shaped fixtures for
each accepted and rejected result shape.

The inspected native plugin also accepts successful invocation when the
aggregate state is anything except `MATCH_FOUND`; that is weaker than validating
the required filter set above. A custom client/plugin boundary must enforce the
stronger contract if required; attaching the stock plugin is not evidence of it.

For output use block-only policy unless the product deliberately implements and
tests an output rewriting contract. Withhold the full answer on a block; do not
release a prefix. Historical output SDP policy inspected PII only and did not
reuse the dedicated credential-deny template. If outputs must also reject
credentials, add and test explicit output coverage; do not claim it already
exists. The provider guide describes sanitisation methods and result fields.
[Sanitise prompts and responses](https://docs.cloud.google.com/model-armor/sanitize-prompts-responses).

## Validate policy as well as plumbing

Exercise mixed results (PII transformation plus another blocking filter), no
verdict, partial invocation, missing transformed text, wrong text modality,
provider failure and split sensitive strings across generated chunks. Verify
the native plugin still executes after successful argument protection. Use
representative synthetic allowed and denied cases to measure detector accuracy
only in a separately approved live campaign; mocks establish orchestration.

A template GET is not an effective-policy audit. Confirm applicable organisation
floor settings, supported filters/modality/locations and payload logging before
production use. See [cloud-lifecycle.md](cloud-lifecycle.md) for the controlled
setup and readiness workflow.
For tenant-specific templates, shadow rollout or detector evaluation, read
[production-policy.md](production-policy.md).
