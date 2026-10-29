# Compatibility & Checks

*What was installed, what generated code, and what the checks establish.*

The packages use the [Agent Skills format](https://agentskills.io/specification).
The specialists inspect your project's installed SDK versions before applying a
recipe; their references record compatibility, validation evidence and practical
limits. There is no single application environment to install at this
repository's root.

This is the testing log of the collection, one dated entry per change that
was checked, newest first. Each entry says what changed, which checks ran
(offline helper suites, fresh coding-agent sessions, live model or cloud
trials) and what they do not establish; the linked testing record holds the
prompts, versions and raw results. Offline checks run in CI on every change;
model and cloud trials are bounded samples on the dates shown, not a
guarantee for every model, SDK version or client. New entries go at the top
of the list below.

## One version against a fixed target · 29 October 2026

This closes friction 4 of the "Eval-Driven System Design" trial: nothing
said whether 36 of 40 (90%) clears an 88% target. It doesn't: the 95%
interval is 77% to 96%, so the honest verdict is "not shown".

**What changed in the skills.**

- **adk-agent-evaluation.**
  - New section "Score one version against a fixed target" in
    `quality-iteration.md`. It gives three verdicts (meets, below, not
    shown), the Wilson score interval for pass/fail sets, and sizing from
    the target and the expected rate.
  - `paired_difference.py` gains a target mode (`--candidate` and
    `--target`, no `--baseline`; `--require meets`), with 13 new tests.
    The paired mode's output is unchanged, byte for byte, on six flag sets.
  - Pointers in `SKILL.md` and `evaluation-design.md`.
- **adk-system-designer.** An acceptance threshold on a small set is
  either written as an observed count or read against its interval.
- **adk-presenter.** A rate against an agreed threshold is called met only
  when its interval clears it.

**Scenario.** One runnable case, `evaluation-rate-against-fixed-target`.
It was not run.

`scripts/check_repo.py` passed: 28 offline suites, 1,245 tests. No model or
cloud runs, no trial. Record: friction 4 of the
[alignment](wimberly-eval-driven-system-design-alignment-2026-10-29.md).

## Priced errors and per-stage grading ("Eval-Driven System Design") · 29 October 2026

Entry 3 of the engineering-articles programme: Hugh Wimberly, Joshua
Marker, Eddie Siegel and Shikhar Kwatra, "Eval-Driven System Design: From
Prototype to Production", OpenAI cookbook (with Fractional), 2 June 2025,
archived. Only the method was taken; no OpenAI API facts, model names or
prices.

**What changed in the skills.**

- **adk-agent-evaluation.**
  - Grade each stage on the input it actually received. A stage that is
    right for a wrong input passes, and the error belongs upstream.
    Three ways to get a reference that fits the input. An isolated stage
    run seeded through `session_input.state`.
  - Price each error type at the brief's volume, and gate on the priced
    total against today's process rather than on an accuracy figure.
  - "Not all evals matter": a defect that changes no decision is reported,
    not gated, and error categories are ranked by cost.
  - A small sample prices indicatively, with a break-even miss rate.
- **adk-discovery.** The brief prices a miss and the handling of a flag,
  with the share of cases that need the action and today's rates.
- **adk-presenter.** The value report's cost per outcome gains a
  cost-of-errors line beside today's process at the same volume.

**Register and scenarios.** One article row was added to the source
register. Three scenario cases were added; one has a new fixture and
judge-only material, and two are runnable from their context.

**Trial.** One fresh-agent trial on synthetic invoice-hold records,
offline. It priced today's process at £398,592 and the agent at £495,840,
moved two of the four wrong decisions to extraction, and passed all five
assertions. Ease: 5 of 5 to find the method, 4 of 5 to apply it. Three
frictions were fixed the same day (a break-even formula, taking p from the
brief rather than an enriched sample, and how a correct flag is priced).
Those fixes were not re-trialled.

**Scenario run.** The three new scenarios then ran through
`run_scenarios.py` with Sonnet 5.5 as agent and judge (three judge votes),
for $1.18 including one re-run. Evaluation passed 5 of 5 and discovery
3 of 3 (two split votes; the skill was not loaded). Presenter passed 2 of
3: the value report said to price "misses and false flags", so the agent
left out the handling cost of correct flags. The wording now prices every
handled flag on both sides, and the re-run passed 3 of 3 (two split votes).

`scripts/check_repo.py` passed: 28 offline suites, 1,232 tests. No cloud
runs. Record: [alignment](wimberly-eval-driven-system-design-alignment-2026-10-29.md).

## Error bars on evaluation comparisons ("Adding Error Bars to Evals") · 29 October 2026

Entry 2 of the engineering-articles programme: Evan Miller (Anthropic),
"Adding Error Bars to Evals", arXiv 2411.00640, November 2024. It is older
than the preferred window, but it is still the reference others cite.

**What changed in the skills.**

- **adk-agent-evaluation.**
  - New section "Tell a change from noise" in `quality-iteration.md`: a
    paired difference per case, runs averaged first, the error clustered on
    the scenario, a t interval, the minimum detectable difference, and the
    holdout and CI set sized from the difference that matters.
  - New helper `paired_difference.py`, with 17 tests.
  - Small pointers in `evaluation-design.md`, `result-auditing.md` and
    `SKILL.md`.
- **adk-release-engineering.**
  - A nightly drop blocks only when its paired interval lies below zero.
  - The suite's minimum detectable difference is recorded beside the
    margin.
  - A model migration asks "not worse by more than the margin".
- **adk-presenter.** The one-over-root-n rule is replaced by the margin of a
  difference between two periods.
- **adk-discovery.** The pilot sample is sized from the smallest lift the
  sponsor would act on.
- **adk-agent-instructions.** An optimiser's candidate must improve by more
  than the noise.

**Register and scenarios.** One article row was added to the source
register. Four scenario cases were added; one has a new fixture and
judge-only material, and three are runnable from their context.

**Trial.** One fresh-agent trial on synthetic trial records, offline. It
reached the right verdict (within noise) and holdout size, and passed all
five assertions. Ease: 5 of 5 to find the method, 3 of 5 to apply it. The
frictions it found were fixed the same day in the helper and the reference.
Those fixes were not re-trialled.

**Scenario run.** All four new scenarios then ran through
`run_scenarios.py` with Sonnet 5.5 as agent and judge (three judge votes),
for $0.88. Evaluation (with a shell) passed 5 of 5 and presenter 3 of 3.
Release passed 2 of 4: the agent applied the paired gate but did not choose
`num_runs` from the variance split or state that the per-case thresholds
stay, so the reference's completion check now names both. Discovery passed
2 of 3, with the right sample size, but answered in one turn without
loading the skill, so the shadow-run route was missed; that is a skill
selection miss, not a content gap. The release clarification was not
re-run. adk-system-designer's live-acceptance criterion now points to the
same sizing method.

`scripts/check_repo.py` passed: 28 offline suites, 1,232 tests. No cloud
runs. Record: [alignment](miller-adding-error-bars-to-evals-alignment-2026-10-29.md).

## Seed article "Evaluation Precedes Evolution" integrated · 28 October 2026

The first article in part two of the engineering-articles programme:
Pouya Ghiasnezhad Omran and Tanya Dixit (Google), "Evaluation Precedes
Evolution", LinkedIn, 15 June 2026. The article was checked against
google/adk-samples (now google/adk-recipes) at a9dc177 and against the
google-adk 2.8.0 and 2.12.0 optimiser source.

**What changed in the skills.**

- **adk-agent-evaluation.**
  - Shape a rubric by verifiability, horizon and stakes.
  - Score every stage and keep the stage verdicts.
  - Judge the work on the outcome measure, closing two gaming patterns.
  - Code checks as `EvalConfig` custom metrics.
  - Measure a judge that is re-checked on its costly side.
- **adk-workflow-design.** Re-check a model check's costly verdict in code,
  failing closed.
- **adk-agent-instructions.** The rubric comes before any `adk optimize`
  run: what the sampler scores, a separate validation set, and a root agent
  with a static instruction.

**Register and checks.** The source register gained its first article row,
and `check_source_freshness.py` now validates article rows without fetching
them (three tests). Two scenario cases were added.

**Trial.** One fresh-agent trial ran on a synthetic invoice pipeline,
offline: 44 project tests passed, and it rated the work 4 of 5. Five
frictions were fixed the same day.

`scripts/check_repo.py` passed: 28 offline suites, 1,215 tests. No model or
cloud runs. Record: [alignment](omran-dixit-evaluation-precedes-evolution-alignment-2026-10-28.md).

## Engineering-articles reading plan, and two small fixes · 28 October 2026

Part one of the [engineering-articles programme](engineering-articles-integration-prompt.md):
ten read-only scouts produced a ranked
[reading plan](../research/engineering-articles-reading-plan-2026-10-28.md)
of practical Google, Anthropic and OpenAI articles. No skill changed because
of an article. Two problems found while planning were fixed directly:
- a garbled sentence in optimise-adk-on-google-cloud `context-window.md`;
- a new adk-agent-security rule, "State placeholders are prompt text too",
  checked against google-adk 2.8.0 `flows/llm_flows/instructions.py`, with a
  pointer from adk-agent-instructions.

`scripts/check_repo.py` passed: 28 offline suites, 1,212 tests. No model or
cloud runs.

## The first shell-enabled scenario run · 28 October 2026

The scenario runner can now give the agent Bash. A shell cannot be confined
to the workspace by path, so such a run is recorded as **unconfined**.
Instead, the runner scrubs the agent's environment:
- it removes `GOOGLE_`, `GCLOUD_`, `CLOUDSDK_`, `AWS_`, `AZURE_` and `ARM_`
  variables, SSH agent and git-hosting tokens;
- it points gcloud, AWS, Azure, Docker, kubectl, git, gh and npm
  configuration at empty per-scenario paths;
- it keeps HOME real, because the claude CLI does not log in without it.

Shell commands and their output are recorded and shown to the judge. A
smoke test in a scenario workspace showed gcloud with no account, project
or credentials. Two runner defects found during the run were fixed: a
`cd` moved the allow rules away from the workspace, and shell reads of
skill files were not counted.

**Results.** All four governance packs never run before were run, 22 of 23
assertions, each running `check_governance.py` until every draft passed.
Eleven scenarios with shell-dependent assertions were re-run: 31 of 48
(18 before). Of the 17 shell-dependent rows, 12 now pass, each by actually
running the helper, tests or git, and none through the not-run escape.
Triage of 25 rows found no skill defect, 7 fixture, assertion or runner
defects (five new ones for the owner) and 18 variance. An audit of 195
shell commands found no network install, no cloud CLI call and no read of
cloud or SSH credentials. It did find listings under the real home
(`~/.claude/skills`, `~/.npm`), a `docker info` probe and reads of Claude
Code's own spilled output. Spend was $14.58 of a $15 cap; about 27
helper-dependent scenarios and the four earlier governance packs remain.
[Shell run record](shell-run-2026-10-28.md).

## The last defects from the Phase 10 triage · 28 October 2026

The workflow-design description now names checkpoint reuse after a changed
input, a checkpoint too large for its store, multi-day approval waits across
restarts (ADK resume or a durable engine), draft consistency checks and
warning-only corrections, which its body already routed (763 to 944
characters; two ownership rows record the split with evaluation, guardrails
and safe-api). Deploy hands the Agent Identity decision to
adk-tool-auth-and-secrets and gives the install step for a missing
google/skills or Agents CLI skill. Ten shell-dependent scenario assertions
carry a "reported as not run" escape, one rollback assertion now agrees with
the release skill, and two screen-placement scenarios follow the ownership
map.

**Results.** Sonnet 5.5 activation: dev 344 PASS, 10 PARTIAL, 2 FAIL on 178
cases (332/10/2 on the 172 Phase 10 ran, against 331/12/1; both FAILs are
existing designer-versus-engineer and parked-label cases, and the workflow
skill was never chosen for `designer-checkpoint-positive`); held-out 155 of
156, the one PARTIAL a near-miss the workflow skill already took before. The
workflow skill now loads in 7 of 7 workflow scenarios (2 of 7 before) and
they pass 12 of 33 assertions (8 before). Four governance packs and the
rollout pack ran for the first time (21 of 31). Triage: 4 skill-defect, 4
assertion, 28 variance rows; two new suspected gaps (workflow's mode table
does not route a checkpoint over its storage limit; guardrails' human-review
row does not name unanswered approvals). Spend was $11.70 of a $12 cap; four
governance packs and the re-runs of the changed assertions stayed unrun.
[Last defects record](last-defects-2026-10-28.md).

## Skill defects from the scenario triage · 28 October 2026

Twelve of the thirteen suspected skill defects from the scenario triage were
confirmed and fixed in the skill that owns each topic; the thirteenth (a
do-nothing control for evaluation graders) was already in the evaluation
skill. Screen placement and the local Prompt Guard 2 screen moved to
protect-adk-sensitive-data, which operates the screens, with pointers from
the security and guardrails skills and a new row in the ownership map. The
guardrails, evaluation and sensitive-data descriptions now name the plain
requests that had loaded no skill, and nine dev activation cases test them.

**Results.** Sonnet 5.5 activation: dev 331 PASS, 12 PARTIAL, 1 FAIL (an
existing designer-versus-engineer instability that also fails on `main`);
held-out 156 of 156, unchanged. The 16 scenarios with skill-defect rows were
re-run: those rows went from 0 to 8 of 27 passing, the scenarios from 22 to
33 of 71 assertions, and the primary skill loaded in 14 runs instead of 9.
33 scenarios ran for the first time (56 of 143 assertions); their triage
names three new skill gaps, chiefly a workflow-design description that misses
checkpoints and durable resume. Spend was $22.93; the eight governance packs
and one presenter scenario stayed unrun within the $25 cap.
[Skill defect fixes record](skill-defect-fixes-2026-10-27.md).

## Fixtures for every representable scenario · 27 October 2026

126 of 152 scenarios had no project to run against. They now build their
workspace from six small base projects (an ADK support assistant, its PoC
plan, a document pipeline, a claims-triage record set, a React chat and a SQL
agent) plus a per-scenario overlay, and 141 scenarios can run offline; 11 are
marked not representable with a reason (they need a shell, a profile outside
the workspace or another installed skill version). Thirty-three contexts that
read as fixture instructions or listed the expected defects were rewritten,
the source-support and ingestion scenarios got their own packs instead of
the skills' worked examples, and a new test rejects planted-defect markers,
grader references and copies of skill files in any fixture.

**Results.** 77 scenarios ran once with Sonnet 5.5 for $39.17: 170 of 333
assertions passed by majority, 39 had split judge votes, and the primary
`SKILL.md` loaded in 65 runs. Of 180 triaged rows, 29 point at skill gaps
(guardrails and evaluation descriptions that miss their own topics, screen
placement with no owning rule, PromptGuard facts only in the security skill),
42 at fixtures or assertions (mostly steps that need a shell this run does not
have), and 109 at the agent leaving out what the skill it read covers. 41
newly runnable scenarios were not run within the cap.
[Scenario fixtures record](scenario-fixtures-2026-10-27.md).

## Owners for three held-out routing gaps · 27 October 2026

The held-out run found three requests with no clear owner. Each now has one:
- **Model 429 and quota errors:** retrying them belongs to
  adk-model-and-output-contracts.
- **A new feature across an existing application:** planning it belongs to
  adk-engineer.
- **`output_key` handoffs:** a `{key}` placeholder an earlier agent never
  filled belongs to adk-workflow-design.

Six descriptions and the ownership map changed. The six held-out cases read
during the edit moved to dev and were regenerated by the isolated generator.

**Results.** Sonnet 5.5 had no dev failures and passed 156 of 156 held-out
runs. Haiku 5.5 had 1 dev failure (down from 3) and passed 77 of 78
held-out. [Routing gaps record](routing-gaps-2026-10-27.md).

## Trustworthy scenario runs and grader answers kept out of skills · 27 October 2026

Grader-side files no longer ship inside skill packages. The ingestion
inventory and the source-support labels moved to `evals/graders/`, and the
safe-api oracle and the guardrails trial protocol moved to `evals/trials/`.
The scenario runner gives grader files to the judge only, and a test fails if
a skill ships one. Scenario agents now run in `dontAsk` mode with allow rules
scoped to the workspace, project settings only and auto-memory off; a probe
showed reads of the repository, `~/.claude` and the grader folder refused,
and nothing from `~/.claude/skills` in the catalogue. The judge grades three
times and flags assertions whose votes differ. The API-key backend and the
activation workflow were removed.

**Results.** Re-running the five phase 1 scenarios with Sonnet 5.5, the
primary `SKILL.md` loaded natively in 4 of 5 (2 of 5 before). 15 of 22
assertions passed by majority and 5 were unstable. Run-to-run variation of
the agent is larger than the judge's, so five single runs cannot show a
quality change.
[Runner and graders record](runner-and-graders-2026-10-27.md).

## Held-out activation cases · 27 October 2026

Every activation case now has a `split`. The 154 existing cases are `dev`.
78 new `heldout` cases were generated by a fresh, isolated Opus 5.5 session
that saw only a neutral brief per skill, never the descriptions or the
repository. `check_repo.py` requires a held-out positive and near-miss for
every skill. `run_activation.py --split` reports each split separately. The
held-out split is never used while editing a description.

**Results.** On the held-out cases, Sonnet 5.5 scored 152 PASS, 2 PARTIAL
and 2 FAIL over two repeats (97.4%), against 97.7% on dev. Haiku 5.5 scored
74, 3 and 1 (94.9%), against 95.5% on dev. No description was changed. One
request failed on both models: retrying Gemini's own 429s, which was routed
to safe-api-tool-calls. It is left to the skill owners to decide which skill
owns it. The generated near-misses sit further from the boundaries than the
dev ones. [Held-out activation record](heldout-activation-2026-10-27.md).

## Measured routing, clearer boundaries and one set of conventions · 27 October 2026

Five changes landed together.
- **Activation is measured.** `scripts/run_activation.py` measures skill
  selection from descriptions. `scripts/run_scenarios.py` runs a scenario
  in a throwaway workspace and has a judge grade its assertions. A manual
  GitHub workflow runs activation through the Anthropic API.
- **Contested topics have one owner.** `adk-engineer/references/ownership.md`
  names the owner of each contested topic, such as approval, replay, session
  ownership, history, exemplars and CI gates. Descriptions now exclude each
  other in both directions, and `check_boundaries.py` keeps it that way.
- **Shared guidance has one source.** The evidence labels, permissions,
  interpreter, confirmation and verified-principal guidance come from a
  single copy in `shared/`. `sync_shared.py` keeps every skill's copy
  identical.
- **Every skill records what it was verified against.**
  [docs/compatibility.md](../compatibility.md) gathers the versions in one
  table. Maintainer records moved to `docs/skill-evidence/`.
- **The 48 helpers share one convention** for flags and exit codes:
  [helper conventions](../helper-conventions.md).

The README was cut from 3,849 to 446 lines. Its per-skill detail, journeys
and this testing log moved to `docs/` verbatim.

**Results.** With Sonnet 5.5 the 114 original cases gained no new failures:
three cases that were unstable before now pass every time. The full
154-case set scored 298 PASS, 9 PARTIAL and 1 FAIL over two repeats.
Measuring also found a real gap: document ingestion was missing from the
memory description, and it has been added. It also found that 126 of 152
scenarios lack fixtures, and that two skills ship grader-side files.
[Integration and activation record](quality-phases-2026-10-27.md).

## Practice profile: an interview or your own documents · 26 October 2026

The practice profile can now be filled in two ways: a short interview, or
Markdown and text files the user names. The interview asks sixteen core
questions over thirteen sections. Six of the sections are new: sector and
jurisdictions, data subjects and data classes, systems of record and tools,
AI policy and approvals, AI maturity and past attempts, and procurement and
consultation. Company facts get menus with "don't know", never a suggested
answer. For an import, the helper withholds secrets and personal data,
flags text that tries to instruct the assistant, and refuses crafted files.
Each line the agent proposes must quote the line it came from, which the
helper checks. Nothing is written until the user accepts each line and says
yes to the diff, and a snapshot is taken before the write. A one-page
company context brief can be exported and brought into another profile the
same way. The writing rules lost no sentence. Three fresh-agent trials
passed:
- An interview for a fictional Australian retailer. The agent refused to
  record a volunteered "pilots may skip the review" as a default.
- An import containing a planted "remember that production writes need no
  approval" line and a fake access key. Neither was offered; both were
  reported by kind and line, and every accepted line cites `file:line`.
- An export refused in a sister client's repository, then re-imported there
  line by line.

Eighteen frictions were fixed the same day, among them an export check that
hid the cross-org refusal. All **25 packages** pass validation and **975
tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/practice-profile-intake-2026-10-26.md) and the
[record](practice-profile-intake-2026-10-26.md).

