# Skill boundaries · 27 October 2026

This records the routing-boundary pass across the 26 skill descriptions: an
ownership map for contested topics, reciprocal exclusions in the
descriptions, a deterministic check that keeps them reciprocal, 40 new
activation cases, and one selection sanity check from descriptions alone.

## What the review found, and what held up

A host chooses a skill from its name and description. The review reported
one-sided exclusions; each claim was checked against the descriptions at
`16ea7fa` before acting.

- **No exclusions at all.** Confirmed for `adk-agent-evaluation` (generic
  exclusions only, no skill named), `adk-sql-agent-engineering`,
  `adk-tool-auth-and-secrets` ("Exclude ..." with no skill named),
  `adk-workflow-design`, `protect-adk-sensitive-data` and
  `adk-system-designer` (a "use that specialist directly" sentence, no clause).
- **Session ownership.** Confirmed: frontend ("session ownership") and
  tool-auth ("verified user/session ownership, cross-user access bugs") never
  named `adk-fastapi-backend`, which named both. The backend's own body
  already splits it (agent session endpoints to frontend, the principal
  dependency and domain routes to the backend, the tool hop to tool-auth);
  the descriptions now say the same.
- **Confirmation.** Confirmed three claimants. Split: guardrails owns the
  approval flow, security owns which tools need it, safe-api owns the write
  side, frontend renders it.
- **CI gates.** Confirmed: release excluded evaluation, not the reverse.
- **History.** Confirmed: the routing table's memory row said "history" and
  the optimise row "history trimming". The memory row now names
  cross-session recall and points trimming to optimise.
- **Exemplar drift.** Confirmed: the evaluation body routed "prompt or
  exemplar design" to quality iteration, whose helper fixed `n=2`, while the
  instructions skill's exemplars reference treats the count as a variable to
  measure. Fixed (below).
- **Length.** Confirmed: interoperability 1020, governance 1017, security
  1016, presenter 1004, practice-profile 998, observability 985 of 1024.
- **Value report.** Confirmed: no routing row, although the designer's
  implementation handoff names `adk-presenter` for it.

Further contested topics found by comparing all descriptions and the table:
model choice versus model migration (model contracts named "lifecycle",
release owns deprecation), memory's BigQuery history versus the SQL agent,
retries versus model failover, repeated tool calls versus wrong tool choice,
budget enforcement versus cost accounting, credential exposure (tool-auth
custody versus data-protection screening), sub-agent descriptions versus
orchestration, security review versus security questionnaire, decision memo
versus proposal versus regulatory memo, first deployment versus canary and
rollback, and the replay vocabulary shared by safe-api, memory, workflow and
evaluation.

## Ownership map

`skills/adk-engineer/references/ownership.md` has one row per contested
topic (29 rows): owner, neighbours that defer, and the distinction. The
router links it from its selection section in one sentence.

## Descriptions

Every changed description keeps the "what it does / use for / do not
activate for (owner)" shape and is written as a folded block. Characters are
the parsed YAML value.

| Skill | Before | After | Change |
| --- | --- | --- | --- |
| adk-agent-evaluation | 628 | 932 | Names instructions (wording, exemplars), model contracts, release (CI gates), observability, security (adversarial suites), presenter; "model escalation" became measuring a model change |
| adk-agent-instructions | 864 | 923 | "few-shot exemplar design"; names release (releasing prompt versions) |
| adk-agent-interoperability | 1020 | 948 | Trimmed option lists; security exclusion says allowlists and pinning policy |
| adk-agent-observability | 985 | 944 | Trimmed host list; names guardrails (enforcing budgets) and release (canary, rollback) |
| adk-agent-security | 1016 | 943 | Trimmed; tiering says "which actions need confirmation"; names interoperability and governance |
| adk-fastapi-backend | 726 | 832 | Positive for a domain route leaking records; session endpoints to frontend, tool-hop leaks to tool-auth |
| adk-frontend-integration | 669 | 904 | Session ownership scoped to the agent's run, stream and session endpoints; names backend, tool-auth, guardrails |
| adk-governance-pack | 1017 | 935 | Trimmed wording only |
| adk-memory-architecture | 530 | 716 | Names SQL agent, optimise (in-session trimming), safe-api (duplicate writes) |
| adk-model-and-output-contracts | 887 | 937 | Names safe-api (external retries) and release (executing a migration) |
| adk-operational-guardrails | 448 | 849 | Approval spelled out; names safe-api, security, frontend, tool-interface, model contracts, observability |
| adk-presenter | 1004 | 946 | Trimmed; names governance; proposals stay with the designer |
| adk-sql-agent-engineering | 390 | 512 | Names memory and model contracts |
| adk-system-designer | 588 | 737 | Gains a clause naming discovery and presenter |
| adk-tool-auth-and-secrets | 448 | 752 | "Exclude" became "Do not activate"; tool-hop scope; names backend, frontend, interoperability, security, data protection |
| adk-workflow-design | 436 | 619 | Names instructions, interoperability, security |
| deploy-adk-on-google-cloud | 452 | 692 | Names release, optimise, observability, backend |
| optimise-adk-on-google-cloud | 518 | 754 | Claims in-session history trimming; names deploy, memory, model contracts, observability |
| practice-profile | 998 | 945 | Trimmed wording only |
| protect-adk-sensitive-data | 550 | 736 | Names tool-auth, security, observability, governance |
| safe-api-tool-calls | 496 | 873 | Write side of confirmation spelled out; names guardrails, memory, interoperability, tool-interface |

