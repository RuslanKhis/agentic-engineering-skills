# When is an LLM agent the right tool?

Primary-source review, 15 October 2026, for the `adk-discovery` skill. Vendor
guides change; each source carries the date it was read. This is a reading of
what the sources say, not a measured comparison of technologies on a workload.

## Conclusion

Google, Anthropic, OpenAI and Microsoft all say the same thing in different
words: start with the simplest mechanism that meets the need and add
probabilistic components only where deterministic ones cannot do the job.
Rules and scripts win when the transformation is known and stable. Classical
ML wins when labelled historical outcomes exist in volume and the output is a
number, class, probability or ranking over structured data; the benchmarks read
here show tree ensembles and fine-tuned small encoders still matching or
beating LLMs on tabular, time-series and pattern-driven text classification. A
single LLM call wins when the input is unstructured language and the output is
a bounded judgment. An agent is justified only when the path cannot be fixed in
advance: step count and order depend on what is found, tools are chosen
dynamically, and the equivalent rules would be unwieldy. A human process change
stays in the triage because the sources require the non-ML baseline to be
optimised first, and because errors users cannot tolerate or review rule out
automation of any kind. The table at the end is our synthesis; it is defensible
as a checklist, not as a proven predictor of project success.

## What the sources actually establish

### 1. Google: try a heuristic before ML

Rules of Machine Learning, Rule #1 "Don't be afraid to launch a product without
machine learning", says "Machine learning is cool, but it requires data" and
gives heuristics that deliver value first (install-rate ranking, known spam
lists, recency). Rule #2 says design and implement metrics first. Rule #3
"Choose machine learning over a complex heuristic" moves to ML once data and
objectives exist, because a learned model is easier to maintain than a
heuristic that has grown complicated. Last updated 2025-08-25.
[Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml),
read 15 October 2026.