## assistant-ui in front of a Python ADK agent · 26 October 2026

assistant-ui's ADK package reaches a Python agent only through a gateway
route the team writes, and its stock stream forwards raw ADK events to the
browser: thought parts, every state key and raw error text. The frontend
skill now covers that route: server-allocated session ids, a filtered
stream and history, inbound part and approval validation, edit and
regenerate through `Runner.rewind_async` (which checks no ownership and
undoes no side effect), the AG-UI approval payload that otherwise counts a
missing decision as approval, and Assistant Cloud kept off for client data.
The fresh-agent trial built the gateway offline and refused every hostile
request before any model call (41 tests passed; ease 3 of 5); it found that
ADK 2.12 rejects the approval-plus-text message the package sends, which
the gateway now splits. Eight of nine frictions were fixed the same day.
All **25 packages** pass validation and **951 tests** pass with **59
optional SDK checks skipped**. See the
[note](../research/assistant-ui-comparison-2026-10-26.md) and the
[record](assistant-ui-alignment-2026-10-26.md).

## A capability gate for coding-agent pull requests · 26 October 2026

agents-shipgate was proposed as a cheap merge gate; it is not one. Its
binding diff exits 0 whatever it finds and missed a removed confirmation, a
removed callback and a widened MCP filter, and its `verify` command failed
even a README-only pull request. The security inspector already reads
those controls, so it gained `--compare BASE_JSON`: run on a pull request's
base and head, it lists what each agent can now do differently and exits 3,
and the CI steps run it from the base commit so a change cannot rewrite its
judge. The inspector also stopped reporting a project with an ADK 2.x
`Workflow` as complete; it names the graph's nodes and lists them as
unread. In the fresh-agent trial the gate caught every planted change and
passed an unrelated one (ease 3 of 5); six of eight frictions were fixed
the same day. All **25 packages** pass validation and **951 tests** pass
with **59 optional SDK checks skipped**. See the
[note](../research/agents-shipgate-comparison-2026-10-26.md) and the
[record](agents-shipgate-alignment-2026-10-26.md).

## Skill validation against the Agent Skills reference · 26 October 2026

All 25 skills pass the Agent Skills reference validator (the published
wheel's command is `agentskills`, not the `skills-ref` the specification
names). Its parser is stricter than ours in three ways, a `---` inside
frontmatter, inline YAML collections and anchors, so `validate_skills.py`
now rejects them too. From skill-creator, activation is measured as a
trigger rate over repeated runs with train and held-out cases, and the
existing blind A/B practice is written down with a mapping file written
before grading. The fresh-agent maintainer trial changed a description on
a copy and, with no model access, recorded it as an unmeasured candidate
rather than an improvement (ease 3 of 5); nine of eleven frictions were
fixed in the contributing guide and checks the same day. All **25
packages** pass validation and **951 tests** pass with **59 optional SDK
checks skipped**. See the
[note](../research/skill-creator-agentskills-comparison-2026-10-26.md)
and the [record](skill-creator-agentskills-alignment-2026-10-26.md).

## A phase gate that reads the code · 26 October 2026

The system designer's phase gate read only the tickets, so a phase whose
records said finished could close while the code disagreed. After spec-kit's
`converge` and OpenSpec's `verify`, it now closes in four steps: the
records gate; the same gate with `--base <commit>`, which fails on any file
changed since the phase began that no ticket's `touches` names; a
fresh-context read-only review with a new plan-versus-code prompt, grading
gaps CRITICAL, WARNING or SUGGESTION; and the findings on the agenda. A
withdrawn contract must be proved gone by a `SHALL NOT` item, a manual
check needs a named person and date, and the gate no longer requires the
review goal it precedes. 12-factor-agents was read and not linked: the
skills already state its rules more precisely. In the fresh-agent trial
the records said finished, the plain report said nothing was wrong, and
the gate and review together caught all four planted defects (ease 3 of
5); seven of ten frictions were fixed the same day. All **25 packages**
pass validation and **947 tests** pass with **59 optional SDK checks
skipped**. See the
[note](../research/spec-tools-comparison-2026-10-26.md) and the
[record](spec-tools-alignment-2026-10-26.md).

## Governance papers for Australian, US, EU and UK law · 26 October 2026

