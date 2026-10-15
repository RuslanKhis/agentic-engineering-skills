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
Notes: Open with the funnel, in one breath. Product choice loses 38% of
eligible advertisers; creative upload loses 12%. Then pause.

- 38% leave at product choice (last quarter, 2,140 advertisers)
- 12% leave at creative upload

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
  one sentence the audience is asked to decide; `decider` and `date` name
  who decides and when (the checker warns when they are missing).
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
  | `final-results` | outcome, adoption, cost, incidents, next, ask | architecture, evidence, operations, handover |
  | `case-study` | challenge, solution, results, next | |

  Other accepted tags: title, agenda, summary, method, demo, team, timeline,
  questions, appendix. Slides tagged `questions` or `appendix` hold the
  answers to expected questions and vanity counts; they do not count
  against the minutes.
- **`Evidence:`** cites where the slide's claim comes from: a goal or
  acceptance ID (`G03/A2`), a contract, decision or requirement ID (`C4`,
  `D2`, `R1`), a file path or URL, or one of the labels `hypothesis`,
  `assumption`, `measured`, or `n/a: <why no evidence is needed>`. A slide
  with a number (a percentage, money, hours, a count) and `n/a` or no
  evidence fails the check. A slide whose only evidence is a hypothesis
  label gets a warning: its title must read as expected, not measured.
- **`Notes:`** holds what the speaker says. Everything after the marker to
  the end of the slide is notes; write it as speech, in full sentences,
  with the pause and the handover to the next slide. On a slide that mixes
  measured and estimated figures, each bullet opens with its voice word.
- **Timing:** about one slide per one to three minutes, title and appendix
  slides excluded, and the notes spoken at about 130 words a minute should
  fill between half and all of the minutes. The checker warns outside
  those ranges.
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

Beside the outline in the same folder: `decision-memo.md` (the one-page
pre-read and record) and `pre-wiring.md` (who was briefed before the
meeting, what they said, and the premortem answers).

Rendering: the outline is the deliverable the reviewer reads and the source
the slides are built from. When the host offers a slide-building tool or
skill, build the slides from this file, one slide per section, action title
as the slide title, bullets as the body, `Notes:` as speaker notes, and keep
the `Evidence:` line out of the audience's view (it goes in the notes or an
appendix). Without such a tool, Pandoc converts the body to PowerPoint or
reveal.js once the `Covers:` and `Evidence:` lines are moved into the notes;
or hand the outline to whoever owns the company template.
