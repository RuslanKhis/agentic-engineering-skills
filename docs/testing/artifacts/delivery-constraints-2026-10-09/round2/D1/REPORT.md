# REPORT: support email triage POC design (headless run, 2026-10-09)

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer`, by the user's slash command. No other skill was invoked.
2. `.claude/skills/adk-system-designer/SKILL.md`, loaded with the skill.
3. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (all of it)
4. `.claude/skills/adk-system-designer/references/design-decisions.md` (all of it)
5. `.claude/skills/adk-system-designer/references/failure-review.md` (all of it)
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (all of it)
7. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md` (grep only, for the ADK pin and the output_schema/tools rows)
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
9. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (lines 1–60)

I did not open `gcp-decisions.md` or `runtime-and-delivery.md`, because their triggers don't apply: the POC runs locally, with no hosting choice and no streaming or capacity requirement. I did not open `system-design-template.md` either, because the compact form tells a POC to leave the template out (delivery-profiles.md:149-150).

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Is the POC continued after the demo or thrown away? | It may continue, so phase 1 code is written to be kept (categories and prompt in files) |
| 2 | How familiar are you with Python, ADK and GCP? | Comfortable with Python, new to ADK, and you won't set up a GCP project today |
| 3 | What spend is available for models? | A small allowance (≤ US$20) on a Gemini API key |
| 4 | Do you already have a Gemini API key, or must you use Vertex AI? | A Gemini API key exists. Vertex would add about 0.5 h and change G01 |
| 5 | What will the head of support look at: a live demo, a table, a number? | A live `adk web` run on 2–3 emails, plus a table of all 50 with an agreement figure |
| 6 | What is the category list? | billing, technical_issue, account_access, feature_request, complaint, other_needs_human |
| 7 | Where are the 50 emails, and in what format? | One `.txt` or `.eml` per email in `data/samples/`. They are not in the repo yet |
| 8 | Are any emails already labelled with the correct category? | None. You label 12 (about 15 min) |
| 9 | Is the anonymisation trustworthy, with no real PII left? | Yes, so sensitive-data controls are deferred |
| 10 | Are there reply policies, templates or a knowledge base the drafts should use? | None. Drafts use `[placeholder]` slots and must not invent facts |
| 11 | Should the system ever send, or save drafts into a mailbox? | No. It shows draft text only, and a human copies and sends it |
| 12 | Language of the emails? | English only |
| 13 | Do you confirm the cut line G01–G03 (2.0–3.0 h of the 5 h)? | Assumed confirmed. It's marked as an open decision in the design |

## 3. Files written or changed, and what was not finished

- Written: `docs/architecture/support-email-triage.md`, which holds the design and plan in one file, as the skill allows for a small effort (SKILL.md:242-245).
- Written: `REPORT.md`, this file.
- Nothing else was changed and no code was written, as requested.
- Not finished:
  - The design is about 1,780 words by `wc` against the compact form's target of about 1,200 (SKILL.md:82-84, delivery-profiles.md:146-148). I did not trim it.
  - The model price is not cited, because there was no network access. G03 includes a pricing-page check.
  - The ADK pin is an assumption (2.8.0) and becomes G01's first acceptance item.
  - None of the assumptions in section 2 has been confirmed.
  - No tickets were written, because none were requested.

## 4. Checks run and not run

Run:
- `wc -w` on the design: 1,784 words, over the target.
- Every skill named in the plan exists under `.claude/skills/` (11 of 11).
- The cited lifecycle file exists, and `gemini-3.8-flash` is listed there as stable with `shutdown: null` (checked_on 2026-10-08).
- Each phase 1 goal has a run prompt (3 of 3).
- A grep for key-like strings in the design found none.

Not run:
- Any Python or ADK test. No code exists, and google-adk is not installed.
- Any network lookup: model pricing, current ADK docs, Gemini lifecycle refresh.
- Any cloud command, such as setting the budget alert.

## 5. Friction log

- **Helpful: the headless rule.** `adk-system-designer/SKILL.md:119-122` says to stop asking, put an Assumed answers table at the top and mark the dependent decisions provisional. That settled at once how to handle "user not available".
- **Helpful: a worked example matching this exact request.** `references/delivery-profiles.md:170-178` covers five hours, one developer, a demo tomorrow and 50 anonymised emails, including the 4 h capacity and the phase 1 split. The plan follows it closely. It is so close that it raises the question of whether the skill was tuned to this prompt.
- **Helpful: the floor in `adk web`.** `delivery-profiles.md:77-80` explains that `max_llm_calls` can't be set when the demo runs through `adk web`, so the cap goes on the model project instead. I would have missed that and claimed a cap the demo doesn't have.
- **Helpful: the lifecycle asset.** `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12` meant the model choice came from data rather than memory. It also showed that the 2.5 models retire on Vertex on 2026-10-20 (line 21–23), which a memory-based choice might have picked.
- **Unsure: two formats for the assumptions.** `SKILL.md:120` asks for an "Assumed answers" table at the top, but `delivery-profiles.md:152-153` folds assumed answers into the constraints table, one line each. I merged them into one table with an "A =" marker.
- **Unsure: how much of the template to adapt.** `SKILL.md:245` says to adapt the design and plan templates, but `delivery-profiles.md:149-150` says to leave the rest of the template out. The compact form won because it is more specific.
- **Unsure: the explanation chain differs.** It has five links at `SKILL.md:126` (requirement → choice → reason → tradeoff → verification) but four at `delivery-profiles.md:156-157` (requirement, choice, tradeoff, check). I used the four-column version and folded the reason into the choice.
- **Unsure: the primary skill for G01.** `references/implementation-handoff.md:21` maps "bounded orchestration / LlmAgent" to `adk-workflow-design`. A one-agent, no-tool classifier is really an output contract (line 24), so I chose `adk-model-and-output-contracts`, but the mapping doesn't cover this case.
- **Unsure: citing prices without network access.** `SKILL.md:199-200` says to check prices and cite sources before relying on them. That was impossible here, so I kept the decision provisional, which SKILL.md:201-202 allows when lookup is unavailable.
- **Unsure: confirming the cut line headless.** `SKILL.md:91-92` and `delivery-profiles.md:118-120` say to ask the user to confirm the cut line. In a headless run I recorded it as an open decision instead.
- **Heavier than needed: reading all of `design-decisions.md`.** `SKILL.md:95-96` says every design reads it, and that is 343 lines. For a draft-only POC, roughly lines 26–61 (proportionality), 115–124 (model interface), 182–196 (trifecta) and 296–313 (pin, output contract) were relevant. The section-level guidance ("for the sections its journey touches") helps, but deciding which sections apply still meant reading the whole file.
- **Heavier than needed: the failure-review table.** At `references/failure-review.md:23-43` it has 20 scenarios, and only 3 applied. `delivery-profiles.md:165-166` correctly limits this to 2–3 rows, which kept the output small, but the reading cost stayed.
- **Hard to hit: the 1,200-word target.** Six sections, phase 1 goals of 4–6 lines, phase 2 goals and a later list (`delivery-profiles.md:152-163`) don't fit comfortably in about 1,200 words when every assumption needs a row. I went over.

## 6. Exact next prompt the skills told the user to type

The skill (`SKILL.md:270-276`) requires the closing message to give the exact prompt for the next ready goal. Its example uses `docs/plans/<topic>.md`, but this design keeps the plan in the design file, so the prompt given is:

```text
/adk-engineer Carry out G01 from docs/architecture/support-email-triage.md.
```