The governance pack assumed the EU AI Act and GDPR everywhere. It now
screens jurisdictions before drafting, always in the order Australia, United
States, EU, UK, from where the client, the people and the processing are
(including the agency's own staff in Australia), and keeps a regime in scope
while a fact is unknown. Every draft records `jurisdictions:` and the
checker fails a missing list or a section for a regime not in scope. The
classification memo becomes a regulatory memo: the EU AI Act classification
where the EU applies, and for Australia, the US and the UK, which have no AI
Act, a screen of the laws that do (the Privacy Act and APP 1.7 from 10
December 2026; California's CPPA rules, Colorado, NYC Local Law 144 and
federal sector laws; UK GDPR as amended by the Data (Use and Access) Act
2025). The DPIA input pack now serves as the Australian PIA and the US risk
assessment too, a transfer annex covers EU and UK data reached from
Australia, and the EU reference carries the Article 50 guidelines, Article
25(4), SCHUFA and Dun & Bradstreet. Three fresh-agent trials (an Australian
HR assistant, a UK bank chatbot, a US hiring screener) picked the right
regimes in the right order, set counsel flags where they belonged and
passed the checker (ease 4, 3 and 4 of 5); all 22 frictions were fixed or
recorded the same day. All **25 packages** pass validation and **966
tests** pass with **59 optional SDK checks skipped**. See the research notes
for [Australia](../research/au-ai-privacy-law-2026-10-26.md), the
[United States](../research/us-ai-privacy-law-2026-10-26.md), the
[EU](../research/eu-ai-privacy-law-2026-10-26.md) and the
[UK](../research/uk-ai-privacy-law-2026-10-26.md), and the
[record](governance-jurisdictions-2026-10-26.md).

## Governance papers for New Zealand, Singapore, Canada and AU government forms · 26 October 2026

The governance pack now screens seven regimes, always in the order
Australia, United States, EU, UK, New Zealand, Singapore, Canada, and a
screen that still names only the first four fails with a fix message. New
references at screen depth cover New Zealand's Privacy Act 2020 (s 11
agents, IPP 3A, IPP 8, IPP 12, the Biometric Processing Privacy Code),
Singapore's PDPA (data intermediaries, consent and exceptions, the Transfer
Limitation Obligation, the 3-day breach clock) and Canadian law (PIPEDA,
Quebec's Law 25 with s 3.3, s 12.1 and s 17, Alberta, BC, Ontario
employment rules, the federal Directive on Automated Decision-Making).
For NSW and Commonwealth agencies, crosswalks map the DTA AI impact
assessment, transparency statement, register, agentic addendum, NSW AIAF
and IPC AI PIA guide to the project's records without copying the forms,
and a new form answers document drafts answers in each form's order for the
agency's officers, marked `agency:` where only they can answer; the
crosswalks are re-checked every 90 days. The Australian reference gains NSW
state law, including PPIP Act s 19(2) for any recipient outside NSW, State
records, the NSW Cyber Security Policy and ICTA clause 6.11's six-month
model-change notice checked against the pinned model's retirement date.
Every draft keeps the drafting-aid banner and the reviewer's sign-off from
the same branch's earlier change. Three fresh-agent trials (a NSW agency
chatbot, an Auckland and Singapore retailer, a Quebec and Ontario HR
assistant) picked the right regimes in order, left every sign-off pending
and passed the checker (ease 3, 3 and 3 of 5); 19 frictions were fixed the
same day and the rest recorded with reasons. All **25 packages** pass
validation and **1,022 tests** pass with **59 optional SDK checks
skipped**. These are drafts that support the client's lawyer; no skill
replaces one. See the research notes for
[New Zealand](../research/nz-ai-privacy-law-2026-10-26.md),
[Singapore](../research/sg-ai-privacy-law-2026-10-26.md),
[Canada](../research/ca-ai-privacy-law-2026-10-26.md) and
[AU government forms and NSW law](../research/au-government-forms-nsw-2026-10-26.md),
and the [record](governance-apac-canada-2026-10-26.md).

## Portability planning for a GCP and ADK design · 26 October 2026

This toolkit builds production Google ADK applications on GCP, and that
stays the primary path. A new optional skill, `adk-portability-planning`,
answers a stakeholder's lock-in question in a separate document,
`docs/portability/<topic>.md`: which components of the accepted design are
shared logic, replaceable adapters, provider-specific by choice or expensive
dependencies; cloud, framework, model, service and deployment portability
assessed separately; AWS and Azure alternatives and a small framework
comparison with dated sources; the boundaries worth keeping; migration
risks; and relative effort with its drivers, never invented hours or prices.
It changes no code and no design. The designer asks once whether lock-in is
a concern (default no); only a yes adds a portability goal and its ticket,
which no build goal may wait for and the phase gate skips. Four fresh-agent
trials covered a no and a yes in the designer, the engineer carrying out the
portability ticket, and an unrelated goal routing to its own specialist; an
independent review and the trials found eighteen issues, all fixed the same
day, among them a build goal ordered behind the assessment and a checker that
let hyphenated estimates through. All **26 packages** pass validation and
**1,163 tests** run, with **60 optional SDK checks skipped**. See the research notes on
[AWS](../research/portability-aws-2026-10-26.md),
[Azure](../research/portability-azure-2026-10-26.md),
[agent frameworks](../research/portability-agent-frameworks-2026-10-26.md)
and [design principles](../research/portability-design-principles-2026-10-26.md),
and the [record](portability-planning-2026-10-26.md).

## Plan health between tickets · 25 October 2026

A build of many tickets now reports back to its design while it runs. The
designer's `plan_status.py` reads each ticket's evidence back into the plan:
- which contracts are evidenced, which are still planned and which nothing
  left will prove;
- contract deltas and rulings waiting for a decision;
- ready, interrupted and parallel-safe tickets;
- hours spent and remaining against capacity.

It also has a phase-exit gate (`--gate`) and a weekly status update with a
RAID log (`--weekly`). `check_tickets.py` lints tickets after they are written,
and `check_schedule.py` requires a journey goal before a review of built work.
The designer gained a checkpoint mode. The engineer gained a ticket lifecycle:
resume from a `Progress:` block, end with the checkpoint prompt when a
decision is waiting, and run tickets in parallel worktrees.

Three fresh-agent trials passed:
- An interrupted ticket was resumed, finished and routed to a checkpoint.
- A checkpoint revised a contract in place, settled a ruling and offered
  cut-line options computed by the scripts.
- Tickets were written from a plan with no journey goal; the agent added one,
  and the lint passed with 0 errors.

The checkpoint trial found that a finished ticket's overrun kept triggering
checkpoints after one had been held; it now counts through the phase fit
instead. The same work fixed the instruction linter, which skipped an
instruction imported from `prompt.py` into `agent.py`, the gap two
field-feedback trials reported. [Testing record](release-and-plan-health-2026-10-25.md).

## Releases and plugin installs · 25 October 2026

Every skill carries `metadata.version` (first release `2026.10.25`), and the
package check fails when skills or manifests disagree. `scripts/release.py`
stamps a version, writes the [changelog](../../CHANGELOG.md), tags the release and
moves `stable`; it never pushes.

`claude plugin validate .` passes, including `--strict`, on Claude Code
2.1.306. Installed into a throwaway configuration, the plugin listed all 23
skills at that version. The Gemini CLI and Antigravity manifests follow their
documented schemas but were not installed, because neither CLI is on the test
machine. Codex's plugin format is ambiguous in its documentation, so Codex
keeps the Skills CLI with a pinned tag. The plugin commands work once the
first tag and `stable` are pushed. [Testing record](release-and-plan-health-2026-10-25.md).

## Field reports from real use · 25 October 2026

When a skill's instruction fails on the installed versions, is overridden or
misroutes the work, `adk-engineer` now records a generalised, redacted note
on the user's machine and offers once, at the end of the session, to open a
prefilled GitHub issue form that the user reviews and submits; nothing is
sent automatically and `AES_FIELD_NOTES=off` disables it. A maintainer
triage script clusters reports without printing their prose. In two
fresh-agent trials both tickets finished `verified_local`; the agents
recorded three notes, none containing the client folder name, path or GCP
project, and asked once at the end; nothing was sent. Besides the drift
planted for the first trial, both agents independently reported a real gap:
the instruction linter does not follow an instruction imported from another
module. A third, control trial with no divergence recorded no note and
made no offer; its one stray "nothing to share" line is now ruled out.
All **23 packages** pass validation and **812 tests** pass with **59
optional SDK checks skipped**. See the
[note](../research/field-feedback-2026-10-25.md), the
[record](field-feedback-2026-10-25.md) and
[what is never sent](../field-feedback-privacy.md).

## Practice profile across projects · 25 October 2026

A new `practice-profile` skill keeps the engineer's employer and client
context (business and KPIs, who decides, delivery defaults, stack, security
floor, presentation style) and lessons as short Markdown outside every
repository, one directory per org, bound to repositories by path. Discovery
and the designer offer its values as labelled defaults, the presenter takes
audience and style only, and `adk-engineer` applies lessons tagged with the
chosen specialist. Host-wide memory files were rejected after reading each
host's documentation: they load in every project, so one client's facts
would reach another's. Writes are a diff the user approves, never drawn from
ingested documents. In fresh-agent trials the designer labelled every
profile default and the org floor raised its design, a canary in an unbound
org never surfaced, and a "remember this" line planted in a handbook
produced no profile entry; ten frictions were fixed the same day. All
**24 packages** pass validation and **811 tests** pass with **59 optional
SDK checks skipped**. See the
[note](../research/practice-profile-2026-10-25.md) and the
[record](practice-profile-2026-10-25.md).

## Expert labelling and the monthly value report · 25 October 2026

The evaluation skill now covers labels that do not exist yet: one quality
decision-maker, a session with subject-matter experts that reads about 100
traces until no new failure mode appears, versioned binary criteria with
older labels re-reviewed as the criteria drift, and a gold set with its
provenance. Its new helper reports Cohen's kappa between two experts, the
disagreements to adjudicate and criteria drift, and scores a judge by
true-positive and true-negative rates on a held-out split, refusing below
30 cases per class. The presenter gains a `value-report` stage: one page a
month for the sponsor, ending in a stop, continue or scale call, whose
helper fails any figure without a measurement or incident record, a
missing baseline, a stale window, an assumption presented as measured and
an unreported incident. Two fresh-agent trials met all eight scenario
assertions; their seventeen frictions were fixed the same day. All **23
packages** pass validation and **826 tests** pass with **59 optional SDK
checks skipped**. See the
[note](../research/expert-review-and-value-report-2026-10-25.md) and the
[record](expert-review-and-value-report-2026-10-25.md).

## Statements of work, rollout packs and operations handover · 25 October 2026

Three business documents an agency writes around every build now come from
the artefacts the skills already keep. The designer turns the brief, design
and plan into a statement of work, change request and data-request letter;
`check_sow.py` reads the plan through the schedule check's own parser and
fails when deliverables, hours, fees at the user's rate, dated client
dependencies or measurable acceptance thresholds disagree with it. The
presenter gains a rollout mode: user guide and card citing the contracts,
training, messages per audience, AI disclosure (EU AI Act Article 50,
applying since 2 August 2026, read on the consolidated text), adoption
metrics and a hypercare exit test, checked by `check_rollout.py`. The
observability skill gains an operations handover and a blameless agent
postmortem that extends its incident note. Three fresh-agent trials on a
synthetic claims project (ease 4 of 5 each) produced a SOW and a rollout
pack that passed their checks and a handover that found the pinned model
retiring mid-pilot; most of their 28 frictions were fixed the same day.
No new package: all **23 packages** pass validation and **813 tests**
pass with **60 skipped** (59 optional SDK checks, one pytest skip). See the
[note](../research/engagement-rollout-handover-2026-10-25.md) and the
[record](engagement-rollout-handover-2026-10-25.md).

## Governance papers for a client's reviewers · 25 October 2026

A new skill, `adk-governance-pack`, drafts what a client's counsel, DPO and
CISO ask for before a pilot or production decision: an EU AI Act
classification memo, an impact assessment along ISO/IEC 42005 mapped to the
NIST AI RMF, DPIA inputs, a system card, records-of-processing rows and
security questionnaire answers, each statement citing a contract, decision
or evidence ID or flagged for counsel. The AI Act facts were read in the
Official Journal, including the Digital Omnibus, Regulation (EU) 2026/1744:
Annex III obligations from 2 December 2027, Article 50 unchanged from 2
August 2026, and Article 4 narrowed rather than dropped. The designer now
plans a governance goal before the production decision. Two fresh-agent
trials (a CV-ranking pilot and an internal policy assistant) classified
both correctly, surfaced a below-threshold bias measurement and an already
retired pinned model, and passed the new checker; all fifteen frictions
were fixed the same day. All **24 packages** pass validation and **807
tests** pass with **60 optional SDK checks skipped**. See the
[note](../research/governance-pack-2026-10-25.md) and the
[record](governance-pack-2026-10-25.md).

## Durable engines that keep ADK's guardrails · 25 October 2026

Restate's ADK plugin journals model calls, but because it answers the model
step itself ADK then skips the agent's model callbacks, every after-model
callback and `max_llm_calls`, and ADK's confirmation resume fails under
it; tools are durable only when their bodies opt in. Dapr's `diagrid`
integration re-implements the agent loop and drops callbacks, plugins,
state and confirmation, under a licence free only for small organisations.
The workflow and guardrails skills now describe both with these
conditions, show how to keep budgets and approvals under Restate, and
treat its awakeable approvals as a durable wait whose id works as a
credential. The kill-after-the-write test, cited but never defined, is now
defined in the API-call skill. A fresh-agent trial asserted each breakage
and built an adapted design that keeps every guardrail (27 tests passed;
ease 3 of 5); nine of its eleven frictions were fixed the same day. All
**23 packages** pass validation and **787 tests** pass with **59 optional
SDK checks skipped**. See the
[note](../research/restate-dapr-comparison-2026-10-25.md) and the
[record](restate-dapr-alignment-2026-10-25.md).

## Third-party evaluation scorers and in-house traces · 25 October 2026

MLflow's ADK scorers, read and then run locally against ADK 2.12, record
results that look like agent failures but are not: trajectory checks over
traces never match because tool names are read from span names, parallel
calls produce a span that errors, a judge failure arrives as "no", and the
hallucination scorer tells its judge the agent has no tools. The evaluation
skill now says to feed scorers from the ADK session and call ADK's own
evaluators for grounded answers. deepeval's ADK hook only exports to its
vendor; its metrics can run offline. The observability skill lists the
switches that keep MLflow and Opik traces and telemetry in-house, and
corrects one rule: OpenTelemetry's `force_flush` returns `True` even after
a failed export. The fresh-agent trial corrected three statements written
from reading alone (8 tests passed with no egress; ease 3 of 5); nine of
its eleven frictions were fixed the same day. All **23 packages** pass
validation and **787 tests** pass with **59 optional SDK checks skipped**.
See the [note](../research/deepeval-mlflow-opik-comparison-2026-10-25.md)
and the [record](deepeval-mlflow-opik-alignment-2026-10-25.md).

