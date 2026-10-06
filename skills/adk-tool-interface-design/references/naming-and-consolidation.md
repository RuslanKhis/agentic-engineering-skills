# Naming, descriptions and consolidation

Use this reference when writing a new tool, renaming one, or deciding whether
two tools should become one. Sources are labelled **V** (vendor guidance),
**D** (documented product behaviour) or **E** (independent evidence); see
[sources](sources.md) for dates and URLs.

## The description is the dominant lever

Anthropic's "Writing effective tools for agents" (V, 2025-09-11) reports that
rewriting descriptions produced the largest gains in its internal evaluations
and recommends writing them as if onboarding a new hire: make implicit context
explicit (identifier formats, how resources relate, what the tool returns, when
not to use it). The Claude define-tools guide (V) asks for three to four
sentences at minimum covering what the tool does, when to use it, what each
parameter means and any caveats. OpenAI's function-calling guide (V) applies an
"intern test": if a person seeing only the name, description and parameters
could not use the tool correctly, the model cannot either.

On ADK 2.8.0 the docstring is the entire description and parameters carry no
description of their own ([contract](function-tool-contract.md)). Follow the
ADK docs' own template (tools overview, `lookup_order_status`): purpose, "Use
this tool ONLY when ...", an `Args:` entry per visible parameter, and a
`Returns:` section that enumerates the `status` values with literal example
dicts. Leave the injected `ToolContext` out of the docstring.

```python
def lookup_order(order_id: str, include_items: bool = False, tool_context: ToolContext = None) -> dict:
    """Fetch the current status and shipping dates for one customer order.

    Use this tool ONLY when the customer has given a specific order number and
    asks about that order. For a list of a customer's orders use
    list_customer_orders instead.

    Args:
        order_id: The order number as printed on the receipt, in the form
            "ORD-123456" (three letters, hyphen, six digits).
        include_items: Set to True only when the customer asks about specific
            products; the item list can be long.

    Returns:
        On success, status is "success" and includes an "order" dictionary.
        On failure, status is "error" and includes "error_message" and "hint".
        Example success: {"status": "success", "order": {"state": "shipped", "ship_date": "2026-10-09"}}
        Example error: {"status": "error", "error_message": "Order ID not found.", "hint": "Confirm the number with the customer."}
    """
```

Google's own samples (adk-samples customer-service agent, read 2026-10-06 from
the last commit before its removal) follow this shape with twelve flat tools,
every return `{"status": ..., "message": ...}`, and business-rule rejections
such as `{"status": "rejected", "message": "discount too large. Must be 10 or
less."}` commented "Send back a reason for the error so that the model can
recover".

Keep the first sentence self-contained: `LongRunningFunctionTool` appends its
own note after the docstring, and some tool browsers show only the first line.

## Names

- Use `verb_noun` in `snake_case` (`get_weather`, `schedule_meeting`); the
  model sees exactly the Python name and, per the ADK tools overview, "uses the
  function name as a primary identifier during tool selection". Avoid `run`,
  `process`, `handle_data`, `do_stuff`.
- Namespace by service or resource when an agent touches several systems:
  `github_list_prs`, `jira_create_issue`. Vendor guidance (V, Anthropic and
  OpenAI) agrees that prefixing reduces wrong-service selection; ADK supplies
  `tool_name_prefix` on toolsets for the same purpose.
- Make sibling names distinguish along the axis the model must decide:
  `search_products` versus `get_product_by_sku`, not `search_products` versus
  `search_products_v2`. The linter flags names whose token sets overlap above
  0.6 Jaccard.
- Never reuse a name within one agent; ADK logs a shadowing warning and the
  call lands on the survivor.

## Parameters

- Names must read as labels: `user_id` not `user`, `departure_date_iso` not
  `date`, `max_results` not `n`. Generic names (`data`, `value`, `input`, `id`,
  `obj`, `param`, `arg`) are flagged because they force the model to guess.
- Fewer parameters are better and primitives (`str`, `int`, `bool`, `Enum`)
  beat custom classes (D, ADK function-tools doc; V, both vendors).
- Make invalid states unrepresentable: one `Enum` parameter instead of two
  booleans (`format: Literal["concise", "detailed"]` instead of
  `concise: bool, detailed: bool`). The linter flags `enable_x`/`disable_x`,
  `on`/`off`, `include_x`/`exclude_x` pairs.
- Never ask the model for a value the code already knows: the authenticated
  user, the tenant, the session, today's date, API keys. Read them from
  `ToolContext` or configuration. A model-supplied `user_id` is never
  authority; `adk-tool-auth-and-secrets` owns that boundary. The linter marks
  `identity_parameter_review` so you check each one.
- Put examples of format-sensitive inputs in the docstring (V): date formats,
  identifier shapes, query syntax, units and currency.
- Give optional parameters defaults that are safe when the model omits them
  (small page sizes, concise format, no destructive flags).

## Consolidate or split

Consolidate when the model would always call two tools in sequence or has to
choose between near-identical siblings. Vendor guidance (V, consistent across
Anthropic and OpenAI) recommends one capable tool such as `schedule_event`
(check availability and create) or `get_customer_context` (profile, recent
orders, open tickets) over several thin wrappers around API endpoints. Each
extra tool costs declaration tokens on every request and one more decision.

Split when:

- the operations have different risk (a read and a destructive write), so that
  confirmation, budgets and auditing attach to the right one;
- the result shapes differ enough that one docstring cannot describe both;
- the parameters would become a union with mutually exclusive branches.

A tool that takes an `action: Enum` plus a bag of optional parameters is a
smell when most parameters apply to one action only; prefer separate tools
with tight schemas. The ADK tools overview gives the same advice from the
other side: decompose `update_user_profile(profile: ProfileObject)` into
`update_user_name(name: str)`, `update_user_address(address: str)` and so on,
because a flat primitive schema is easier to select and fill than a nested
object. Pass data between tools through `temp:` state keys rather than making
the model relay it.

The Gemini function-calling doc (D) adds that generic low-level tools (a shell)
are used more often but less accurately than specific high-level tools; prefer
the specific tool when accuracy matters.

## Parallel calls

Gemini may emit several function calls in one turn when it judges them
independent (D, Gemini function-calling doc). ADK runs them concurrently only
when the tools are `async def`; a synchronous tool blocks the others (ADK
performance doc). Write I/O tools as `async def`, and say in the docstring
when a tool may be called several times in one turn ("call once per city").
Tools that can be selected together must be side-effect-safe when run in
parallel or in any order; if two tools must run in sequence, state the order
in both docstrings and in the agent instruction (`adk-agent-instructions` owns
that text, and should "reference a tool by its function name" and say how to
handle each return value: retry, give up or ask). Compositional (sequential,
dependent) calls are a model behaviour, not a guarantee; do not rely on the
model to serialise writes.

## Checklist before committing a tool

- [ ] First sentence states what it does and what it returns.
- [ ] Says when to use it and names the alternative for the nearby case.
- [ ] Every visible parameter has a self-describing name, a type hint and a
      documented format; no `*args`/`**kwargs`.
- [ ] No parameter asks for identity or secrets the code already knows.
- [ ] Mutually exclusive flags replaced by one enum.
- [ ] Live declaration inspected and its size recorded.
- [ ] Scripted-model test asserts the tool and arguments the model should
      produce for one representative prompt ([validation](validation.md)).
