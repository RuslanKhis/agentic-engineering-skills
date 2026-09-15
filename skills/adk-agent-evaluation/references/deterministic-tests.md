# Deterministic tests

Use this mode to implement or review business rules, tool boundaries, callback behaviour and ADK orchestration without paid inference. Start with read-only inspection. Preserve the target project's language, test runner, dependency pins and architecture; do not replace it with a demonstration agent.

## Procedure

1. **Define observable invariants.** Identify the allowed actors, required authorisation, business preconditions, idempotency scope, permitted state lifetime and expected effects. Distinguish attempted tool calls from executed backend operations. A scripted model may attempt a forbidden call; the invariant is that the trusted boundary rejects it without disclosure or mutation.

2. **Test the narrowest real layer.** Exercise pure validators and backend policies directly. For orchestration, retain the actual ADK `Runner`, agent, tools, callbacks and session service. Substitute the external model with a `BaseLlm` subclass implementing the installed `generate_content_async` signature. Queue valid `LlmResponse` objects containing model-selected function calls or text, record deep copies of incoming requests, and raise if responses are exhausted. Unexpected extra generations must not silently receive a convenient answer. Confirm imports and signatures against the target ADK version before adapting code.

3. **Control external boundaries.** Inject deterministic service fakes through the project's existing seams. Use synthetic fixtures and disable implicit credential/dotenv discovery in the isolated test process where appropriate. Deny external network access when claiming hermetic execution. A model double alone does not stop real tools, telemetry or callbacks from reaching external services. Do not intercept the Runner or fabricate its observed events.

4. **Establish scope explicitly.** Create sessions with synthetic identities representing the application's authenticated principal. Model-visible arguments must not choose an identity they are unauthorised to impersonate. Test missing and wrong identity according to the real domain contract; do not introduce a permissive demo fallback. Reset business stores separately from conversation sessions. Scope prerequisites to the domain's actual lifetime: invocation, transaction or durable workflow. Invocation-local verification is a useful pattern, not a requirement to invalidate legitimate durable approvals.

5. **Collect the complete invocation.** Consume `run_async` to exhaustion, retaining calls, results, errors and final events, and close the Runner in `finally`. Distinguish partial text from completed output. Correlate calls and results by their IDs when repeated names or batches make position ambiguous. A displayable answer or HTTP 200 does not establish successful completion. Mark interrupted collection incomplete; preserve observed effects rather than resubmitting a mutation.

6. **Assert across boundaries.** Compare required names, stable arguments, allowed ordering, duplicate attempts, actual backend effects and final claims. Choose exact sequence, ordered subsequence or unordered requirements deliberately. If a field is volatile, assert its relationship to the observed result instead of ignoring the whole argument object.

## Regressions that matter

Include applicable cases: missing prerequisite; wrong actor; expired or stale verification; fresh valid verification after a rejection; idempotent repeat; backend failure; and successful mutation followed by a later rejected or unrelated call in the same batch. The last case must retain the earlier success while accurately describing subsequent outcomes.

If the application renders a terminal receipt from trusted tool output, test current-workflow provenance, consumption, dynamic identifiers and amounts, forged conversation content, stale receipts and multiple outcomes. Preserve completed effects without allowing an old receipt to answer a new unrelated request. This is a truthfulness invariant; do not impose a universal receipt format or replace valid model-generated explanations without a product reason.

An environment-simulation callback plus scripted model verifies interception and orchestration only. It does not establish live model recovery, remote authentication or service-contract compatibility.

## Completion

Run the focused suite and required existing checks. Confirm expected tests were collected and executed, not merely skipped. Report actual counts, changed files, remaining failures and the substituted boundaries. For a reproduced bug, retain failing-before/passing-after evidence. Label results **deterministic/offline**; identify live integration and production identity checks that remain unverified.
