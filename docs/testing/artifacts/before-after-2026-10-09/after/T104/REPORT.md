# REPORT: T-104 security review before external-customer launch

## 1. Skills invoked and reference files opened (in order)

1. Skill `adk-engineer` (invoked by the user): `.claude/skills/adk-engineer/SKILL.md`, loaded by the command.
2. Project files: `tickets/T-104.md`, `README.md`, `pyproject.toml`, `.github_workflows_ci.yml`, `support_agent/{__init__,agent,tools}.py`, `tests/test_tools.py`, `tickets/T-101,102,103,105.md` (to keep T-104 out of their scope).
3. Specialist `adk-agent-security`, read from the filesystem (sibling directory, not through the Skill tool):
   1. `.claude/skills/adk-agent-security/SKILL.md`
   2. `references/compatibility.md`
   3. `references/threat-model.md`
   4. `assets/threat-model-checklist.md`
   5. `references/injection-patterns.md`
   6. `references/agency-and-output.md`
   7. `references/tool-supply-chain.md`
   8. `references/adversarial-testing.md`
   9. `references/validation.md`
   10. `assets/adversarial-cases.json`
4. Script `adk-agent-security/scripts/inspect_security_surface.py` (`--help`, three runs).

Not opened: `references/sources.md`; `adk-agent-evaluation`'s deterministic-tests reference, which `adversarial-testing.md:54` points to.

## 2. Specialist chosen and why

**Specialist: `adk-agent-security`**, because T-104 is a pre-release security review. The agent reads untrusted customer email and can act: it refunds money and sends mail. That matches the routing row at `adk-engineer/SKILL.md:68` ("Prompt-injection resilience … excessive agency … pre-release security review"). The ticket names no `Primary skill`. Mode (f) "Security review" applies, plus modes (a), (b), (d) and (e) for the fixes. Supporting skills are named as owners in the review but were not loaded: `adk-tool-auth-and-secrets`, `adk-operational-guardrails`, `safe-api-tool-calls`, `protect-adk-sensitive-data`, `deploy-adk-on-google-cloud`, `adk-frontend-integration` and `adk-agent-instructions`.

## 3. Files changed, and what is not finished

| File | Change |
| --- | --- |
| `docs/security/T-104-security-review.md` (new) | The deliverable: inventory, tool tiers, 15 prioritised findings with file:line, OWASP ID, enforcement point, observable check, evidence label and owner; per-agent worksheets; owner questions Q1–Q8 |
| `docs/security/inventory-before.json`, `inventory-after.json` (new) | Inspector output scoped to `support_agent/` and `pyproject.toml` |
| `support_agent/security.py` (new, stdlib only) | `before_tool_gate`: fail-closed; refuses identity arguments (`user_id`, `to`, …), malformed IDs, refunds outside `0 < amount <= REFUND_LIMIT_EUR` (env, default 100) and mail without an application-written address; logs each denial. `label_untrusted`: after-tool provenance label on `fetch_email` and `search_kb` results |
| `support_agent/tools.py` | `issue_refund`: `user_id` parameter removed (identity from `tool_context.user_id`); ownership and order-total check; bounded error dict instead of raising with backend text. `send_email`: `to` removed, recipient from `state["user:email"]`. `search_orders` and `get_order`: filtered to the session user, failing closed. `fetch_email` and `get_order`: ID pattern checked before URL interpolation |
| `support_agent/agent.py` | `fetch_email` removed from `support_root` (only triage reads raw mail). `triage_agent`: `disallow_transfer_to_parent/peers=True`. `issue_refund` wrapped as `FunctionTool(..., require_confirmation=True)`. Every agent gets `before_tool_callback` and `after_tool_callback` |
| `support_agent/__init__.py` | `root_agent` resolved lazily through module `__getattr__`, so `support_agent.security` imports without google-adk |
| `tests/test_security_policy.py` (new) | 7 SDK-free policy tests |
| `tests/test_security_runner.py` (new) | 4 scripted-model Runner tests (attacker recipient refused, mail only to the session customer, refund over the limit refused, refund within the limit waits for confirmation). `importorskip("google.adk")` |
| `tickets/T-104.md` | Evidence section added |

