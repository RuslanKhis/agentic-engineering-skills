# Changelog

One section per tagged release, newest first. Pin a release with
`npx skills@latest add RuslanKhis/agentic-engineering-skills#v<version> --skill '*'`.

## 2026.10.28 · 28 October 2026

Changes since v2026.10.27:

- **Skill fixes found by scenario runs.** The skill defects confirmed by
  scenario triage were fixed across evaluation, guardrails, memory, release,
  interoperability, observability, deploy and workflow design.
  - Screen placement and the Prompt Guard 2 section now live in
    protect-adk-sensitive-data; adk-agent-security keeps a threat-model view
    with pointers, and guardrails points there.
  - adk-workflow-design's description now names checkpoints, reusing saved
    stages, oversized checkpoints, multi-day approval waits (ADK resume or a
    durable engine), draft consistency checks and warning-only corrections.
    The skill loaded in 7 of 7 workflow scenarios, up from 2.
  - deploy-adk-on-google-cloud hands the Agent Identity decision to
    adk-tool-auth-and-secrets and gives the `npx skills@latest add
    google/skills --skill <name>` step where it used to point at adk-engineer.
  - Guardrails routes unanswered approvals and unreadable approval arguments
    to their section of `human-review.md`.
- **Routing.** Three routing gaps got owners in `ownership.md` (model 429s,
  a multi-area feature in an existing app, `output_key` `{key}` handoffs),
  plus rows for checkpoint and resume ownership. Activation (Sonnet, two
  repeats): dev 344 PASS / 10 PARTIAL / 2 FAIL on 178 cases, held-out 155 /
  1 / 0 on 78 cases. One designer-versus-engineer case remains unstable on
  main as well.
- **Governance pack.** The consultancy's home now comes from an employer
  profile's staff countries, Australia by default and recorded as an
  assumption; a client profile never sets it.
- **Evaluation harness (maintainers).**
  - Grader answers and trial oracles moved out of skill packages into
    `evals/graders/`; only the judge sees them.
  - Scenario workspaces are composed from shared bases and overlays; every
    scenario has a fixture.
  - Scenario agents are confined to their workspace, auto-memory is off,
    skill loading is recorded and the judge votes three times.
  - Activation cases have a held-out split generated from neutral briefs.
  - The API-key backend and the activation workflow were removed; runs use
    the claude CLI.
  - A shell-enabled mode scrubs cloud, SSH and token variables, redirects
    tool config to empty per-case paths, keeps Bash in the workspace and is
    recorded as unconfined.
- **Scenario evidence.** 77 scenarios were run and triaged
  (`docs/testing/scenario-fixtures-2026-10-27.md`), then the defect fixes
  were measured (`skill-defect-fixes-2026-10-27.md`,
  `last-defects-2026-10-28.md`) and a first shell-enabled run was recorded
  (`shell-run-2026-10-28.md`): with a shell, 12 of 17 shell-dependent
  assertions passed by actually running the helper, and the four new
  governance packs passed 22 of 23 assertions. One run per scenario, so
  single verdicts are indicative.
- About 100 links in moved maintainer records and research notes were
  repaired.

## 2026.10.27 · 27 October 2026

Changes since v2026.10.26.3:

- **Helper flags and exit codes (check your scripts).** All 48 helper
  scripts now follow one convention, set out in `docs/helper-conventions.md`.
  - `--project DIR` names the target directory. A GCP project ID goes in
    `--gcp-project`.
  - Exit codes: 0 clean, 1 findings or a failed gate, 2 bad arguments or
    unusable input, 3 incomplete.
  - Old flags and positional arguments still work. Each prints a one-line
    deprecation note.
  - One break, in `deploy-adk-on-google-cloud`'s `inspect_project.py`:
    `--project` now means the directory, and a value that is not a
    directory fails with a pointer to `--gcp-project`.
  - Several exit codes changed meaning. For example, an incomplete scan now
    exits 3 everywhere (it was 1, 2 or 4), and a failed `--fail-on`-style
    gate now exits 1 (it was 3).
  - `docs/testing/helper-conventions-2026-10-27.md` lists every helper
    whose behaviour changed. Any CI job that reads a helper's exit status
    should be updated together with the vendored helper.
