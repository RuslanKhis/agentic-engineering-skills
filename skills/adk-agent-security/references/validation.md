# Validate a security change

Use the target's interpreter, test runner and pinned versions. Every control
gets a before and after observation; the structural checks need no paid model
call.

## 1. Inventory before and after

```bash
python "$SKILL_DIR/scripts/inspect_security_surface.py" --project . > /tmp/security-before.json
# ... change ...
python "$SKILL_DIR/scripts/inspect_security_surface.py" --project . > /tmp/security-after.json
```

Compare `counts` and each agent's `trifecta`. Expect the targeted findings to
disappear (`trifecta_present`, `write_tool_without_gate`, `mcp_unfiltered`,
`unsafe_code_executor`, `bash_policy_allow_all`, `identity_parameter_review`)
and explain any that remain. A `partial: true` result means an area was not
scanned; inspect it by hand. The output names identifiers and flags only, so
it can be attached to a review. `adk_pins` must show
`at_or_above_cve_floor`, or the report says why not.

## 2. Completed checklist

Attach the [threat-model checklist](../assets/threat-model-checklist.md) with
one worksheet per agent. Every row has an enforcement point other than
"instruction" and an observable check, or an owner-signed acceptance of the
residual risk.

## 3. Declaration dump for server-supplied tools

For each `McpToolset` and `OpenAPIToolset`, resolve the tools in a test
(`await toolset.get_tools(readonly_context)`), dump name, description and
input schema, and compare the SHA-256 of each against the committed hash.
Assert the allowlist equals the expected names. A hash mismatch fails the
test; the fix is a review, not a hash update without one.

## 4. Scripted-model Runner tests

One test per gate and per structural change, following
[adversarial testing](adversarial-testing.md): the scripted model attempts
the forbidden action; the gate's error dict is the function response; fakes
show no effect and no egress; identity in the backend equals the session
user; confirmations from non-user authors are ignored; the quarantined
reader's request has no tools and no history. Run the suite with network
egress denied in the test process.

Also keep one positive case per gate: the legitimate action with user-entered
values succeeds, so the gate is shown to discriminate rather than block.

## 5. Plugin actually blocks

When policy lives in a plugin, run a Runner test on the pinned version showing
that a blocked user message or tool call produces no model request or no tool
effect. Community report #6828 (closed) documented an early-exit path that was
bypassed; test, do not assume.

## 6. Executor and deployment checks

- Executor class in the after inventory is a sandboxed one; for
  `ContainerCodeExecutor`, `network_enabled` is absent or `False`; for
  `GkeCodeExecutor`, the namespace network policy denies egress.
- `BashToolPolicy.allowed_command_prefixes` lists prefixes; a test asserts a
  command outside the list is refused.
- Deploy configuration contains no `--allow-unauthenticated` for the agent
  service unless the owner documents the public endpoint; the API server
  requires authentication.
- Denied tool calls, refused confirmations and blocked screening verdicts
  appear in logs with the agent, tool and principal; an alert exists for
  them.

## 7. Live campaign (approved)

Only after steps 1 to 6, and with written approval naming model, project,
case count, cost ceiling and egress controls. Report attack success per
scenario, with and without screening layers, as a measurement on your system.

## Completion report

State files changed, the exact commands and their results, and separate:

| Evidence | What it supports |
| --- | --- |
| Source verified | Behaviour read in the named ADK file at the pinned version |
| Local | Inventory diff, hash comparison, unit tests of gates and validators |
| Mocked | Scripted-model Runner tests with backend fakes and denied egress |
| Live | Approved red-team or `adk eval` runs on a named model and date |
| Not run | Anything above that was not executed on the target |

Each finding in the report carries its `file:line`, OWASP LLM or ASI
identifier, enforcement point, observable check, evidence label and owning
skill. List the residual risks the structure still accepts, in the owner's
words.
