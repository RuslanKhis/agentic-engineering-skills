# REPORT — Gmail support auto-reply POC (design only)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`).
2. Listed `.claude/skills/` and `adk-system-designer/{references,assets}` (no project files exist besides `.claude/`).
3. `.claude/skills/adk-system-designer/references/design-decisions.md` (full)
4. `.claude/skills/adk-system-designer/references/failure-review.md` (full)
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (full)
6. `.claude/skills/adk-system-designer/assets/system-design-template.md` (full)
7. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (full)
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
9. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md` (grep only: pinned ADK 2.8.0)
10. `.claude/skills/adk-agent-security/SKILL.md` (grep only: version line and a search for POC/accepted-risk guidance; none found)

Not opened (triggers did not apply): `references/runtime-and-delivery.md`
(no browser, streaming or release continuity), `references/gcp-decisions.md`
(no GCP service is chosen beyond the Gmail API and Gemini API; no capacity or
cost estimate), `assets/ticket-template.md` (no tickets requested). No other
skill was invoked.

## 2. Questions I would have asked, and the answers assumed

These are also the *Assumed answers* table at the top of the design.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | Time and money? | ~4 h, one person; no money budget; spend capped at 25 emails/run, ≤ 2 model calls each. |
| Q2 | Who judges, reading what? | The user: live demo + a tally of right/wrong replies on ~30 real emails. |
| Q3 | Artifact type? | Exploration / POC, local, not hosted. |
| Q4 | Send to real customers immediately, or drafts until quality is measured? | **Draft-first**; `MODE=send` exists but is off and allow-list-limited until the user reviews the tally. This narrows the literal "automatically sends" request and is the most important assumption to confirm. |
| Q5 | What counts as "simple", and where do answers come from? | Questions answerable from a user-written `faq.md` (≤ ~2 pages, stable IDs); everything else is skipped. |
| Q6 | Mailbox type and access? | Workspace or Gmail account the user can sign in to; OAuth desktop flow, local `token.json`, scope `gmail.modify`; no domain-wide delegation. |
| Q7 | How are new emails picked up? | Local polling script; no Pub/Sub `watch`. |
| Q8 | Model backend? | Gemini API key, paid tier, `gemini-3.8-flash`. |
| Q9 | OK to send customer email content to the Gemini API? | Yes for the POC, on the paid tier; check the provider's current data-use terms before the live run. |
| Q10 | Languages, attachments, HTML? | English plain-text replies; attachments ignored; emails with no extractable text skipped. |

## 3. Files written or changed; what was not finished

Written:
- `docs/architecture/gmail-support-autoreply.md` (new, 270 lines): draft design
  with the assumed-answers table, scope gate and deferred controls, invariants
  I1–I6, decisions D1–D7, model-facing contracts, data/security posture,
  failure table, and the plan inline (goals G00–G03 with run prompts). The
  plan is kept in the design because the skill allows that for a small effort.
- `REPORT.md` (this file).

No other files changed. Not done, by design or because it could not be:
- No implementation, scaffolding, dependency changes or tickets (the request
  was design-only).
- Gmail API quotas, Gemini pricing and Gemini API data-use terms were **not
  looked up** (network not allowed). The design says so and does not quote numbers.
- ADK interface names (`LlmAgent(output_schema=…)`, `Runner`,
  `InMemorySessionService`, `RunConfig.max_llm_calls`) were not checked against
  any installed version; the design assumes `google-adk` 2.8.0 (from the
  specialist compatibility files) and makes the check a G01 acceptance item.
- All decisions are provisional; the design is marked **draft**.

## 4. Checks run and not run

Run:
- Confirmed `gemini-3.8-flash` is `stable`, released 2026-09-02, no shutdown, in
  `model-lifecycle-2026-10-01.json` (`checked_on` 2026-10-08) — matches D6.
- Confirmed `gemini-3.6-flash` has `vertex_retirement` 2026-11-19 (the
  reason D6 avoids it).
- `git status --short` → only `docs/` (and now `REPORT.md`) untracked; no other
  files touched.

Not run:
- Any test: there is no code, and tests importing `google.adk` cannot run here
  (dependencies not installed). The offline tests for I1–I6 are planned in G01.
- The skill-bundled tests (e.g. `adk-model-and-output-contracts/tests/*`) —
  not relevant to a design deliverable and some may need ADK.
- Any live Gmail/Gemini check, provider-documentation lookup or link check
  against external URLs (network forbidden).

## 5. Friction log

**Unsure what to do**
- *User waived security, but the design rules require a structural split for
  read-untrusted-and-send.* `SKILL.md:146-148` ("An agent that reads untrusted
  content and can write or send needs a structural split, not a warning
  sentence") and `references/design-decisions.md:180-194` (lethal-trifecta
  check) versus the user's "don't worry about security". Nothing in the
  skill says how to honour an explicit waiver; the template offers "accepted
  risk" as a resolution (`assets/system-design-template.md:71`) but gives no
  guidance on when a waiver is enough. I resolved it by choosing the cheapest
  structural version (agent has no tools; code fixes the recipient) because it
  costs nothing extra in a 4-hour build, and recorded everything else as
  deferred.
- *"Automatically sends" vs. proportionality.* The proportionality rule
  (`references/design-decisions.md:37-44`) only names spend-safety controls ("a
  call budget and a stop"); it is silent on irreversible, customer-visible
  effects in a POC. I added draft-first (Q4) as an assumption. A line in the
  rule about irreversible external effects would have removed the doubt.
- *Which primary skill for G01.* The handoff table (`references/implementation-handoff.md:21`)
  maps "bounded orchestration" to `adk-workflow-design`, but the substance of
  G01 is equally output-schema work (`:24`) and Gmail writes (`:29`). I picked
  `adk-workflow-design`; the choice felt arbitrary.
- *Supporting-skill rule vs. tool-less agent.* `references/implementation-handoff.md:44-47`
  attaches `adk-agent-security` to a goal that "reads untrusted content … and
  holds a write or egress tool". Here the *pipeline* writes but the *agent*
  holds no tools. I read it as not applying to G01 and attached it to G03.
- *Plan location and the prompt shape.* `SKILL.md:218` lets a small effort keep
  the plan in the design, but the closing example (`SKILL.md:246`) and the plan
  template run prompt (`assets/implementation-plan-template.md:50`) assume
  `docs/plans/<topic>.md`. I pointed the prompt at the design file.
- *G00 is user setup, not an engineer goal.* The template requires every goal
  to have a primary skill and run prompt (`SKILL.md:231-235`,
  `assets/implementation-plan-template.md:56`); a "create OAuth client in the
  console" goal has no natural specialist. I wrote "none needed".

**Heavier than needed**
- The design is 270 lines; `SKILL.md:64` asks for a design a reviewer reads in
  ten minutes for a four-hour job. The template sections (security posture,
  model-facing contracts, data table, failure table, verification/release
  bullets in `assets/system-design-template.md:53-123`) pull toward length even
  when most rows are "none" or "deferred".
- Reading `references/implementation-handoff.md:108-139` (other planning
  workflows) was unnecessary; the skill says to skip it, but it is in the same
  file as the required mapping.
- Per-goal fields (`assets/implementation-plan-template.md:36-52`: 11 fields)
  are a lot for 45-minute goals; I shortened G02/G03.

**Genuinely helpful**
- The headless rule (`SKILL.md:92-96`): an *Assumed answers* table with the
  decisions that depend on each row — exactly the right shape for this session.
- The scope gate and proportionality rule (`SKILL.md:52-66`,
  `references/design-decisions.md:26-44`) kept hosting, Secret Manager,
  telemetry and RAG out of the plan and gave a clean "deferred controls" table.
- The model lifecycle snapshot (`SKILL.md:168-172`,
  `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`)
  steered away from `gemini-3.6-flash` (Vertex retirement 2026-11-19) without
  a network lookup.
- The failure-review table (`references/failure-review.md:23-43`) prompted the
  "send succeeded, ledger write lost" case and, by extension, the auto-reply
  loop with customer autoresponders (I3) — the most likely real-world failure
  of this POC.
- "Structured output … design a refusal shape" (`references/design-decisions.md:304-311`)
  directly produced the `skip` result and I5.

## 6. Next prompt the skills told the user to type

The skill (`SKILL.md:242-247`) requires a closing copyable prompt. The one
given in the design's *Resume here* section is:

```text
/adk-engineer Carry out G01 from docs/architecture/gmail-support-autoreply.md.
```