- **Clearer routing between skills.** A new
  `adk-engineer/references/ownership.md` gives each of 29 contested topics
  one owner, for example:
  - human approval, replay of an approved write and session ownership at
    each hop;
  - in-session history and cross-session memory;
  - prompt wording and exemplars versus measuring them;
  - CI eval gates versus writing eval cases.

  The descriptions of 21 skills now exclude each other in both directions,
  and `scripts/check_boundaries.py` keeps it so. `adk-memory-architecture`
  now names document ingestion, and `adk-agent-evaluation` no longer claims
  exemplar design. 40 activation cases were added.
- **Routing is measured.** `scripts/run_activation.py` measures skill
  selection from descriptions alone, and `scripts/run_scenarios.py` runs a
  scenario and has a judge grade its assertions. A manual GitHub workflow
  runs activation through the Anthropic API.
  - With Sonnet 5.5 over two repeats, the 154 cases scored 298 PASS,
    9 PARTIAL and 1 FAIL.
  - The 114 cases that existed before gained no new failure.

  51 scenario prompts were rewritten in plain user language.
- **One source for shared guidance.** The evidence vocabulary, the rules for
  consequential operations, interpreter selection, tool confirmation and the
  verified principal are each kept once in `shared/`. `scripts/sync_shared.py`
  checks that every skill's copy matches. The skills used nine different
  evidence vocabularies; they now use one. Copies that had drifted were
  corrected against the ADK 2.8.0 and 2.12.0 packages:
  - 2.12.0's user-id fix covers A2A requests only.
  - A confirmation callable gets `tool_context` only when the tool function
    declares it.
- **Version facts.**
  - Every skill now carries `verified-against`, and `docs/compatibility.md`
    gathers them into one table with the ADK security floors.
  - `adk-model-and-output-contracts` records ADK 2.13.0's
    `litellm<1.106.3` cap: 1.107.0 was a compromised release.
  - `safe-api-tool-calls` warns that below ADK 2.12.0 a re-sent approval
    could run a tool again.
- **Less always-loaded context.**
  - `adk-engineer` dropped from about 3,060 to about 2,500 words; ticket
    closing, teardown and estimates moved to `ticket-lifecycle.md`.
  - The designer now points to its plan template rather than repeating it.
  - The governance pack turns its Australian scoping rules into a table.
  - 14 maintainer records moved out of the skill packages to
    `docs/skill-evidence/`.
  - `validate_skills.py` warns when a SKILL.md body passes 2,500 words.
- **A shorter README.** It went from 3,849 lines to 446. The per-skill
  detail, the journeys, troubleshooting and the testing log moved verbatim
  to `docs/skills.md`, `docs/journeys.md`, `docs/troubleshooting.md` and
  `docs/testing/index.md`.

## 2026.10.26.3 · 26 October 2026

Changes since v2026.10.26.2:

- **New skill: `adk-portability-planning`.** The toolkit still builds
  production Google ADK applications on GCP, and that stays the primary
  build. The new optional skill answers a stakeholder's lock-in question in
  a separate document, `docs/portability/<topic>.md`: it classifies the
  accepted design's components, assesses cloud, agent framework, model,
  service and deployment portability separately, compares AWS, Azure and a
  small set of other frameworks with dated sources, and gives relative
  effort with its drivers. `check_portability.py` checks it; the skill
  changes no code and no design. The designer asks once whether lock-in is
  a concern (default no, and no changes nothing); a yes adds a portability
  goal, depending only on the design and blocking no build goal, and its
  ticket. The plan checks keep it off the primary build's path:
  `check_schedule.py` reports any goal but a presentation that waits for
  it, and the phase gate skips it. `check_tickets.py` accepts a
  `(deliverable)` tag on a portability ticket's acceptance items, and
  `adk-engineer` routes lock-in and exit-plan requests to the skill.

## 2026.10.26.2 · 26 October 2026

Changes since v2026.10.26.1:

- **Governance pack: drafting aid, reviewer sign-off and law freshness.**
  Every `adk-governance-pack` template opens with a banner saying the draft
  is drafting-aid output, not legal advice, and is not reviewed until its
  reviewer signs, and ends with a Review and sign-off table. The checker
  requires both, keeps every decision `pending` while `status: draft`, and
  requires a dated decision once `status: reviewed`; the skill never fills a
  reviewer's decision. Each law reference carries a `verified:` date that
  `scripts/validate_skills.py` requires for the governance pack and warns on
  when due, and `docs/maintenance/law-refresh.md` with a quarterly GitHub
  workflow opens a refresh issue in January, April, July and October.
- **Governance pack: New Zealand, Singapore and Canada.** The jurisdiction
  screen now runs Australia, United States, EU, UK, New Zealand, Singapore,
  Canada, with codes `nz`, `sg` and `ca`; Canada is named Canada or Quebec,
  never CA (California). New references at screen depth cover the Privacy
  Act 2020 (s 11 agents, IPP 3A, IPP 8, IPP 12, the Biometric Processing
  Privacy Code, public sector guidance), the PDPA (data intermediaries,
  consent and exceptions, the Transfer Limitation Obligation, the 3-day
  breach clock, the agentic AI framework) and Canadian law (PIPEDA, Quebec's
  Law 25 with s 3.3, s 12.1 and s 17, Alberta and BC, Ontario employment
  rules, the federal Directive on Automated Decision-Making). The memo and
  privacy pack require each regime's sections, the transfer annex covers
  New Zealand, Singapore and Quebec flows, and a screen that names only the
  first four regimes is now an error with a fix message.
- **Governance pack: NSW and Commonwealth government clients.** A new
  `au-government-crosswalks.md` maps the DTA AI impact assessment tool,
  transparency statement, use-case register, agentic addendum, NSW AIAF
  registration and assessment, and the IPC AI PIA guide to the project's
  records, re-checked every 90 days; a new `government-form-answers`
  document drafts answers in the official form's order for the agency's
  officers, names the form, version, URL and checked date, never claims to
  be the form, and marks what only the agency can answer `agency:`.
  `australia.md` gains NSW state law: PPIP Act s 19(2) for any recipient
  outside NSW, the HRIP Act, the Part 6A breach scheme, GIPA, the State
  Records Act 1998, the NSW Cyber Security Policy (Essential Eight Maturity
  Level One, 24-hour reporting), ICTA clause 6.11 tied to the model
  lifecycle check, s 7B(5), DCS-2026-02 and the Operational Policy's AIAF
  bands and review committee referral.
- The engineer's routing, the designer's governance goal and scoping, and
  the practice-profile interview name the seven regimes.

## 2026.10.26.1 · 26 October 2026

Changes since v2026.10.26:

- **Practice profile: interview and document import.** `practice-profile`
  now offers two ways in. `init` asks "interview, import, or both?"; the
  interview has sixteen core questions over thirteen sections (six new:
  sector and jurisdictions, data subjects and data classes, systems of
  record and tools, AI policy and approvals, AI maturity and past attempts,
  procurement and consultation), with menus and "don't know" for company
  facts. `import` reads Markdown or text files the user names: the helper's
  `extract` withholds secrets and personal data, flags instruction-like and
  hidden text and refuses crafted files; `verify-candidates` keeps only
  lines whose quote is on the cited line; the user accepts each line, and
  the write needs a yes to the diff, after a snapshot. `export` prints a
  one-page company context brief to reuse elsewhere, refused in a
  repository bound to another org. Discovery, the designer and the
  presenter read the new sections; the profile cap rises to 200 lines.
