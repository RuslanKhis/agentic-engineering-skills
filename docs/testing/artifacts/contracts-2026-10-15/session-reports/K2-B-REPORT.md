# REPORT: ADK travel-policy bot design session

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (by the user, via `/adk-system-designer`). It was the only skill invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (model choice, as SKILL.md:199-204 requires)
7. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md`, first 30 lines (pinned ADK version 2.8.0)
8. `.claude/skills/adk-memory-architecture/references/compatibility.md`: grep only
9. `.claude/skills/adk-agent-instructions/SKILL.md` and `references/adk-instruction-mechanics.md`: grep, plus lines 90–115 (`static_instruction` and templating `KeyError`)
10. `.claude/skills/adk-operational-guardrails/references/*`: grep only (`adk web` does not apply `RunConfig.max_llm_calls`)
11. `.claude/skills/adk-system-designer/assets/system-design-template.md`, lines 1–25
12. `.claude/skills/adk-system-designer/scripts/check_schedule.py`, header and argument parser

I did not open `gcp-decisions.md` or `runtime-and-delivery.md` because their triggers don't apply: there's no cloud and no streaming or concurrency contract. I also skipped the plan template, the ticket template and the plan-review prompt, since this is a compact POC with no tickets and a single person, so review is skipped.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer | Depends on it |
| --- | --- | --- | --- |
| Q1 | How many hours is "one afternoon", and does the demo happen inside it? | 4 build hours; the demo comes afterwards | Capacity of 2.4 h after reserve, and the cut line |
| Q2 | Who builds it, and how familiar are they with ADK and GCP? | One developer, new to ADK | ×1.5 multiplier on every estimate |
| Q3 | Is the code thrown away or continued? | Kept if the demo lands | PDF path configurable; phase 2 written |
| Q4 | What spend is available, and through which key? | A few dollars on a Gemini API (AI Studio) key | D4 Flash tier, D5 budget alert, U3 |
| Q5 | Does the company require Vertex AI and a GCP project instead of an API key? | No | U3: Vertex would add about half a day |
| Q6 | How long is the PDF? Does it have a text layer, and does it have tables? | Under about 50 pages and 50k tokens, with a text layer, and some tables | D1 (whole document in context, no RAG), D2 (pypdf extraction), U1, U2 |
| Q7 | Must answers cite pages, and how should the bot handle questions outside the policy? | Cite `[page N]`; reply "not covered by the policy" | D3, G03/A1–A2 |
| Q8 | Is this POC profile right, or is it meant to become a daily internal tool? | POC | Depth table and graduation conditions |
| Q9 | Do you accept cut line G01–G03, with G03 shrunk if time runs short? | Yes | §5 cut line |

## 3. Files written or changed, and what was not finished

- **Written:** `docs/architecture/travel-policy-bot.md`. It holds the compact design and plan: the assumed scope gate, profile, journey, six decisions (D1–D6), floor and depth table, graduation conditions, a failure grid, phase 1 goals G01–G03 with acceptance items and run prompts, phase 2 goals G04–G06, a later list and open decisions U1–U4.
- **Written:** `REPORT.md`, this file.
- **Not done:** no code (`travel_policy_bot/`, `policy_loader.py`, tests). The request was for a design and plan only, and the skill forbids implementing from a design request. The design stays a **draft** because every scope-gate assumption needs the user to confirm it. The cut line has not been confirmed by the user. The design is about 1,600 words including tables, above the skill's target of about 1,200 words. The model lifecycle table (checked_on 2026-10-08) was not refreshed because the network is off.

## 4. Checks

**Run:**
- `python3 -m pytest -q .claude/skills/adk-system-designer/tests` → 16 passed. These tests cover the helper script, not the design.
- `check_schedule.py --design docs/architecture/travel-policy-bot.md` → exit 2: "give --plan, --tickets or both".
- `check_schedule.py --plan <design> --design <design>` → exit 2: "no fenced yaml block with '- goal:' entries". The compact form deliberately has no yaml block, so the grid check could not run.
- I checked the grid citations by hand with grep. All ten cited items (G01/A1–A3, G02/A1–A3, G03/A1–A4) exist, and every other cell is `n/a: <two+ words>`.
- Capacity arithmetic by hand, as the compact form prescribes: 4 × 0.8 = 3.2 h, minus 25% = 2.4 h. Phase 1 is 0.75–1 + 0.75–1.25 + 0.5–0.75 = 2.0–3.0 h, so the low end fits and the high end does not.
- Word count: about 1,612 words, excluding markdown punctuation.

**Not run:**
- Any test importing `google.adk`. None exists yet, and the dependencies aren't installed.
- `adk web`, Gemini calls, and checks of the PDF token count or text layer (no PDF was provided, and the network is off).
- The model lifecycle refresh and the ADK version check against official docs (network is off).
- Python 3.9.13 is installed; the skill wants 3.11+ for the helper (delivery-profiles.md:223). The helper's own tests passed on 3.9 anyway.

## 5. Friction log

- **Unsure: interview versus headless.** SKILL.md:50-52 tells me to let the user answer before settling material choices. SKILL.md:121-127 covers the no-reply case with an **Assumed answers** table, and that resolved it cleanly. *Helpful.*
- **Contradiction: schedule helper for a POC.** SKILL.md:94-95 says to compute totals with `scripts/check_schedule.py` "rather than by hand". delivery-profiles.md:165 and :294 say a one-person POC adds goals by hand, with "no schedule block or helper run". failure-review.md:33-35 says to run the helper with `--design` to check grid cells, but scripts/check_schedule.py:451 refuses `--design` without `--plan`, and the plan must contain a yaml block. **So a compact POC cannot get its grid machine-checked without breaking the compact form.** I checked by hand. Suggested fix: allow `--design` alone.
- **Heavier than needed: full failure grid for a no-tool, read-only bot.** failure-review.md:14 has eight columns. Most cells are `n/a`. failure-review.md:36-37 ("A proof of concept fills the rows it touches in a few words each") kept it tolerable, but the 2×8 table is the densest part of a 10-minute document.
- **Unsure: the word budget.** SKILL.md:84 and delivery-profiles.md:273 say about 1,200 words. The mandatory parts already push it to about 1,600: the six-decision table, depth table, grid, three goals with numbered acceptance items and run prompts, phase 2, the later list and open decisions. It's unclear whether tables count.
- **Unsure: the 1.5 multiplier and rounding.** delivery-profiles.md:149-151 (×1.5 applied to everything) combined with delivery-profiles.md:113 (quarter-hour rounding) produces awkward values like 1.125, and the skill doesn't say which way to round. I rounded up.
- **Genuinely helpful: the `adk web` spend-cap caveat.** delivery-profiles.md:77-80 says to put the cap on the model project when `adk web` is the host. adk-operational-guardrails/references/evidence.md:14 confirms that ADK Web doesn't apply a separate runtime budget. Without these I would have proposed `max_llm_calls`, which wouldn't work in this demo.
- **Genuinely helpful: the templating trap.** adk-agent-instructions/SKILL.md:19,51 and references/adk-instruction-mechanics.md:94-100 point out that a string `instruction` containing PDF text with `{` raises `KeyError`. That is a concrete demo-killer, and it led to D2 (`static_instruction`) and the G02/A2 test.
- **Genuinely helpful: the dated model table.** adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:21-23 shows `gemini-2.5-*` retiring on Vertex on 2026-10-20, five days from now. From memory I would have picked it.
- **Light friction: the specialist name for a no-tool single agent.** implementation-handoff.md:21 maps "bounded orchestration" to `adk-workflow-design`. For a single agent with no tools, `adk-agent-instructions` is arguably the real owner of G01/G02, so I used workflow-design for G01 and instructions for G02.
- **Heavier than needed, though correctly skipped:** SKILL.md:204-206 says to check service availability, regions and prices with citations. That isn't applicable to a local demo, but the skill gives no explicit "skip when local only" line.

## 6. Exact next prompt the skills told the user to type

The skill's own example (SKILL.md, "Deliver and hand off") is:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Adapted to this design, where the compact form keeps the plan inside the design file:

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```
