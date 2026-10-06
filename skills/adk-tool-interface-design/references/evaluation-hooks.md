# Evaluation hooks for tool interfaces

This skill changes names, docstrings, schemas, results and delegation shapes.
Each change needs a before/after observation, and the durable measurement of
selection and parameter accuracy over a case set belongs to
`adk-agent-evaluation`. This reference says what to measure, how to produce the
cheap observations here, and what to hand over.

## What to measure

Final-answer correctness hides interface problems: a model can reach the right
answer after three wrong tool calls. Measure the trajectory (V, Anthropic; E,
BFCL for metric design):

| Metric | Definition | Where it is produced |
| --- | --- | --- |
| Tool selection accuracy | Share of cases where the first tool called is the expected tool (or no tool when none is expected) | `adk-agent-evaluation` case set; cheap proxy here with a scripted model for wiring only |
| Parameter correctness | Share of calls whose arguments match the expected values after normalisation (identifier format, enum value, defaults left unset) | Same |
| Calls per task | Number of tool calls to completion; repeated identical calls counted separately | `report_tool_result_sizes.py` on recorded events |
| Result tokens per task | Serialised bytes of all tool responses, bytes/4 as a token estimate | Same |
| Declaration tokens per request | Serialised bytes of all declarations the agent sends | Declaration dump ([tool count](tool-count-and-toolsets.md)) |
| Error recovery | After an `error` result, share of cases where the next action matches the hint (ask, stop, alternative tool) rather than a repeat | Case set with injected errors |
| Routing accuracy | For delegation, share of cases routed to the intended sub-agent | Case set |

The KAMI study (E, single study, arXiv 2512.07497) names three failure modes
worth labelling in error analysis: **premature action** (calling a write before
the required read or confirmation), **over-helpful substitution** (calling a
different tool when the right one is unavailable or errored) and **context
pollution** (earlier large results degrading later decisions). Each maps to an
interface fix: docstring ordering guidance, an explicit "do not substitute"
caveat plus an actionable error, and result-size bounds.

## Cheap observations produced here

1. **Declaration dump** before and after: name, description length,
   properties, `required`, enum values, bytes. Save the JSON next to the
   change so the reviewer sees the exact text the model will read.
2. **Scripted-model Runner test**: a model double that returns a fixed
   `function_call` for the prompt, asserting the tool ran with the expected
   arguments and that the result reached the next model request. This proves
   wiring and result shape, not model choice. See [validation](validation.md)
   for the test shape.
3. **Result-size report** on a recorded session (`adk web` session export or
   events captured in a test): per tool count, bytes, p95, repeated identical
   responses, over-limit flags.
4. **Linter report**: counts per finding type, used as a regression gate (no
   new `missing_docstring`, `non_dict_return`, `exclusive_boolean_pair`).

## Hand-off to adk-agent-evaluation

Provide, in the completion report:

- The list of tools and sub-agents whose interface changed, with the before
  and after declaration dumps.
- Five to twenty representative prompts per changed tool, each with the
  expected tool and arguments, plus near-miss prompts where the tool must not
  be chosen (the sibling tool, or no tool). Include at least one prompt per
  documented error branch with the expected next action.
- The budget to beat: current calls per task, result tokens per task,
  declaration tokens per request.
- Which observations were **offline simulated** (scripted model), **live
  verified** (real model, approved run) and **not run**.

`adk-agent-evaluation` turns these into a labelled set, runs the real model
within an approved budget, and reports selection and parameter accuracy with
error analysis. Do not report a scripted-model pass as evidence that the model
will choose the tool.
