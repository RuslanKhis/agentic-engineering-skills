# REPORT: ADK shopping assistant design session (2026-10-09)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer` (by the user's `/adk-system-designer`). No other skill was invoked.

Files opened, in order (paths under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the invocation)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/gcp-decisions.md`
6. `adk-system-designer/references/implementation-handoff.md`
7. `adk-system-designer/assets/system-design-template.md`
8. `adk-system-designer/assets/implementation-plan-template.md`
9. `adk-system-designer/references/runtime-and-delivery.md` (trigger: browser delivery and concurrent sessions)
10. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (model choice, as SKILL.md requires)
11. `adk-model-and-output-contracts/references/compatibility.md` (first 40 lines; ADK version assumption)
12. `safe-api-tool-calls/references/compatibility.md` (first 30 lines) and a heading/keyword grep of `safe-api-tool-calls/references/writes-and-confirmation.md` and `adk-model-and-output-contracts/references/model-selection.md`
13. `adk-system-designer/assets/ticket-template.md` (first 5 lines only; no tickets written)
14. A grep across all `*/references/compatibility.md` for the google-adk version. All of them name 2.8.0.

## 2. Questions I would have asked, and the answers I assumed

These match the **Assumed answers** table at the top of `docs/architecture/shopping-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Exact launch date, and is it continued afterwards? | Live by 2026-10-23, then continued (from the request) |
| A2 | How many hours per person, and how familiar with ADK and GCP? | ~25 h/week each; Python/web-capable; new to ADK; light GCP |
| A3 | Model and cloud budget? | ≤ US$300/month; app-enforced daily stop around US$10/day |
| A4 | Does "place orders" mean creating the order in chat, or handing the customer to Shopify checkout? | Build the cart via the Storefront API, then hand off to Shopify-hosted checkout; the customer pays there. No Admin API order writes |
| A5 | Who uses it, logged in or not, which languages, how much traffic? | Anonymous guests on an existing theme, English, < 500 conversations/day |
| A6 | Catalogue size and content? Are reviews included? | ≤ 5,000 variants, merchant-authored text, no reviews |
| A7 | Should it read customer data (orders, accounts)? | No, not in the MVP |
| A8 | Shopify plan, dev store, ability to create a Storefront API token? | A dev store exists or can be created; a custom/headless app token is available; plan unknown |
| A9 | GCP project and region; Gemini API or Vertex? | Team-owned project, `europe-west1` placeholder, Vertex AI |
| A10 | Markets and legal (EU/UK disclosure, privacy notice)? | EU/UK customers possible; the founders own the disclosure and privacy text |
| O4 | Do you accept off-brand or wrong-answer risk at launch, mitigated by eval cases and a kill switch, or do you want output screening in phase 1? | Left open as a founder decision. The design assumes eval cases plus the kill switch |
| O5 | Widget delivery: theme app extension, snippet or App Proxy? | Left to a 1 h spike inside G05 |

## 3. Files written or changed; what was not finished

Written (nothing else was changed):

- `docs/architecture/shopping-assistant.md`: the design, status **draft**. It covers assumed answers, the journey, the delivery profile (MVP), depth per concern, the floor, invariants I1–I6, a component diagram, decisions D1–D10, model-facing contracts, data and authority, a security posture (trifecta), budgets, failure/recovery, verification, and open decisions O1–O6.
- `docs/plans/shopping-assistant.md`: the phased plan. It covers capacity (≈90 focused h, ≈68 h after reserve), the cut line and a day-6 cut rule, the implementation map, discovery goal D01, and phase 1 goals G01–G07 (57–79 h) with full fields and run prompts. It also lists coarse phase 2 goals G08–G14 with triggers, a Later list, and Resume here.
- `REPORT.md` (this file).

Not finished, or not possible here:

- **No provider facts were verified** (no network). Shopify Storefront API semantics (absolute-quantity cart update, `checkoutUrl`, cart expiry, rate limits, token scopes) are provisional and assigned to discovery goal D01. Vertex/Gemini and Cloud SQL **prices were not looked up**, so the cost estimate is symbolic and pricing is assigned to G06/O6. The region and Vertex availability of `gemini-3.8-flash` were not checked.
- `gemini-3.8-flash` has no `vertex_retirement` entry in the lifecycle JSON. The "not before 2027-09-02" date is derived from the ≥ 12-month Vertex commitment quoted in `model-selection.md:22`; it is not a listed date.
- **No user confirmation** of any decision. The cut line, A4/O1 (checkout handoff) and the budget numbers all need founder sign-off.
- No tickets were written: the user did not ask for them (SKILL.md:264–266).
- Estimates are assumptions for an assumed team; no actual effort data exists.

