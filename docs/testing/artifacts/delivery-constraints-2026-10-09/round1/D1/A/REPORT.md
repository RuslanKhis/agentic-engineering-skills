# REPORT — support email triage POC design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's slash command); `SKILL.md` loaded.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/assets/system-design-template.md`
7. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
9. Grep across `.claude/skills/adk-*/references/compatibility.md` for the checked ADK version (2.8.0).
10. Grep excerpts of `.claude/skills/adk-model-and-output-contracts/references/model-selection.md`, `output-contracts.md` and lines 1–20 of its `compatibility.md` (refusal shape, `output_schema` behaviour in 2.8.0).

Not opened, on purpose: `runtime-and-delivery.md`, `gcp-decisions.md` (their triggers — streaming, concurrency, hosting, service choice — do not apply to a local, tool-less POC), and `ticket-template.md` (no tickets requested). No other skill was invoked.

## 2. Questions I would have asked, and the answers assumed

These are also the **Assumed answers** table at the top of the design.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | After the demo, is this thrown away or continued? | Probably continued, so phase 1 code is kept (config in one place). |
| A2 | How familiar are you with ADK and GCP? | New to ADK; comfortable with Python; no GCP project set up for this. |
| A3 | How much can you spend on models? | Under USD 10, with a spend cap set in the provider console. |
| A4 | Which categories does support use? | `billing`, `technical_issue`, `account_access`, `feature_request`, `complaint_or_cancellation`, `other` (in one config list so they can be renamed). |
| A5 | What format are the 50 samples in? | One CSV or JSONL file with `id`, `subject`, `body`; unlabelled. |
| A6 | Are there reply macros or a knowledge base to ground drafts? | No. Drafts must not invent policy facts; they use `[CONFIRM: ...]` placeholders. |
| A7 | May anonymised samples go to a hosted model (Gemini API, paid tier)? | Yes. If not, Vertex AI in a company project (about half a day more, breaks the cut line). |
| A8 | What will the head of support look at? | A live `adk web` run on 2–3 emails, plus a 50-row results table with an agreement score. |
| A9 | Will you label some emails yourself? | Yes, about 15, during G03 (~20 min). |
| — | Confirm the profile (proof of concept) and the cut line (G01–G04, ~3 h of 4 focused hours)? | Assumed confirmed. |

## 3. Files written or changed; what was not finished

- **Written:** `docs/architecture/support-email-triage.md` — design and plan in one file (the skill allows a small effort to keep its plan in the design): assumed answers, profile, depth table, floor, cut line, invariants, decisions D1–D6, model-facing contracts, security posture, failure table, goals G01–G04 with run prompts, phase 2 (P2-1 to P2-6), a later list, open decisions.
- **Written:** `REPORT.md` (this file).
- No other files changed. No code, tests, dependencies or config were written (design-only request).
- **Not finished / still open:** every product decision is provisional (user not available). Model pricing, the Gemini models page and the ADK pin were not rechecked live (no network); the design cites the lifecycle snapshot dated 2026-10-08 and marks it for rechecking. The document is longer than the skill's "ten-minute read" target (see friction log). No tickets were written (not requested).

## 4. Checks run and not run

Run:
- Word count of the design: 3,495 words — over a ten-minute read.
- Grep for unfilled template placeholders (`<...>`): one hit, intentional (`google-adk==<pin>`, because the pin is decided in G01).
- Every skill named in the design exists under `.claude/skills/`: all 15 names resolved.
- `git status`: only `docs/` (and this report) added.

Not run:
- Any Python test or ADK import: no code exists, and google-adk is not installed (and installing was forbidden). Every acceptance check in G01–G04 is **planned, not run**.
- Live model calls, pricing lookup, ADK version check against official docs: forbidden (no network).

## 5. Friction log

- **Unsure: how to run a "scope gate" when the user can't answer.** SKILL.md:73–74 says to let the user correct the profile, and SKILL.md:87–91 says to ask the user to confirm the cut line; SKILL.md:117–120 settles it (no further questions; an Assumed answers table; decisions provisional). Helpful once found, but it sits ~50 lines after the instructions to ask.
- **Genuinely helpful: the worked example matches this request almost word for word.** `references/delivery-profiles.md:137–145` ("Five hours, one developer, demo tomorrow, 50 anonymised emails") gave the profile, capacity arithmetic, the goal split and the floor ("drafts only"). I used it directly; the risk is that a designer copies it without thinking about details it leaves out (category list, knowledge-base grounding).
- **Helpful: the floor list.** `references/delivery-profiles.md:76–83` turned "POC" into five concrete minutes-cost items; it drove I1, I5, I6 and D5.
- **Helpful: the lethal-trifecta check.** `references/design-decisions.md:182–191` made it clear that a tool-less agent breaks the trifecta structurally, so no security goal was needed in phase 1 — only one adversarial sample.
- **Helpful: model choice from a dated file, not memory.** SKILL.md:192–197 pointed to `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`; it showed that the 2.5 models retire on Vertex on 2026-10-20 and that `gemini-3.8-flash` is the stable pick.
- **Unsure: plan in a separate file or not.** SKILL.md:241–242 says `docs/plans/<topic>.md` "for a multi-goal effort" but "a small effort can keep its plan in the design". Four goals is both. I kept one file because SKILL.md:81–83 wants ten minutes of reading. The example prompt at SKILL.md:274 and `implementation-handoff.md:105` assume a separate plan path, so I adapted the prompt to the design path.
- **Heavier than needed: per-goal fields vs the ten-minute target.** `assets/implementation-plan-template.md:50–69` asks for 11 fields per goal, and `assets/system-design-template.md` has ~10 sections. Filling them for four small goals took the design to ~3,500 words, against SKILL.md:81–83 ("a reviewer reads in ten minutes"). The template does not say which fields can be skipped for a POC. The failure table (`references/failure-review.md:23–43`) was also more than needed; most rows were "not applicable" and I put them on one line, as `failure-review.md:4–5` allows.
- **Unsure: which reference files are mandatory.** SKILL.md:93–96 says every design reads design-decisions and failure-review, and others only "when their trigger applies"; the trigger for `gcp-decisions.md` (SKILL.md:183–184) says "when selecting services". Using a Gemini API key is arguably a service choice; I skipped it because nothing is hosted. A one-line "skip for local POCs" would remove the doubt.
- **Unsure: the primary skill for a goal with no specialist (G04 demo rehearsal).** `references/implementation-handoff.md:42–51` requires one primary skill per goal; a demo run sheet has none. I wrote "none needed; `adk-engineer` directly".
- **Unsure: the ADK version.** SKILL.md:188–193 says to use the version in each specialist's `compatibility.md`. Grepping them gave 2.8.0, plus notes about 2.9–2.11 (e.g. observability recommends ≥2.10 for new production deployments). For a POC I used 2.8.0 and made confirming the pin part of G01's acceptance.

## 6. Next prompt the skills told the user to type

The skill (SKILL.md:268–277) says to end with the exact prompt for the next ready goal. Following its pattern, adapted to where the plan lives, the prompt given in the design's "Resume here" section is:

```text
/adk-engineer Carry out G01 from docs/architecture/support-email-triage.md.
```

The skill's own literal example, which has a placeholder path, is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
