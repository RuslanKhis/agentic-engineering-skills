# Session report: HR policy Q&A proof of concept (design only)

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (the user's `/adk-system-designer` command). No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (whole file)
3. `.claude/skills/adk-system-designer/assets/ticket-template.md`
4. `.claude/skills/adk-system-designer/references/design-decisions.md` lines 1–170, 168–230, 261–300
5. `.claude/skills/adk-system-designer/references/failure-review.md` (whole file)
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md` lines 1–113
7. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
8. `.claude/skills/adk-memory-architecture/references/compatibility.md` (first 30 lines)
9. `.claude/skills/adk-memory-architecture/references/document-ingestion.md` lines 1–62
10. `.claude/skills/adk-memory-architecture/references/local-document-coverage.md` lines 1–42
11. `.claude/skills/adk-memory-architecture/references/retrieval-strategy.md` lines 1–30, plus `SKILL.md` lines 1–30
12. grep across `*/references/compatibility.md` for the ADK version, and across `adk-system-designer/references/gcp-decisions.md` for Gemini API data terms (no hits)
13. `.claude/skills/adk-system-designer/scripts/check_schedule.py` header only

Not opened: `runtime-and-delivery.md` and `gcp-decisions.md` in full (their triggers didn't apply: local `adk web`, no hosting in phase 1), and the design and plan templates (the compact form replaces them).

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer | Depends on it |
| --- | --- | --- | --- |
| Q1 | Is the POC continued after Friday or thrown away? | Continued if the demo lands | Phase 1 code is kept; phase 2 written |
| Q2 | How familiar are you with ADK and GCP? | New to ADK, comfortable with Python, no GCP project set up | 1.5× multiplier; Gemini API key rather than Vertex |
| Q3 | Are the 6 hours two dedicated blocks or interrupted time? | Two dedicated blocks (focus 0.8) | Capacity 4.8 h, 3.6 h after reserve |
| Q4 | Which model access and billing? May internal HR documents be sent to it? | Paid-tier, company-billed Gemini API key; sending published policies is allowed | D5; no calendar wait; open decision 1 |
| Q5 | What will HR leadership do in the demo? | Watch live and ask their own questions | Citations and an honest "not covered" answer (D3) over UI polish |
| Q6 | Do the PDFs hold any employee personal data, or are any scanned? | Published policies only, no personal data; some pages may be scanned | Sensitive data deferred; ingestion report (D4) |
| Q7 | Budget for model spend? | Small allowance; quota cap on the project | D6 |
| Q8 | Is a web UI needed, or is `adk web` acceptable for the demo? | `adk web` is acceptable | No frontend goal |
| Q9 | Confirm the cut line (G01–G03 now; G04–G06 later)? | Accepted as proposed | Phase split |
| Q10 | Can you write 10 gold questions with known answers from the PDFs? | Yes, the builder writes them in G03 | G03 hands-on hours |

## 3. Files written or changed; what was not finished

Written:
- `docs/architecture/hr-policy-qa.md`: compact design and plan in one file (profile, 6 decisions, depth table, phase 1–2 plan, Later list, open decisions). Marked **draft**.
- `docs/tickets/hr-policy-qa/G01.md`, `G02.md`, `G03.md`: phase 1 tickets, status `ready`.
- `REPORT.md` (this file).

Not finished, or deviating from the skill:
- Nothing was implemented, as requested.
- The design is about 1,355 words by `wc -w` (target about 1,200; table syntax adds to the count). Ticket bodies are 135–165 words (target about 120), mostly because of the fixed 40-word run prompt.
- Phase 1 **fits only at the low end** (3.0 h of 3.6 h after reserve; the high end is 5.25 h). The design names the fallback, but the user has not confirmed the cut line.
- No ADK interface, model availability or Gemini data-use terms were checked online; all three are marked provisional, with a verification step.
- The plan does not use the helper's `yaml` schedule block (the compact form says to leave it out).

## 4. Checks run and not run

Run:
- `wc -w` on the design: 1,355 words. A word count on each ticket body: 135 / 165 / 138.
- Hand check that each ticket's `hands_on + review_and_verify = total` and that the tickets sum to the plan's phase 1 total of 3.0–5.25 h: consistent.
- Goal-ID consistency after renumbering phase 2 (grep): G01–G06 each referenced, no gaps.
- `python3 --version`: 3.9.13.

Not run:
- `scripts/check_schedule.py`: not run. The compact form says not to use it, and it needs Python 3.11+, while 3.9.13 is installed. **The schedule was not checked by the helper.**
- The skill's own tests (`tests/test_check_schedule.py`): not relevant to this design and not run.
- Any test importing `google.adk`: none exist (nothing implemented), and google-adk is not installed.
- No network, cloud or install commands were run. Model IDs and ADK 2.8.0 come from the bundled lifecycle table (checked_on 2026-10-08) and the compatibility files, not a live lookup.

## 5. Friction log

**Unsure what to do**
- `adk-system-designer/SKILL.md:93` says to compute totals with `scripts/check_schedule.py` "rather than by hand". `references/delivery-profiles.md:160-161` and `:269` say a one-person POC adds them by hand with "no schedule block or helper run". I followed the more specific compact-form rule. The SKILL.md line should say "except the compact form".
- `SKILL.md:123` asks for an **Assumed answers** table at the top. `delivery-profiles.md:254-255` folds assumed answers into the scope-gate table "as one line each". I used the scope-gate table with an "A = assumed" marker, plus a full question table in REPORT.md. It's unclear whether both tables are wanted.
- Focus factor: `delivery-profiles.md:206-208` offers 0.6 (part-time or interrupted) or 0.8 (dedicated block). "6 hours spread over two days" fits either. The choice moves capacity between 2.7 and 3.6 h after reserve, enough to flip whether phase 1 fits at all. I assumed 0.8 and recorded it as Q3.
- `delivery-profiles.md:144` says to multiply by 1.5 for a team new to ADK. The scope-gate default (`SKILL.md:62`, "new to ADK") makes that the norm. Combined with the retrieval slice of 3–6 h (`delivery-profiles.md:137`), the standard retrieval goal alone (4.5–9 h) exceeds 6 hours of capacity. Nothing in the references suggests a cheaper retrieval shape for a small corpus. I had to invent the "catalogue in the instruction + read whole document" design (D2) myself.
- Sending internal documents to a model provider (free-tier vs paid-tier data use) is not covered in the floor (`delivery-profiles.md:76-86`) or in `gcp-decisions.md` (grep, no hits). It seems like a floor item for any POC on internal company documents.
- `SKILL.md:196` says to take the ADK version from "each specialist's `references/compatibility.md`". Most say 2.8.0, but `adk-agent-observability/references/compatibility.md:40` recommends 2.10.0+ for new deployments. I used 2.8.0 and left a confirm-the-pin acceptance item in G02.

**Heavier than needed**
- `SKILL.md:98` says "Every design reads design decisions" (343 lines) and `SKILL.md:232` says to read the failure review. For a read-only POC, most of it (external effects, approvals, OAuth, shared budgets) didn't apply. The compact form (`delivery-profiles.md:271-272`) rightly drops failure tables, but the reading cost stays.
- The ticket template (`assets/ticket-template.md:1-18`, `:53-57`) has 15 front-matter fields and a 3-line run prompt. That makes the "under about 120 words" limit (`delivery-profiles.md:267`) hard to meet without cutting acceptance content.
- The template's `## Scope` section (`assets/ticket-template.md:27-32`) clashes with the compact ticket form (`delivery-profiles.md:267-268`: "front matter, outcome, acceptance and run prompt"). I omitted Scope.

**Genuinely helpful**
- The capacity arithmetic and the "only the low end fits → name the fallback" rule (`delivery-profiles.md:214-223`) forced an honest cut line instead of an optimistic plan.
- The spend stop for `adk web`, where the app does not own `RunConfig` (`delivery-profiles.md:77-80`), applied directly (D6).
- The dated model lifecycle table (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`) let me pin `gemini-3.8-flash` with a source and avoid the 2.5-series Vertex retirement on 2026-10-20, which lands inside the plan's horizon.
- The ingestion qualification guidance (`adk-memory-architecture/references/document-ingestion.md:10-62`) surfaced the scanned-page risk, which leads to a false "not covered" answer in front of leadership (D4).
- The compact form's six sections (`delivery-profiles.md:246-272`) gave a clear, short document shape.

## 6. Next prompt the skills told the user to type

The skill's pattern (`SKILL.md:279`) is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`. Because tickets were requested, the ticket template's run prompt (`assets/ticket-template.md:53-57`) applies. As instantiated in the design and in G01:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
