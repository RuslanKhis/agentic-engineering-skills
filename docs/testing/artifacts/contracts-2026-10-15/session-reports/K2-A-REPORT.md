# REPORT: travel policy bot design session

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (through `/adk-system-designer`). No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`: read in full.
3. `.claude/skills/adk-system-designer/references/failure-review.md`: read in full.
4. `.claude/skills/adk-system-designer/references/design-decisions.md`: lines 1–255 (contracts, sizing to the judge, outcome/orchestration, state and knowledge, identity and tools). I skipped external effects, latency/ops and analytics because they don't apply to a read-only local demo.
5. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`: used to choose the model ID.
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`: read in full.
7. `.claude/skills/adk-memory-architecture/references/local-document-coverage.md`: lines 1–40, and the headings of `retrieval-strategy.md`.
8. `grep` over `.claude/skills/adk-agent-instructions/references/*.md`. Used `compatibility.md:14` to confirm that an `InstructionProvider` callable bypasses state injection (ADK 2.8.0), and `compatibility.md:15` for the `KeyError` on a missing template key.
9. `grep` over the specialists' `references/compatibility.md` files, to get the ADK version they assume (2.8.0).

Files I didn't open: `gcp-decisions.md`, `runtime-and-delivery.md` (their triggers don't apply: no GCP services, no streaming or capacity concerns), the templates under `assets/`, and `plan-review-prompt.md` (`SKILL.md:286` says a single-person POC skips the review).

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Is it continued after the demo? | Maybe, so the code is written in a form that can be kept |
| 2 | Who builds it, and how many hours? How familiar are they with ADK? | One developer, about 4 h, knows Python, new to ADK (×1.5 multiplier) |
| 3 | What is the model/cloud budget? | A small allowance on an existing Gemini API key |
| 4 | Who judges it, and what do they see? | The team, watching a live `adk web` session |
| 5 | Data and effects | Given by the user: one public PDF, no personal data, read only |
| 6 | Is the PDF text-based or scanned, and how many pages? | Text-based, under about 60 pages |
| 7 | Can the PDF be committed to the repo? | Yes (it's public) |
| 8 | Gemini API key or Vertex AI? | Gemini API key |
| 9 | Should answers cite page or section? | Yes, page and section heading |
| 10 | Who is the policy owner the bot should refer people to? | Unknown; left as an open decision in the design |
| 11 | Is the user's ADK version already chosen? | No; assume `google-adk==2.8.0` and confirm in G01/A1 |

## 3. Files written or changed; what was not finished

- Written: `docs/architecture/travel-policy-bot.md`. This is the design and plan together, in the compact form for a POC (status: draft, all answers assumed).
- Written: `REPORT.md` (this file).
- No code was written. The user asked for a design and plan, and the skill says not to scaffold or implement merely because a design names a component. G01–G03 are not started. No tickets were written (the user didn't ask for any).
- Not finished or unresolved: all the assumed answers in section 2 still need the user's confirmation. The policy owner's name for C2 is unknown. The budget alert on the API key's project is a console step only the user can do.
- The design is about 1,630 words with table markup removed, against the compact form's "about 1,200". The assumed-answers table, the failure grid and the depth table account for the overrun. I kept them rather than cutting floor or failure rows.

## 4. Checks run and not run

Run:
- Plan arithmetic with `python3 -c`: goals sum to 1.5–2.5 h; capacity after reserve is 4 × 0.8 × 0.75 = 2.4 h. The figures match the plan.
- Word count with `wc -w`: 1,855 raw, 1,630 with markup stripped.
- `git check-ignore .env`: there is no `.gitignore` yet. That is expected, because creating it is in G01's scope (G01/A3).

Not run:
- Any test that imports `google.adk`: none exist yet, and google-adk is not installed.
- `scripts/check_schedule.py`: the compact form says to add the estimates by hand with no helper run (`delivery-profiles.md:172`, `:306`), and the plan has no `yaml` schedule block for it to read.
- `tests/test_check_schedule.py`: not relevant to this design.
- No network lookups. Model lifecycle facts come from the bundled table (`checked_on` 2026-10-08), not from live docs. ADK API facts come from the specialist's compatibility notes (2.8.0), not the user's installed version.
- Independent plan review: skipped, because `SKILL.md:286` says a single-person proof of concept skips it.

## 5. Friction log

- **Contradiction on the schedule helper.** `SKILL.md:95` says to compute totals with `scripts/check_schedule.py` "rather than by hand". `delivery-profiles.md:172-173` and `delivery-profiles.md:306` say a one-person POC adds the estimates by hand with no helper run. I followed the compact form. The SKILL line should carry the exception.
- **Word budget versus mandatory content.** `SKILL.md:82-84` sets about 1,200 words. Several required pieces push past it:
  - the Assumed answers table at the top (`SKILL.md:125`);
  - the failure grid, which every cell must fill (`failure-review.md:29-37`);
  - the depth table (`delivery-profiles.md:66`).

  `delivery-profiles.md:289-290` says to fold assumed answers into the scope table, which helped. Even so, a headless POC ends up over budget. It's unclear which of these should give.
- **Failure-grid requirement versus the compact form.** `SKILL.md:100-101` says every design reads the failure review. `failure-review.md:29-31` says every cell cites an acceptance item or `n/a`. Against that, `delivery-profiles.md:308-309` says failure tables appear "only when the journey actually holds that risk… two or three rows". `failure-review.md:37` ("A proof of concept fills the rows it touches in a few words each") reconciles them, but only once you've read both files.
- **Where the file goes.** `SKILL.md:294-296` gives `docs/architecture/<topic>.md`, and a plan that "a small effort can keep… in the design". But the closing example prompt at `SKILL.md:328` points at `docs/plans/<topic>.md`. I adapted the prompt to the architecture file. A short note would remove the doubt.
- **Spend floor under `adk web`.** `delivery-profiles.md:84-87` was helpful. It anticipates that `adk web` owns the Runner and moves the cap to a project budget alert. Without it I would have planned a `max_llm_calls` that can't be set.
- **Model choice.** The dated lifecycle table (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, mandated at `SKILL.md:231-234`) was genuinely helpful. It ruled out `gemini-2.5-*` (Vertex retirement in 5 days) and `gemini-3.6-flash` (Nov 19).
- **Templating trap.** `adk-agent-instructions/references/compatibility.md:14-15` surfaced a real bug that would have hit the demo: braces in the PDF text raising a templating `KeyError`. This led to D2's `InstructionProvider` choice. The designer skill doesn't point to it; I found it by grep.
- **Heavier than needed.** The full scope gate and the six-field contract format (`SKILL.md:164-182`) are more than a one-afternoon, read-only demo needs. The compact form's one-line contracts (`delivery-profiles.md:293-295`) were the right size, and I used those.
- **Estimate table.** `delivery-profiles.md:147` has no row for "an agent with no tools", and its smallest row (1–2 h) includes tools. So my G01 base estimate is a judgment call. The multiplier rule at `delivery-profiles.md:156-158` was clear.
- **Unsure whether to implement.** The user's "Give me a short design and plan" sounds design-only, but "show my team this afternoon" suggests they might want code. `SKILL.md:24-27` and `SKILL.md:339-341` settled it: design only, and the plan hands off to `adk-engineer`.

## 6. Exact next prompt the skill told the user to type

The skill's own example, verbatim (`SKILL.md:328`):

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

The concrete prompt given in the design, adapted to where this plan actually lives:

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```