**Not finished / not done:**
- Refund idempotency (duplicate refund on retry or replay): F9, owned by `safe-api-tool-calls`.
- Durable staff review for refunds above the limit: they are only refused now (`adk-operational-guardrails`).
- The front end must render ADK's `adk_request_confirmation`, or refunds will stall. The UI is not in the repo.
- Vertex AI versus the API-key backend for customer PII (F10): a Legal decision.
- Cloud Run authentication (F11) and renderer sanitisation (F12): not verifiable from the repo.
- The `refunds_agent` instruction still says "MUST call issue_refund", and the `{plan}` KeyError remains (F13, `adk-agent-instructions`).
- Alerting on denied calls (F14): only WARNING logs exist.
- google-adk 2.11.0 upgrade decision (F15).
- The skill asks to "show the owner the tool tier table before merging" (`adk-agent-security/SKILL.md:109-110`). The owner was unavailable, so the table is in the review and this is still pending. Nothing was committed.

**Assumptions made (questions I would have asked):**
- Q1: The session user after launch is the authenticated external customer, and ADK `user_id` equals the orders system's `customer_id`.
- Q2: The refund auto-limit is 100 EUR.
- Q3: The orders API returns `customer_id` and `amount_eur` per order, and `/orders?q=` returns a list.
- Q4: Message and order IDs match `^[A-Za-z0-9_-]{1,64}$`.
- Q5: The application writes the verified customer address to `state["user:email"]` at session creation.
- Q6: Mailing customers their own order data is acceptable residual risk.
- Q7: "Carry out the ticket" includes making the fixes the review recommends, not just writing the review.
- Q8: Keeping the param name `get_order(data)` is right, because renaming it belongs to T-101 (tool interface).

## 4. Checks run and not run

Run:
- `python3.11 -I .claude/skills/adk-agent-security/scripts/inspect_security_surface.py --project .`, before and after. It exits 1 with `partial: true` because `.claude/skills/adk-memory-architecture/scripts/local_retrieval.py` is reported `malformed_file`, which is unrelated to the project. Project-scoped counts:
  - `write_tool_without_gate` 3 → **0**
  - `identity_parameter_review` 1 → **0**
  - `untrusted_content_source` 9 → 8
  - `egress_capable_tool` 12 → 11
  - `trifecta_present` 4 → 4. The heuristic counts every `httpx` call and the name `send_email` as egress. It cannot see recipient binding. Explained by hand in the review.
- `python3.11 -I -m py_compile support_agent/*.py tests/*.py`: OK.
- `tests/test_security_policy.py`: the 7 test functions were called directly with python3.11, because pytest is not installed. **7 passed.**

Not run:
- `tests/test_security_runner.py`: needs google-adk 2.8.0 and pytest. The `ScriptedModel`/`InMemoryRunner` API usage and the 2.8.0 behaviours it relies on are unverified: `FunctionTool(require_confirmation=)`, injection of `tool_context` by name with a string annotation, and the `adk_request_confirmation` event name.
- `tests/test_tools.py`: needs httpx and pytest.
- No HTTP-level tool tests: httpx is absent.
- Live adversarial campaign: needs approval and network.
- Deployed IAM and Cloud Run authentication checks.

## 5. Friction log

