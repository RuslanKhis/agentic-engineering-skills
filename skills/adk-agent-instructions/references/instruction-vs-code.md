# Code, schema or tool before prose

Read this when a prompt has grown constraints, when a rule must hold every
time, or when deciding where a new requirement lives. The rule: anything the
application already knows or must guarantee stays out of the prompt. The
prompt carries the judgment the model alone can make.

## Decision table

| Requirement | Where it lives | Why not the prompt | Observable check |
| --- | --- | --- | --- |
| Who may perform an action (authorisation) | code: the tool checks the authenticated principal; `require_confirmation` or a callback gates execution | the model cannot authenticate anyone; a prompt rule is advisory | a test calls the tool as an unauthorised user and the side effect does not run |
| Spending, call and loop budgets | code: `RunConfig` limits, plugins, operational guardrails | the model has no reliable counter; budgets must hold under adversarial input | a test exceeds the budget and the run stops with a recorded reason |
| Idempotency and retries | code: replay keys, retry policy in the tool (safe-api-tool-calls) | the model does not know whether a lost response committed | a lost-response test produces one side effect |
| Output shape | `output_schema` (adk-model-and-output-contracts) | prose formats drift; a schema fails loudly | schema validation in the evaluation run |
| Field the server can fill (IDs, offsets, counts, timestamps) | code fills it after the model answers | copying is error-prone and costs tokens | the schema has no such field; the server test fills it |
| Which tools exist and their parameters | `tools=` and the docstring (adk-tool-interface-design) | the declaration is what the API receives; prose duplicates and drifts | `tool_never_mentioned` and `unknown_tool_reference` are empty |
| When and why a tool is used | prompt, as conditions | this is a judgment about the situation | trajectory cases per situation |
| Which sub-agent handles what | sub-agent `description` plus coordinator conditions | the framework renders descriptions into the transfer instruction | routing set passes |
| Session facts (plan, locale, open tickets) | state written by code, read with `{key}` or a provider | prose values go stale; state is current per request | contract test renders fixture state |
| Documents and tool results | labelled inputs marked as data, delimited (adk-workflow-design content safeguards) | instructions in data are injection | hostile-document fixture leaves the decision unchanged |
| Secrets and internal URLs | never in the prompt; code resolves them | system instructions do not fully prevent leaks (Google system-instruction introduction, updated 2026-10-01, vendor guidance) | a scan of recorded requests finds none |
| The decision itself and its criteria | prompt | this is the work | error-analysis categories |
| Tone, audience, length | prompt, one sentence each | cheap to state, hard to encode | rubric-based response quality in the evaluation |

## Two worked examples

**Authorisation.** A prompt said "Only refund orders for the authenticated
customer." The model complied until a pasted email contained another
customer's order number. The fix removed the sentence and made
`issue_refund` look up the order owner and compare it with the session's
authenticated user id, returning a structured refusal otherwise. The prompt
now says "offer a refund only for orders the lookup marks refundable", which
is a judgment the model can make from data it holds.

**Budget.** A prompt said "Never call the search tool more than three times."
Under a hostile document the model called it eleven times. The fix moved the
cap into a repeated-tool guard (adk-operational-guardrails) and kept one
sentence in the prompt: "After a failed search, report what you could not
find and ask the user", which gives the model a graceful path when the guard
fires.

## Moving a constraint out of the prompt

1. Name the constraint and whether it must hold every time (code) or usually
   (prompt).
2. Find the enforcement point: tool, callback, schema, plugin, state.
3. Write the test that shows the enforcement holds without the prompt
   sentence.
4. Delete the sentence, or replace it with the graceful-path sentence.
5. Re-run the development set; the category the sentence protected must not
   grow.

Completion: every sentence left in the prompt is a judgment, an input label,
a format rule or a graceful path; every guarantee has a test that does not
depend on the model.