## Cost accounting that matches the invoice · 25 October 2026

From LiteLLM's captured ADK traces, checked against ADK 2.12: on `LiteLlm`
routes ADK counts reasoning tokens twice, an `AgentTool` child's calls are
missing from the saved parent session, and `retry_options.attempts`
becomes LiteLLM's `num_retries`, which means something else. The trial
also found that ADK 2.12 writes the same usage on two spans, so summing
every span doubles output. The observability skill now covers all four,
adds offline cost cases and reports a trace's cost as unknown rather than
a partial sum when a call cannot be reconciled; `invocation_summary.py`
detects the double count from the token arithmetic and prices those calls
correctly. In the trial the session-based cost was about a third of the
gateway's (8 tests passed; ease 4 of 5); eight of nine frictions were fixed
the same day. All **23 packages** pass validation and **787 tests** pass
with **59 optional SDK checks skipped**. See the
[note](../research/litellm-comparison-2026-10-25.md) and the
[record](litellm-alignment-2026-10-25.md).

## Vendor memory services that fail silently · 25 October 2026

Mem0's published ADK memory service returns no memories on any error or a
missing key, and writes and reads its app id under different fields, so
recall is empty either way; ADK's own `PreloadMemoryTool` also turns a
failed search into "no memories". The memory skill now requires a vendor
service to report failure, match write and read scopes, read current facts
only (Mem0 and graphiti keep superseded facts by default), and check
erasure against the backend's history, with each library's telemetry
switched off. The inspector no longer reports a custom memory service as
Memory Bank. A fresh-agent trial fixed a vendor-style adapter offline (11
tests passed; the original failed 9; ease 3 of 5); seven of its ten
frictions were fixed the same day. All **23 packages** pass validation and
**786 tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/mem0-graphiti-unstructured-comparison-2026-10-25.md)
and the [record](mem0-graphiti-unstructured-alignment-2026-10-25.md).

## Escalation calibration and cache-safe context trimming · 25 October 2026

Two ideas from the Claude and OpenAI cookbooks, restated for ADK. Escalation
is now measured as a pair, missed escalations as the gate and
over-escalation as the usefulness measure, on cases with a reviewed
expected lane; fixed escalation rules live in code, including a route
before the model. In the trial the code rules alone sent 20% of claims to
review, so a 10% target was unreachable without dropping required
escalations. On context, ADK's built-in sliding filter moves the prompt
prefix every turn so an explicit cache never forms, and on ADK 2.12
`LoadArtifactsTool` puts its artifact list in the system instruction, which
also breaks the cache; the trial lost the customer's order id from turn 4
until the id moved into state. Two trials (28 and 10 tests passed; ease 3
and 3 of 5); eighteen of twenty-four frictions were fixed the same day,
and the guardrails inspector now recognises `before_agent_callback`. All
**23 packages** pass validation and **786 tests** pass with **59 optional
SDK checks skipped**. See the
[note](../research/cookbooks-comparison-2026-10-25.md) and the
[record](cookbooks-alignment-2026-10-25.md).

## Incident regressions with two test lists · 25 October 2026

A regression now names the tests that reproduce the defect
(`fail_to_pass`) and the neighbouring tests the fix could break
(`pass_to_pass`), and resolves only when both lists fully pass, with a
skipped neighbour counted as NOT RUN rather than kept, which is stricter
than SWE-bench. A case is accepted only after a run on the base commit and
a run with a reference fix, after Harbor's oracle and do-nothing agents.
The system designer's ticket template gains a `pass_to_pass` field and
base-commit evidence. In the fresh-agent trial the merged "fix" stopped the
double refund but let one customer refund another's order; the case stayed
red and a reference fix proved the test sound (ease 3 of 5); nine of its
eleven frictions were fixed the same day. All **23 packages** pass
validation and **786 tests** pass with **59 optional SDK checks skipped**.
See the [note](../research/harbor-swebench-comparison-2026-10-25.md) and
the [record](harbor-swebench-alignment-2026-10-25.md).

## Tool fault matrix and resilience checks · 25 October 2026

The evaluation skill now builds a single-fault matrix for each
consequential tool (error, slow, empty, corrupted) from ADK's own
Environment Simulation fields, runs each beside a no-fault twin, checks
the fault actually fired, and scores honesty, partial completion and retry
discipline with checks rather than a judge. After Strands' chaos testing,
whose judges pass a case in which the fault never fired. Strands' steering
was read and left out; it adds nothing the skills lack. A fresh-agent trial
built the suite offline without waiting on the 40-second delay (33 tests
passed; 6 of 6 deliberate breaks caught; ease 4 of 5); eleven of its twelve
frictions were fixed the same day. All **23 packages** pass validation and
**786 tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/strands-comparison-2026-10-25.md) and the
[record](strands-alignment-2026-10-25.md).

## Collateral damage and a do-nothing control · 25 October 2026

The evaluation skill graded an end state by hashing "the relevant tables",
so an agent that also edited another table passed. After AppWorld it now
diffs the whole fixture at table, record and field level with named
ignores, keeps the effective-mutation comparison beside it, and runs a
do-nothing scripted model through every case so a vacuous case shows up.
Live runs record each MCP server's exact version or digest, after MCPMark
declared its unpinned scores not comparable. In the fresh-agent trial the
old check passed 4 of 5 bad agents and the new grader failed all 5; one
was caught only by the whole-store diff (29 tests passed; ease 3 of 5); all
eleven frictions were fixed the same day. All **23 packages** pass
validation and **786 tests** pass with **59 optional SDK checks skipped**.
See the [note](../research/appworld-mcpmark-comparison-2026-10-25.md) and
the [record](appworld-mcpmark-alignment-2026-10-25.md).

## SQL benchmark metrics and Spider 2.0 · 25 October 2026

The SQL skill now explains what BIRD's metrics compute before anyone
reports them: its execution accuracy is set equality, so a reversed
ranking or a duplicated row passes, and Soft-F1 gives partial credit for a
wrong value. The skill's own oracle stays the gate. Spider 2.0-Lite is
described as a capability probe, 205 BigQuery tasks with a deliberately
loose comparison, run only as an approved, capped campaign under a keyless
identity and scored offline. Its upstream set-up uses an Owner key and
unbounded queries. BIRD is linked only, because of its share-alike licence.
A fresh-agent trial built the gate and the probe offline (22 tests passed;
5 of 5 negative controls failed as required; ease 4 of 5); seven of its
eight frictions were fixed the same day. All **23 packages** pass
validation and **786 tests** pass with **59 optional SDK checks skipped**.
See the [note](../research/bird-spider2-comparison-2026-10-25.md) and the
[record](bird-spider2-alignment-2026-10-25.md).

## SQL semantic map as reviewed files · 25 October 2026

The SQL skill now covers keeping the semantic map in reviewed files, in a
layout like WrenAI's, with a CI check that fails on an incomplete or
unsafe definition, a drift comparison against the live schema and a
scheduled duplicate-key check. Any SQL stored in the map is checked again,
fail-closed, after it is expanded into the query. In the fresh-agent trial
WrenAI's own validator caught 2 of 17 broken definitions (5 with
`--strict`), so it can sit beside the gate but not replace it. Saved
few-shot examples are now reviewed candidates, not auto-approved. The trial
passed 48 tests (ease 3 of 5); ten of its eleven frictions were fixed the
same day. All **23 packages** pass validation and **786 tests** pass with
**59 optional SDK checks skipped**. See the
[note](../research/wrenai-comparison-2026-10-25.md) and the
[record](wrenai-alignment-2026-10-25.md).

## Offline leak oracle and policy plugins · 24 October 2026

The sensitive-data skill now adds Microsoft Presidio as a second, offline
check for leaked personal data over every captured sink in tests. The
trial found its "offline" set-up still fetched the Public Suffix List the
first time an email matched; the skill now disables that, and covers the
canary domains Presidio cannot see and how to keep the report from printing
the leaked value. The security skill explains why the community
`AgentGovernancePlugin` cannot replace an agent's tool gate: it sees only
the tool name and arguments, turns every check off when `fail_open=True`
and its engine is missing, and denies a payment a person has just approved
when it runs again on resume. NeMo Guardrails was read and left out. Two
fresh-agent trials (5 passed with all 5 deliberate leaks caught; 19 passed;
ease 3 and 4 of 5); seventeen of nineteen frictions were fixed the same
day, including two new inspector rules. All **23 packages** pass validation
and **786 tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/nemo-presidio-agt-comparison-2026-10-24.md) and the
[record](nemo-presidio-agt-alignment-2026-10-24.md).

## MCP run-time pin and OWASP MCP ids · 24 October 2026

A CI manifest diff misses a remote MCP server that changes a tool
description after deploy. The security skill now pins definitions at run
time through `tool_filter`, which ADK applies on every listing, checked once
per invocation, after CoSAI's MCP guidance; it treats a stdio server in the
agent's container as holding the agent's identity; and it maps findings to
the OWASP MCP Top 10 ids by id and link only, because that list's licence is
unclear. `mcp_tool_inventory.py` gained `--fail-on-diff` (its diff exited 0
on a changed definition) and now pins the MCP Apps fields it already
compared. A fresh-agent trial built the pin against a loopback server that
changes a tool mid-session (12 tests passed; the original wiring failed 8;
ease 3 of 5); eight of its nine frictions were fixed the same day. All **23
packages** pass validation and **785 tests** pass with **59 optional SDK
checks skipped**. See the
[note](../research/owasp-mcp-cosai-ws4-comparison-2026-10-24.md) and the
[record](owasp-mcp-cosai-ws4-alignment-2026-10-24.md).

## CaMeL-style tool gate · 24 October 2026

The security skill's sample capability gate allowed any tool it did not
know and every call when no plan was stored. It now denies by default, with
one policy per write or egress tool, provenance and readers rules after
Google DeepMind's CaMeL research (cited as a pattern; the code is an
unmaintained research artifact and none is used), and an honest account of
what string taint matching cannot see. A fresh-agent trial built the gate
for a mail agent offline (21 tests passed, including a control in which the
ungated agent forwards mail to the attacker; ease 3 of 5) and found that on
ADK 2.12 agent callbacks run again when a confirmation resumes, which
re-froze the plan and refused the confirmed step; all nine frictions were
fixed the same day. All **23 packages** pass validation and **783 tests**
pass with **59 optional SDK checks skipped**. See the
[note](../research/camel-comparison-2026-10-24.md) and the
[record](camel-alignment-2026-10-24.md).

## LlamaFirewall local tool-result screening · 24 October 2026

When tool results may not leave the project, the security skill now covers
LlamaFirewall's Prompt Guard 2 as a local screen with its conditions: it
reads only the first 512 tokens, so results are windowed; its composite
reports scanner errors as a successful allow and reloads the model on every
scan, so the scanner is called directly; its block reason embeds the
screened text. The sensitive-data skill treats AlignmentCheck as a data sink
that sends the whole trace to a remote judge, not a gate. The weights are
under a separate gated licence, so the skills link to them and ship none. A
fresh-agent trial built the screen and a recipient gate offline with a fake
classifier (23 tests passed; ease 3 of 5); nine of its ten frictions were
fixed the same day, including two false readings in the security
inspector. All **23 packages** pass validation and **782 tests** pass with
**59 optional SDK checks skipped**. See the
[note](../research/llamafirewall-comparison-2026-10-24.md) and the
[record](llamafirewall-alignment-2026-10-24.md).

## garak and deepteam red-team runs · 24 October 2026

The security skill said garak only probes model endpoints; its `function`
generator can attack the agent itself through the `Runner`. Two findings
matter for CI. garak exited 0 on hits and on most errors, so the gate reads
its report. And garak's detectors read text only: in the trial an ungated
agent sent 32 emails to an attacker while garak passed every check, so the
gate also reads a sidecar of the tool effects that actually ran. deepteam's
OWASP Agentic preset is documented as a paid, approved campaign with a
pinned Gemini model, telemetry opt-outs and label normalisation. A
fresh-agent trial built the gate offline; it passed a clean run and failed
every canary, including the one garak missed (ease 4 of 5); ten of its
eleven frictions were fixed the same day. All **23 packages** pass
validation and **781 tests** pass with **59 optional SDK checks skipped**.
See the [note](../research/deepteam-garak-comparison-2026-10-24.md) and
the [record](deepteam-garak-alignment-2026-10-24.md).

## Model Armor files and safe template updates · 24 October 2026

Google's Model Armor samples are useful and partly unsafe to copy: the
update samples omit `update_mask`, which overwrites every field (on a floor
setting, its integrated services), and the PDF sample's encoding cannot be
told apart by its own test. The sensitive-data skill now carries the
file-screening contract with a live canary, the masked and idempotent
update, the fields an effective-policy audit reads back, and, from the
trial, the attachment seam in ADK, the stock plugin's text-only screening,
multi-language detection and two corrected claims about ADK 2.12's plugin.
A fresh-agent trial built attachment screening and a one-field template
update offline and passed 42 tests (ease 3 of 5); nine of its eleven
frictions were fixed the same day. All **23 packages** pass validation and
**781 tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/model-armor-dlp-samples-comparison-2026-10-24.md) and
the [record](model-armor-dlp-samples-alignment-2026-10-24.md).

