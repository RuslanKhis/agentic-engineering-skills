# Structure an instruction around the judgment

Read this when designing a new instruction or reviewing one that has grown. The
skeleton is domain-neutral; adk-agent-evaluation's quality-iteration reference
uses the same shape for its prompt sketch, and this reference explains why each
part exists and how to keep it small.

## The skeleton

```text
ROLE AND TASK (two sentences)
Who the agent is and what one invocation produces.

THE JUDGMENT YOU OWN (one paragraph)
The decision the model makes that nothing else in the system can make, and
the criteria it weighs. This is the part worth the most words.

WHAT YOU RECEIVE (inputs by label)
- each input with its label, its source and whether it is data or a request
- which labelled inputs may be missing and what to do then

HOW TO WORK (numbered steps, only when order matters)
Which tool or sub-agent is used for which situation, and what to do when the
information is missing. Name tools and sub-agents exactly, in backticks.

HOW TO ANSWER (format, length, audience)
Sized to what the model must decide; anything the server fills is not here.

EXEMPLARS (two to five, structurally identical, from other cases)
```

Google's own samples use the same order under the headings Role, Objective,
Instructions or Workflow Steps and Output format, with numbered steps that
name tools and sub-agents in backticks, and an explicit "Given inputs" block for
sub-agents reached as tools ([adk-samples financial-advisor
prompt.py](https://github.com/google/adk-samples/blob/main/contrib/python/financial-advisor/app/prompt.py),
read 2026-10-06, vendor sample). The ADK LLM-agent page lists the same
ingredients: core task, persona, constraints, how and when to use each tool,
output format ([llm-agents](https://adk.dev/agents/llm-agents/), read
2026-10-06, vendor guidance).

## Altitude

Write at the altitude of the judgment, not of the keystrokes. A prompt that
enumerates every edge case is brittle; a prompt that says only "be helpful"
gives no signal. Anthropic's context-engineering note calls this the "right
altitude" and recommends starting from the smallest prompt that works and
adding only for observed failures ([Effective context engineering for AI
agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
2025-09-29, vendor guidance). Google's Gemini 3 guide says the model "may
over-analyze verbose or overly complex prompt engineering techniques used for
older models" and asks for concise, direct instructions
([gemini-3](https://ai.google.dev/gemini-api/docs/gemini-3), updated
2026-09-23, vendor guidance).

Observable check: each sentence either states the judgment, names an input, or
responds to a defect recorded in the error-analysis table. A sentence with no
such owner is removed and the development set re-run.

## Delimiters and order

Pick one delimiter style (Markdown headings, XML-style tags, or upper-case
labels) and use it for every section. Keep the order fixed across agents in a
project so reviewers can diff prompts. All three major vendors recommend
explicit section structure and consistent delimiters (OpenAI GPT-4.1 prompting
guide, 2025-04, [cookbook](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide);
Google [prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies),
updated 2026-09-17; Anthropic [prompting best
practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices);
all vendor guidance). The ADK docs recommend Markdown for readability of
complex instructions (vendor guidance).

Observable check: the contract test in [prompt as code](prompt-as-code.md)
asserts the section headings appear once each, in order.

## Positive phrasing with a reason

State the wanted behaviour and why. "Quote the policy number you relied on so
the reviewer can check it" carries more than "Do not make up policy numbers".
Keep a prohibition only when no positive phrasing exists, and pair it with the
target behaviour. Anthropic recommends positive instructions and explaining
the reason (vendor guidance, no published effect size); the ADK tutorial's
"Your ONLY task is ... Do nothing else" pattern is a legitimate narrowing for
a tightly scoped sub-agent, not a template for every sentence
([agent-team tutorial](https://adk.dev/tutorials/agent-team/), read
2026-10-06, vendor guidance).

Observable check: the linter's `prohibition_only_sentences` count falls and
the targeted defect category does not grow.

## Contradiction review

Read the prompt once as the model will: a rule that says "always look up the
profile first" and another that says "escalate immediately when urgent" is a
contradiction until one names its precedence. OpenAI's GPT-5 guide reports
that the model "expends reasoning tokens searching for a way to reconcile the
contradictions rather than picking one instruction at random"
([GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide),
2025-08, vendor guidance). Resolve by deleting one rule or stating the
exception inside the rule it overrides.

Shouting modifiers ("CRITICAL", "MUST", "NEVER") were a workaround for older
models; current vendor guides ask for plain reasons and warn that
over-emphasis can over-trigger the behaviour (OpenAI GPT-4.1 guide, Anthropic
best practices, vendor guidance). Replace each with the reason it was
shouting about.

Observable check: the linter's `possible_contradiction` findings are each
resolved or recorded as intentional with the precedence written into the
prompt, and `shouting_modifier_density` is below one per hundred words.

## Long inputs

Where a long document goes relative to the question is model specific and the
vendors disagree: Anthropic places documents at the top and the query after;
the Gemini 3 guide places context first and the question last; OpenAI suggests
instructions at both ends for very long contexts (all vendor guidance, read
2026-10-06). Check the current guide for the pinned model and measure on the
development set rather than carrying a rule across generations.

## The thousand-word restart

A prompt that has grown past a thousand words of constraints is a signal to
restart from the skeleton: list every constraint, move each into code, a
schema, a tool, a callback or an exemplar ([instruction versus
code](instruction-vs-code.md)), and keep only the judgment. The linter's
`--max-words` budget defaults to this threshold. Memory and context files
loaded into the prompt follow the same rule: Google's long-horizon harness
loads one project-context file rather than several because several "inflates
the prefix by ~3x and gives conflicting directives", and writes memories as
declarative facts because "imperative phrasing gets re-read as a directive
later" (adk-samples long-horizon-harness AGENTS.md, read 2026-10-06, vendor
sample).

Completion for a structure change: the rendered prompt has the sections above
in order, no sentence without an owner, no unresolved contradiction, and the
evaluation run through adk-agent-evaluation shows the targeted category
shrinking with no other category growing.