Google's problem-framing course adds: "first verify that your current non-ML
solution is optimized", asks "How much better do you think an ML solution can
be?", requires abundant, correct, representative data with predictive
features, and warns "There's no value in predicting something if you can't
turn the prediction into an action."
[Understand the problem](https://developers.google.com/machine-learning/problem-framing/problem),
read 15 October 2026.

These are one organisation's engineering recommendations, not controlled
studies. They establish Google's stated order: heuristic, metrics, then ML.

**Apply here:** the first question for any candidate process is what the
current version achieves and whether it is optimised. Require a measurement
plan before proposing any model.

### 2. Google PAIR: where AI is and is not better

The People + AI Guidebook lists where AI is probably better: personalised
recommendation, prediction, natural language understanding, recognising
classes of entities, rare and evolving patterns such as fraud, and repeated
domain-specific tasks. It lists where AI is probably not better: when
predictability matters, when information is static and standard, when "the
cost of errors outweighs the benefits", when users need complete transparency,
when speed to market matters most, and when "people explicitly tell you they
don't want a task automated."
[PAIR Guidebook, User needs](https://pair.withgoogle.com/chapter/user-needs/),
read 15 October 2026.

This is design guidance and establishes a vocabulary, not an outcome.

**Apply here:** carry the "not better" list as explicit stop conditions.
"Users do not want this automated" is a process answer, not a technology one.

### 3. Google Cloud and ADK: non-agentic first, deterministic orchestration where the path is fixed

The Architecture Center states: "If your workload is predictable or highly
structured, or if it can be executed with a single call to an AI model, it can
be more cost effective to explore non-agentic solutions", citing
summarisation, translation and feedback classification. It recommends a single
agent first, warns that performance "can be less effective when it uses more
tools and when tasks increase in complexity", and recommends sequential or
parallel workflow agents for processes "where the sequence of operations
doesn't change". Last updated 2026-05-28.
[Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system),
read 15 October 2026.

ADK's workflow agents "determine the execution sequence according to their
type, such as sequential, parallel, or loop, without consulting an AI model
for assistance with the orchestration. This approach results in deterministic
and predictable execution patterns." Function tools wrap ordinary Python
functions so an agent can "connect to proprietary databases or implement
unique algorithms".
[ADK workflow agents](https://adk.dev/agents/workflow-agents/),
[ADK function tools](https://adk.dev/tools-custom/function-tools/),
read 15 October 2026.

These establish the framework's stated preference and mechanics, not measured
cost or quality differences.

**Apply here:** a fixed step order means a workflow agent or plain code, never
an LLM orchestrator. Deterministic logic lives in a function tool or around
the agent.

### 4. Anthropic: workflows versus agents, simplest first

"Building effective agents" (19 December 2024) defines workflows as "systems
where LLMs and tools are orchestrated through predefined code paths" and
agents as "systems where LLMs dynamically direct their own processes and tool
usage." It recommends "finding the simplest solution possible, and only
increasing complexity when needed", notes agents "trade latency and cost for
better task performance", and reserves them for "open-ended problems where
it's difficult or impossible to predict the required number of steps, and
where you can't hardcode a fixed path." Often "optimizing single LLM calls
with retrieval and in-context examples is usually enough."
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents),
read 15 October 2026.

Vendor experience, not a benchmark. It gives a precise test for "agent": the
path is unknowable in advance.

**Apply here:** ask "can we write the step list down?" Yes means workflow or
script; "it depends on what each step finds" means agent candidate.

### 5. OpenAI: three criteria, otherwise deterministic may suffice

"A practical guide to building agents" (PDF dated 7 April 2025) names three
triggers: complex decision-making ("nuanced judgment, exceptions, or
context-sensitive decisions, for example refund approval"), difficult-to-
maintain rules ("extensive and intricate rulesets, making updates costly or
error-prone, for example performing vendor security reviews"), and heavy
reliance on unstructured data ("interpreting natural language, extracting
meaning from documents, or interacting with users conversationally"). Then:
"Before committing to building an agent, validate that your use case can meet
these criteria clearly. Otherwise, a deterministic solution may suffice." It
excludes "simple chatbots, single-turn LLMs, or sentiment classifiers" from
the definition of agent and recommends single-agent systems first.
[OpenAI guide (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf),
read 15 October 2026.

Recommendations drawn from customer deployments, not a validated instrument.

**Apply here:** use the three criteria as the gate between a single LLM call
and an agent, and quote the "deterministic solution may suffice" line.

### 6. Microsoft: who decides what happens next?

The Agent Framework "Workflows" page (updated 2026-08-25) draws an
"intelligence spectrum" from "model decides everything" to "code decides
everything", says "most real-world applications live somewhere in the middle",
hinges its decision table on "who should decide what happens next?", and
closes: "The best agent systems use the simplest pattern that meets their
requirements."
[Microsoft Agent Framework: Workflows](https://learn.microsoft.com/agent-framework/journey/workflows),
read 15 October 2026.

**Apply here:** the per-step question "model, code or human?" is a clean,
framework-neutral hybrid design tool.

### 7. Benchmarks: LLMs do not displace classical ML on structured prediction

Grinsztajn, Oyallon and Varoquaux (NeurIPS 2022), on 45 datasets: "tree-based
models remain state-of-the-art on medium-sized data (~10K samples) even
without accounting for their superior speed."
[arXiv 2207.08815](https://arxiv.org/abs/2207.08815), read 15 October 2026.

Tan et al. (NeurIPS 2024 spotlight): removing the LLM from LLM-based
time-series forecasters, or replacing it with a basic attention layer, "does
not degrade forecasting performance" and often improves it; LLMs "do not
assist in few-shot settings."
[arXiv 2406.16964](https://arxiv.org/abs/2406.16964), read 15 October 2026.

Zhang et al. (May 2025), six hard text classification datasets: "BERT-like
models often outperform LLMs"; they "excel in pattern-driven tasks, while LLMs
dominate those requiring deep semantics or world knowledge."
[arXiv 2505.18215](https://arxiv.org/abs/2505.18215), read 15 October 2026.
Vajjala and Shimangaud (February 2025), 32 datasets in 8 languages: zero-shot
LLMs do well for sentiment but "are outperformed by other approaches for the
rest of the tasks" when a full labelled set is available.
[arXiv 2502.11830](https://arxiv.org/abs/2502.11830), read 15 October 2026.

These establish results on the tasks and models tested; they do not prove an
LLM never helps on structured data, and they predate the newest models.

**Apply here:** with labelled outcomes in volume over tabular, series or
pattern-driven text inputs, default to classical ML or a small fine-tuned
model; use an LLM only for the residue needing reading or world knowledge.

### 8. Cost, lifecycle and operations

Gemini API usage is billed per input and output token, with cached-context and
batch discounts; batch is listed at roughly half the standard rate (Gemini 3.8
Flash: $0.75 per million input tokens standard, $0.375 batch, at reading).
[Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing),
read 15 October 2026.

The Vertex AI lifecycle page says stable Gemini models are available for at
least 12 months after release and a posted retirement date gives "at least 45
days to migrate", with a migration guide for mission-critical features.
[Model versions and lifecycle](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions),
read 15 October 2026.

So an LLM component carries a recurring per-call cost and a vendor-set
migration cadence; a trained model's retraining cadence is set by the team's
drift measurements; a script has neither. Neither page quantifies latency, so
measure it per workload. Evaluation needs a labelled set in every case.

**Apply here:** an LLM proposal states call volume, batch versus interactive,
and who owns model migration; an ML proposal states who owns retraining and
drift monitoring; a script proposal states who owns rule changes.

## Decision procedure

Ask in order and record each answer per candidate process.

1. **What does the current process achieve, and is it optimised?** If a
   process change or clearer rule meets the goal, stop (Rules of ML #1).
2. **Structured data or unstructured language?** Structured with known rules:
   script. Structured, rules unknown, labelled outcomes in volume: classical
   ML. Unstructured language: LLM candidate.
3. **Is the rule set known and stable?** Yes: script or workflow agent. Known
   but unwieldy: OpenAI's second criterion; ML or LLM.
4. **What is the output?** Number, class, probability or rank: classical ML.
   Fixed transformation: script. Judgment over text with a bounded action set:
   single LLM call with a schema. Multi-step with tool choice and an
   unknowable path: agent.
5. **Error cost and review?** High cost, no review path: do not automate
   (PAIR). High cost with review: LLM interprets, human or code decides.
6. **Volume and latency?** High volume, delay-tolerant: batch pricing or a
   trained model. Interactive and high volume: measure LLM cost and latency
   before committing.
7. **Determinism and audit?** Regulated or contestable decisions: the decision
   is code or a reviewable model; the LLM may only prepare inputs.

## Common mistakes

| Mistake | Tell | Better choice |
| --- | --- | --- |
| LLM doing arithmetic, lookups or exact matching | Prompt says "calculate", "look up the ID", "compare codes" | A function tool or plain code; the LLM only decides when to call it |
| Agent where a workflow suffices | The step list can be written down and never changes | ADK Sequential or Parallel agent, or ordinary code (Google Cloud, Microsoft) |
| Classical ML on 40 labelled rows | Tiny training set, or no outcome column | A heuristic, or an LLM with in-context examples, plus a labelling plan (Rules of ML #1) |
| LLM forecasting or scoring tabular data | Input is a table or series with history | Gradient-boosted trees or a conventional forecaster (Grinsztajn, Tan) |
| Chatbot as the default interface | A form, button or batch job already exists | Keep the interface; put the model behind it, or omit it (PAIR: predictability) |

## Hybrid patterns

- **LLM interprets, code decides.** The model extracts fields into a schema;
  deterministic code applies policy and produces the effect (OpenAI's
  unstructured-data criterion; PAIR transparency).
- **ML model as a tool.** A trained classifier or forecaster wrapped as an ADK
  function tool; the agent chooses when to call it and explains the result.
- **Rules first, LLM for the residue.** Settle what a rule can settle; send
  only ambiguous cases to the model (Rules of ML #1; Google Cloud).
- **Workflow outside, agent inside.** Fixed orchestration with a model-driven
  step only where judgment is needed (Microsoft's spectrum; ADK workflow
  agents).

## Proposed triage table

| Criterion | Script or rules | Classical ML | Single LLM call | LLM agent | Human process change |
| --- | --- | --- | --- | --- | --- |
| Input | Structured, known fields | Structured, many examples | Unstructured language | Unstructured plus external systems | Any |
| Rules | Known and stable | Unknown but learnable | Known in prose, hard to encode | Unwieldy, context-dependent | Unclear or disputed |
| Labelled history | Not needed | Thousands of rows or more | Dozens, for evaluation | Dozens of end-to-end cases | Not needed |
| Output | Fixed transformation | Number, class, probability, rank | Bounded judgment with a schema | Sequence of actions and a result | A decision owned by a person |
| Path | Fixed | Fixed | Single step | Unknowable in advance | Variable |
| Error cost | Any, if tested | Must be measurable | Needs review or low cost | Needs guardrails and review | Required when errors are intolerable |
| Determinism and audit | Full | Reproducible per model version | Partial; log prompts and outputs | Lowest; log every tool call | Full |
| Recurring cost | Compute only | Inference plus retraining | Per token per call | Per token per step, many steps | Staff time |
| Who maintains | Developers | ML engineers, data owners | Prompt and eval owners; model migration | Same plus tool and guardrail owners | Process owner |
| Example | Tax calculation, format conversion | Churn score, demand forecast | Route a support email to one of eight queues | Investigate a claim across three systems and draft a decision | Approve refunds above a threshold |

## Explaining it to a business stakeholder

One sentence per slot: "You asked whether AI can handle [process]. The input
is [structured records / free-text documents], the rules are [stable / known
but hard to keep current / dependent on context], and we [do / do not] have
[N] past outcomes to learn from. That points to [a script / a predictive
model / a language model with a fixed output / an agent that works through the
steps itself]. We chose it over [nearest alternative] because [one observable
reason]. The error cost is [low / high], so [a person reviews every output /
the system decides only within these limits]. It costs about [per-item cost or
staff time] to run, and [role] keeps it current, including [rule changes /
retraining / model upgrades the vendor requires at least yearly]."

Each bracket maps to a table row, so the explanation and the triage are the
same artefact.