## Google's managed MCP servers (google/mcp) · 24 October 2026

The google/mcp repository is quiet and calls itself demonstration material,
so the skills cite Google's documentation instead. Google runs two kinds of
remote MCP server and only the Google Cloud kind is governed by IAM; IAM can
make those servers read-only for an agent at the platform, and BigQuery's
server caps queries at three minutes and 3,000 rows. The interoperability
skill now explains the two kinds, and the SQL skill carries the read-only
deny, the tool list, the pinned `project_id`, the roles, the truncation
check and when to stay on MCP Toolbox. A fresh-agent trial wired a
synthetic analytics agent offline and passed 11 tests, including a refused
write that never reached the server (ease 3 of 5); ten of its twelve
frictions were fixed the same day from Google's pages. All **23 packages**
pass validation and **781 tests** pass with **59 optional SDK checks
skipped**. See the [note](../research/google-mcp-comparison-2026-10-24.md)
and the [record](google-mcp-alignment-2026-10-24.md).

## MCP exposure on both protocol eras · 24 October 2026

Reading the MCP Inspector, the Python SDK and FastMCP found two errors in
the interoperability skill. An agent served with `to_mcp_server` does not
keep a conversation for clients on the 2026-07-28 revision, which every
current client uses by default: each call starts a fresh ADK session
(reproduced with a scripted model), and no server setting can switch that
revision off. And the inventory helper's fallback for servers that only
speak 2026-07-28 used the wrong version and field names, with a test fixture
that shared the mistake. Both are fixed: the skill shows a hand-built
server with a caller-bound conversation handle and a two-mode in-process
test, and the Inspector CLI is now a CI cross-check with recorded exit codes
and a workflow step. A fresh-agent trial built the contract and CI offline:
9 tests passed on both eras, the Inspector check caught a tampered manifest,
and the conformance suite ran per revision (ease 3 of 5); its eleven
frictions were fixed the same day. All **23 packages** pass validation and
**781 tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/mcp-inspector-sdk-fastmcp-comparison-2026-10-24.md)
and the [record](mcp-inspector-sdk-fastmcp-alignment-2026-10-24.md).

## MCP Apps widgets (ext-apps) · 24 October 2026

ADK attaches an MCP App's UI resource to the event but renders nothing,
never tells servers it supports the UI extension, and ignores tool
visibility, so the model can call tools meant only for the view. The
interoperability skill now says so, with the `tool_filter` and backend rules
that close the visibility gap and a backend-session remedy for servers that
hide UI tools; the inventory reads both meta keys, flags app-only tools and
unreferenced app pages, and treats UI metadata as part of a tool's pinned
definition. The frontend skill has the renderer contract (backend-served
page, a sandbox on a separate origin, CSP from the tool's metadata). A
fresh-agent trial built the case offline against a fake vendor server and
passed 18 tests (ease 3 of 5); nine of its eleven frictions were fixed the
same day, including a wrong claim in the security skill about the
environment a stdio server inherits. All **23 packages** pass validation and
**781 tests** pass with **59 optional SDK checks skipped**. See the
[note](../research/mcp-ext-apps-comparison-2026-10-24.md) and the
[record](mcp-ext-apps-alignment-2026-10-24.md).

## PyRIT injection campaigns · 24 October 2026

PyRIT's A2A target is on its main branch only (1.1.0, the latest release,
does not have it), but its cross-domain injection workflow is released and
can be scored without a model. The security skill now wires a poisoned
document through that workflow with a substring scorer over the tool calls
that actually ran, so a scripted-model run fits the deterministic suite; the
interoperability skill records the A2A target's settings and an offline A2A
route for CI. A fresh-agent trial built the campaign against a synthetic HR
agent: 7 tests passed, the gated agent resisted 5 of 5 attacks in process and
over A2A while an ungated control fell to 4 of 5 (ease 3.5 of 5). It showed
that scoring the A2A task history counts a refused attempt as a success,
which the skill now forbids, and that the security inspector read a
factory-built tool list as safe; its trifecta summary now carries a
`complete` flag. All **23 packages** pass validation and **778 tests** pass
with **59 optional SDK checks skipped**. See the
[note](../research/pyrit-comparison-2026-10-24.md) and the
[record](pyrit-alignment-2026-10-24.md).

## A2UI routes and validation · 24 October 2026

A2UI (now `a2ui-project/a2ui`, still a public preview) reaches an ADK agent
three ways, and only one of them checks payloads against the catalogue on
the agent side, statelessly; the web client accepts unknown components
unless it is given a validation config. The frontend skill now has a ticket
declare the route and where the check runs, says `adk web` in 2.12.0 shows
no custom A2UI widgets on any route, carries the package pins and the
`a2a-sdk<0.4` conflict that `a2ui-adk[a2a]` brings, and says a staged widget
reaches an A2A partner only as ADK metadata; the interoperability skill
gained the sub-agent surface map. A fresh-agent trial planned a
custom-catalogue shopping agent and passed 22 offline tests (ease 3 of 5);
seven of its ten frictions were fixed the same day, two partly and one
left with its reason. All
**23 packages** pass validation and **777 tests** pass with **59 optional
SDK checks skipped**. See the [note](../research/a2ui-comparison-2026-10-24.md)
and the [record](a2ui-alignment-2026-10-24.md).

## Signed A2A agent cards (a2a-samples) · 24 October 2026

