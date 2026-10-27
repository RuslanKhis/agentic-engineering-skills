# Shared guidance and context cost, 2026-10-27

Branch `phase-3-shared-guidance`. This work answers a review that found nine
evidence vocabularies, duplicated safety guidance that had drifted, mixed
version baselines and an oversized always-loaded context. Every problem was
checked against the files before anything changed.

## Mechanism

- **Canonical snippets** live in `shared/<name>.md`. The leading HTML comment
  is a maintainer note and is not copied. Its `carriers:` line lists the
  packages that must carry the snippet.
- **Each carrier holds a copy** between `<!-- shared:<name> -->` and
  `<!-- /shared:<name> -->`. Every skill stays self-contained, and no link
  crosses a package.
- **`scripts/sync_shared.py`** rewrites the marked blocks from the canonical
  files.
  - With `--check` it changes nothing. It fails on drift, unclosed, nested or
    mismatched markers, an unknown snippet, a listed carrier that lacks the
    block, and a block in a package that is not listed.
  - `check_repo.py` runs it with `--check` after the package validation.
  - `tests/test_sync_shared.py` has 10 tests, including one that checks the
    repository itself is in sync.
- **Word budget.** `scripts/validate_skills.py` warns (it never fails) when a
  SKILL.md body is over 2,500 words. Before this work it flagged
  adk-engineer, adk-system-designer and adk-governance-pack. Now it flags the
  last two only.

## Snippets and carriers

| Snippet | Where it sits | Carriers |
| --- | --- | --- |
| `evidence-labels` | `references/operating-rules.md` | adk-engineer and the 19 building specialists |
| `evidence-labels-brief` | SKILL.md report step | the same 20 |
| `consequential-operations` | `references/operating-rules.md` | the 19 building specialists |
| `consequential-operations-brief` | SKILL.md permissions step | the 19 building specialists |
| `helper-interpreter` | `references/operating-rules.md` | adk-engineer and the 19 building specialists |
| `tool-confirmation` | the existing confirmation reference | operational-guardrails (`human-review.md`), safe-api-tool-calls (`writes-and-confirmation.md`), agent-security (`agency-and-output.md`), tool-interface-design (`function-tool-contract.md`), agent-interoperability (`mcp-consumption.md`), workflow-design (`orchestration.md`) |
| `verified-principal` | the existing identity reference | tool-auth-and-secrets, fastapi-backend, agent-security, frontend-integration, memory-architecture, deploy, protect-sensitive-data, agent-interoperability, safe-api-tool-calls |

The 19 building specialists are agent-evaluation, agent-instructions,
agent-interoperability, agent-observability, agent-security, fastapi-backend,
frontend-integration, memory-architecture, model-and-output-contracts,
operational-guardrails, release-engineering, sql-agent-engineering,
tool-auth-and-secrets, tool-interface-design, workflow-design, deploy,
optimise, protect-sensitive-data and safe-api-tool-calls.

The document-only skills carry none of these snippets: discovery, presenter,
governance, portability, practice-profile and system-designer.

## A. One evidence vocabulary

The base is adk-engineer's, which the designer's templates already used.

- **Tiers:** `offline`, `local`, `live`, `release`.
- **Outcomes:** `pass`, `fail`, `blocked`, `not run`, `inconclusive`, `n/a`.
- **Qualifiers** keep the specialist distinctions without adding tiers:
  `(source read)`, `(rendered)`, `(mocked)`, `(provider)`, `(browser)`,
  `(hosted)`.
- **Non-evidence labels** never count toward a status: `historical`,
  `vendor-measured`, `guidance`.

How the old vocabularies map:

| Old labels | Skills that used them | New labels |
| --- | --- | --- |
| offline simulated / live verified / not run | safe-api, model-contracts, tool-interface | `local (mocked)`, `live`, `not run` |
| source verified / local / mocked / live | security, interoperability | `offline (source read)`, `offline`, `local (mocked)`, `live` |
| local / mocked / live | deploy, release, observability, optimise | the same tiers; mocked becomes `local (mocked)` |
| offline rendered / mocked model / live evaluated | instructions | `offline (rendered)`, `local (mocked)`, `live` |
| passed / failed / blocked / not run | memory, workflow | outcomes |
| live provider / live browser / untested production | frontend | `live (provider)`, `live (browser)`, `guidance` |
| fresh offline / fresh live / historical live / production guidance | protect | `offline` or `local`, `live`, `historical`, `guidance` |
| LIVE VERIFIED / OFFLINE VERIFIED / PRODUCTION PRINCIPLE | sql | `live`, `offline` or `local (mocked)`, `guidance` |

The reference-level label tables were rewritten the same way, in the
`validation.md` files of interoperability, security, observability,
model-contracts, sql, protect, deploy, safe-api and guardrails, and in
`evaluation-across-boundaries.md`, `evaluation-hooks.md` and the interop
checklist asset.

Not converted: the "source-verified" provenance notes on a reference's own
facts (for example "source-verified 2.8.0" in compatibility tables). They
describe how the skill's own statement was checked, not a report label.

