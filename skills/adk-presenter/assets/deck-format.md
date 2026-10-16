# Deck outline format

One Markdown file per presentation, saved under `docs/presentations/<topic>/`
as `<stage>-<audience>.md`. The format carries the evidence beside every
claim so that `scripts/check_deck.py` can check the outline before anyone
builds slides, and so that a slide tool, a Marp or Pandoc conversion, or a
host's slide-building skill can render it afterwards without losing the
sources. Speaker notes stay in the same file.

```markdown
---
stage: poc-approval            # poc-approval | production-approval | final-results | case-study
audience: business             # business | technical | public
minutes: 15                    # the speaking time agreed, not the meeting length
title: Guided campaign briefs for small advertisers
sources: docs/discovery/ads.md, docs/architecture/ads.md, docs/plans/ads.md
decision: Approve a four-week proof of concept with one developer
decider: Director of SMB Sales
date: 2026-10-30
---

## Guided campaign briefs: a four-week proof of concept
Covers: title

---

## Small advertisers abandon the purchase at product choice more than at any other step
Covers: problem
Evidence: docs/discovery/ads.md funnel table; measured

- 38% leave at product choice (last quarter, 2,140 advertisers)
- 12% leave at creative upload

Notes: Open with the funnel, in one breath. Product choice loses 38% of
eligible advertisers; creative upload loses 12%. Then pause.

---

## A guided brief should recover a share of them without raising refunds
Covers: hypothesis
Evidence: hypothesis; docs/discovery/ads.md §4
Notes: Say the word hypothesis out loud. We expect a lift; the proof of
concept measures it.
```

Rules the checker enforces:

- **Front matter** names the `stage`, the `audience` and the `minutes`.
  `sources` lists the documents every number came from; `decision` is the
  one sentence the audience is asked to decide, or "information only: <what
  is reported>" at a results review with no ask; `decider` and `date` name
  who decides and when (the checker warns when they are missing). On a
  technical deck the decider is the person who grants what the ask needs
  (access, environment, reviewer, hosting).
- **Slides** are separated by a `---` line. Each opens with an action title,
  `## <claim>`: the sentence the audience should remember if they read nothing
  else. "Results" is a label; "Checkout completion rose from 31% to 36% on
  2,140 advertisers" is a title. The title slide may be short.
- **`Covers:`** lists the stage tags the slide satisfies, comma separated.
  Required tags per stage (a technical audience adds the second list):

  | Stage | Every audience | Technical audience adds |
  | --- | --- | --- |
  | `poc-approval` | problem, hypothesis, success-criteria, scope, cost, risks, ask | architecture, contracts, evidence-plan, dependencies |
  | `production-approval` | criteria-results, learned, production-scope, cost, risks, ask | architecture, contracts, evidence, operations |
  | `final-results` | outcome, adoption, cost, incidents, next (an `ask` slide only when there is a decision) | architecture, evidence, operations, handover |
  | `case-study` | challenge, solution, results, next | |

  Other accepted tags: title, agenda, summary, method, demo, team, timeline,
  questions, appendix. Slides tagged `questions` or `appendix` hold the
  answers to expected questions and vanity counts; they do not count
  against the minutes.
- **`Evidence:`** cites where the slide's claim comes from: a goal or
  acceptance ID (`G03/A2`), a contract, decision or requirement ID (`C4`,
  `D2`, `R1`), a measurement or incident record in the plan (`M2`, `I1`),
  a file path or URL, or one of the labels `hypothesis`,
  `assumption`, `measured`, or `n/a: <why no evidence is needed>`. A slide
  with a number (a percentage, money, hours, a count) and `n/a` or no
  evidence fails the check. A slide whose only evidence is a hypothesis
  label gets a warning: its title must read as expected, not measured.
- **`Notes:`** is the last block of the slide and holds what the speaker
  says. Everything after the marker to the end of the slide is notes; the
  body (what the audience sees) comes before it. Write the notes as speech,
  in full sentences, with the pause and the handover to the next slide. The
  checker warns when a title or a body passes its budget: 20 and 40 words
  for a business or public deck, 30 and 80 for a technical deck (whose
  titles carry the qualifier and whose bodies quote contracts), 70 for the
  ask slide's body; title and appendix slides are not budgeted. See
  [slide craft](../references/slide-craft.md).
- **Redrafts:** a deck drafted from the brief alone is redrafted from the
  design and plan under the same name; keep the earlier draft as
  `<stage>-<audience>.v1.md` beside it when the user wants the history.
  Before the design exists, cite the brief's sections and write "pending
  design" on the cost and scope slides. Pre-wiring rows read "pending"
  until someone has been briefed. On a slide that mixes
  measured and estimated figures, each bullet opens with its voice word.
- **Timing:** `minutes` is the slot. The speech takes about two thirds of
  it and questions the rest, so the notes spoken at about 150 words a
  minute should cover between 40 and 80 percent of the minutes; about one
  timed slide per one to three minutes, title and appendix slides excluded.
  The checker warns outside those ranges.
- **Public wording:** on a `case-study` deck the checker fails wording
  Google's co-branding guidelines do not allow: `GCP`, `powered by Google`,
  `with Google Cloud AI`, partner or preference claims. See the
  [case-study reference](../references/case-study.md) for the approved phrases.

Run the check from the project root with any Python 3.9 or later:

```bash
python3 "$SKILL_DIR/scripts/check_deck.py" --deck docs/presentations/<topic>/poc-approval-business.md
```

Exit 0 means every slide cites evidence or says why not, and the stage's
coverage is complete. Exit 1 lists what to fix. Warnings do not fail the
check; read them anyway.

Beside the outline in the same folder, one per stage:
`decision-memo-<stage>.md` (the one-page pre-read and, after the meeting,
the record) and `pre-wiring-<stage>.md` (who was briefed before the meeting,
what they said, and the premortem answers). A headline number on the title
slide cites its evidence like any other number. When the record names a
role but no person as decider, the role is acceptable. A table in a slide
body is a visual and is not counted against the word budget. Short notes
are acceptable when a recorded demo or the linked documents fill the slot;
say so in the title slide's notes, and read the timing warning as
information.

Rendering: the outline is the deliverable the reviewer reads and the source
the slides are built from. When the host offers a slide-building tool or
skill, build the slides from this file, one slide per section, action title
as the slide title, bullets as the body, `Notes:` as speaker notes, and keep
the `Evidence:` line out of the audience's view (it goes in the notes or an
appendix). Without such a tool, Pandoc converts the body to PowerPoint or
reveal.js once the `Covers:` and `Evidence:` lines are moved into the notes;
or hand the outline to whoever owns the company template.
