# REPORT — support-email triage PoC (design and plan only)

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (by the user's `/adk-system-designer`). No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/design-decisions.md` (whole file)
3. `.claude/skills/adk-system-designer/references/failure-review.md`
4. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
5. `.claude/skills/adk-system-designer/assets/system-design-template.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/SKILL.md` (re-read with `grep` for line numbers)
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
9. `.claude/skills/*/references/compatibility.md`. I grepped the version lines from every specialist; I didn't read them in full.
10. `.claude/skills/adk-agent-evaluation/references/quality-iteration.md` (lines 1–80), plus a grep of `adk-model-and-output-contracts/references/compatibility.md` for `output_schema`.

I didn't open `gcp-decisions.md` or `runtime-and-delivery.md`. Their triggers (choosing a GCP service, context limits, streaming, concurrency, releases) don't apply to a local batch PoC. I didn't open `ticket-template.md` because no tickets were requested.

## 2. Questions I would have asked, and the answers I assumed

These are recorded in the design's **Assumed answers** table (A1–A10), with the decisions that depend on each.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | What time and money are available? | About 5 h of one person, under US$10 of model spend, a hard cap of 600 calls |
| A2 | Who judges, and what do they read? | The head of support, at a demo: per-email category and draft, plus a one-page accuracy summary |
| A3 | Is this an exploration, a pilot or production? | An exploration (proof of concept) |
| A4 | What is the category taxonomy? | None was given. The user writes 6–8 categories; a default list of 8 is proposed |
| A5 | Are the 50 emails labelled? Are there reference replies? | No. The user labels categories (15 dev / 35 holdout). There are no reference replies |
| A6 | What format are the samples in? | Files or a CSV, normalised to `data/emails.jsonl` |
| A7 | Is there a KB, macros or policy text for replies? | No. Drafts use `[CONFIRM: …]` placeholders and must not invent commitments |
| A8 | Which model access is allowed for the anonymised data? | A Gemini API key on the laptop. Vertex AI if policy requires it |
| A9 | Live or pre-computed demo? | Pre-computed static page. One optional live email in `adk web` |
| A10 | Does the system ever send? | No. A human copies the draft; there are no tools |

## 3. Files written or changed, and what was not finished

Written:
- `docs/architecture/support-email-triage.md`: the design, marked **draft**, with assumed answers, deferred controls, guarantees, decisions D1–D7, model-facing contracts, security posture, budget, failure review and open decisions.
- `docs/plans/support-email-triage.md`: the plan with goals G00–G03, each with a primary and supporting skills, acceptance criteria and a run prompt, plus a "Resume here" section.
- `REPORT.md` (this file).

Not finished, by design or by limits:
- **No code was implemented**, as the request said not to.
- No assumption has been confirmed by the user. Everything is provisional.
- The model price and rate limit weren't checked, because no network access was allowed. The budget rests on the call cap rather than on a dollar figure.
- The ADK version is assumed to be 2.8.0, the version the specialists were checked against. Confirming it against the real pin is an acceptance item of G01.
- The lifecycle table (checked_on 2026-10-08) was not refreshed from Google's pages.
- No tickets were written; none were requested.

## 4. Checks run and not run

Run:
- A relative-link check over both docs, using a short Python script run with `python3 -I`: all 4 links resolve.
- A word count: design 2,792 words, plan 1,325 words.
- `grep` confirmed that `gemini-3.8-flash` appears in the lifecycle JSON, with status `stable`, released 2026-09-02 and no shutdown.

Not run:
- No tests exist, since no code was written. The planned tests that import `google.adk` couldn't run here anyway: ADK isn't installed and installing it wasn't allowed.
- No live model calls, no pricing or availability lookups, and no ADK API verification. Network access wasn't allowed.

## 5. Friction log

- **Helpful: headless mode is explicit.** `.claude/skills/adk-system-designer/SKILL.md:94` says to keep asking nothing and put an Assumed-answers table at the top. That settled how to behave without the user straight away.
- **Helpful: the proportionality rule.** `SKILL.md:81` and `references/design-decisions.md:26-59` keep the first slice to "core judgment on real inputs, measured, plus a call budget and a stop", with a deferred-controls table. That kept the design from growing approval, persistence and hosting machinery.
- **Unsure: the artifact type doesn't fit.** `SKILL.md:52-60` and `SKILL.md:63-66` offer exploration, assignment, pilot or production. A "PoC for a demo tomorrow" sits between exploration and pilot. I chose exploration, which sets the ten-minute-read target.
- **Heavier than needed: the length target and the template pull against each other.** `SKILL.md:63-64` asks for a ten-minute read for an exploration. But `assets/system-design-template.md:53-117` (model-facing contracts, security posture, budgets, failure, observability and release bundle) and `references/failure-review.md:23-43` (21 scenarios, each needing a reason when not applicable) push the document longer. The result is about 4,100 words across the two docs, more than ten minutes. The template doesn't say which sections an exploration may drop.
- **Unsure: one doc or two.** `SKILL.md:217-218` says to use `docs/plans/` for a multi-goal effort, but that a small effort can keep its plan in the design. This effort is small *and* has 4 goals. I wrote both, which added length.
- **Unsure: two prompt formats.** The short form at `SKILL.md:246` (`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`) differs from the long form at `assets/implementation-plan-template.md:50-52` and `:89-95`. I used the long per-goal form in the plan and the multi-line form in "Resume here". It isn't clear which one the closing chat message should quote.
- **Unsure: holdout versus demo set.** `adk-agent-evaluation/references/quality-iteration.md:14` and `:150-151` require a holdout that nothing tunes on. The demo shows all 50 emails, so I split 15/35 and marked the split on the demo page. Neither skill covers the case where the judge looks at the holdout.
- **Needed adapting: error categories.** The categories at `quality-iteration.md:23-30` (`missed_policy`, `weak_condition` and so on) come from a planning domain. I replaced them with email-specific ones (`wrong_category`, `invented_commitment` …). This was easy but not signposted.
- **Helpful: the model lifecycle table.** `SKILL.md:167-171` points to `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`. It made the model choice quick and dated, and steered away from `gemini-3.6-flash` (Vertex retirement 2026-11-19, line 14) and the 2.5 models (`limited`, lines 21-23).
- **Helpful: the trifecta check.** `references/design-decisions.md:180-194` turned "should we harden the prompt against injection?" into a structural answer: there are no tools, so there is no egress. `references/implementation-handoff.md:39-51` then made it clear that `adk-agent-security` isn't needed as a supporting skill.
- **Slightly heavy: pin confirmation for greenfield.** `SKILL.md:164-171` asks for the ADK version to be confirmed from every specialist's `compatibility.md`. They all said 2.8.0, so a grep was enough. A single canonical pin file would save that step.
- **A missing skill for G00.** The template expects a `Primary skill` per goal (`implementation-plan-template.md:41`), but the first goal is the user's own data-labelling task. I wrote "none (user task)".

## 6. The exact next prompt the skills told the user to type

The skill (`SKILL.md:241-249`) says to end with the exact prompt for the next ready goal. The ready goal G00 is the user's own data preparation; it has no prompt. The prompt to type once G00 is done is in the plan's "Resume here" section:

```text
/adk-engineer Carry out G01 — Triage all dev emails end to end, measured — from docs/plans/support-email-triage.md.
Read docs/architecture/support-email-triage.md and preserve its accepted decisions.
Use adk-model-and-output-contracts with adk-agent-instructions and adk-agent-evaluation.
Work within local code and at most 600 model calls on my Gemini API key, verify the G01 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

The short template form the skill gives as its example (`SKILL.md:246`), quoted verbatim, is: `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