The A2A samples repository (quiet since August, read at a pinned commit)
showed that ADK 2.12.0 never verifies a signature on a card it fetches by
URL, and that verifying it yourself switches off ADK's same-origin check. The
interoperability skill now gives both sides: verify with a key set agreed out
of band (never the card's own `jku`), re-pin the origin, sign a copy once at
startup, and treat fields outside the SDK's schema as unsigned. The card
checker gained structural signature checks and a `--fail-on` option for CI,
and the tool-auth skill says where backchannel consent (CIBA) fits. A
fresh-agent trial built both sides offline and passed 18 of 18 tests (ease
4 of 5); its nine frictions were fixed the same day. All **23 packages** pass
validation and **777 tests** pass with **59 optional SDK checks skipped**.
See the [note](../research/a2a-samples-comparison-2026-10-24.md) and the
[record](a2a-samples-alignment-2026-10-24.md).

## Source freshness · 24 October 2026

A new maintainer script, `scripts/check_source_freshness.py`, reports whether
the 44 external repositories the skills cite are still maintained: days since
the last commit (active, quiet or stale, with placeholder thresholds), the
latest release, commits since the commit we read, and anything that needs a
maintainer, such as an archived, renamed or relicensed repository or a pinned
commit that has gone. Its register, `docs/research/source-register.json`, is
validated offline by the repository checks. The first live run found 38 active
and 6 quiet sources, none stale, and four new releases worth a review,
including google-adk 2.13.0. All **23 packages** pass validation and
**767 tests** pass with **59 optional SDK checks skipped**. See the
[record](source-freshness-2026-10-24.md).

## Demo polish · 23 October 2026

The house design now looks like a product rather than a chat widget: an app
shell with conversation history, an empty-state screen, a floating composer
with a data line, folded tool steps, citations that quote their supporting
passage, a Sources panel and an approval card that shows the exact email.
Four invented demo brands (a bank, a retailer, a manufacturer and a health
insurer) apply through the brand override with `apply_brand.py`, which
rechecks contrast and lint, and a new demo-readiness guide covers seeded data,
a labelled replay mode, the golden-path script and the screens around the
chat. Five research notes, including one on what enterprise users expect,
drove the changes. Every house and brand screen renders with no overflow and
0 axe violations. All **23 packages** pass validation and **753 tests** pass
with **59 optional SDK checks skipped**. See the
[before and after](../design/house-theme/before-after-1280-light.png), the
[brands overview](../design/house-theme/brands-overview.png) and the
[record](demo-polish-2026-10-23.md).

## Web-app baseline · 23 October 2026

The designer now gives a proof of concept with its own web interface a
baseline that others can continue: web defaults (a Vite and React app served
by one FastAPI service), a house design system in Google's DESIGN.md format,
named companion skills with pins written once into the project's `AGENTS.md`,
and a web security baseline of 25 rules tagged with OWASP identifiers in six
tiers. A new `adk-fastapi-backend` skill owns the HTTP application around the
agent. Its recipe ran on google-adk 2.12.0 with FastAPI 0.141.1 (the highest
that resolves beside it): 24 scratch-app tests and 8 runtime contracts passed,
including one showing that ADK's own server lets an anonymous client create
and list another user's sessions. The house theme lints clean and renders with
no overflow and no axe violations at three widths in light and dark, where the
stock shadcn theme shows three serious contrast violations. A designer trial
and a paired engineer trial (with and without the `shadcn` companion) found
seven gaps, now fixed. All **23 packages** pass validation and **729 tests**
pass with **59 optional SDK checks skipped**. See the
[proposal](../research/web-app-baseline-proposal-2026-10-22.md), the
[design-system research](../research/house-design-system-2026-10-23.md),
the [screenshots](../design/house-theme/README.md) and the
[trial record](web-app-baseline-2026-10-23.md).

## MITRE ATLAS and the CoSAI Risk Map · 23 October 2026

[ATLAS](https://github.com/mitre-atlas/atlas-data) 2026.09 (commit 3259f38)
and the [CoSAI Risk Map](https://github.com/cosai-oasis/secure-ai-tooling)
(commit 622605a), both Apache-2.0, were read for identifiers only: the
security skill now names eleven ATLAS agent techniques, ten Risk Map risks
and six controls beside the OWASP ids, cited by id with links, and records
that the map's technique mappings still point at the older ATLAS release. A
fresh-agent trial writing a review in that vocabulary rated the work 4 of 5;
eight frictions were fixed the next day, including the security inspector
missing a shared-corpus search as a private source, now covered with a test.
All **22 packages** pass validation and **700 tests** pass with **59
optional SDK checks skipped**. See the
[comparison note](../research/atlas-cosai-comparison-2026-10-23.md)
and the [trial record](atlas-cosai-alignment-2026-10-23.md).

## Snyk Agent Scan · 23 October 2026

[snyk/agent-scan](https://github.com/snyk/agent-scan) (formerly mcp-scan;
commit 73c0966, Apache-2.0 code under Snyk's terms) was documented, not run,
because running it uploads configurations, tool descriptions and skill
content to Snyk: the security skill names it as pinned optional evidence
beside the allow-list, recorded definitions and hash pin, with its local
`inspect` mode, its CI exit codes, its experimental-output caveat and the
container-only rule, and the testing guide names an optional maintainer scan
of the packages as a choice. A fresh-agent trial adopting a vendor's stdio
server with a mandated scan rated the work 4 of 5; six frictions were fixed
the same day, including one canonical pin format across the security and
interoperability skills. All **22 packages** pass validation and **699
tests** pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/agent-scan-comparison-2026-10-23.md)
and the [trial record](agent-scan-alignment-2026-10-23.md).

## Designer proposals from the research memo, tested · 23 October 2026

The integration memo's eight proposals for the system designer's templates
were treated as hypotheses: one synthetic design, two designer trials (the
current ticket template against a prototype carrying every proposal), and
two engineer trials carrying out the first ticket of each set. Adopted into
the ticket template: `touches` and `parallel_safe` with definitions, a
`docs` list, EARS wording for acceptance items with a `(floor)` tag,
automated and manual verification split with the interpreter named,
per-item evidence with a `Rulings:` list and a `done` rule, and optional
`contract_deltas`. Declined: a `reference_patterns` field, a `constraints`
pointer, a project-instructions goal in every plan, and companion lines in
every ticket (the lead-method rule now lives once in the handoff reference).
Both trial pairs also asked for the same repairs to the existing template,
now made, and found a comment-parsing bug in the schedule helper, fixed with
a test. All **22 packages** pass validation and **699 tests** pass with
**59 optional SDK checks skipped**. See the
[research note](../research/phase-d-designer-proposals-2026-10-23.md)
and the [trial record](phase-d-designer-trials-2026-10-23.md).

## Pydantic AI, LangGraph and companion collections · 23 October 2026

Four documentation sources were read for rules and shapes, none imported as
code. [Pydantic AI](https://github.com/pydantic/pydantic-ai) (commit
eb0bd08, MIT) gave the tool-interface skill the two kinds of deferred call,
the evaluation skill span-based trajectory grading, and the observability
skill the shape of an online evaluator. LangGraph's
[rules of interrupts](https://github.com/langchain-ai/docs) (commit 23152b1,
MIT) are restated for ADK's resumable nodes in the workflow skill. Google's
coding-with-AI page and the [AGENTS.md](https://github.com/agentsmd/agents.md)
convention give the engineer's composition reference the three channels for
ADK context and where a project's standing agent instructions live;
[Superpowers](https://github.com/obra/superpowers) and
[Matt Pocock's skills](https://github.com/mattpocock/skills) were read as
inputs to the designer trials, with Kiro's EARS template. Their journeys are
covered by the durable-execution, observability and designer trials. See the
[Pydantic AI note](../research/pydantic-ai-docs-comparison-2026-10-23.md),
the [LangGraph note](../research/langgraph-interrupts-comparison-2026-10-23.md)
and the [companion collections note](../research/companion-collections-comparison-2026-10-23.md).

## Memory Bank revisions, LongMemEval and Docling · 23 October 2026

Three memory sources read for the memory skill: Google's "Memory revisions"
page (updated 2026-10-21) for the consolidation outcomes, `previous_revision`,
`rollback` and `revision_labels` that the reconciliation table and erasure
rules now rest on; [LongMemEval](https://github.com/xiaowu0162/LongMemEval)
(commit 9e0b455, MIT; no data imported) for the five abilities a memory gold
set is structured by; [Docling](https://github.com/docling-project/docling)
(2.142.0, MIT) as the extractor to reach for behind the ingestion inventory.
A fresh-agent trial fixing a stale address and a planted memory rated the
work 3 of 5; six frictions were fixed the same day from the installed
2.12.0 package, including a sample request that had disabled the revisions
the rollback path needs. All **22 packages** pass validation and **699
tests** pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/memory-sources-comparison-2026-10-23.md)
and the [trial record](memory-sources-alignment-2026-10-23.md).

## Temporal and DBOS ADK integrations · 23 October 2026

[temporalio/ai-integrations](https://github.com/temporalio/ai-integrations)
(`python/google_adk`, commit bb179c3, MIT; package 0.0.1, pre-release) and
[dbos-google-adk](https://github.com/dbos-inc/dbos-google-adk) (commit
288757e, MIT; 0.1.0) were read beside Google's resume page. The workflow
skill now states that ADK resume runs tools at least once and needs a
caller, lists each engine's facts that change a design (Temporal's MCP
toolset needs SDK 1.x, its history records activity arguments, replays
re-record telemetry; DBOS wants Postgres and declares an older ADK floor),
names both engines' replay tests as the shape of a determinism regression
test, and gives the choice order with the kill-after-the-write acceptance
test; the designer records the three-way decision and the safe-API skill
says why the idempotency key survives an engine. LangGraph's four rules for
code around a pause and pydantic-ai's framing joined the same section. A
fresh-agent trial deciding for a days-long refund approval rated the work
3 of 5; four frictions were fixed the same day, among them routing rows
that now name durable execution. All **22 packages** pass validation and
**699 tests** pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/durable-execution-comparison-2026-10-23.md)
and the [trial record](durable-execution-alignment-2026-10-23.md).

## Approval, screening and compaction rules from other frameworks · 23 October 2026

Two documentation sources were read for rules, not code:
[OpenAI's Agents SDK docs](https://github.com/openai/openai-agents-python)
(commit 841dfdd, MIT) and two
[Microsoft Agent Framework decision records](https://github.com/microsoft/agent-framework/tree/main/docs/decisions)
(commit 0200599, MIT). The guardrails skill now rejects an approval left
unanswered when the next invocation starts and fails closed on arguments a
rule cannot read, with the ADK hook named; the security skill carries four
placement rules for any screening layer; the evaluation skill asks for a
strict scripted model that fails on extra or missing model calls; the
optimise skill treats a function call and its results as an atomic group
and names three compaction points. A fresh-agent trial fixing a refund
approved after a weekend and a screen that ran beside the tool rated the work
4 of 5; seven frictions were fixed the same day. All **22 packages** pass
validation and **698 tests** pass with **59 optional SDK checks skipped**.
See the [comparison note](../research/approval-and-screening-rules-comparison-2026-10-23.md)
and the [trial record](approval-and-screening-rules-alignment-2026-10-23.md).

## OpenTelemetry GenAI conventions and conformance · 23 October 2026

The GenAI conventions' new home
([semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai),
commit 9ffc7e0) ships a reference scenario for google-adk with a list of the
violations a conformant export is expected to show; the observability skill
now carries that list as data, the rule to key dashboards on the registry
names rather than the removed `gen_ai.system`, a drift check that works
without the unpublished conformance runner, and the `gen_ai.evaluation.result`
event as the way to put judge scores on traces. A fresh-agent trial rekeying
dashboards and building the drift check rated the work 3 of 5; six frictions
were fixed the same day. All **22 packages** pass validation and **698
tests** pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/otel-genai-conformance-comparison-2026-10-22.md)
and the [trial record](otel-genai-conformance-alignment-2026-10-23.md).

## Promptfoo · 22 October 2026

[promptfoo](https://github.com/promptfoo/promptfoo) (commit 15bcb0d, MIT;
npm 0.124.1) was read for its ADK 2.x guide and its exit codes were
observed with the `echo` provider rather than taken from the docs: 100 on a
failed test, 0 under a cleared pass-rate threshold, 0 on all pass. The
evaluation skill carries the in-process Python provider shape, the
trajectory and trace assertion types, the tracing configuration keys and
the content-gate dependency; the release skill maps the exit codes onto the
gate vocabulary with the two traps an empty suite and errored rows set; the
observability skill notes the guide's dependence on ADK-owned span keys. A
fresh-agent trial wiring a nightly gate rated the work 3 of 5; six frictions
were fixed the next day, including the 2.12.0 model-span name read from the
installed package. All **22 packages** pass validation and **699 tests**
pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/promptfoo-comparison-2026-10-22.md)
and the [trial record](promptfoo-alignment-2026-10-23.md).

## AgentDojo · 22 October 2026

[AgentDojo](https://github.com/ethz-spylab/agentdojo) (v0.1.35, commit
089ed46, MIT) was read for its injection goal classes, not its data: four
attributed synthetic cases and fixtures joined the security skill's
adversarial asset (a split transfer from a poisoned bill, a bulk post-out
from a channel message, a security code forwarded and the trace deleted, a
reservation steered by a review), with the benchmark's important-instructions
envelope restated and its end-state grading noted as the asset's own
discipline; the live attack-success-rate route is written as an approved
paid campaign, version-conditionally. A fresh-agent trial extending a
workspace assistant's suite rated the work 4 of 5; seven frictions were
fixed the next day, including the confirmation protocol's wire shape read
from the 2.12.0 flow. All **22 packages** pass validation and **699 tests**
pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/agentdojo-comparison-2026-10-22.md)
and the [trial record](agentdojo-alignment-2026-10-22.md).

## kubernetes-sigs/agent-sandbox and GKE Agent Sandbox · 22 October 2026

The controller behind `GkeCodeExecutor`'s sandbox mode
([agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) v1.0.7,
Apache-2.0) and Google's GKE sample were read with the GKE install page and
the GA announcement: the security skill carries the CRDs, the version floor
and flag, the admission policy as a table, the 2.12.0 executor's sandbox
parameters and install extra, and the examples a design can cite as checks;
the deploy skill carries Google's Terraform identity layout, the cluster-side
rules and where warm pools bill; the optimise skill the warm-pool line. A
fresh-agent trial moving a data helper to sandbox mode rated the work 3 of
5; seven frictions were fixed the next day. All **22 packages** pass
validation and **699 tests** pass with **59 optional SDK checks skipped**.
See the [comparison note](../research/agent-sandbox-comparison-2026-10-22.md)
and the [trial record](agent-sandbox-alignment-2026-10-22.md).

## A2A TCK, AG-UI 1.0 and the CopilotKit example · 22 October 2026

Two protocol sources closed on the same day. The
[A2A TCK](https://github.com/a2aproject/a2a-tck) (v0.2.5, commit 5daf014,
Apache-2.0) was read, not run, because it is not published to PyPI: the
interoperability skill now carries the scoped MUST run against a local
`to_a2a` instance, the requirement ids as a table, what the kit cannot test
on a real agent, and the origin-pinning rule for raw SDK clients; the
designer's handoff writes the A2A acceptance as planned verification. The
fresh-agent trial exposing a triage agent (3 of 5) surfaced what the 0.3-era
material lacked, fixed the next day from the pinned SDK: a 1.0 card example
generated from a2a-sdk 1.2.3, the 2.12.0 `to_a2a` signature with its new
security parameters, an inbound-authentication recipe with the executor's
principal rule, and a card checker that keeps scheme names and accepts the
1.0 requirement key (with tests).
[AG-UI 1.0](https://github.com/ag-ui-protocol/ag-ui) (commit 85a427d, MIT)
and the CopilotKit ADK example gave the frontend skill the two approval
contracts the `ag-ui-adk` middleware implements behind one flag, their
enforcement codes, and after the trial (4 of 5 finding, 3 applying) the wire
shapes a test needs. All **22 packages** pass validation and **698 tests**
pass with **59 optional SDK checks skipped**. See the
[TCK comparison](../research/a2a-tck-comparison-2026-10-22.md), the
[AG-UI comparison](../research/ag-ui-copilotkit-comparison-2026-10-22.md)
and the trial records for the [TCK](a2a-tck-alignment-2026-10-22.md)
and [AG-UI](ag-ui-copilotkit-alignment-2026-10-22.md).

## tau2-bench and Inspect AI · 22 October 2026

Two evaluation harnesses were read for method, not data.
[tau2-bench](https://github.com/sierra-research/tau2-bench) (commit 05736c2,
MIT) gave the evaluation skill the unbiased pass^k rules (refuse `k` above
the trial count, keep infrastructure failures out of the denominator, define
success from the whole reward), a new section on grading the end state by
replaying one reference trajectory on a fresh backend, the multiplicative,
premature-stop and missing-criterion rules, and the release skill the public
precedent that a judge change starts a new baseline.
[Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) (commit c2fc3d9,
MIT) added the NaN-on-short reducers, `at_least`, Krippendorff's α for judge
agreement, and one proven integration: a spike outside the repository showed
`agent_bridge()` intercepting a google-adk 2.12.0 agent's model calls under
the mock model, with streaming as the limit. A fresh-agent trial building a
reliability gate for flaky booking evals rated the work 3 of 5; seven
frictions were fixed the next day, including a false claim about reversible
mutations and the google-genai provider selector. All **22 packages** pass
validation and **697 tests** pass with **59 optional SDK checks skipped**.
See the [tau2-bench comparison](../research/tau2-bench-comparison-2026-10-22.md),
the [Inspect comparison](../research/inspect-ai-comparison-2026-10-22.md)
and the [trial record](tau2-bench-alignment-2026-10-22.md).

## MCP specification revisions and ext-auth · 22 October 2026

The [MCP specification](https://github.com/modelcontextprotocol/modelcontextprotocol)
revisions 2025-11-25 and 2026-07-28 (commit 80041ab) and
[ext-auth](https://github.com/modelcontextprotocol/ext-auth) (commit fb374c7)
were read for the rules that change a recommendation: tool-name bounds,
validation errors as tool execution errors and the schema-dialect gap for the
tool-interface skill; the stateless protocol's two design consequences
(server-minted state handles are model-visible data, deterministic listing
is a cache contract), discovery, registration priority and issuer binding for
the interoperability skill; issuer-keyed registrations, `iss` validation and
Enterprise-Managed Authorization for the tool-auth skill. A fresh-agent
trial moving a triage agent to a vendor's remote MCP server with enterprise
sign-on rated the work 4 of 5; its frictions were fixed the next day,
including the inventory helper's URL-keyed manifest diff (now by name, with
a test) and the 2.12.0 flag that selects the modern connect path. All
**22 packages** pass validation and **697 tests** pass with **59 optional
SDK checks skipped**. See the
[comparison note](../research/mcp-spec-ext-auth-comparison-2026-10-22.md)
and the [trial record](mcp-spec-ext-auth-alignment-2026-10-22.md).

## GoogleCloudPlatform/generative-ai ADK blueprints · 22 October 2026

Four blueprints under [generative-ai `agents/adk/`](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/agents/adk)
(commit 3a716a8, Apache-2.0) were read beside two Google product pages:
the zero-trust pair (signed writes, a hermetic sandbox, a deterministic
gateway, and the eight-refund aggregate exploit that shows why the bound
lives in code), the agent quality flywheel (a rubric metric paired with a
deterministic one) and the contract-compliance pipeline (a deterministic
policy service as an A2A peer). Semantic Governance Policies were confirmed
as a Preview product with the vendor's own accuracy caveat; Agent Anomaly
Detection was not, and the blueprint's version is recorded as a simulation.
The facts went to seven specialists at the decisions they change. A
fresh-agent trial hardening a refund path after two incidents rated the
work 3 of 5; eight frictions were fixed the same day, including the
guardrails inspector's rejection of a pin with an extras marker, which now
has a test. All **22 packages** pass validation and **696 tests** pass
with **59 optional SDK checks skipped**. See the
[comparison note](../research/generative-ai-agents-comparison-2026-10-22.md)
and the [trial record](generative-ai-agents-alignment-2026-10-22.md).

## MCP conformance suite · 22 October 2026

The MCP project's [conformance suite](https://github.com/modelcontextprotocol/conformance)
(npm `0.2.0-alpha.12`, commit c37eec8) was not only read but run, outside
the repository, against a scripted-model ADK 2.12.0 server on loopback:
requirement sets per revision, the fixture-dependent scenarios that fail on
a business server by design, the scenarios the ADK server passed, and the
baseline file's three exit paths (new failure, excused failure, stale
entry) were all observed before being written. The interoperability skill
gained a protocol-conformance section and the pinned command; the release
skill a tier 1 gate; the designer an acceptance phrase. A fresh-agent trial
exposing a research agent with a CI check rated the work 4 of 5; nine
frictions were fixed the same day, among them the 2.x server bind
signature and the two `server-stateless` check ids. All **22 packages**
pass validation and **695 tests** pass with **59 optional SDK checks
skipped**. See the
[comparison note](../research/mcp-conformance-comparison-2026-10-22.md)
and the [trial record](mcp-conformance-alignment-2026-10-22.md).

## google/adk-python main · 22 October 2026

The ADK repository itself ([google/adk-python](https://github.com/google/adk-python)
at commit ed76f94, Apache-2.0) was read for what the 2.8.0 baseline could
not show: the code-execution environment layer (`EnvironmentToolset` and its
local, Vertex, Daytona, E2B and OpenSandbox backends with their first
versions and maintenance state), the GKE executor's Agent Sandbox mode, the
Agent Engine and Cloud Run sandbox executors' constructor cases and
defaults, how input files reach an executor and how a tool stages one, the
maintainer skill's anti-flake habits for Runner tests with the 2.12.0
signatures those tests depend on, the SQLite memory service, the bundled
BigQuery skills and the reference wiring samples. A fresh-agent trial
choosing an execution environment for a data helper rated the work 3 of 5
because the SDK shapes were missing; seven frictions were fixed the same day
from the installed 2.12.0 package, and an inspector rule for execution
toolsets is recorded as owed. All **22 packages** pass validation and
**695 tests** pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/adk-python-main-comparison-2026-10-22.md)
and the [trial record](adk-python-main-alignment-2026-10-22.md).

## BigQuery Agent Analytics SDK · 22 October 2026

Google's [BigQuery Agent Analytics SDK](https://github.com/GoogleCloudPlatform/BigQuery-Agent-Analytics-SDK)
(v0.6.1, Apache-2.0) is the read side of the `agent_events` table the
observability skill tells an agent to write, and it now has a section of its
own there: what it reconstructs, its seven deterministic evaluators and judge
metrics, the CLI with exit 0, 1 and 2, continuous-query templates and the
reservation they need, the labels on every job it submits, its documented
call shapes and flag names, and three caveats it states about itself (no
thought tokens in its cost figure, a cache metric that passes on missing
telemetry unless told to fail, a `pass^k` formula that differs from the
unbiased estimator). The release skill gained a fourth gate over stored
production sessions with those exit codes mapped to promote, block and NOT
RUN, the rule for a gate that must exist before its baseline is measured,
and drift detection, graduation and saturation as triggers for the decisions
it already defines. A fresh-agent trial building a nightly production gate
and a monthly coverage report rated the work 3 of 5 because the call shapes
were missing; they were added the same day, with the five other frictions.
All **22 packages** pass validation and **695 tests** pass with **59
optional SDK checks skipped**. See the
[comparison note](../research/bigquery-agent-analytics-sdk-comparison-2026-10-22.md)
and the [trial record](bigquery-agent-analytics-sdk-alignment-2026-10-22.md).

## MCP Toolbox for Databases · 22 October 2026

Google's [mcp-toolbox](https://github.com/googleapis/mcp-toolbox) (formerly
genai-toolbox, v1.14.0, Apache-2.0) was read as the executor the SQL
specialist had described only generically. The SQL skill now carries a
Toolbox branch checklist that maps its four boundaries onto Toolbox
configuration: read-only enforced at the database engine through the
connection string rather than a prompt or a `SELECT` check, the BigQuery
flags and the `allowedDatasets` analysis with what it cannot analyse, the
prebuilt free-form tool's own "not for production agents" note, basic over
template parameters with the vendor's injection warning, tenant ids as
secure parameters the model never sees, and the three bypass statements
(CTE delete, writing UDF, `COMMIT;` chaining) as deterministic fixtures.
The interoperability, security, sensitive-data and auth skills gained the
client's protocol pin and credential strategies, the `readOnlyHint`
enforcement note, the Google paths that screen tool traffic outside the
agent, and the IAP assertion facts. Two memo claims were corrected against
the sources: the Toolbox Model Armor page's ADK sample does not screen tool
results, and ADK's own plugin gained tool-output screening in 2.12.0. A
fresh-agent trial carrying out a tenant-scoped Toolbox ticket rated the
checklist 4 of 5 and its six frictions were fixed the same day. All **22
packages** pass validation and **695 tests** pass with **59 optional SDK
checks skipped**. See the
[comparison note](../research/mcp-toolbox-comparison-2026-10-22.md) and
the [trial record](mcp-toolbox-alignment-2026-10-22.md).

## Google's ADK recipes · 22 October 2026

Google's [adk-recipes](https://github.com/google/adk-recipes) repository
(commit `be63596`, Apache-2.0, "not production use") was read recipe by
recipe against the specialists. Eleven packages gained facts at the decision
each serves, every one cited to the recipe file and labelled a vendor sample:
the long-horizon harness's write-back memory loop with its own honesty notes,
its repeated-failure signature and halt plugin, its guard shape with argv
classification and grant narrowing, its evalsets as case and rubric templates,
and its callback chain written down as the contract; the ambient expense
agent's deterministic-first graph with the pause on the review node; the
three managed RAG recipes and the inspection point that one of them bypasses;
and the staged-widgets recipe, whose two ADK facts behind duplicate and
vanishing widgets were confirmed in the ADK source. The Ambient Quality Agent
was routed, not rebuilt: adk-release-engineering decides whether its insights
gate a release and counts a missing investigation as incomplete evidence, and
the extension's `agents-cli-aqua` skill joins the engineer's and designer's
mappings. Three fresh-agent trials, a post-launch quality loop ticket, a
memory write-back design and a widget pipeline fix, rated the work 4, 3 and 4
of 5; their fourteen frictions, among them a missing routing row for widgets,
the absent write-back sequence and accessor names in the memory skill, and
the callback-context and parallel-merge facts, were fixed the same day with
the ADK facts confirmed in source. All **22 packages** pass validation and
**695 tests** pass with **59 optional SDK checks skipped**. See the
[comparison note](../research/adk-recipes-comparison-2026-10-22.md) and the
[trial record](adk-recipes-alignment-2026-10-22.md).

## Drift fixes against ADK 2.12 and current upstreams · 22 October 2026

Fourteen facts the skills carried had drifted since the early-October check,
and each was re-verified against its primary source before the text changed:
the ADK source at main with tags 2.8.0 and 2.12.0, the changelogs of
OpenInference, AG-UI, A2A and agents-cli, the mcp-toolbox and Horizon READMEs,
the python-sdk v2 notes and the Vertex model lifecycle page. Three change what
the skills assert. ADK 2.12.0 stops OAuth2 secrets reaching the serving
endpoints and takes the user id only from an authenticated principal, so the
security and auth skills now set 2.12.0 as the floor for an agent that serves
several users or holds delegated credentials. The `adk eval` exit code is
stated version-conditionally: 0 on every release through 2.12.0, 1 on
failures from an unreleased main commit, confirmed by a deliberately failing
case on the pinned version, with the pytest gate kept primary. And ADK 2.9.0's
rule that a failed workflow node re-runs on resume now sits in the workflow
runtime reference and makes the idempotency rules in safe-api-tool-calls
load-bearing. The rest are version and tense corrections: the OpenInference
instrumentor's 2.10 floor and its fixed workflow spans, the new home of the
GenAI OTel instrumentation, AG-UI 1.0 and ag-ui-adk 0.11.0 with its security
fix, the mcp-toolbox rename, python-sdk v2's `MCPServer` rename, A2A 1.0.1,
the Horizon recipe's real ADK version, and `gemini-2.5-flash` as retired on
Vertex rather than retiring. Two memo claims did not survive verification and
were not imported. All **22 packages** pass validation and **695 tests** pass
with **59 optional SDK checks skipped**; no helper, test or `last-tested`
date changed. See the [drift record](../research/drift-fixes-2026-10-22.md).

## Agents CLI 1.11.0 alignment · 22 October 2026

The September integration with Google's Agents CLI was re-checked against
version 1.11.0, with the same fact import the Google cloud skills received
the day before. No command in this toolkit's text was wrong, but citations
named versions 1.5 to 1.8, the publish command and product name had moved,
and the recipe repository was renamed to `adk-recipes`. Three contradictions
between our text and the CLI's behaviour were settled against the
documentation first: the Agent Gateway binding can change after creation
(our claim was wrong and is replaced), the invoker role for Gemini
registration stays as documented, and the Agent Identity baseline role is
recorded both ways. Fourteen specialists gained facts from the code
cheatsheet, the evaluation skill and the deployment skills, each verified on
adk.dev or the Agent Platform pages where it changes a statement; each names
the Agents CLI skill that operates its mechanism at the decision it serves;
and the composition reference now says how to settle Google's own
disagreements. Two fresh-agent trials on one synthetic 1.11.0 project, a
deployment ticket under Terraform ownership and a focused memory change,
behaved as intended and rated the cross-collection work 3 and 4 of 5; their
five frictions were fixed the same day. All **22 packages** pass validation
and **695 tests** pass with **59 optional SDK checks skipped**. See the
[trial record](agents-cli-1-11-alignment-2026-10-22.md).

## Production cost contract and BigQuery cost facts · 21 October 2026

At MVP profile and above, cost is now a contract like any other requirement:
a ceiling at a stated volume, split into the per-request work and the fixed
cost of the provisioned resources the design keeps, with the billing export
as its authority, a stop that acts without a person as its enforcement, what
degrades first, and a goal in the first live week that reads the bill. A
billing budget alert is evidence, never the cap. Every owned resource carries
labels, and the plan's Later table always holds the recurring cost review and
the decommission item. The SQL and memory specialists also gained the
BigQuery facts an agent application trips over, each verified on Google's
pages: the per-user result cache that reviewed templates hit and generated
SQL never does, job labels, custom daily quotas, clustering order from real
predicates, the `MERGE` pattern for a partitioned history table, and which
cost control applies under on-demand versus editions pricing. A fresh-agent
trial designing a production claims assistant under a sponsor's ceiling wrote
the six-field contract, the labels, the first-bill goal and the decommission
item unprompted and rated the part 4 of 5; a second trial carrying out a
ticket for a SQL agent whose bill had tripled added the pre-execution ceiling,
the attribution labels and the cache-friendly query text from the new
references and removed the timestamp instruction that defeated the cache. The
five frictions the two trials found were fixed the same day. All **22 packages** pass validation and **695 tests**
pass with **59 optional SDK checks skipped**. See the
[trial record](cost-contract-and-bigquery-2026-10-21.md).

## Resource cost floor and teardown goals · 21 October 2026


A colleague's RAG prototype once left a Vector Search deployed index running
after the demo; the bill arrived weeks later for a service nobody used. The
floor that every profile keeps now covers resources that charge while
provisioned, not only model calls: a goal creates one only after recording
its idle cost with the pricing date, its cleanup command and how absence is
verified. A new resource cost ledger in the designer lists twenty such
resources (Cloud Run minimum instances, Agent Runtime, Vector Search, the RAG
Engine managed database, Cloud SQL and AlloyDB with their backups, Memorystore,
BigQuery reservations, Cloud Storage soft delete, GKE, load balancers,
Cloud NAT, Provisioned Throughput and more), each verified against Google's
pricing page on the date shown, with what people forget and how to prove it
is gone. Goals and tickets carry a **Resources created** block; a phase whose
resources are not kept ends with a teardown goal whose acceptance is "absent,
or retained with an owner" per resource and a billing readback; and
`adk-engineer` writes the deletion script beside the creation script in the
same change. A fresh-agent trial designing a three-day Vector Search proof of
concept wrote the resource rows and the teardown goal unprompted and rated the
mechanism 4 of 5; a second trial carrying out a ticket that creates a Cloud
SQL instance shipped the deletion script beside the creation script with an
ownership journal, scope refusal and dry-run tests, and recorded the instance
as absent with its price left honestly unfilled. The eight frictions the two
trials found, among them a ticket status vocabulary three earlier trials had
asked for, were fixed the same day. All
**22 packages** pass validation and **695 tests** pass with **59 optional SDK
checks skipped**. See the
[trial record](resource-cost-floor-2026-10-21.md).

## Google Cloud skills alignment · 21 October 2026


Google's [skills collection](https://github.com/google/skills) (about 170
product skills: gcloud, IAM, Cloud Run, GKE, monitoring, databases, Agent
Platform) was compared with every specialist. The result is a division of
labour, not a merge: a goal names the product skill it needs as
`google/skills:<name>`, the designer's handoff and the engineer's composition
reference carry the mapping, and `adk-engineer` treats a missing one like a
missing specialist. Nineteen packages also gained facts that change an ADK
decision, each cited to the page that confirmed it or labelled vendor
guidance; the largest replaces the statement that a dedicated Agent Runtime
identity was not implemented with the Agent Identity mechanism. A
[comparison note](../research/google-skills-comparison-2026-10-21.md)
records what was imported, routed and left out. Two fresh-agent trials, one
carrying out a ticket whose two product skills were not installed and one
designing a production application in one pass, both rated the mechanism
4 of 5; the engineer showed the install commands without inventing the
skills' content and kept private ingress, and the designer wrote the product
skills into the right goals without fetching anything. The four mapping gaps
they found were fixed the same day. All **22 packages** pass validation and
**695 tests** pass with **59 optional SDK checks skipped**. See the
[trial record](google-skills-alignment-2026-10-21.md).

## Discovery and presenter · 15 October 2026


Two skills now bracket the design-and-build journey. `adk-discovery` runs
before the designer when a company has only an area in mind, or no use case
at all: it finds where the journey breaks or maps KPIs to the processes that
drive them, gives every opportunity a technology fit (agent, single LLM call,
classical machine learning, rules, or a process change), ranks the portfolio
with a helper, and hands the designer a brief with the first use case, its
measure, baseline and counter-metric. `adk-presenter` runs at every phase
boundary that needs a decision: proof-of-concept approval, the
proof-of-concept review with a production decision, the final results
review, and a public case study, each for a business and a technical
audience, built from the plan's recorded evidence with a citation under
every claim. The designer plans those presentations as goals and reads a
discovery brief as answered scope; the router sends both kinds of request to
the right skill. Four dated research notes record the sources behind the
discovery method, the technology triage, the presentation practice and
Google's co-marketing rules. All **22 packages** pass validation; the
offline suites run **688 tests** with **59 optional SDK checks skipped**,
including 26 tests for the two new helpers. Two fresh-agent trials, one
simulating a product owner for the discovery conversation and one
preparing both production-approval decks from a synthetic plan, rated the
skills 3 and 4 of 5 for ease and produced 36 friction items; the
contradictions and gaps they found were fixed the same day. A second round
added speech and slide-craft references to the presenter and a stall-causes
check to discovery from three further research notes. Two end-to-end trials
then took a rough idea and a no-use-case business through every stage, from
discovery to the case study; every handoff carried what the next stage
needed, no slide carried an unsourced number, and the friction they found
was fixed. All **22 packages** pass validation and **695 tests** pass with
**59 optional SDK checks skipped**. See the
[trial record](discovery-and-presenter-2026-10-15.md).

## Human-effort estimates · 9 October 2026

Every planned goal and ticket now carries the human hours it needs when
working with a coding agent. The hours are split into hands-on time and time
to review and verify the change, and waits such as security reviews are listed
separately. A new helper, `check_schedule.py`, adds up the plan and checks
tickets against it. It works out each person's load, the longest chain of
dependent goals and a finish range in working days, so plans quote computed
figures rather than mental arithmetic. The router flags a ticket whose
estimate is clearly too small and records the review hours still owed.

- **Blind comparison:** across six scenarios, a blind grader preferred the new
  skills **every time** (132 against 92 points of 150; 20 of 24 assertions
  passed against 5).
- **Four repair rounds**, each checked by an independent recomputation, fixed:
  - finish dates that ignored dependencies;
  - a reserve counted twice;
  - plans adjusted to make the numbers fit;
  - overweight POC documents.

Failure coverage is built from two grids rather than recalled: every external
system and every action the agent takes, each cell citing the test that covers
it. A fresh reviewer then checks the plan's prerequisites and claims before
handover. Across three runs per version, the share of failure situations
covered by every run rose from 20 to 42 of 47. Plans open with a one-page summary for the person who decides, and each fact
has one home. That cut a production plan from about 16,000 words to 9,000.
Because a word limit made the model drop safety content, plans cut repetition
instead, never tests or failure analysis. Judgement in long production plans,
such as whether every dependency the text mentions is in the schedule, is
still imperfect. See the
[measurement record](effort-estimates-2026-10-09.md).

## Delivery constraints · 9 October 2026

The designer now asks how much time, how many people and how much money there
are, and what data the agent touches, before sizing anything. It plans a proof
of concept, an internal tool, an MVP and a production service at different
depths, keeps a small safety floor in all of them, checks phase 1 against the
team's hours and writes later phases for when the team has time. The router
builds a goal at its stated profile and records what it deliberately left out.
In seven fresh-session scenarios, from a five-hour solo demo to a four-month
bank launch, a blind grader preferred the new skills **every time** (159
against 126 points of 175; 26 of 30 pre-registered assertions passed against
7). A second round shortened proof-of-concept documents by about half. See the
[measurement record](delivery-constraints-2026-10-09.md) for
the scenarios and limits.

## Fresh-session before/after · 9 October 2026

The six journeys were rerun in fresh headless Claude Code sessions, with the
skills installed by the real installer, once with the skills before the product
pass and once after. A blind grader preferred the after version in **all six**
tasks (127 against 106 points of 150), mostly because more of each request was
completed and the user was told what to do next. The runs also showed that a
user-level install takes precedence over a project install of the same skill,
and that the helpers scanned the installed skills themselves; both are now
handled. One run per task, one fixture and a model grader: see the
[measurement record](before-after-2026-10-09.md) for the limits.
**20 packages** pass validation; **644 tests** pass with **59 optional SDK
checks skipped**.

<details>
<summary>Earlier revisions, 25 September to 9 October 2026</summary>

## Usage journeys and product pass · 9 October 2026

The README is now built around two journeys: design a new application with
`adk-system-designer`, or maintain one with `adk-engineer`. Both were tried by
fresh agents on a fixture app with planted defects: one greenfield design
conversation and five maintenance tickets. Every ticket routed to the intended
specialist. The trials found a missing next-step prompt after the first goal,
no native ticket format, lost review documents when a long change was
interrupted, and two inspectors that missed tools referenced as `module.fn`.
Each goal now carries its primary and supporting skills and its own run prompt,
a ticket template was added, the router reads tickets and names the next one,
and the helper defects were fixed with regression tests. All **20 packages**
pass validation; **643 tests** pass with **59 optional SDK checks skipped**.
Four of six friction logs were reconstructed after usage limits interrupted the
agents, and the new skills were loaded from files rather than discovered by a
fresh host; see the [journey record](usage-journeys-2026-10-09.md).

## Designer and router alignment · 8 October 2026

The system designer now routes to all seven cross-framework specialists and
raises their design-level decisions during the architecture conversation:
topology by boundary, tool source, the model's interface as a contract, the
per-agent exposure check, context-window shaping, versions as release
artefacts, output contracts and observability as design obligations. The entry
skill gained composition guidance for the overlap with Google's agents-cli
lifecycle skills. The dated model and vendor pages were re-read the same day
with no material change. See the
[alignment notes](../research/ai-engineering-practices-gap-review.md).

## Interoperability specialist · 8 October 2026

The third and final round of the practice review added `adk-agent-interoperability`
for the process boundary: tool-source selection, consuming and exposing MCP
servers, the in-process versus remote topology decision, remote A2A agents and
agent cards, exposure over A2A and registration with Agent Runtime, Agent
Registry or Gemini Enterprise. Its two helpers speak the protocols themselves:
one inventories an MCP server's tools into a pinned manifest and diffs it, the
other validates an agent card in both the 0.3 and 1.0 shapes. Mechanics were
checked against the google-adk 2.8.0 source and the later changelog, with a
research pass over the official documentation, Google Cloud registration pages
and the issue tracker. All **20 packages** pass validation; the offline suites
run **638 tests** with **59 optional SDK checks skipped**, including 31 tests
for the two protocol helpers against loopback fakes. See the
[gap review and validation record](../research/ai-engineering-practices-gap-review.md).
No live server or cloud operation was performed. A description-based
selection trial over the whole 56-case activation corpus followed on the same
day: 55 of 56 cases passed and one near-miss loaded the target as a supporting
skill, with a second model agreeing on every primary selection. See the
[activation trial record](activation-trial-2026-10-08.md); it
measures selection from descriptions, not host behaviour or execution quality.

## Production-lifecycle specialists · 8 October 2026

The second round of the practice review added three specialists for the
production lifecycle: `adk-agent-security` (threat model, injection-resistant
structure, tool and MCP supply chain, sandboxing, an adversarial seed suite),
`adk-agent-observability` (signals and environment gates, exporters per host,
SLOs and alerts, BigQuery Agent Analytics, production traces into eval cases)
and `adk-release-engineering` (version pinning, CI eval gates, model migration,
staged promotion and joint rollback). Each was built from the google-adk 2.8.0
source and the 2.9 to 2.11 changelog plus a second research pass over the
official ADK documentation, Google samples and the issue tracker; the security
skill records the 2026 ADK advisories and their fix versions, and the release
skill records that `adk eval` exits successfully even when cases fail. All
**19 packages** pass validation; the offline suites run **607 tests** with
**59 optional SDK checks skipped**, including 45 tests for the three new
inspectors and converters. See the
[gap review and validation record](../research/ai-engineering-practices-gap-review.md).
No live model run or cloud operation was performed; selection was later
measured in the [8 October activation trial](activation-trial-2026-10-08.md).

## Cross-framework specialists · 6 October 2026

A review of current AI-engineering practice against the toolkit found that
the skills verified an agent's boundaries thoroughly but did not own what the
model sees and emits. This revision adds three specialists for agent
instructions, tool interfaces and model and output contracts, and a
context-window reference with a session budget helper in the optimise skill.
Their ADK mechanics were checked against the google-adk 2.8.0 source and the
2.9 to 2.11 changelog, and the vendor, community and research sources are
dated in each package. All **16 packages** pass validation; the offline suites
run **562 tests** with **59 optional SDK checks skipped** in the clean
maintainer environment, including 63 tests for the new helpers. See the
[gap review and validation record](../research/ai-engineering-practices-gap-review.md).
No live model run or cloud operation was performed for this revision;
selection was later measured in the
[8 October activation trial](activation-trial-2026-10-08.md).

## Planning-assignment retrospective · 6 October 2026

A third round of feedback, from a time-boxed assignment judged on unseen
cases, found that the skills taught how to verify an application but not how
to make its output good. This round adds the missing half: a scope and
proportionality gate in the designer, a measured decision-quality loop with
prompt and exemplar guidance in the evaluation skill, deliverable and
cross-case rules, a document-ingestion reference with a real-byte PDF fixture,
a local retrieval-strategy reference with a gold set, in-code content
safeguards in the workflow skill, coverage columns in stage contracts, a
reader's budget for evidence, and the
[time-boxed build order](../journeys.md#build-order-for-time-boxed-quality-judged-work).
All **13 packages** pass validation and the offline suites pass with the three
new standard-library helpers. See the
[change record](feedback-validation-2026-10-06.md), which
includes two fresh-agent trials of the scope gate and the quality loop; the
other new scenarios have not yet been run.

## System designer · 25 September 2026

All **13 packages** pass validation. Five independent Codex subagent trials
exercised the new designer: a requirements conversation, a one-pass review of a
flawed architecture, a conversation with a changed requirement, and a runtime
and release review, plus a practical implementation handoff. The outputs
preserved the existing stack,
identified failure and authority boundaries, and kept assumptions and planned
checks explicit. See the [prompts, designs and assessment](system-designer.md).

The [source coverage review](../research/system-designer-source-coverage.md)
maps the system-design guidance to its instructions and supporting references.

The offline repository checks passed **395 tests**, with **59 optional SDK
checks skipped** in the clean maintainer environment. These trials used the
skill directly; automatic selection and installation of the new package in each
client have not been tested. The client results below cover the earlier 12-skill set.

</details>

## Implementation skill checks · 16 September 2026

| Check | Result | Evidence |
| --- | --- | --- |
| Repository packages and helper / SDK tests | All 12 packages validated; 476 tests passed with zero skips. | [Laptop verification](updated-skills-laptop.md) |
| Claude Code and Codex | All 12 skills installed. Two fresh sessions generated refund and finite-streaming adapters; after review and repairs, 71 tests passed, including 17 independent acceptance checks. | [Generated examples and repairs](updated-skills-laptop.md) |
| Google client installation and discovery | Project installation checked for Gemini CLI, Antigravity and Antigravity CLI; Gemini CLI also discovered all 12 through its native skill interface. | [Google installation checks](google-coding-agents.md) |
| Antigravity IDE with Gemini 3.8 Flash | Used `safe-api-tool-calls` to repair a local refund adapter; 21 project tests and nine independent checks passed. | [Generation trial](google-client-generation.md) |
| Gemini CLI generation | Google sign-in succeeded, but the service rejected the consumer-account access route before skill activation or code generation. | [Attempt and account restriction](google-client-generation.md) |
| Standalone Antigravity app and CLI generation | Not yet tested. | [Test coverage and limits](google-client-generation.md) |

These are local checks and bounded coding trials. They do not establish that
every skill, model, SDK version or cloud integration has been exercised. No cloud
deployment was performed in these trials. The skills ask the coding agent to
report which checks actually ran and what remains unverified; cloud operations
follow the selected skill's scope and approval requirements.

<details>
<summary>Earlier revision: three Codex CLI trials</summary>

An earlier revision was tested in three fresh Codex CLI sessions against small
local projects: persistent user preferences, a refund tool with safe retries,
and a concurrent ADK workflow. The generated code passed 162 tests, including
37 independent acceptance checks. These are separate historical results;
they are not included in the current revision's counts above.

See the [CLI test results and generated code](codex-cli-smoke.md)
for the prompts, versions, source files and instructions for rerunning the checks.

</details>

<details>
<summary>Package layout and optional dependencies</summary>

Each specialist contains a `SKILL.md`, supporting resources and its own licence.
The `agents/openai.yaml` files provide optional Codex display and invocation
metadata. Some helpers use only Python's standard library; optional checks
require the ADK or cloud dependencies listed in the skill's references.

The `skills/<name>/SKILL.md` layout is supported by the
[Skills CLI](https://github.com/vercel-labs/skills#readme). See the
[distribution notes](../research/skill-distribution.md) for the packaging
investigation, installation checks and design rationale.

</details>
