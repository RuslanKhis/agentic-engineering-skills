# What makes an effective engineering skill?

Primary-source review, 15 September 2026. Upstream repositories and their
instructions can change. This is a design assessment, not a ranking by downloads
or stars, and the external skills were read as research material.

## Conclusion

The useful pattern is a skill that is **easy to select, specific about the
work, economical to navigate, portable to another project, and tested through
observable results**. This repository already has substantial domain guidance,
selective references and credible implementation smoke tests. Its next gains
are likely to come from repeatable package checks and evaluations of discovery,
scope and composition, rather than adding more general advice to every file.

That final prioritization is our assessment of this checkout. It is not a
measured improvement from the changes proposed below.

## What the sources actually establish

### 1. A valid package is the starting point

The Agent Skills specification requires a `SKILL.md` with a valid name and
description, and supports bundled scripts, references and assets. It recommends
staged loading and references that are easy to reach from the entry document.
Format constraints and recommendations are different: a length recommendation
does not establish that a longer domain skill is ineffective.
[Agent Skills specification](https://agentskills.io/specification)

**Apply here:** validate metadata, folder/name agreement and installed-package
links automatically. Keep each specialist usable after copying only its own
directory. Validate the router's optional sibling dependencies separately from
the specialists' internal files.

### 2. Test selection separately from execution

OpenAI's evaluation guide separates explicit, implicit, contextual and negative
invocation cases. It also separates outcome, process, style and efficiency
checks, and recommends captured trajectories and artifacts so failures can be
explained. These are vendor recommendations illustrated by an example, not a
published comparison proving a universal best format.
[OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)

Vercel's Next.js 16 experiment found the skill was never invoked in 56% of its
cases. Explicit instructions improved results, with wording and inspection
order affecting behavior. Its persistent documentation index performed best in
that particular evaluation. This establishes a discovery failure in its setup;
it does not establish that persistent instructions outperform every ADK skill
or that all twelve specialists should be loaded on every task.
[Vercel's first-party evaluation report](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)

**Apply here:** retain the explicit `/adk-engineer` and `$adk-engineer` examples,
then add realistic prompts that omit the skill name. Include nearby requests
that should not activate a specialist, such as ordinary database administration
or unit tests unrelated to agents. Score which instructions were actually read,
as well as whether the result works.

### 3. Improve against a baseline, with independent checks

Anthropic recommends identifying concrete failures without a skill, building
representative evaluations, and writing enough guidance to address those gaps.
It advises observing the files an agent actually reads, keeping optional detail
in references, and using scripts for repeatable mechanical operations.
[Anthropic authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Its current `skill-creator` implementation runs paired skill and baseline
conditions, gathers assertion evidence, and records timing and token usage.
It includes analysis of uninformative assertions and run variability. This is
an implemented evaluation workflow, not independent evidence that every skill
it creates improves task performance.
[Anthropic's skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

SkillsBench evaluated 84 tasks across 11 domains and seven agent/model
configurations. It reported an average benefit from curated skills, but 16
tasks had negative differences. Its analysis by skill count and complexity
groups different tasks; it is not a controlled instruction to always install
exactly two or three skills or cap every file at a particular length. The
relevant lesson is to measure benefit for the intended tasks and environment.
[SkillsBench paper](https://arxiv.org/abs/2602.12670),
[paper text and tables](https://www.skillsbench.ai/skillsbench.pdf)

**Apply here:** preserve the current independent acceptance tests and add
comparable runs without these skills before claiming improvement. Keep input
projects, task contracts, dependency versions and graders fixed across
conditions. Record failures, unavailable runs and repeat count; a successful
retry must not erase a failed observation.

### 4. Borrow concrete teaching patterns, not an entire workflow

Vercel's React skill uses a short topic index and separate rule files. A typical
rule pairs a condition and explanation with contrasting code examples. This
is a useful presentation pattern; the existence of that structure is not a
benchmark of its effectiveness.
[React skill](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md),
[an individual rule](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-parallel.md)

Superpowers' authoring skill tests behavior under pressure and includes
counterexamples for deciding when a pattern does not apply. Its description
and word-count prescriptions are that collection's guidance. In particular,
its preference for descriptions containing only triggering conditions is
stricter than the shared specification's description of what a skill does and
when to use it. Do not turn either collection's stylistic preference into an
unsupported universal rule.
[Superpowers writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md)

**Apply here:** where a real miss occurs, add a compact reference example with
four parts: the trigger, the tempting mistake, the corrected pattern and an
observable check. Examples should target costly ADK mistakes such as interpreting
an uncertain write as safe to retry, or treating a model-supplied user ID as
authority. Avoid repeating the same rule across every entry document.

### 5. Make composition explicit

Matt Pocock's `ask-matt` distinguishes a main workflow, standalone tasks and
supporting vocabulary. His `tdd` focuses on behavior at public interfaces and
links to supporting material. These are useful examples of role separation;
the current collection also has its own setup and test-boundary agreement
requirements, which users need to understand when choosing it.
[ask-matt](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md),
[tdd](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)

Google's Agents CLI suite covers a generated project's lifecycle as well as ADK
code recipes. Its lifecycle guidance is broader than a single application
feature. The existing [comparison](agents-cli-comparison.md) and
[integration guide](../integrations/agents-cli.md) document the overlap and
scope implications.
[Google's skills reference](https://google.github.io/agents-cli/reference/skills/)

**Apply here:** select one leading workflow and a primary ADK specialist.
Use Google's skills for the requested Agents CLI operations and generated
project conventions; use this collection for the feature's engineering
contracts; use an explicitly selected development skill for its method. Optional
collections should not become mandatory dependencies. A memory request should
not acquire an unrelated scaffold, deployment, tracker or commit workflow.

## Assessment of this repository

These observations describe the checkout reviewed at the start of this change.

| Area | Existing strength | Gap worth addressing |
| --- | --- | --- |
| Discovery | Twelve named skills, clear descriptions, router and practical README prompts | Recorded CLI generation checks use explicit skill names; they do not measure implicit selection across the collection |
| Navigation | Specialists select modes and load references as needed | Package integrity and internal reference reachability need one repeatable repository-wide check |
| Domain work | Memory, API and evaluation skills inspect real boundaries, preserve target conventions and define failure cases | Preserve this depth; improve specific confusing paths when a run demonstrates a miss |
| Portability | Each specialist bundles its own references, helpers and license | Catch accidental links to the source checkout or another package before release |
| Evidence | Saved code, independent tests, version records and explicit limitations | No paired skill/no-skill comparison establishing performance lift |
| Composition | Router supports Matt's process; README explains Agents CLI | Carry actionable composition guidance in the installed router and test scope preservation |
| Maintenance | Individual helper tests and compatibility notes | A central offline command and CI job should catch regressions without model credentials |

The [Codex CLI report](../testing/codex-cli-smoke.md) records three successful
generation scenarios and 162 passing generated/independent tests. That is useful
evidence of successful use in those environments. The report correctly says it
does not measure improvement over running the same tasks without skills.
Representative instructions examined include the
[router](../../skills/adk-engineer/SKILL.md),
[memory specialist](../../skills/adk-memory-architecture/SKILL.md),
[API specialist](../../skills/safe-api-tool-calls/SKILL.md) and
[evaluation specialist](../../skills/adk-agent-evaluation/SKILL.md).

## Priorities

1. **Automate package checks.** Validate required metadata, local resources and
   standalone portability; run the existing offline helper tests in CI.
   Packaging failures should be easy to reproduce without an agent account.
2. **Create a discovery and scope corpus.** Cover direct use, ordinary user
   wording, adjacent negatives, unavailable specialists and composition with
   Google's and Matt's collections. Separate this corpus from claims that it
   has already been executed successfully.
3. **Define an evidence record.** Capture skill revision, agent/model, fixture,
   prompt, installed collection, loaded resources, artifacts, independent
   checks, duration, available token counts and failed/blocked/not-run cases.
4. **Clarify router composition.** Put the short, operational guidance in its
   installed package, with references only where relevant. Preserve existing
   project ownership and the user's requested scope.
5. **Run controlled comparisons before broad rewriting.** Start with the memory,
   API and workflow fixtures already available. Expand to other specialists
   according to observed risk and failures. Record a new version's benefit or
   regression against the same baseline instead of inferring it from prose.

These priorities do not imply that more testing infrastructure always helps.
Keep mechanical checks small, deterministic and separate from slower model
trials. Reserve claims of better skill performance for observed behavior under
specified conditions.
