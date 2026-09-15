# Validation by evidence level

Use only checks relevant to the chosen mode and user's scope. Preserve the project's existing test runner. The examples below describe test contracts; adapt endpoint and event schemas to the installed ADK version.

## Offline first

1. Run the project's formatter/static checks and affected tests in its existing environment. Check imports and SDK method signatures without importing agent modules that might contact services. Check shell syntax without executing deployment scripts. Parse generated manifests locally; a Kubernetes server-side dry run still contacts a cluster.
2. Build a source manifest from the actual staged context. Test that nested `.env`, credentials, caches, virtual environments, state journals and symlink escapes cannot be uploaded. Inspect SDK-generated packaging separately from `.dockerignore` or `.gcloudignore` assumptions.
3. Use a fake model/provider boundary with the real HTTP server and session implementation. Verify tool invocation, exact structured result, grounded final text and error handling. Run the server on a loopback ephemeral port with a readiness timeout and guaranteed owned-process cleanup.
4. Exercise repeated setup/cleanup and interrupted state transitions with fake provider responses: same source does not rebuild, unowned/replaced target refuses mutation, denied lookup is not absence, uncertain accepted submission is not repeated, completed deletion repeats as reads only.
5. For containers, check non-root execution, configured port, readable app files and a writable home if the ADK UI is enabled. Exercise telemetry preference HTTP writes/reload where that endpoint exists. Label these local results; a fixed Dockerfile does not establish that the deployed image contains the fix.

## Shared HTTP acceptance for Cloud Run and GKE

At the tested ADK 2.8.0 baseline, the app identifier is the agent package directory, which can differ from `root_agent.name`. Discover it using `GET /list-apps`; never substitute the internal agent name blindly.

An approved synthetic session uses `POST /apps/{app}/users/{user}/sessions/{session}`. The body is the state dictionary itself, not a nested `state` object. For example, `{ "purpose": "deployment-verification" }`. Session/user IDs are synthetic unique values and are not authentication credentials.

For `POST /run`, use the actual API schema. At this baseline the request contains:

```json
{
  "appName": "agent_package",
  "userId": "synthetic-user",
  "sessionId": "synthetic-session",
  "newMessage": {
    "role": "user",
    "parts": [{"text": "Synthetic technical issue: login failed."}]
  }
}
```

The strings above illustrate the schema; resolve the discovered app and newly created IDs for a real request. `/run` returns a JSON event array; `/run_sse` streams events. Validate the relevant tool result and a final answer grounded in it, not incidental text anywhere in the response. Scan for contradictions such as claiming that a read-only classification actually sent a ticket or issued a refund.

For routing-style tools, cover materially different branches with synthetic messages, including one precedence case. For another domain, substitute its real tool contract rather than installing the chapter's routing tool. The chapter's three queues were billing, technical support and general support; the tool only classified a message.

Then ask an explicit follow-up that requires an earlier synthetic fact. Assert that the answer recalls the correct fact within the same session. A second unrelated prompt is not a recall test. Read the session history and verify expected accepted turns/tool calls. Delete the created session and verify absence. Restart against the same local database when testing process persistence; this does not establish durability through instance or Pod replacement.

Negative cases: malformed request (422 at the baseline), missing session (404), anonymous/invalid caller credentials at the actual authentication boundary, and failed downstream model/tool response. A different caller-supplied `userId` tests lookup partitioning, not cross-user security. Production authorisation requires an authenticated principal bound to permitted user/session IDs and tests attempting cross-user access.

## Browser acceptance is additional evidence

Open the actual documented access path and use the packaged UI or application's UI. Confirm JavaScript modules load, streaming completes, the expected tool result and grounded answer are visible, and explicit recall works. A successful `curl` or health probe alone does not prove this workflow.

For a retry test, disconnect the owned local tunnel before dispatch, confirm the request never reached the server, verify visible error feedback and usable input, reconnect, then submit one explicit retry within the budget. Count server-accepted user turns and tool results. Duplicate local message bubbles alone do not prove duplicate tool execution.

Keep failures separate:

| Failure | Acceptance question |
| --- | --- |
| Known pre-dispatch network failure | Was it visible, did input recover, and did one explicit retry create one accepted operation? |
| HTTP 502/500 | Was there visible feedback? Reconcile acceptance before repeating a non-idempotent operation. |
| Accepted request timed out | Can server history/operation state establish the outcome? If not, stop and report uncertainty. |
| Optional telemetry/debug route absent | Is the endpoint required by this application? Report separately from chat success. |

The historical UI restored input but showed no visible error for an audit proxy's HTTP 502; the direct disconnected tunnel produced visible failure and successful recovery. Do not declare all retry/error behaviour verified from the direct case.

## Live tests and rebuilt artefacts

Live tests require explicit approval, an isolated target, synthetic data, per-call bounds and a cleanup reserve. Record each model attempt and accepted turn, each build submission and terminal result, conservative control-action usage, source fingerprint, resource UID and image digest/revision. Follow [lifecycle.md](lifecycle.md) for recovery and teardown.

Verify model/backend and runtime identity independently of deployer access. For a repair, confirm the running revision/digest contains the rebuilt source and reproduce the repaired behaviour through the intended user workflow. A local pass or a newly built image that never receives traffic is not a live repair verification.

Use explicit evidence labels:

- **Local real component:** actual server/SDK/session store, with precise external boundaries identified.
- **Mocked provider/model:** validates orchestration and assertions, not Google Cloud availability or model behaviour.
- **Live verified:** names the approved target privately, date, source/version, actual request and observed result.
- **Not run:** states the untested branch and practical implication.

Report latency only if measured under an agreed acceptance condition. Production scaling, durability, tenant authorisation and arbitrary-failure retry guarantees require dedicated tests beyond this skill's historical evidence.