- **Governance pack: Australian, US, EU and UK law.** `adk-governance-pack`
  now screens jurisdictions before drafting, always in the order Australia,
  United States, EU, UK, from where the client, the people and the
  processing are (the model's region and the consultancy's own staff
  included), the client type, sector and decision effects; an unknown fact
  keeps a regime in scope as a `gap:`. The classification memo becomes a
  regulatory memo: the EU AI Act classification stays (corrected against
  the Official Journal and the Commission's Article 50 guidelines), and
  Australia and the UK get screens of existing law with no risk tier. The
  DPIA input pack becomes a privacy impact input pack serving the
  Australian PIA (APPs, APP 8 offshore processing, APP 1.7 automated
  decisions from 10 December 2026), the EU and UK DPIA (GDPR Article 22,
  UK Articles 22A to 22D) and US risk assessments (CPPA), with a new
  transfer assessment annex for EU and UK data reached from Australia. The
  checker follows each draft's `jurisdictions:` and dates AU, US and UK law
  references. The pack reads the practice profile's jurisdiction, data,
  AI-policy and consultation sections; a profile fact can add a check,
  never remove one.
- **Wave 3 process and toolkit sources.** Five Medium-tier sources
  integrated (12-factor-agents, spec-kit/OpenSpec/Conductor/HumanLayer, the
  Agent Skills reference and skill-creator, agents-shipgate, assistant-ui).
  `plan_status.py --gate` reads the code against every ticket's touches;
  `inspect_security_surface.py` gains `--compare` for a pull-request
  capability gate and reports ADK 2.x Workflow graphs as unread.

## 2026.10.26 · 26 October 2026

Changes since v2026.10.25:

- `adk-memory-architecture`'s `local_retrieval.py` now parses on Python 3.11,
  the minimum the skills support; in 2026.10.25 it failed to compile there.

## 2026.10.25 · 25 October 2026

First tagged release. Earlier changes are recorded in the README under
Compatibility & Checks.

- **Releases and updates.** Every skill carries `metadata.version`.
  `scripts/release.py` stamps a release, writes this changelog and tags it.
  The validator fails when skills or manifests disagree. `adk-engineer`
  reports a mixed installation or a newer release in one line and never
  updates anything itself. Plugin manifests for Claude Code, Gemini CLI and
  Antigravity follow the `stable` branch.
- **Plan health during the build.** The designer's `plan_status.py` reads
  ticket evidence back into the plan: contract and security-rule coverage,
  contract deltas and rulings waiting for a decision, the ready and
  interrupted tickets, safe parallel groups, hours spent and remaining
  against capacity, a phase-exit gate (`--gate`) and a weekly status update
  with a RAID log (`--weekly`). `check_tickets.py` lints tickets after they
  are written. `check_schedule.py` requires a journey goal before a review of
  built work. The designer gains a checkpoint mode. The engineer gains a
  ticket lifecycle covering resume from a `Progress:` block, checkpoint
  routing and parallel worktrees. The ticket and plan templates gain `type`,
  `status`, `actual:` and `Progress:`; nothing was removed.
- **Field reports.** When a skill's instruction fails on the installed
  versions, is overridden or misroutes the work, `adk-engineer` records a
  generalised, redacted note on the user's machine. It offers once, at the
  end of the session, to open a prefilled GitHub issue form that the user
  reviews and submits; nothing is sent automatically. Includes a maintainer
  triage script and a page on what is never sent.
- **New skill: `practice-profile`.** Employer and client context and lessons
  are kept outside every repository, one directory per org, bound to
  repositories by path. Discovery, the designer, the presenter and the
  engineer read them as labelled defaults; writes are diffs the user approves.
- **New skill: `adk-governance-pack`.** Drafts the papers a client's
  reviewers ask for: an EU AI Act classification memo, an impact assessment,
  DPIA inputs, a system card, processing records and security-questionnaire
  answers. Every statement is checked for a citation, and counsel is flagged
  where the law needs judgment.
- **Expert labelling and value reports.** `adk-agent-evaluation` gains an
  expert-review workshop and `label_agreement.py` (Cohen's kappa, criteria
  drift, judge TPR and TNR). `adk-presenter` gains a monthly value report
  with `check_value_report.py`.
- **Scoping, rollout and handover.** The designer drafts a statement of
  work, change request and data-request letter (`check_sow.py`). The
  presenter gains a rollout-pack mode (`check_rollout.py`). Observability
  gains an operations handover and an agent postmortem template.
- **Instruction linter.** `adk-agent-instructions`' linter now follows an
  instruction imported from the prompt module into `agent.py`, which a field
  trial showed it had silently skipped.