## B. Duplicated guidance and the drift found

**Permissions.**
- The permissions sections in 19 SKILL.md files now share one brief, followed
  by each skill's own operations and limits.
- The canonical text is the union of the copies, reconciled to the strictest
  version. Deploy's "end the turn after asking" and "typed confirmation for
  irreversible deletion" now apply to every skill. So do workflow's "billing
  linkage, upgrades and quota" approvals and tool-auth's "stop on an
  exhausted allowance".
- Rules specific to one skill stay in that SKILL.md:
  - guardrails: a separate operator identity;
  - memory: shared RAG infrastructure is excluded from corpus cleanup;
  - frontend: no bundled helper makes network calls;
  - evaluation: never delete shared project resources;
  - tool-auth: secret-payload reads and token minting are separate actions;
  - security: red-team scope.
- Instructions had no permissions section, so it gained the brief.

**Interpreter rules.**
- adk-engineer's SKILL.md lines 181 to 198 moved into the shared block.
  Specialists can now read the rules when installed alone.
- Frontend, guardrails and memory had pointed to "the adk-engineer rule". They
  now link their own operating-rules section.

**Confirmation drift**, checked against the google-adk 2.8.0 and 2.12.0
wheels, read 2026-10-27:
- On `FunctionTool`, the `require_confirmation` callable receives the tool
  function's own prepared arguments. It gets the context only when the
  **tool function** declares it (`_prepare_invocation_args` uses the
  function's signature).
- Guardrails (`human-review.md`) and security said the opposite: "when the
  callable's signature names it". Tool-interface had it right.
- `McpTool` does use the callable's own signature.
- Security's claim that "a non-bool truthy value or None is not a gate" was
  narrowed. `None` lets the call run. From 2.10.0 the framework gate holds
  only on exactly `True`.
- New in the block, from 2.12.0 `_confirmation.py`: a confirmation whose
  original call's name or arguments differ is refused.
- The "2.12.0 runs a confirmed tool once per approval; below it a re-sent
  approval could run it again" fact is kept with the duplicate-reply test.

**Identity drift.**
- ADK 2.12.0's "take the ADK user id only from an authenticated principal"
  (d0c4060) changes the A2A request converter only. It is
  `a2a/converters/request_converter.py` in the 2.12.0 wheel, and the fastapi
  skill's topology reference already said so.
- These places described it as protecting the HTTP endpoints and are
  corrected:
  - tool-auth: SKILL.md, `compatibility-and-evidence.md` and
    `identity-and-output.md`, which said 2.12.0 "fixes both";
  - security: SKILL.md and `compatibility.md`, two rows.

**No rule dropped.** For each removed copy, the canonical block or the
remaining skill-specific sentence was checked to hold the same rule.

## C. Version baselines

- **Metadata.** Every skill now has `metadata.verified-against`:
  - the 19 that lacked it were added;
  - the 7 existing values were kept, because they honestly say "source read";
  - skills that run no ADK code say "not applicable".
- **Validator.** `validate_skills.py` accepts the field, since metadata is
  free-form string to string.
- **Matrix.** `docs/compatibility.md` has the matrix, the 2.7, 2.10, 2.11 and
  2.12 floors, and what a 2.12.0 re-baseline needs. No skill was
  re-baselined.
- **What the skills were verified against:**
  - tested on 2.12.0: fastapi-backend only;
  - tested on 2.8.0: 11 skills;
  - source or CHANGELOG reads only: instructions, interoperability (apart
    from its offline MCP conformance run on 2.12.0), observability, security,
    model-contracts, release and tool-interface.
- **Open finding.** Guardrails' `last-tested: 2026-10-22` has no recorded
  test on that date. It was left alone because another branch owns it.

## D. Context cost

SKILL.md body word counts are measured after the frontmatter. Marker comments
count as words.

| Skill | Before | After | Change |
| --- | --- | --- | --- |
| adk-engineer | 3,060 | 2,441 | ticket closing, teardown, estimate and interpreter guidance moved to `references/ticket-lifecycle.md` and `references/operating-rules.md` |
| adk-system-designer | 4,497 (500 lines) | 4,115 (467 lines) | the goal rules point to `assets/implementation-plan-template.md`, which gained the facts only SKILL.md had |
| adk-governance-pack | 3,858 | 3,548 | the screen is a pointer with four rules (`jurisdiction-screen.md` gained the AI Act and sections rules and "children's services"); the Australian scoping paragraph is a decision table |
| agent-evaluation | 1,766 | 1,781 | |
| agent-instructions | 1,213 | 1,355 | gained a permissions brief it lacked |
| agent-interoperability | 1,371 | 1,503 | |
| agent-observability | 1,633 | 1,751 | |
| agent-security | 1,349 | 1,473 | |
| fastapi-backend | 1,287 | 1,395 | |
| frontend-integration | 1,355 | 1,311 | |
| memory-architecture | 1,250 | 1,254 | |
| model-and-output-contracts | 1,058 | 1,178 | |
| operational-guardrails | 1,292 | 1,251 | |
| release-engineering | 1,681 | 1,799 | |
| sql-agent-engineering | 1,283 | 1,282 | |
| tool-auth-and-secrets | 884 | 868 | |
| tool-interface-design | 1,261 | 1,385 | |
| workflow-design | 1,152 | 1,112 | |
| deploy | 1,217 | 1,158 | |
| optimise | 1,131 | 1,116 | |
| protect-sensitive-data | 1,046 | 1,041 | |
| safe-api-tool-calls | 1,052 | 1,002 | |

Skills with long permissions sections shrank. Skills whose old label and
permission text was one sentence grew by about 100 to 140 words for the two
briefs and their markers. The full rules now load only from the reference.

The "consultancy is in Australia" default in adk-governance-pack was left as
the owner chose it.

### Files moved out of references/

Each file was moved with `git mv` to `docs/skill-evidence/<skill>/`, after it
was read and checked for runtime instructions. Every moved file gained a note
saying where it came from. Each in-skill link became a plain sentence naming
the new home.

| File | Reason |
| --- | --- |
| optimise `skill-validation.md` (814 lines), `provenance.md` (371) | Package test records and the rule-to-evidence map. The SDK facts in them are repeated in the gke and context references |
| memory `skill-validation.md`, `provenance.md` | Test records and provenance. One runtime fact (the 2.8.0 search adapter drops entry metadata; the 24-hour TTL) was copied into `memory-bank.md` first |
| protect `skill-validation.md` | Dated creation and recheck results. `retry=None` and the regional endpoint are repeated in the recipes and `sdp.md` |
| deploy `skill-validation.md`, `evidence.md` | Forward tests and the historical campaign scope. Its two runtime lines are repeated in `compatibility.md` and `agent-runtime.md` |
| tool-auth `skill-validation.md` | Package execution results |
| guardrails `validation-results.md` | Maintainer test log |
| workflow `validation-results.md`, `provenance.md` | Creation-time checks and provenance. The callback trap is repeated in `callbacks.md` |
| sql `verification-record.md` | The skill's own validation record |
| evaluation `provenance.md` | Rule-to-evidence map. Its two runtime rules (no demo identity fallback in production; do not import the example's fixture IDs, models or thresholds as requirements) were copied into `compatibility.md` |
| frontend `provenance.md` | Historical results. The `[adk]` extra note is repeated in `compatibility.md` |

Kept in place:
- **`sources.md` files.** They are the citations an agent quotes to an owner.
- **tool-auth `compatibility-and-evidence.md`.** It mixes in runtime rules
  found nowhere else.
- **guardrails `evidence.md`.** It holds the ADK Web budget-wrapper fact that
  trials used.

`skills/deploy-adk-on-google-cloud/tests/recheck-results.json` still lists
SHA-256 hashes of the moved deploy files. Nothing checks them, and they were
already stale, so the frozen record was left unchanged.

## Fresh-agent sanity trial

Setup:
- A scratch copy of the designer's `plan-in-progress` fixture, with a tiny
  `app/agent.py` and `app/stream.py`, built under the system temp dir.
- adk-engineer, adk-frontend-integration and adk-system-designer installed
  project-locally in `.claude/skills/`.
- Run with `claude -p` (Claude Code 2.1.306) in plan mode, with the prompt
  `/adk-engineer Resume docs/tickets/support/G02.md from its Progress block`
  plus a dry-run instruction.

| Run | Settings | Result |
| --- | --- | --- |
| 1 | default | Loaded the user-level `~/.claude/skills` install (release 2026.10.26.3), not this branch's copies. It read that install's `ticket-lifecycle.md`. Inconclusive for this change. Finding: a user-level install shadows project-local copies with the same version number |
| 2 | `--setting-sources project,local` | Loaded this branch's copies. **Pass**; details below. 12 turns, about $0.39 |

Run 2 in order:
1. It read the ticket, then `.claude/skills/adk-engineer/references/ticket-lifecycle.md` immediately.
2. It ran the resume checks. It found that the fixture's Progress block does
   not match the repo and did not invent the missing A2.
3. It read `references/operating-rules.md` for the evidence labels.
4. It proposed Evidence in the unified vocabulary:
   `C3: evidenced, offline, A1`, `actual: … | not reported`, and owed
   `live (browser) not run`, with status `verified_local`.
5. It proposed updating the design's Evidence cell and running
   `plan_status.py`, ending on its next-ticket or CHECKPOINT prompt.

Plan mode wrote one plan file under `~/.claude/plans/`. It changed nothing in
the scratch project.

## Checks

`.venv/bin/python scripts/check_repo.py` passed: package validation, shared
snippets in sync, evaluation case structure, repository tests and every
skill's helper tests. Two word-budget warnings remain, for designer and
governance, as intended.

## Owed

- **Further cuts.** adk-system-designer (4,115 words) and adk-governance-pack
  (3,548) are still over the word budget.
- **Live and companion runs.** No live or companion run was repeated. The
  verified-against values describe past evidence only.
- **Other client paths.** The trial covered one resume path on Claude Code
  only. Codex and Gemini CLI were not tried.
