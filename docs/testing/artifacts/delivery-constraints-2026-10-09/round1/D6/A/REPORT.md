# REPORT: support-inbox reply POC design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's slash command. Its SKILL.md was loaded in full.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`, read in full.
3. `.claude/skills/adk-system-designer/references/design-decisions.md`, read in full.
4. `.claude/skills/adk-system-designer/references/failure-review.md`, read in full.
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`, read in full.
6. `.claude/skills/adk-system-designer/assets/system-design-template.md`
7. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, used for the model choice.
9. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md`. I only grepped this for the pinned ADK version (2.8.0).
10. `.claude/skills/adk-agent-security/SKILL.md`. I only grepped this for "trifecta" and "gmail".

Not opened: `gcp-decisions.md` and `runtime-and-delivery.md`, because their triggers don't apply (no hosting or streaming in phase 1), and `ticket-template.md`, because no tickets were requested. No other skill was invoked.

## 2. Questions I would have asked, and the answers I assumed

These are also recorded as the "Assumed answers" table at the top of the design.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Can the POC send to real customers with nobody checking first? (The delivery-profile floor requires this question.) | **No.** It produces drafts that a person sends. Automatic sending is deferred to phase 2, after measured precision and explicit user acceptance. |
| A2 | When is it due, and is it continued afterwards? | Today, about 4 h. It is continued if the demo lands, so the code is written to be kept. |
| A3 | Who builds it, and how familiar are they with ADK, GCP and Gmail? | One developer, new to ADK, has used GCP before, has never set up a Gmail OAuth client. |
| A4 | What budget is there? | A few dollars of model spend on a paid-tier Gemini API key. No cloud spend. |
| A5 | Who judges it, and what do they read? | The builder and a support lead: a live demo and a table of drafts to review. |
| A6 | Which mailbox is it, and is OAuth allowed? | A Workspace mailbox the developer can sign in to; the admin allows an internal OAuth app. |
| A7 | What counts as "simple", and where do the answers come from? | A question fully answered by a short FAQ (≤ 2 pages) with no system lookups. |
| A8 | Is it OK to send real customer mail to the model? | Yes, minimised to subject and body, truncated, and kept out of logs. |
| A9 | What language, and how much mail? | English, fewer than 100 a day. The POC processes 25 messages. |
| A10 | Which ADK version? | None is installed, so I assumed 2.8.0 (from the specialists' compatibility notes). Confirming it is in G01's acceptance. |

## 3. Files written or changed, and what was not finished

**Written:**
- `docs/architecture/support-inbox-poc.md`: the design and phase 1 plan in one file, as the skill allows for a small effort. It contains:
  - assumed answers, scope and depth table, floor and cut line
  - invariants I1–I5 and decisions D1–D5
  - model-facing contracts, security posture and failure table
  - goals G01–G04 in full, phase 2 goals G05–G08 at a coarser level, the Later list, open questions Q1–Q4, and a resume prompt
- `REPORT.md`: this file.

**Not changed:** anything under `.claude/`.

**Not finished, by design** (the request was design only):
- No code, no tests, no `pyproject`.
- No tickets.
- No separate `docs/plans/` file.

**Still open:**
- All decisions are provisional, because the user could not confirm them.
- The model lifecycle, Gmail API scope semantics (that `gmail.compose` also permits sending) and the OAuth policy were **not verified online**: network was not allowed. They come from my own knowledge and the skill's bundled lifecycle file (checked_on 2026-10-08).

## 4. Checks run and not run

**Run:**

| Check | Result |
| --- | --- |
| Every phase 1 goal (G01–G04) has exactly one detail section, one `Primary skill` line and one `/adk-engineer` run prompt | Pass, for all 4 goals |
| Grep of the design for secret-like strings (`api_key=`, `AIza`, `client_secret`, `ya29.`) | None found |
| Every skill named in the plan exists under `.claude/skills/` | Pass, 13 names checked |
| The chosen model `gemini-3.8-flash` appears in the bundled lifecycle JSON | Pass: stable, released 2026-09-02, no shutdown date |
| Design length | 266 lines, about 3,600 words |

**Not run:**
- Any test that imports `google.adk`: none exist, and the dependencies are not installed.
- ADK API or version confirmation, and the Gmail API or OAuth checks: no network or credentials allowed.
- A Markdown renderer or link check: no tool installed for it.
- Model calls.

## 5. Friction log

**Where I was unsure what to do:**
- **Ask first, or proceed on assumptions?** `adk-system-designer/SKILL.md:52` says "Let the user answer before treating a material product choice as settled", which conflicts with a headless run. `SKILL.md:117-119` resolves it: in a headless run, add an Assumed answers table and mark the decisions provisional. That was clear once I found it, but it comes about 65 lines after the scope-gate instruction (`SKILL.md:54`) that tells me to ask.
- **Auto-send versus the floor.** The user explicitly asked for automatic sending. The floor (`references/delivery-profiles.md:78-80`) allows it only if the user accepts the risk "after hearing it in one sentence". In a headless run nobody can accept it, so I defaulted to drafts. The skill doesn't say what to do with an *explicit request* that conflicts with the floor when acceptance is impossible. I treated it as not accepted and wrote a phase 2 goal (G05) to ask the user.
- **Where the plan lives.** `SKILL.md:241-242` says a multi-goal effort goes in `docs/plans/<topic>.md`, but "a small effort can keep its plan in the design". Four goals could count as either. I kept one file, so the run prompt points at the design path rather than the `docs/plans/...` path shown at `SKILL.md:274`.
- **Gmail OAuth setup time.** `references/delivery-profiles.md:104-105` gives setup costs for an API key (1 h) and a GCP project with IAM (half a day). Gmail installed-app OAuth on a Workspace mailbox fits neither, and Workspace admin approval is a separate unknown. I estimated it and flagged it as open question Q1.
- **No Gmail or OAuth-scope guidance.** Nothing in the files I opened covers Gmail scopes; in particular, that `gmail.compose` also permits sending, so the scope cannot enforce "drafts only". This rests on my own knowledge and is unverified. I did not open `adk-tool-auth-and-secrets` to check, because that seemed heavier than a design-only POC needs.

**Heavier than needed:**
- `SKILL.md:93` says every design reads `design-decisions.md`, a 343-line file, "for the sections its journey touches". Locating those sections still meant scanning the whole file. For this POC only about 60 lines mattered: lines 26-46 (proportionality), 168-196 (identity, trifecta) and 228-243 (effects).
- The system design template (`assets/system-design-template.md:111-133`, observability and release bullets) and the plan template's "What the reviewer reads" section (`assets/implementation-plan-template.md:84-95`) are sized for larger efforts. I dropped them for the POC; the skill only requires N/A markers at production depth (`SKILL.md:83-85`).
- The target is "a design and plan a reviewer reads in ten minutes" (`SKILL.md:82`). Even after trimming, my document is about 3,600 words, probably 12–15 minutes. Filling every per-goal field in the plan template (`assets/implementation-plan-template.md:48-69`) for four goals pushes it over the target.

**Genuinely helpful:**
- `references/delivery-profiles.md:24-27` and `:85-89` describe nearly exactly this case: a "POC" that emails real customers carries production risk, so offer drafts a human sends. The worked example at `:137-145` is almost this exact project, and it set the shape of the plan directly.
- The capacity formula and reserve at `references/delivery-profiles.md:101-107` gave a concrete cut line: 3.2 h of capacity, about 2.4 h after reserve, so G04 is the stretch.
- The lethal-trifecta guidance at `references/design-decisions.md:182-196` led to the key structural choice, D3: an agent with no tools and code that does all the writing.
- The dated model lifecycle file (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12-14`) caught that `gemini-3.6-flash` retires on Vertex on 2026-11-19 and the 2.5 models are `limited`. Without it I might have picked a model from memory.
- `references/failure-review.md:4-5` ("do not invent write machinery for a read-only product") kept the failure table to five rows.

## 6. Next prompt the skills told the user to type

The format comes from `SKILL.md:272-275` and `references/implementation-handoff.md:104-107`, applied to this plan's path:

```text
/adk-engineer Carry out G01 from docs/architecture/support-inbox-poc.md.
```

Then: `/adk-engineer Continue the next ready goal in docs/architecture/support-inbox-poc.md.`