1. **Helpful.** `adk-engineer/SKILL.md:68`: the routing row names "pre-release security review" directly, so choosing the specialist took seconds, even though the ticket has no `Primary skill` field (`:34`).
2. **Unsure.** `adk-agent-security/SKILL.md:73-74` makes fixes conditional on "when the request also says to carry the work out". It was unclear whether "take the ticket and carry it out" counts, when the ticket itself only asks for a review. I chose to fix, and recorded that as Q7.
3. **Heavy before useful work.** `adk-agent-security/SKILL.md:73` says mode (f) should "Use all references". That meant 8 reference/asset files, about 1,000 lines (`sources.md` skipped), before any finding could be written. A short "review quick path" covering the top checks for the common shape (reads mail, can pay, can send) would have been enough to start.
4. **Assumed something I could not provide.** `adk-agent-security/SKILL.md:41` and `references/validation.md:10-12` run `python "$SKILL_DIR/..."`. On this machine `python3` is 3.9; I had to find `python3.11` myself. `adk-engineer/SKILL.md:102` does warn about this, which was **helpful**. `validation.md:10-12` also redirects to `/tmp/security-*.json`. In this sandbox the `/tmp` file was gone by the next call, and the session rule limited writes to the current directory. I stored the inventories under `docs/security/` instead.
5. **Tool noise.** `adk-agent-security/scripts/inspect_security_surface.py:31` (`EXCLUDED`) does not exclude `.claude/`, so the inspector scanned the 20 installed skills' own test fixtures. That gave 35 KB of output, mostly irrelevant agents, and `partial: true` with exit 1 from an unrelated skill file. There is no `--exclude` or `--path` option (`--help`). I had to post-filter the JSON by hand.
6. **Tool gap.** The inspector reads callbacks through `node.keywords` by name (`inspect_security_surface.py:164`). It does not resolve `**GATES` dict-splat, so my first wiring showed `callbacks: []`. I rewrote the agents with explicit kwargs to make the inventory truthful. That is arguably clearer anyway, but it is a tool limitation dictating code style.
7. **Over-flagging.** The trifecta heuristic (`SKILL.md:50-53`) flags `get_order`, `search_orders` and `billing_agent` as egress and untrusted because they call `httpx.get` on fixed internal hosts. Every agent stays `trifecta_present` after the fix, so the "after" inventory cannot show the main risk reduction. Findings are also emitted twice per tool (once per referencing agent), which inflates the counts.
8. **Unsure / unverifiable.** `references/adversarial-testing.md:54-58` delegates the scripted `BaseLlm` harness to `adk-agent-evaluation`'s deterministic-tests reference. I wrote `ScriptedModel` from memory to avoid loading another skill, so the Runner tests are plausible but unverified. An inline minimal harness in this skill would help.
9. **Assumed something I could not provide.** `adk-agent-security/SKILL.md:60-62` and `:109-110`: "Ask only for decisions …" and "show the owner the tool tier table before merging". With no owner available, these became Q1–Q8 in the review.
10. **Helpful.** `references/injection-patterns.md:80-120` (the capability-gate code and the "fail closed / return None to allow" rules) and `references/agency-and-output.md:60-67` ("Identity never comes from the model") translated directly into `security.py` and the `issue_refund` change.
11. **Helpful.** `references/compatibility.md:12-42` gave pin-specific facts (2.8.0 fences sub-agent output but not own tool results; no integrity plugin). Without it I could not have scoped F7 and F15 correctly.
12. **Helpful.** `adk-engineer/SKILL.md:117-123` ("keep `google.adk` imports out of package `__init__.py`", "never imitate the SDK … and call the result a pass") explained why the existing `tests/test_tools.py` could never run SDK-free. It led to the lazy `__init__` and the clean split between run and not-run tests.
13. **Minor.** `assets/adversarial-cases.json` uses tool names that don't exist here (`read_ticket`, `approve_refund`, `delete_order`). It was useful as a shape, but every case needed mapping by hand.
14. **Unsure what to type next.** `adk-engineer/SKILL.md:40` says to "end with the run prompt for the next ready goal or ticket", but gives no template, and the tickets carry no prerequisites or status. I could not tell which ticket is "next ready", and no prompt text was provided to quote.

## 6. Rating

**3 / 5.** Routing was instant and the security content was accurate and directly usable. Cost came from reading all the references, inspector noise from `.claude/`, and unverifiable SDK test scaffolding.

Three changes that would help most:
1. Inspector: exclude `.claude/` (and any skill install directory) by default, add a `--path`/`--exclude` flag, resolve `**kwargs` callbacks, and deduplicate per-tool findings. Treat calls to fixed hosts with no model-controlled URL or recipient as "internal read", not egress, so the before/after diff shows real risk reduction.
2. Mode (f): add a one-page "review quick path" (inventory, tier table, trifecta, top 6 checks), with the full references loaded only per finding. State plainly whether "carry out the ticket" means fix or review only.
3. Ship a minimal tested scripted-model Runner harness (a `conftest.py` asset) inside `adk-agent-security`, and give `adk-engineer` a literal next-prompt template (for example `Please take ticket tickets/<ID>.md and carry it out.`) plus a rule for "next ready" when tickets have no prerequisites.

## 7. Next prompt the skills told the user to type

none given. `adk-engineer/SKILL.md:40` asks the agent to end with "the run prompt for the next ready goal or ticket" but supplies no prompt text.
