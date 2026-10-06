# Validate an interface change

Use the target's interpreter, test runner and pinned versions. Every interface
change gets a before/after observation; none of the checks below needs a paid
model call.

## 1. Lint and compare

```bash
python "$SKILL_DIR/scripts/lint_tool_schemas.py" --project . --max-tools 20 > /tmp/lint-after.json
```

Compare `counts` with the pre-change run. Expect no new findings of the types
the change targeted; explain any remaining `identity_parameter_review` or
`similar_tool_*` entries in the report. A `partial: true` result means an area
was not scanned; inspect it manually. The output names identifiers only, not
docstrings or prompts, so it is safe to attach to a review.

## 2. Dump the live declaration

```python
import json
from google.adk.tools import FunctionTool

def dump(tool):
    declaration = tool._get_declaration()   # private API; confirm on the pinned version
    return json.loads(declaration.model_dump_json(exclude_none=True))

for func in (lookup_order, cancel_order):
    d = dump(FunctionTool(func))
    print(d["name"], len(json.dumps(d)), "bytes")
    print(json.dumps(d, indent=2))
```

Assert in a test:

- the description equals the cleaned docstring and starts with the sentence
  you intend;
- the property names, `required` list, enum values and defaults are the ones
  you designed;
- no context parameter is visible;
- the byte size is at or under the budget you recorded.

For an `AgentTool` or a `single_turn` sub-agent, dump the parent's request
through the flow or call `_get_declaration()` on the wrapper and assert the name,
description and `request`/`input_schema` parameters.

## 3. Scripted-model Runner test

A scripted model returns a fixed `function_call` for the test prompt, then a
fixed text once it sees the tool response. The test proves that the registered
tool runs with the arguments the model would send, that the result reaches the
next request in the shape you designed, and that error dicts carry their hints.
It does not prove the real model will choose the tool.

```python
import asyncio, json
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.genai import types


def test_lookup_order_wiring(scripted_model):
    scripted_model.script([
        types.Part.from_function_call(name="lookup_order", args={"order_id": "ORD-123456"}),
        types.Part.from_text(text="Your order ships on Friday."),
    ])
    agent = LlmAgent(name="root", model=scripted_model, tools=[FunctionTool(lookup_order)])
    runner = Runner(app_name="t", agent=agent, session_service=InMemorySessionService())
    events = asyncio.run(collect(runner, "Where is order ORD-123456?"))
    responses = [p.function_response for e in events for p in (e.content.parts or []) if p.function_response]
    assert responses[0].name == "lookup_order"
    assert responses[0].response["status"] == "success"
    assert responses[0].response["order_id"] == "ORD-123456"
    assert len(json.dumps(responses[0].response)) < 2000
    # The second model request must contain the declaration once and the response once.
    second = scripted_model.requests[1]
    assert [d.name for t in second.config.tools for d in t.function_declarations] == ["lookup_order"]
```

`scripted_model` is a `BaseLlm` double the project already owns or one you add
following `adk-agent-evaluation` (deterministic tests). Record the requests it
receives so you can assert on declarations and on the tool response as the
model sees it. Add one scripted case per error branch asserting the `hint`
text arrives intact.

## 4. Result-size report

Capture events from the scripted test (or export a session from `adk web`) to
JSON, then:

```bash
python "$SKILL_DIR/scripts/report_tool_result_sizes.py" --events events.json --max-bytes 20000
```

Record per tool `response_bytes_max`, `response_bytes_p95`,
`approx_tokens_total` and `repeated_identical_responses` before and after. A
non-zero `over_max_bytes` or repeated identical responses after the change is a
finding to fix or explain.

## 5. Tool-count report

From the linter output, list each agent's `tool_count`, `toolsets` and
`sub_agents`. For toolsets, resolve the real count in a test with
`await toolset.get_tools(None)` (or a `ReadonlyContext` built for the phase) and
assert the allow-list.

## 6. Hand off accuracy measurement

Give `adk-agent-evaluation` the case set and budgets described in
[evaluation hooks](evaluation-hooks.md). Selection and parameter accuracy on a
real model are its results, not this skill's.

## Completion report

State files changed, the exact commands and their results, and separate:

| Evidence | What it supports |
| --- | --- |
| Linter and declaration dump | The text and schema the model will receive; sizes |
| Scripted-model Runner test | Wiring, argument passing, result shape, error hints |
| Result-size report on recorded events | Context cost of the tools in that recording |
| Live evaluation (adk-agent-evaluation, approved) | Selection and parameter accuracy on the named model |
| Vendor guidance (V) or documented behaviour (D) | A default worth measuring, not a measurement |

List unverified behaviour explicitly: anything read in source but not executed
on the target's interpreter, any threshold taken from vendor measurements, and
any toolset whose runtime count was not resolved.
