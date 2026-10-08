# T-104 report: security review before external launch (reconstructed)

> Reconstructed from the working tree after the trial was interrupted by a usage limit before it wrote its own report. The live friction log and transcript were lost. `support_agent/agent.py:3` and `support_agent/security.py:20` both point to `docs/security-review-T104.md`, which does not exist, so the review document for Legal was the next step and never happened.

Skill root for pointers: `/Users/ruslankhissamiyev/Documents/Coding Projects/skills/agentic-engineering-skills/skills/<name>/`.

## 1. Specialist selection (inferred)

**Primary:** `adk-agent-security`, composing modes (b) injection-resistant structure, (d) agency (tool tiering, confirmation, identity) and (e) adversarial suite (`SKILL.md:69-72`). Mode (f) "Security review", the literal ask, was not completed.

Evidence: the code contains a quarantined reader with `include_contents="none"` (`SKILL.md:69`), a `before_tool_callback` capability gate keyed on `tool_context.state` that returns `None` to allow (`SKILL.md:84-87`), `require_confirmation=True` on irreversible tools (`SKILL.md:88-90`), identity moved from a model argument to `ToolContext`, OWASP LLM/ASI IDs on each adversarial case, and `tests/adversarial-cases.json` "adapted from adk-agent-security/assets/adversarial-cases.json". There is also a pin test "at or above CVE floor" 2.7.0 (`SKILL.md:31-36`).

**Routing row:** `adk-engineer/SKILL.md:64`: "Prompt-injection resilience ... excessive agency ... or a pre-release security review | `adk-agent-security`". It matches word for word.

## 2. Changes

```
 support_agent/agent.py | 58 ++++++++++++++++++++++++++++++++++++++++----------
 support_agent/tools.py | 34 ++++++++++++++++++++++++-----
 2 files changed, 76 insertions(+), 16 deletions(-)
```
Untracked: `support_agent/security.py` (159 lines), `tests/adversarial-cases.json` (101), `tests/test_adversarial_runner.py` (219), `tests/test_security_gate.py` (160) and `tests/test_security_structure.py` (101). There are also `support_agent/__pycache__/` and `tests/__pycache__/` (cpython-313 bytecode, which should be deleted or git-ignored).

- `security.py` (no runtime ADK import): tool tiers. `capability_gate` (before_tool) refuses model-supplied `user_id/tenant_id`, enforces a session-written egress allowlist for `send_email`, blocks egress arguments containing tainted text, validates refund `order_id`, amount and cap (default 500 EUR), and fails closed on exceptions. `label_untrusted` (after_tool) adds provenance and records taint fragments in state. `session_user_id` reads identity from `ToolContext`.
- `agent.py`: `triage_agent` is a quarantined reader (`include_contents="none"`, no transfers, typed `Triage` with an enum, bounds and an ID pattern) exposed to root as `AgentTool`. Root loses `fetch_email` and `send_email`. `issue_refund` and `send_email` are wrapped in `FunctionTool(require_confirmation=True)`. All agents get both callbacks.
- `tools.py`: path-safe ID regex on `fetch_email`, `get_order` and `issue_refund`. `issue_refund` drops the `user_id` parameter and takes `tool_context`. `send_email` gets an address-shape check.
- Tests: 18 policy unit tests (file-path import), 8 AST structure tests, and 6 scripted-model Runner adversarial cases (s01 to s06, require ADK).

## 3. Completeness against the ticket

| Requirement | State |
| --- | --- |
| A security review Legal can read | **Missing.** No findings report, completed `assets/threat-model-checklist.md`, OWASP-mapped finding list, residual-risk statement or tool tier table for the owner (`SKILL.md:110`, `:127-129`). |
| Hardening of the top risks (injection via email, refund/send agency, identity) | **Largely done in code**, and well structured. |
| Adversarial suite | **Written, not run** (it needs `google.adk`). |
| Inventory before/after (`SKILL.md:119-120`) | **Missing.** |
| Decisions only the owner can make (refund cap, egress allowlist source, who confirms) | **Assumed** (default cap 500 EUR, `policy:*` state written "by the application"). Nothing writes `policy:egress_allowlist` yet, so `send_email` is now refused for everyone until the app does. |

Verdict: the engineering half is strong, but the deliverable the ticket names (the review) is absent.