## 4. Checks run and not run

Run:

- Relative links between the design and the plan resolve to existing files (shell `test -f`): all OK. The anchors `#open-decisions` and `#delivery-profile-and-capacity` match headings.
- Arithmetic: phase 1 sums to 57–79 h; capacity 3 × 25 × 2 × 0.6 = 90 h, and 75 % of that is 67.5 h ≈ 68 h. This matches the documents.
- `git status`: only `docs/` is new (REPORT.md was added afterwards).

Not run:

- No application code or tests exist (design only). No test importing `google.adk` was run, because the dependencies are not installed.
- No network checks: Shopify docs, Gemini/Vertex docs and pricing, ADK 2.8.0 API names. Pin confirmation is an acceptance item of G01.
- No cloud or Shopify calls, and no evaluation runs.

## 5. Friction log

**Unsure what to do**

- **Scope gate in a headless run.** SKILL.md:54–66 says to open with the scope-gate questions and wait for answers. SKILL.md:116–120 (the **Assumed answers** table, "keep asking nothing further") settled it. This was clear once found, but it sits about 60 lines after the instruction to ask, so I read on before acting.
- **The "orders" requirement.** `delivery-profiles.md:154–157` (three people, two weeks, orders) prescribes "idempotent order creation and explicit confirmation are in phase 1". I chose a Shopify-checkout handoff instead, so the customer approves and Shopify creates the order. I was unsure whether this honours the example or sidesteps it. I recorded it as provisional (D3, O1), with in-chat order creation in Later.
- **No specialist owns third-party commerce APIs.** None covers Shopify contracts. `gcp-decisions.md:37–41` requires current official sources before relying on a provider fact. With no network, every Shopify claim had to become discovery goal D01.
- **Model lifecycle gap.** The JSON lists no `vertex_retirement` for `gemini-3.8-flash`, while the designer asks for "a model that retires within the plan's horizon" to be designed in (SKILL.md:193–197). I had to fall back to the prose in `adk-model-and-output-contracts/references/model-selection.md:22`.
- **Two closing-prompt formats.** SKILL.md:271–275 gives a one-line `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`, but `implementation-plan-template.md:113–119` gives a five-line form. I used the long form in the plan and both in chat.
- **Depth for observability and release at MVP.** `delivery-profiles.md:62–63` says MVP is "Build: traces" and "Build: evaluation in CI", but the worked example at `delivery-profiles.md:156–157` defers both to phase 2. I followed the example and recorded the deviation in the depth table.

**Heavier than needed**

- The plan template's per-goal block (`implementation-plan-template.md:48–69`, 13 fields) repeated for 8 phase-1 goals makes the plan long for a three-person MVP. The fields are useful for handoff, but several (Execution scope, Status) are near-boilerplate at design time.
- The design template (`system-design-template.md:12–43`) has two separate tables (depth per concern, then deferred controls) that overlap heavily for an MVP. I merged them into one depth table plus graduation conditions.
- Reading all six references is required or triggered for any cross-cutting design (SKILL.md:96–99 plus the triggers). That is about 1,200 lines before writing, which is acceptable but not light.

**Genuinely helpful**

- `delivery-profiles.md:95–113`: the capacity formula, focus factor, reserve and "cut scope, not the floor" gave a defensible cut line quickly.
- `delivery-profiles.md:154–157`: a worked example that matches this request almost exactly.
- `design-decisions.md:182–196`: the lethal-trifecta check made the "one agent, no private data in MVP" argument crisp and set the trigger for re-checking it (login and order lookup).
- `design-decisions.md:274–279`: "a billing notification is an observation mechanism". This drove the app-level daily stop (D7), not just budget alerts.
- `runtime-and-delivery.md:37–40`: "streaming earns its extra state … when progressive delivery matters". This justified completed JSON for phase 1, with streaming behind a measured trigger.
- `implementation-handoff.md:39–51`: the rule for choosing supporting skills made the Primary/Supporting lines fast to fill.
- The `model-lifecycle-2026-10-01.json` table flagged `gemini-3.6-flash` (Vertex retirement 2026-11-19) and the 2.5 models (2026-10-20) as traps.

## 6. Next prompt the skills told the user to type

The skill's template (SKILL.md:271–275), verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated for this plan, from the plan's **Resume here** section, following `implementation-plan-template.md:113–119`:

```text
/adk-engineer Carry out G01 (local agent recommends real products) from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-workflow-design with adk-tool-interface-design, adk-agent-instructions and adk-model-and-output-contracts.
Work locally against the Shopify dev store only, verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```
