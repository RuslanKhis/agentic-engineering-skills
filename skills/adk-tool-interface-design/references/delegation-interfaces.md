# Delegation interfaces: AgentTool, sub_agents and modes

A sub-agent is also an interface the parent model has to select correctly.
This reference covers how each ADK 2.8.0 delegation shape appears to the parent
model and how to choose between them. Verified in `agents/llm_agent.py`,
`tools/agent_tool.py` and `flows/llm_flows/agent_transfer.py` on 2026-10-06.
`adk-workflow-design` owns the control-flow decision (sequential, parallel,
loop, graph); `adk-agent-instructions` owns the wording of agent descriptions
and instructions. This reference owns what the parent model sees and how to
verify it.

## What the parent model sees

| Shape | Declaration the parent receives | Interaction | Return |
| --- | --- | --- | --- |
| `sub_agents=[a]` with `a.mode` unset or `'chat'` (default for an `LlmAgent` sub-agent) | A `transfer_to_agent` tool plus an instruction block listing `Agent name: <name>` and `Agent description: <description>` verbatim for every transfer target | Sub-agent talks to the user until it transfers back | Manual, via transfer |
| `sub_agents=[a]` with `a.mode='task'` | A tool named after the sub-agent (`_TaskAgentTool`) whose parameters come from `a.input_schema` or a default `request: str` ("Detailed instructions or context for the task sub-agent"); description = `a.description` | Sub-agent may ask the user clarifying questions | Automatic through `finish_task`; excluded from transfer targets |
| `sub_agents=[a]` with `a.mode='single_turn'` | A tool named after the sub-agent (`_SingleTurnAgentTool`); parameters from `a.input_schema` or `request: str`; description = `a.description` | None; runs inline in the parent's session | Automatic, with the result as the tool response; excluded from transfer targets |
| `tools=[AgentTool(a, skip_summarization=False)]` | A tool named `a.name`, description `a.description`, parameters from `a.input_schema` or `request: str` | None; runs in a separate in-memory session under a nested `Runner` | Final text (or validated `output_schema` object) as the tool result |

The `AgentTool` docstring in 2.8.0 says "Direct usage of `AgentTool` is
discouraged" and recommends `mode='single_turn'` with `sub_agents`. Prefer that
unless you need the isolation `AgentTool` provides (separate session, state
copied in, state deltas forwarded back) or you are wrapping a non-`LlmAgent`
that does not declare `mode`.

The description is the whole interface in every row. The parent model chooses
among sub-agents the way it chooses among tools: by name and description. A
description that only repeats the name, or that lists capabilities without
saying when to route there, produces wrong transfers. The linter flags
sub-agent descriptions shorter than eight words or equal to the name.

## Choose the shape

Google's own summary (Cloud blog, 2025-11-08, V): "Use tools for discrete,
stateless, and reusable capabilities. Use sub-agents to manage complex,
stateful, and context-dependent processes." An `AgentTool` runs in an isolated
context and cannot see the caller's history; a `chat` sub-agent inherits the
conversation. Google's financial-advisor sample is a coordinator with four
`AgentTool`s only; its data-science sample wraps `AgentTool(...).run_async`
in plain functions that stash the output in state. Built-in tools (Google
Search, code execution) that cannot share an agent with other tools are
isolated the same way (`AgentTool(search_agent)` in the software-bug-assistant
sample; see [tool count](tool-count-and-toolsets.md)).

1. **Does the user need to talk to the specialist?** Yes, for several turns:
   `chat` sub-agent (transfer). Only for clarification: `task`. No:
   `single_turn` or `AgentTool`.
2. **Should the result come back to the parent as data?** `single_turn` and
   `AgentTool` return a tool result the parent reasons over; `task` returns
   through `finish_task`; `chat` returns nothing structured.
3. **Does the parent need a typed input?** Set `input_schema` on the
   sub-agent; the tool parameters come from it. Otherwise the model fills one
   `request` string, so the description must say what to put in it.
4. **Does the parent need to run several specialists in parallel?** Only
   `single_turn` sub-agents are documented as parallel-capable (ADK
   collaboration doc, Table 1). Their tools must therefore be side-effect-safe
   when called together.
5. **Should the parent summarise the result?** `AgentTool(skip_summarization=True)`
   sets `tool_context.actions.skip_summarization`, so the sub-agent's text is
   returned to the user without another parent model call. Use it when the
   sub-agent's output is already final (a drafted reply, a formatted table) and
   a paraphrase would lose precision or cost a model call. Keep it `False` when
   the parent must combine several results. Historically `skip_summarization`
   on an `AgentTool` ended the turn with no text (adk-python #3881, fixed
   2.4.0; the text append was scoped to `AgentTool` in 2.7.0, #6230); assert
   the user-visible text in a test on the pinned version.

## Write the sub-agent as a tool

For `single_turn`, `task` and `AgentTool`, write `description` with the same
discipline as a docstring: what it does, when to route there, what to put in
`request`, what comes back. Example for a `single_turn` sub-agent:

```python
policy_checker = LlmAgent(
    name="policy_checker",
    mode="single_turn",
    description=(
        "Check whether a proposed refund complies with the refund policy and return "
        "a verdict with the policy clause. Use before promising any refund. Put the "
        "order_id, the amount and the customer's reason in the request. Returns "
        "status, allowed (true/false), clause and a one-sentence explanation."
    ),
    instruction=...,
    output_schema=PolicyVerdict,
)
```

The `output_schema` (owned by `adk-model-and-output-contracts`) makes the tool
result a validated object instead of free text; for `AgentTool` the result is
validated with `validate_schema`, and for `single_turn` the structured output is
preserved (2.11.0 CHANGELOG "preserve single-turn structured output" fixed a
regression; verify on the pinned version).

For `chat` sub-agents, the description is rendered into the transfer
instruction:

```
Agent name: billing
Agent description: Answers questions about invoices, refunds and payment methods...
```

followed by "If another agent is better for answering the question according
to its description, call `transfer_to_agent`". The parent's own description
is also used ("If you are the best to answer the question according to your
description, you can answer it"), so write the root agent's description too.

## Prompt injection through relayed output

Sub-agent output returned as a tool result is model-generated text entering the
parent's context. 2.8.0 fences relayed agent output "so it cannot pose as
instructions". Still design the interface so the parent treats it as data:
return structured fields (an `output_schema`) rather than prose where the parent
must act on it, and keep policy decisions in code.

## Observable checks

- Dump the parent's declarations in a test (`LlmRequest` built through the
  flow, or `tool._get_declaration()` for an `AgentTool`) and assert each
  sub-agent appears exactly once with the intended name, description and
  parameters.
- Scripted-model Runner test: the scripted parent emits the sub-agent tool call
  (or `transfer_to_agent`) for a representative prompt; assert the sub-agent
  ran, the result shape, and that `skip_summarization` produced (or did not
  produce) a second parent model call.
- Count sub-agent declarations in the tool budget
  ([tool count](tool-count-and-toolsets.md)).
- Hand routing accuracy over a case set to `adk-agent-evaluation`.