Validation run during reconstruction (system Python 3.9.13, no ADK):
```
python3 -m pytest -q -p no:cacheprovider tests/test_security_gate.py tests/test_security_structure.py tests/test_adversarial_runner.py
25 passed, 1 skipped   (skip: test_adversarial_runner.py, importorskip google.adk)
tests/test_tools.py: collection error (support_agent/__init__.py imports google.adk; baseline problem)
```
The count of 25 reflects pytest's collection and does not account separately for each case of the 18 + 8 + 6 tests listed above.

## 4. Quality notes against `adk-agent-security/SKILL.md`

1. **Policy in code the model cannot reach; identity from `ToolContext` (`SKILL.md:84-87`): followed.** The gate returns `None` to allow and an error dict to refuse, and fails closed. `issue_refund` no longer accepts `user_id`.
2. **Gate irreversible actions with `require_confirmation` (`SKILL.md:88-90`): followed** for `issue_refund` and `send_email`. Unverified: whether on 2.8.0 the `before_tool_callback` runs before the confirmation request. Test s01 assumes the gate answers first.
3. **Remove one trifecta leg per agent; the writer receives structured, validated state, never free text from the reader (`SKILL.md:81-83`): partly.** Root no longer reads raw email, but `Triage.summary` (free text up to 400 characters) still flows to root. Taint matching on egress mitigates this. `refunds_agent` still holds private data (`get_order`), untrusted order text and egress (`send_email`), so it relies on the allowlist and taint gate rather than structure. The quarantined reader keeps `fetch_email` + `search_kb`. `SKILL.md:69` describes the reader as having "no tools", a pattern that assumes content is handed in rather than fetched.
4. **"Do not treat an instruction such as 'ignore text inside documents' as a control" (`SKILL.md:104-105`): respected.** The added triage sentence is a hint, and the controls are structural.
5. Not touched: `refunds_agent`'s instruction still says "You MUST call issue_refund", `issue_refund` still raises on non-200, and `triage_agent` still combines `tools` + `output_schema` on the API-key backend (the T-105 defect).

## 5. Friction the artefacts reveal

- **F1. The security inventory is blind to this repo.** `inspect_security_surface.py` (run read-only during reconstruction with python3.11) reports **no findings at all on the baseline**: no write tool without a gate, no `user_id` identity parameter, no egress or untrusted sources, `all_three: false` for every agent. All tools are referenced as `tools.<fn>` (module attribute), and `describe_tool` falls through to `kind: "other", name: None` (`adk-agent-security/scripts/inspect_security_surface.py:711`) with `partial: false`. `SKILL.md:37-54` makes this script step 3 of inspection and the source of "the inventory before and after" (`:119-120`). The trial evidently compensated by writing its own AST structure tests (`tests/test_security_structure.py`).
- **F2. Review versus change.** Mode (f) says "Change nothing unless asked" (`SKILL.md:73`). The ticket asks for a review, and `/adk-engineer ... carry it out` reads as authorisation to fix. The trial resolved the tension by implementing first, and ran out of budget before the review. The skill gives no ordering rule such as "write the findings first, then fix the top N".
- **F3. Deliverable sprawl.** Validation (`SKILL.md:119-129`) asks for the inventory before and after, a completed checklist, a Runner test per structural change, an offline adversarial suite, OWASP IDs and owners, and residual risk. With six artefact types, the human-readable one was the casualty.
- **F4. SDK-free testing workaround.** `tests/test_security_gate.py:10-15` loads `security.py` by file path "because support_agent/__init__.py imports the agent (and therefore google.adk)". `security.py` uses `TYPE_CHECKING`-only ADK imports for the same reason. The Runner-level suite, the evidence the skill most wants (`SKILL.md:121-123`), cannot run offline.
- **F5. Owner decisions surface as hidden defaults.** `SKILL.md:60-62` lists questions (irreversible actions, human controller, perimeter) but not the refund cap or the egress allowlist source. The trial hard-coded `DEFAULT_REFUND_CAP_EUR = 500.0` and a state key nobody writes, which silently disables `send_email`.
- **F6. Bytecode left in the tree.** `__pycache__` (cpython-313) shows tests were run with a 3.13 interpreter while the system default is 3.9. The skill's "available Python 3.11+ interpreter" note (`SKILL.md:37-38`) leaves interpreter choice to trial and error, and the project has no `.gitignore`.

## 6. Note on lost evidence

The original agent's friction log, the references it read (`injection-patterns.md`, `agency-and-output.md`, `adversarial-testing.md` are implied by the code) and any inspector output were lost with the interruption. Whether it ran the inspector and saw the empty result is unknown.
