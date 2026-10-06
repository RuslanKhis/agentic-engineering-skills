# Prompt-side notes per model generation

Read this when moving an agent to a new model generation or when a prompt
written for an older model behaves oddly on a newer one. Every note is dated
and sourced; all of it is vendor guidance unless marked otherwise, and all of
it is re-checked on the target's own evaluation set before it is kept.
Configuration mechanics (temperature, `thinking_level`, `thinking_budget`,
safety settings) belong to adk-model-and-output-contracts; this reference
covers what changes in the prompt text.

## Gemini 3 (guide updated 2026-09-23)

Source: [ai.google.dev/gemini-api/docs/gemini-3](https://ai.google.dev/gemini-api/docs/gemini-3),
read 2026-10-06, vendor guidance; practitioner summary by Phil Schmid,
2025-11-19, [link](https://www.philschmid.de/gemini-3-prompt-practices).

| Prompt-side consequence | Source wording | Re-check |
| --- | --- | --- |
| Remove chain-of-thought scaffolding written for 2.5 | "If you were previously using complex prompt engineering (like chain of thought) to force Gemini 2.5 to reason, try Gemini 3 with thinking_level: 'high' and simplified prompts" | category counts before and after removal |
| Shorten and simplify | "Be concise in your input prompts ... It may over-analyze verbose or overly complex prompt engineering techniques used for older models" | word count and the targeted category |
| Ask for the persona you want; the default is terse | "By default, Gemini 3 is less verbose and prefers providing direct, efficient answers ... you must explicitly steer the model in the prompt" | rubric-based response quality |
| Long context: data first, question last | "place your specific instructions or questions at the end of the prompt, after the data context" | long-input cases |
| Remove repeated 2.x-era constraints and shouting | Schmid (practitioner) and the guide's concision advice | `shouting_modifier_density`, contradiction findings |
| Temperature stays at the default | "we strongly recommend keeping the temperature parameter at its default value of 1.0 ... setting it below 1.0 may lead to unexpected behavior, such as looping or degraded performance" | this is configuration; hand it to adk-model-and-output-contracts and note that prompt rewrites cannot fix a looping caused by temperature |

## Gemini 2.5 and earlier

Older guides favoured explicit step-by-step scaffolding and strong emphasis.
Prompts inherited from that era commonly carry repeated constraints and
"think step by step" instructions. Keep them only when the development set
shows a loss without them on the pinned model.

## OpenAI models reached through LiteLLM

The GPT-4.1 guide (2025-04) describes close literal instruction following:
dial back shouting, never mandate a tool call, place instructions at both ends
of very long contexts. The GPT-5 guide (2025-08) adds that contradictory
instructions cost reasoning tokens and recommends explicit eagerness
settings ([link](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)).
Both vendor guidance. ADK's OpenAI path serialises non-string system
instructions from 2.10.0 (CHANGELOG); check the pinned version when
`static_instruction` is a `Content`.

## Anthropic models reached through LiteLLM

Anthropic's best-practices page recommends explaining the reason behind an
instruction, positive phrasing, three to five examples, XML-style delimiters
and documents before the query
([link](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices),
read 2026-10-06, vendor guidance). ADK passes no system instruction when the
instruction is empty (CHANGELOG, Anthropic `NOT_GIVEN` fix).

## Migration procedure

1. Freeze the development set and record the baseline category counts on the
   old model with the old prompt.
2. Run the old prompt on the new model unchanged. Many migrations stop here.
3. Apply the generation notes above one change at a time (remove scaffolding;
   shorten; restate persona), re-running after each.
4. Hand configuration changes to adk-model-and-output-contracts and run them
   as separate iterations.
5. Record model, prompt version, exemplar IDs and settings with every run.

Completion: the migration record shows which notes were applied, which were
reverted, and the final category counts against the baseline. A note that
was not re-checked is listed as unverified.
