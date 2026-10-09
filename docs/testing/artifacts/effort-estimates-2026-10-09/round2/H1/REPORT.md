# Session report: HR policy Q&A POC design

## 1. Skills invoked and reference files opened, in order

Skill: `adk-system-designer`, invoked by the user's `/adk-system-designer`
command. I invoked no other skill. I read other skills' files only as
references, as `SKILL.md` directs.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md`: whole file
3. `adk-system-designer/references/design-decisions.md`: whole file
4. `adk-system-designer/references/failure-review.md`: whole file
5. `adk-system-designer/references/implementation-handoff.md`: whole file
6. `adk-system-designer/assets/ticket-template.md`: whole file
7. `adk-system-designer/references/gcp-decisions.md`: whole file
8. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`: whole file
9. `adk-memory-architecture/references/compatibility.md`: lines 1–30
10. `adk-model-and-output-contracts/references/compatibility.md`: grep for version lines only
11. `adk-memory-architecture/references/retrieval-strategy.md`: headings and lines 1–40; `local-document-coverage.md` and `document-ingestion.md`: headings only
12. `adk-operational-guardrails/`: grep for "adk web" (hit `references/evidence.md:14`)

Not opened: `references/runtime-and-delivery.md` (its trigger at `SKILL.md:180`
didn't apply), `assets/system-design-template.md` and
`assets/implementation-plan-template.md` (the compact form at
`delivery-profiles.md:207-208` says to leave the rest of the template out), and `agents/openai.yaml`.

## 2. Questions I would have asked, with the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Which Friday? Today, 2026-10-09, is a Friday. | Friday 2026-10-16 |
| 2 | Will this be continued after the demo? | Yes if the demo goes well, so phase 1 code is kept |
| 3 | How are the 6 hours split, and how familiar are you with ADK and GCP? | Two ~3 h focused blocks; new to ADK (×1.5); already has a GCP project |
| 4 | What can be spent on models and cloud? | ≤ ~USD 20 for the week |
| 5 | Who drives the demo? Will leadership type their own questions? | The builder drives and takes questions from the room |
| 6 | Do the PDFs contain personal data, or only policy text? | Policy text only; internal, not personal |
| 7 | Which model endpoint is approved for internal HR documents? | Vertex AI in the builder's company project via ADC (left open as O1) |
| 8 | Are any PDFs scanned images with no text layer? | Unknown; G01's report finds them and they are excluded (O2) |
| 9 | Are superseded policy versions among the 30? | Possibly; the builder removes them by hand (O3) |
| 10 | What language are the documents in? | English |
| 11 | Do you accept the cut line (G01–G03, 2.75–4.0 h against 3.6 h)? | Assumed accepted; recorded as O4 |
| 12 | Do you accept that an answer can be wrong despite its citation, with a disclaimer in the demo? | Accepted risk, owned by the builder until phase 2 |

## 3. Files written or changed, and what is unfinished

Written (all new; nothing committed):

- `docs/architecture/hr-policy-qa.md`: compact design and plan together:
  assumed-answers table, profile, journey, decisions D1–D6, floor and depth
  table, graduation conditions, failure paths, phase 1 goals G01–G03 with run
  prompts, capacity and cut line, phase 2 (P2-1 to P2-4), later list, open
  decisions O1–O4.
- `docs/tickets/hr-policy-qa/G01-index-hr-pdfs.md`
- `docs/tickets/hr-policy-qa/G02-cited-answer-in-adk-web.md`
- `docs/tickets/hr-policy-qa/G03-gold-questions-and-demo.md`
- `REPORT.md` (this file)

Not finished:

- No implementation, as requested.
- The design is ~1,700 words by `wc -w`, including table markup. The target was about 1,200.
- The design stays **draft** because every scope answer is assumed and O1–O4 are open.
- Provider facts (model availability on Vertex, prices, the ADK pin) are not
  verified, because network access was not allowed.
- Phase 2 goals have no tickets. Only phase 1 tickets were requested.

## 4. Checks

Run:

- Estimates are consistent. The goal totals in the plan (1–1.5, 1–1.5,
  0.75–1) sum to 2.75–4.0 (checked with `python3`), which matches the phase
  total. Each ticket's `total` matches its goal.
- The relative `design` and `plan` link target exists from each ticket.
- `git status --short` shows only the new `docs/` folder (plus this report).
- The model ID was checked against `model-lifecycle-2026-10-01.json`.
  `gemini-3.8-flash` is stable with no shutdown or retirement listed. The
  2.5 models (Vertex retirement 2026-10-20) and `gemini-3.6-flash` (Vertex
  retirement 2026-11-19) were avoided.

Not run:

- Code tests: none exist, and `google.adk` is not installed.
- Markdown lint and a link checker.
- Online checks of the model, Vertex availability, prices or the ADK version
  (network barred). The file itself says to refresh it before relying on it.
- Any live model call.

## 5. Friction log

- **Helpful:** `SKILL.md:121-124` (headless rule: an assumed-answers table and
  no further questions) settled how to proceed with nobody to answer.
- **Unsure:** `SKILL.md:121-124` asks for an "Assumed answers table at the
  top". `delivery-profiles.md:210-211` asks for the scope-gate table "with
  assumed answers folded in as one line each". I merged them into one table
  and wasn't sure that met both instructions.
- **Heavier than needed / tension:** the ~1,200-word target (`SKILL.md:84`,
  `delivery-profiles.md:204`) conflicts with what the same files require in
  that document:
  - an assumed-answers row per question
  - six decisions, each in the requirement-to-check chain
  - a depth table and graduation conditions
  - five fields per phase 1 goal
  - a skill, an estimate and a check per phase 2 goal (`delivery-profiles.md:190-192`)
  - the later list and open decisions

  The result came to ~1,700 words.
- **Unsure:** the focus factor (`delivery-profiles.md:162-164`) is 0.6 for
  part-time or interrupted work and 0.8 for a dedicated block. "6 hours spread
  over two days" fits either reading, and the choice moves capacity by about
  1 h, which decides whether the plan fits. I chose 0.8 and said so.
- **Unsure:** applying the ×1.5 multiplier (`delivery-profiles.md:142-144`) to
  the starting-point row "Retrieval over a small document set ... 3–6"
  (`delivery-profiles.md:135`) gives 4.5–9 h, more than the whole 3.6 h
  capacity. I split the work into smaller goals with lower estimates, so my
  figures quietly undercut the table. It was unclear whether a POC can treat
  that row as an upper bound.
- **Helpful:** `delivery-profiles.md:170-179` ("if only the low end fits, say
  so and name the goals that move") gave the cut-line wording directly.
- **Tension:** for `adk web`, `delivery-profiles.md:77-80` says to put the cap
  on the model project ("a quota or budget alert"). But `gcp-decisions.md:65-66`
  says budgets only alert and do not cap. I chose an in-agent
  `before_model_callback` cap plus a budget alert.
  `adk-operational-guardrails/references/evidence.md:14` confirmed that ADK Web
  does not apply an external runtime wrapper, which was helpful.
- **Heavier than needed:** the supporting-skill rules
  (`implementation-handoff.md:39-51`) give G02, a 1–1.5 h goal, four
  supporting skills. That sits awkwardly with "only the supporting skills the
  slice needs" on the same lines.
- **Helpful:** the model lifecycle requirement (`SKILL.md:197-200`) stopped me
  choosing `gemini-2.5-flash` from memory. Its Vertex retirement is 2026-10-20,
  four days after the demo.
- **Mildly unsure:** for the ADK version source, `SKILL.md:193-197` says each
  specialist's `compatibility.md` names it. I read two (memory and model
  contracts). Both agreed on 2.8.0, but one calls it a "historical resolved
  version" and the other the "pinned reference".
- **Unsure:** where the plan lives. `SKILL.md:246` allows the plan to stay in
  the design for a small effort. But the example prompt at `SKILL.md:278`
  points to `docs/plans/<topic>.md`, and `ticket-template.md:4-5` has separate
  `design`/`plan` fields. I used one file for both fields.
- **Unsure:** there are two prompt forms, `SKILL.md:278` (goal in the plan) and
  `ticket-template.md:53-57` (ticket path). Since tickets were requested, I
  used the ticket form.
- **Helpful:**
  - `failure-review.md:4-5` ("do not invent write machinery for a read-only
    product") kept the failure section to three lines.
  - `design-decisions.md:182-190` (lethal-trifecta check) produced D3 in one line.
  - `adk-memory-architecture/references/retrieval-strategy.md:1-10` (local
    standard-library index) supported the cheap D1.
- **Deviation:** `retrieval-strategy.md:16-34` recommends chunking by heading,
  with pages only as a fallback. I chose page-level chunks as a POC time cut
  and recorded heading chunks as P2-1.

## 6. Next prompt the skills told the user to type

The skill's generic example (`SKILL.md:278`), verbatim:

> `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`

The prompt I gave for the next ready goal, built from the ticket template's
"Run this ticket" block (`ticket-template.md:53-57`):

> `/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-hr-pdfs.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.`
