# Validate a security change

Use the target's interpreter, test runner and pinned versions. Every control
gets a before and after observation; the structural checks need no paid model
call.

## 1. Inventory before and after

```bash
python "$SKILL_DIR/scripts/inspect_security_surface.py" --project . > .adk-evidence/security-before.json
# ... change ...
python "$SKILL_DIR/scripts/inspect_security_surface.py" --project . > .adk-evidence/security-after.json
```

Compare `counts` and each agent's `trifecta`; a `tool_filter` built from a constant, a callable or any non-literal list is reported as `predicate`, which clears `mcp_unfiltered` but raises `mcp_filter_predicate_review` and marks the agent's trifecta incomplete, because the admitted names (and so any write or egress leg) are unknown; two or more `McpToolset`s on one agent without `tool_name_prefix` on each raise `mcp_toolsets_without_prefix`; an `AgentGovernancePlugin` with `fail_open=True` or without `strict=True` raises `governance_plugin_settings`; a tool named for its channel (`email_`, `mail_`, `sms_`) counts as egress; a retrieval tool counts as a private source only when its name carries a private token (`corpus`, `knowledge`, `kb`, `customer`, `records` and similar), so confirm the trifecta in the tool body when the inventory says otherwise; the inspector resolves only literal `name=` strings, so an agent built by a factory that passes `name` through a parameter appears as `<unnamed agent>` until the name is a literal (a helper change is owed); it also counts agents and findings in test files, so exclude `tests/` from the inventory you compare or expect the test agents to appear. Expect the targeted findings to
disappear (`trifecta_present`, `write_tool_without_gate`, `mcp_unfiltered`,
`unsafe_code_executor`, `bash_policy_allow_all`, `identity_parameter_review`)
and explain any that remain. A `partial: true` result means an area was not
scanned; inspect it by hand. The output names identifiers and flags only, so
it can be attached to a review. `adk_pins` must show
`at_or_above_cve_floor`, or the report says why not.

When a coding agent writes a pull request, gate what the production agent can
do: run the inspector on the base commit's tree, save its JSON, then run it on
the head with `--compare base.json`. It exits 1 and lists `capability_changes`
when any agent gained or lost a tool, a gate changed on a tool
(`require_confirmation` removed, a callback dropped), a toolset's filter,
confirmation or transport changed, a sub-agent or code executor changed, or a
guard finding count rose (`write_tool_without_gate`, `mcp_unfiltered`,
`trifecta_present`, `egress_capable_tool`, `workflow_graph_unread`); require a
human review label for that merge. Exit 1 takes precedence over 3. Exit 3 means
no listed change but an area the inspector could not read, named in
`unread_paths`: a `Workflow` graph, whose function nodes it names but does not
read, is always unread, so block only when one of the pull request's changed
files is in `unread_paths`, otherwise every pull request in a project with a
`Workflow` would fail. Run the inspector and the gate script from the base
commit (`git show <base>:path`), never the pull request's own copy, so the
change cannot rewrite its judge; vendor the skill under `.agents/skills/`,
which the inspector skips; let only a code owner apply the review label; and
expect the pull request that adds the gate to report NOT RUN, since its base
has no inspector.

```bash
git show "$BASE":.agents/skills/adk-agent-security/scripts/inspect_security_surface.py > /tmp/inspect.py
git worktree add -q /tmp/base "$BASE"
python /tmp/inspect.py --project /tmp/base > base.json || true
python /tmp/inspect.py --project . --compare base.json > head.json; status=$?
changed=$(git diff --name-only "$BASE"...HEAD)
if [ $status -eq 1 ]; then exit 1                     # capability changed: needs the review label
elif [ $status -eq 3 ]; then
  python -c 'import json,sys; u=set(json.load(open("head.json"))["unread_paths"]); sys.exit(1 if u & set(sys.argv[1:]) else 0)' $changed
elif [ $status -ne 0 ]; then exit 2; fi               # NOT RUN
```

Tool references resolve by name, module attribute (`tools.fn`) or import
(`from .tools import fn`, `from pkg import tools as t`) to the definition in the
scanned file of that module; anything else is `unresolved_tool_reference`, is
not classified, and leaves that agent's `trifecta` possibly incomplete.

## 2. Completed checklist

Attach the [threat-model checklist](../assets/threat-model-checklist.md) with
one worksheet per agent. Every row has an enforcement point other than
"instruction" and an observable check, or an owner-signed acceptance of the
residual risk.

## 3. Declaration dump for server-supplied tools

For each `McpToolset` and `OpenAPIToolset`, resolve the tools in a test
(`await toolset.get_tools(readonly_context)`), dump name, description and
input schema, and compare the SHA-256 of each against the committed hash;
the committed form is the interoperability skill's `mcp_tool_inventory.py`
manifest (`description_sha256`, `input_schema_sha256` per tool), so the
two skills pin the same thing and `--diff` is the SDK-free form of this
test. On an interpreter below 3.11 the inspector exits 2 with a message on
stderr; a redirected file holding that message is not evidence.
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

State files changed, the exact commands and their results, and label each
result as [evidence labels](operating-rules.md#evidence-labels) defines:

| Label | What it supports here |
| --- | --- |
| `offline (source read)` | Behaviour read in the named ADK file at the pinned version |
| `offline` | Inventory diff, hash comparison, unit tests of gates and validators |
| `local (mocked)` | Scripted-model Runner tests with backend fakes and denied egress |
| `live` | Approved red-team or `adk eval` runs on a named model and date |
| `not run` | Anything above that was not executed on the target |

Each finding in the report carries its `file:line`, OWASP LLM or ASI
identifier, enforcement point, observable check, evidence label and owning
skill. List the residual risks the structure still accepts, in the owner's
words.
