# Descriptions are the routing contract

Read this when a coordinator routes to the wrong sub-agent, never delegates,
or delegates too eagerly, and when adding a sub-agent. Orchestration shape
(sequential, parallel, loop, graph) belongs to adk-workflow-design; this
reference covers what the model reads when it decides to transfer.

## What the model actually receives

In chat mode, the framework appends this text to the parent's system
instruction for every request (`flows/llm_flows/agent_transfer.py`, 2.8.0):

```text
You have a list of other agents to transfer to:

Agent name: billing_agent
Agent description: <the sub-agent's description, verbatim>

If you are the best to answer the question according to your description,
you can answer it.

If another agent is better for answering the question according to its
description, call `transfer_to_agent` function to transfer the question to that
agent. When transferring, do not generate any text other than the function
call.

**NOTE**: the only available agents for `transfer_to_agent` function are ...
```

A parent that may transfer to its own parent also gets "If neither you nor
the other agents are best for the question, transfer to your parent agent".
Targets are the chat-mode sub-agents, the parent (unless
`disallow_transfer_to_parent`) and chat-mode peers (unless
`disallow_transfer_to_peers`). From 2.9.0 the tool accepts a
`transfer_reason` argument, and transfers are restricted to the declared
targets (CHANGELOG 2.9.0, 2.10.0).

Consequences:

- The parent's `description` is also a routing input: the text says "if you
  are the best ... according to your description".
- Every word of a sub-agent `description` is prompt. The ADK docs ask for text
  "specific enough to differentiate it from peers (e.g., 'Handles inquiries
  about current billing statements,' not just 'Billing agent')"
  ([llm-agents](https://adk.dev/agents/llm-agents/), read 2026-10-06, vendor
  guidance). `BaseAgent.description` says "One-line description is enough and
  preferred" (2.8.0 field docstring).
- The coordinator instruction does not need to re-describe the mechanism. It
  invests in decision criteria: the ADK tutorial's best practice is to
  "Mention the sub-agents by name and describe the conditions under which
  delegation should occur" ([agent-team
  tutorial](https://adk.dev/tutorials/agent-team/), read 2026-10-06, vendor
  guidance), and the patterns page says LLM-driven delegation "requires clear
  descriptions on sub-agents and appropriate instruction on Coordinator".

## Write differentiating descriptions

A description answers "which requests are mine and which are not" in one
sentence a sibling could not also claim:

| Weak | Differentiating |
| --- | --- |
| Billing agent | Explains charges on the customer's current and past invoices and handles refund requests for them |
| Support agent | Troubleshoots login, device and connectivity problems after the customer has an active account |
| Handles questions | Answers plan and pricing questions before purchase; hands existing-customer billing to billing_agent |

Rules that the linter checks: at least eight words
(`short_description`), text that is not the name restated
(`description_equals_name`), and pairwise token overlap below 0.6 between
siblings (`similar_sibling_descriptions`). Rules it cannot check: the
description names the boundary with its nearest sibling, and it describes what
the agent does for the user, not how it is built.

Observable check: a routing evaluation set with at least one case per
sub-agent and one ambiguous case per sibling pair, asserting the
`transfer_to_agent` target (adk-agent-evaluation trajectory checks).

## Modes and what each means for the prompt

`LlmAgent.mode` is `'chat' | 'task' | 'single_turn' | None` in 2.8.0; a
sub-agent with `None` is set to `'chat'` by its parent.

| Mode | Runtime behaviour (2.8.0) | Prompt consequences |
| --- | --- | --- |
| `chat` (default) | reachable through `transfer_to_agent`; owns the conversation after transfer until it transfers back | its instruction addresses the end user directly; the parent's description must say when control comes back |
| `task` | wrapped as a tool of the parent (`_TaskAgentTool`); receives no transfer instructions; finishes through the `finish_task` tool; `output_key` on text is skipped; the tool description gets the suffix "Do NOT call this tool in parallel with any other tools" | the instruction describes a delegated task with a defined finish; do not mention `transfer_to_agent` (the linter flags `transfer_mentioned_in_non_chat_mode`); the parent's instruction states what the task returns |
| `single_turn` | exposed as an inline tool (`_SingleTurnAgentTool`); excluded from transfer targets; completes without talking to the user | self-contained instruction: inputs come from the call arguments and state placeholders, and the result goes back to the parent; `input_schema` names the inputs |

`AgentTool` wrapping is the explicit older form of `single_turn`; the 2.8.0
`AgentTool` docstring says direct use "is discouraged" in favour of
`mode='single_turn'` on the sub-agent. Either way the wrapped agent "cannot
access the calling agent's conversation history", so its instruction must be
self-contained, and Google's guidance is to "use tools for discrete,
stateless, and reusable capabilities" and "sub-agents to manage complex,
stateful, and context-dependent processes" (Google Cloud blog, 2025-11-08,
[link](https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools),
vendor guidance). Google's samples phrase the input contract of a tool-reached
sub-agent as "Given inputs ... do not solicit further input" (adk-samples,
read 2026-10-06, vendor sample).

## When the parent must speak last

After a chat-mode transfer the sub-agent owns the turn and the parent does
not summarise (adk-python discussion #3330). When the user-facing answer must
come from the parent, make the child `task` or `single_turn` (or set
`disallow_transfer_to_parent=False` and instruct the child to transfer back
after answering, which is weaker because it depends on the model). Siblings
inside a `LoopAgent` are not transfer targets; use state and `output_key`.

## Damping over-delegation and under-delegation

Over-delegation shows up as transfers for requests the coordinator could
answer, or as spawning several sub-agents for a simple question. Anthropic's
multi-agent research write-up added explicit scaling rules ("simple fact-finding
requires one agent with three to ten tool calls ...") after the lead agent
spawned too many sub-agents (Anthropic, multi-agent research system,
2025-06-13,
[link](https://www.anthropic.com/engineering/multi-agent-research-system),
vendor guidance). In ADK the same damping is a sentence in the coordinator
instruction naming what it answers itself, plus a description on each child
that excludes the coordinator's own cases.

Under-delegation shows up as the coordinator answering billing questions from
general knowledge. Name the trigger condition and the child in the
coordinator's step list ("when the request concerns an existing invoice,
transfer to `billing_agent`"), and check the routing set.

Observable check: transfer counts per case in the evaluation run; the
ambiguous cases route as labelled; the coordinator answers its own cases
without a transfer.

Completion for a routing change: the recorded parent request shows the
rendered agent list with the new descriptions, the routing set passes, and
no sibling pair exceeds the overlap threshold without a written reason.