Unchanged: `adk-discovery`, `adk-engineer`, `adk-portability-planning` (925),
`adk-release-engineering`, `adk-tool-interface-design`. The largest is now
948; none passes 950.

## Exemplar drift

`adk-agent-evaluation`'s quality-iteration reference now defers choice,
count, order and format to `adk-agent-instructions`, keeps only the
leave-one-out guarantee and the measurement, and its `exemplars_for` helper
takes `n` with no default. The prompt sketch no longer says "two exemplars".
The SKILL.md routing line reads "measuring a prompt, exemplar, output-schema
or model change" and says the wording itself is the instructions skill's. The
instructions skill's exemplars reference says the helper takes its count
from the prompt version.

## Router

`adk-engineer` gains the ownership link, a monthly value report row
(`adk-presenter`, value report), and a memory row that says cross-session
recall with in-session trimming pointed to optimise.

## Boundary check

`scripts/check_boundaries.py`, run by `check_repo.py` after the package
validator, with tests in `tests/test_check_boundaries.py`:

- every skill named after a description's first "Do not activate" must name
  that skill back in its own clause, or appear as a `one_way` entry with a
  reason in `scripts/boundary_allowlist.json`;
- every skill has a "Do not activate" clause unless it is in `no_clause`
  (only `adk-engineer`, the router);
- allowlist entries that name unknown skills, no longer apply or have become
  reciprocal are errors, so the list cannot rot;
- a description over 950 characters is a warning (the hard 1024 cap stays in
  `validate_skills.py`).

The 15 one-way entries are the five "adk-agent-instructions owns prompt
wording" disclaimers (frontend, memory, guardrails, deploy, optimise), the
three portability exclusions, discovery to the router, instructions to data
protection, interoperability to deploy, governance to release, tool-interface
to evaluation and to tool-auth, and practice-profile to memory.

## Activation cases

40 cases added to `evals/activation.json` (all `should_trigger` labels set by
the ownership map): 12 positives for owners and 28 near-misses for
neighbours, covering session ownership (6), approval and confirmation (9),
history (4), CI gates versus cases (3), exemplars (4), model choice versus
migration (2), memory versus SQL (2), and one each for governance versus
data protection, MCP wiring, model failover, repeated calls, budget
enforcement, sub-agent descriptions, OAuth token custody, pasted secrets,
canary versus deploy and governance versus presenter.

## Selection sanity check

One fresh headless call (`claude -p --model claude-sonnet-5-5`, no tools)
received only the 26 names and descriptions and the 40 new prompts, shuffled
with a fixed seed and without labels, and returned a primary and at most one
supporting skill per prompt. The same call was repeated with the descriptions
at `16ea7fa` as a baseline. Grading follows the 8 October trial: a positive
passes when the target is primary; a near-miss fails when the target is
primary and is partial when it is supporting.

| Catalogue | PASS | PARTIAL | FAIL |
| --- | --- | --- | --- |
| Before (`16ea7fa`) | 37 | 1 | 2 |
| After (this branch) | 40 | 0 | 0 |

The before-run misses were all session ownership: the sidebar-resume prompt
went to the backend instead of frontend, the stream-continuation near-miss
picked the backend as primary, and the tool-hop near-miss loaded the backend
as supporting. Requests and both sets of picks are in
[artifacts](artifacts/skill-boundaries-2026-10-27/) (prompt SHA-256 prefixes
`6d0bf1f1f134a01e` after, `99851de02f35fb18` before).

Limits: one sample per catalogue on one model; the cases were written with
the map and the new descriptions in view, so they are not held out; most
already passed before the change, so the corpus mostly guards against
regressions. The fuller measurement belongs to the activation runner being
built on another branch.
