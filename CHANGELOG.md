# Changelog

One section per tagged release, newest first. Pin a release with
`npx skills@latest add RuslanKhis/agentic-engineering-skills#v<version> --skill '*'`.

## Unreleased

Not yet tagged; `release.py prepare` will add the dated section above this
one, and these notes move into it.

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
