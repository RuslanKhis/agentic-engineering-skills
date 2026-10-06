# Guide tool use from the instruction

Read this when an agent calls a tool it should not, fails to call one it
should, invents arguments, or loops on the same call. Tool docstrings,
parameter names and schemas belong to adk-tool-interface-design; this
reference covers the instruction's side of the contract.

## Check the mechanism before the prose

1. **What the model sees.** In 2.8.0 a `FunctionTool`'s description is the
   function docstring (`inspect.cleandoc(func.__doc__)`), and parameter
   descriptions are not derived from the docstring
   (`_automatic_function_calling_util.py`: "Do not support parameter
   description for now"). So "when and why" guidance lives in the docstring
   body and in the instruction, and parameter meaning lives in the parameter
   names and types.
2. **The tool mix.** Built-in search tools and function calling have
   combination limits, and a built-in retrieval tool was the actual cause of
   "flaky routing" in adk-python issue #2686 (2025-08). Read the tools
   limitations page for the pinned version before rewriting prose.
3. **The declared names.** Most tool failures in practice are invalid tool
   names and wrong parameters rather than wrong intent (Chip Huyen, Agents,
   2025-01-07, [link](https://huyenchip.com/2025/01/07/agents.html),
   practitioner). The linter's `unknown_tool_reference` and
   `tool_never_mentioned` findings compare the prose with `tools=`.
4. **The recorded request.** Confirm the tool declarations and the
   instruction both arrived (`llm_request.tools_dict`,
   `config.system_instruction`) before concluding the model ignored them.

## Tools in the tools field, reasons in the prompt

Declare tools only through `LlmAgent.tools`; the framework rejects
`generate_content_config.tools`. In the instruction, for each tool, state the
situation that calls for it, the information the model needs before calling,
and what to do when that information is missing. The ADK docs put it as
"Don't just list tools; explain when and why the agent should use them",
"supplementing any descriptions within the tool itself"
([llm-agents](https://adk.dev/agents/llm-agents/), read 2026-10-06, vendor
guidance). OpenAI reports a small accuracy gain from passing tools in the
API's tools field rather than describing them in prose, and recommends
keeping usage examples in a dedicated prompt section (GPT-4.1 prompting
guide, 2025-04, vendor guidance).

```text
HOW TO WORK
1. When the customer gives an order number, call `lookup_order` with that
   number and base the status answer on its result.
2. When they ask about a refund, read the order first; offer `issue_refund`
   only for orders the lookup marks refundable, and confirm the amount with
   the customer before calling it.
3. When the order number is missing or malformed, ask for it. Answer from
   general policy only when no order is involved.
```

Observable check: an evaluation case per situation (number given, number
missing, refund on a non-refundable order) with the expected tool trajectory,
run through adk-agent-evaluation.

## Calibrate eagerness instead of mandating calls

"You must call a tool before responding" produces calls with invented
arguments when the required information is absent; the GPT-4.1 guide reports
this failure and recommends adding that the model should ask the user when it
lacks the information (vendor guidance). Google lists the dimensions worth
steering explicitly: logical decomposition, problem diagnosis, information
exhaustiveness, adaptability, persistence and recovery, risk assessment that
"explicitly distinguishes between low-risk exploratory actions (reads) and
high-risk state changes (writes)", ambiguity and permission handling, and
verbosity ([prompting strategies, Agentic
workflows](https://ai.google.dev/gemini-api/docs/prompting-strategies),
updated 2026-09-17, vendor guidance). OpenAI's GPT-5 guide frames the same
knob as eagerness, with explicit tool-call budgets and "proceed under
uncertainty" or "stop and ask" clauses depending on the task (2025-08, vendor
guidance).

Write the calibration as conditions, not emphasis:

| Observed failure | Prompt-side change | Code-side partner |
| --- | --- | --- |
| Hallucinated arguments | "When the order number is missing, ask for it" replaces "always call lookup first" | tool validates inputs and returns a structured error |
| Under-triggering (answers from memory) | name the situation that requires the lookup and say the answer must come from the result | evaluation case with expected trajectory |
| Over-triggering (calls on every turn) | state when the information already in the conversation suffices | repeated-call guard (adk-operational-guardrails) |
| Loops on failure | "After one failed lookup, report the failure and ask"; a budget of attempts | invocation limits and tool retries in code (safe-api-tool-calls) |
| Shouted rules | plain condition with the reason | none needed |

Observable check: the linter's `mandatory_tool_call_phrasing` finding is
empty and the trajectory cases above pass.

## Reads, writes and parallel calls

Say which tools read and which change state, and that state-changing tools
are called once, after the inputs are confirmed. Confirmation and
authorisation are enforced in code (`require_confirmation`, callbacks); the
prompt's job is to make the model gather and restate the inputs first.
The framework appends "Do NOT call this tool in parallel with any other
tools" to a task-mode sub-agent's tool description (`agent_tool.py`, 2.8.0);
for ordinary tools with side effects, state the sequencing in the
instruction and enforce it in code.

## Planning in words, binding in code

For multi-step work, let the model plan in natural language ("find the order,
check refundability, then refund") and bind each step to the exact tool in
the step list, so a renamed tool breaks a test rather than the plan (Huyen,
practitioner). Keep exact names in backticks so the linter can cross-check
them.

Completion for a tool-use change: the recorded request shows the declarations
and the prose agree, the trajectory cases pass, and the error-analysis table
shows the targeted category (wrong tool, missing call, bad arguments)
shrinking with no other category growing.
