# Topology: one agent, in-process sub-agents, or a remote A2A agent

Read this for mode (d). The decision is about ownership, context and failure
isolation, not about protocol enthusiasm. In-process orchestration patterns
(sequential, parallel, loop, graph, dynamic) are `adk-workflow-design`'s;
this page decides whether the boundary is a function call, a sub-agent or a
network hop.

## Default order

1. **One agent with tools.** Start here. A single context holds every
   decision and its reasons; there is nothing to lose in a handoff.
2. **Code around the model.** When the split is a known sequence or a fan-out
   of independent work, use `SequentialAgent`, `ParallelAgent`, `Workflow` or
   plain Python (`adk-workflow-design`). Sub-agents share the process, the
   pins, the identity and the session store.
3. **`AgentTool` or sub-agent for context isolation.** When raw tool output or
   a long trial-and-error loop would crowd the parent's context, or when a
   step needs a different model or instruction set.
4. **Remote A2A agent.** Only when the peer is a separate service, owned by
   another team or organisation, written in another language or framework,
   or when a formal contract between components is itself the requirement.

## Vendor criteria (documented behaviour)

The ADK A2A introduction (`docs/a2a/intro.md`) says to use A2A when the
agent is a separate standalone service, is maintained by a different team or
organisation, is written in a different language or framework, or when you
want a strong formal contract; and to prefer local sub-agents for internal
code organisation, performance-critical tightly coupled operations, shared
memory or context, and simple helpers. The A2A project's "A2A and MCP" topic
frames MCP as the agent-to-tool protocol and A2A as agent-to-agent, with an
agent able to be both an MCP client and an A2A participant (a2a-protocol.org,
read 2026-10-08). The Google Cloud blog of 2025-11-08 on sub-agents versus
agents-as-tools (vendor guidance, supplied by research) adds: a sub-agent
transfer hands the conversation over; an agent-as-tool returns a result and
keeps the parent in control. Choose the transfer only when the user should
now be talking to the specialist.

## Independent evidence on multi-agent systems

| Finding | Source | Use it to |
| --- | --- | --- |
| Multi-agent research paid off for parallelisable, breadth-first work that exceeds one context window; subagents with isolated windows returned condensed results; the system used about 15 times the tokens of a chat interaction | Anthropic engineering, "How we built our multi-agent research system", 2025-06-13 (vendor-measured, supplied by research) | Justify a split by context size and parallelism, and budget tokens for it |
| Default to a single thread; when splitting, share full traces because actions carry implicit decisions, and parallel agents that cannot see each other's decisions produce inconsistent results | Cognition, "Don't build multi-agents", 2025-06-12 (practitioner analysis, supplied by research) | Put decisions and omissions in the handoff contract, not only results |
| MAST taxonomy: 14 failure modes across specification and system design, inter-agent misalignment, and task verification; inter-annotator agreement κ = 0.88 across 1,600+ traces | Cemri et al., arXiv 2503.13657, 2025 (independent evidence, supplied by research) | Review each boundary against the three categories ([evaluation-across-boundaries](evaluation-across-boundaries.md)) |
| Remote agent card descriptions, tool descriptions and task messages are attacker-reachable text; ADK 2.8.0 fences relayed agent output but relays card descriptions unmodified | `adk-agent-security` compatibility table (source-verified) | Count a remote peer as an untrusted content source in the trifecta check |

Treat the Anthropic and Cognition pieces as two vendors describing their
products' sweet spots; the agreement between them is on the mechanism
(context is the constraint; handoffs lose decisions), not on a universal
rule.

## The decision table

| Question | In-process (`sub_agents`, `AgentTool`, workflow) | Remote A2A |
| --- | --- | --- |
| Who owns the code, pins and deploy cadence? | You, in one repository | Another team, service or framework |
| Does the step need the parent's session state or memory directly? | Yes: `tool_context.state`, `output_key`, artifacts | No: only what you put in the message (and `a2a_metadata`) |
| Is the step's identity the same principal? | Yes | Usually a different principal with its own card-declared auth |
| Latency and failure budget | Function-call latency; failures are exceptions you handle in process | Network, timeouts, task states, partial streams; failures are error events |
| Contract enforcement | Pydantic schemas, tests in one suite | Agent card, task states, versioned protocol; tests need a fake peer |
| Context cost | Raw results unless isolated with `AgentTool` | Final text and task messages only |
| Observability | One trace | Two traces joined by W3C headers if both sides propagate them |

If every answer sits in the left column, a remote agent adds cost without
isolation. If any answer sits in the right column for ownership or identity,
a remote boundary is the honest shape even when both sides use ADK.

## Writing the boundary contract

Before wiring a remote peer, fill one row per boundary (the in-process
equivalent is `adk-workflow-design`'s contract table):

```text
boundary: parent -> catalog_agent (A2A) | in: user question + sku list (text) | out: text answer, a2a:task_id
identity: parent service account -> card securitySchemes bearer (audience catalog) | timeout: 45s (SLA p99 20s)
failure: error event -> parent answers "catalog unavailable", no retry | pause: input-required -> relayed to user only
coverage: peer states which SKUs it could not find | evidence: fake-peer tests + 1 live exchange on 2026-10-08
```

The `coverage` column matters more across a network than in process: the
peer's omissions do not travel unless its contract says they must.

## Mixed shapes that work

- An ADK agent consuming MCP tools **and** exposed via `to_a2a`: the MCP
  boundary stays inside your service; the card advertises capability, not
  the MCP servers behind it.
- An `AgentTool` wrapping a `RemoteA2aAgent`: keeps the parent in control
  while the remote work happens, and isolates the remote text from the
  parent's history. Confirm on your version that the long-running pause
  still reaches the user through the wrapper.
- Several remote peers under a `ParallelAgent` or `Workflow` with a
  `JoinNode`: `RemoteA2aAgent._run_impl` promotes the first terminal text to
  `event.output` so the join sees it (source-verified 2.8.0).

## Shapes to question

- A remote agent whose only job is to call one API: that is a tool.
- Two agents in one repository talking over A2A to "keep them decoupled":
  the pins, identity and deploy are still shared; use sub-agents and a
  contract table.
- An Agent Runtime root agent delegating to remote A2A sub-agents returned
  HTTP 400 in a community report (discuss.google.dev 303219, Dec 2025,
  unresolved at research time); test the hosted combination before
  committing to it.
