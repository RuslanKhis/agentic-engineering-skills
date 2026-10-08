# REPORT — T-101 Wrong tool picked for order lookups

## 1. Skills invoked and reference files opened (in order)

1. Skill `adk-engineer` (entry; `.claude/skills/adk-engineer/SKILL.md`, loaded by the slash command)
2. Project files: `tickets/T-101.md`, `README.md`, `pyproject.toml`, `.github_workflows_ci.yml`, `support_agent/{__init__,agent,tools}.py`, `tests/test_tools.py`
3. `.claude/skills/adk-tool-interface-design/SKILL.md` (primary specialist)
4. `.claude/skills/adk-tool-interface-design/references/compatibility.md`
5. `.claude/skills/adk-tool-interface-design/references/naming-and-consolidation.md`
6. `.claude/skills/adk-tool-interface-design/references/validation.md`
7. `.claude/skills/adk-tool-interface-design/references/results-and-errors.md` (read in full, in two parts)
8. `.claude/skills/adk-tool-interface-design/references/evaluation-hooks.md`
9. Script `adk-tool-interface-design/scripts/lint_tool_schemas.py`: run before and after the change. I also grepped `GENERIC_NAMES` in it.
10. `.claude/skills/adk-agent-instructions/SKILL.md`: I read only the section headings and line 49 ("never mandate a call"), to support the one-line billing instruction fix.
11. Other tickets T-102..T-105 (skimmed headers only, to find the next ticket)

Not opened: `function-tool-contract.md`, `tool-count-and-toolsets.md`, `delegation-interfaces.md`, `sources.md`. Mode (b) sends you to tool-count, but there are only 5 tools on the root agent, so I skipped it.

## 2. Specialist chosen and why

**Specialist: `adk-tool-interface-design`**, because the ticket describes the model picking the wrong tool (`search_orders` instead of `get_order` when it has an ID) and putting a wrong value into an argument (a name in the ID slot). The adk-engineer routing table maps exactly that to this skill: "Wrong tool or wrong arguments chosen, tool docstrings and parameter schemas". I used mode (b), wrong tool or parameter diagnosis.
**Supporting: `adk-agent-instructions`**, used for one sentence only. The billing agent's instruction said "ALWAYS call search_orders first". That directly causes the reported behaviour and is instruction text, which belongs to that skill.

## 3. Files changed / not finished

Changed:
- `support_agent/tools.py`
  - `search_orders(value)` → `search_orders(query)`, `get_order(data)` → `get_order(order_id)`.
  - Full docstrings with "use ONLY when …", the other tool named in each, the ID format with examples, and the `Returns:` statuses with example dicts.
  - `get_order` validates the ID shape and returns an error dict with a hint pointing to `search_orders` before any HTTP call. This also stops a model-supplied value being put unchecked into the URL path.
  - 404, non-200 responses and transport errors now become error dicts with `hint` and `retryable`.
- `support_agent/agent.py`: billing_agent instruction now says when to use each tool instead of mandating `search_orders`.
- `support_agent/__init__.py`: `root_agent` is now loaded lazily (PEP 562 `__getattr__`), so `support_agent.tools` imports without google-adk. This follows adk-engineer SKILL.md:118-120. `support_agent.root_agent` still resolves when the package attribute is accessed.
- `tests/test_tools.py`: 12 new offline tests covering valid IDs, rejected names, e-mails and path strings with no HTTP call, 404 hint, retryable outage, search query passing, and docstrings that cross-reference each other.
- `tests/test_tool_declarations.py` (new): checks the declaration text and schema through `FunctionTool._get_declaration()`. It is skipped when google-adk is absent.
- `tickets/T-101.md`: added an Evidence section.

Not finished:
- No scripted-model Runner test. That needs a `BaseLlm` double written against the real SDK, and I could not check it here.
- No live declaration dump and no result-size report (no recorded events).
- No hand-off case set run by `adk-agent-evaluation`.
- Out of scope, but flagged by the linter: tools are still sync `def` (`sync_io_blocks_parallelism`), `search_orders` results are unbounded (no `max_results`), sub-agent descriptions are 1–2 words, `issue_refund` takes a model-supplied `user_id` and raises on failure, and the root instruction is unchanged.

### Assumptions / questions I would have asked
1. **What is the real order ID format?** I assumed a single token of letters, digits, `-` or `_`, 3–64 characters, containing at least one digit. If real IDs can be purely alphabetic, `get_order` will wrongly reject them.
2. **What does the orders API `q` parameter actually search?** I assumed customer name, e-mail or purchase description.
3. **Should `get_order` be renamed** (e.g. `get_order_by_id`) to sharpen the naming axis? I kept the existing names to avoid churn in prompts and any recorded eval data.
4. **Does the deployment load the agent via `support_agent.root_agent`** (works with the lazy `__getattr__`) or something that relies on `__init__` importing `.agent` eagerly? I could not verify the ADK 2.8.0 loader.
5. **Was editing the billing instruction within scope?** I judged yes, because it directly mandated the wrong tool.
6. Which model, budget and cases are approved for the live selection-accuracy run?

## 4. Checks

Run:
- `python3 -m pytest -q` (Python **3.9.13**, httpx 0.28.1, pytest 7.1.2): **13 passed, 1 skipped**. The skipped module is `tests/test_tool_declarations.py` (google.adk missing). Caveat: the project declares `requires-python >=3.11`, and the only interpreter with httpx and pytest is 3.9, so this is not the project's target interpreter.
- AST parse of the changed modules with `feature_version=(3,11)`: OK.
- `python3.11 -I .claude/skills/adk-tool-interface-design/scripts/lint_tool_schemas.py --project . --max-tools 20` before and after (support_agent findings only):
  - `generic_parameter_name`: 2 → 0
  - `short_docstring`: 5 → 3 (the three left are fetch_email, search_kb and send_email, which this ticket did not touch)
  - No new findings
  - The exit code was 1 both times, with `partial: true`, caused by a malformed file inside `.claude/skills/adk-memory-architecture`, not the project.
- Docstring (model-facing description) size: get_order 13 → 907 bytes, search_orders 14 → 939 bytes.

Not run:
- `tests/test_tool_declarations.py`: google-adk is not installed.
- Live declaration dump on google-adk 2.8.0.
- Scripted-model Runner test (not written).
- `report_tool_result_sizes.py` (no recorded events).
- Live evaluation of tool selection and parameter accuracy (needs a model, approval and budget; adk-agent-evaluation).
- Nothing in this report shows the real model now picks the right tool.

Hand-off cases for adk-agent-evaluation (suggested):
- "Where is order A10023?" → `get_order(order_id="A10023")`
- "Status of ORD-123456 please" → `get_order`
- "I'm Jane Smith, where's my order?" → `search_orders(query="Jane Smith")`, not `get_order`
- "Order for jane@x.com" → `search_orders`
- Injected `get_order` error "not an order ID" → next action is to ask the customer or call `search_orders`, not to retry `get_order`
- Same prompts routed via billing_agent

## 5. Friction log

- **Unsure: tickets have no `Primary skill` field.** `adk-engineer/SKILL.md:31-33` says to use the ticket's named skill or else the table. T-101 has two lines of prose, so I chose from the table. The row at `adk-engineer/SKILL.md:69` matched immediately. *Helpful.*
- **Assumed something I could not provide: Evidence section.** `adk-engineer/SKILL.md:39` says "write actual evidence and status into the ticket's Evidence section", but the ticket has none. I appended one myself.
- **Unsure what to type: next-ticket prompt.** `adk-engineer/SKILL.md:40` says "end with the run prompt for the next ready goal or ticket" but gives no template or wording. I had to make one up.
- **Linter scanned the skills directory.** The command in `adk-tool-interface-design/SKILL.md:38` (`--project .`) scanned `.claude/skills/**` too, because `.claude` is not in the excluded directories. The output was mostly skill test fixtures, and it returned `partial: true` with exit code 1 because of `.claude/skills/adk-memory-architecture/scripts/local_retrieval.py` ("malformed_file"). I had to post-filter the results to `support_agent/`. This was the heaviest step.
- **Undefined `$SKILL_DIR`.** `SKILL.md:38` and `validation.md:10` use `$SKILL_DIR`, which is not set in the shell. `adk-engineer/SKILL.md:99-101` defines what it means, but I still had to set it myself.
- **Interpreter friction.** `adk-engineer/SKILL.md:101-103` (3.11+ for helpers) was helpful: system `python3` is 3.9 and `python3.11` exists. But no interpreter has both 3.11+ and httpx/pytest, so the project tests ran on 3.9.
- **Assumed a test double the project lacks.** `adk-tool-interface-design/SKILL.md:126-129` and `references/validation.md:54-93` require a scripted-model Runner test. `validation.md:89` assumes a `scripted_model` `BaseLlm` double "the project already owns or one you add following adk-agent-evaluation". The project has none and the SDK is absent, so writing one blind would have been unverifiable. I skipped it.
- **Validation steps not possible here.** The live declaration dump (`validation.md:25-48`) and the result-size report (`SKILL.md:48-53`, `validation.md:95-107`) assume installed ADK and recorded events. I wrote the dump as a skip-guarded test instead.
- **Reading cost before useful work.** I opened ~5 references (~800 lines) before the first edit. The most useful parts were `naming-and-consolidation.md:27-47` (docstring template, almost directly reusable), `results-and-errors.md:75-95` (error dict with hint) and `compatibility.md:16` (on 2.8.0 no per-parameter description reaches the model, so parameter names and the docstring matter). `evaluation-hooks.md` was only needed for the hand-off list. *Genuinely helpful overall.*
- **Mode (b) is out of order for an offline setting.** `SKILL.md:67` says "Dump the live declarations and compare against the prompt that failed". There is no failed-prompt trace in the ticket and no SDK, so step one of the mode could not be done.
- **Helpful: `adk-engineer/SKILL.md:118-123`** (keep `google.adk` out of `__init__`, report SDK tests as not run). That directly unblocked running the tool tests offline.
- **Boundary friction.** `adk-tool-interface-design/SKILL.md:4` excludes agent instruction text. But the root cause sat partly in the billing instruction ("ALWAYS call search_orders first"), so I had to open a second skill for one sentence. `adk-agent-instructions/SKILL.md:49` ("never mandate a call") confirmed the fix.
- **Unclear what "Ask only for…" covers.** `adk-tool-interface-design/SKILL.md:58-60` lists the questions to ask, but the most important unknown (the order ID format) is not among them. I recorded it as an assumption.

## 6. Rating

**3 / 5.** Routing was instant and the references contained near copy-paste patterns. Friction came from the linter scanning the skill install itself, and from validation steps that assume the SDK, a scripted model double and recorded events.

Three changes that would most help:
1. Have `lint_tool_schemas.py` exclude `.claude/` (and other skill install dirs) by default, or add `--exclude`. Don't let one malformed skill file make the project scan `partial`/exit 1.
2. Ship a ready-to-copy scripted `BaseLlm` double (in adk-agent-evaluation assets, linked from `validation.md:89`), and give an explicit "SDK absent" validation path for mode (b): docstring checks plus skip-guarded declaration tests.
3. In adk-engineer, give a literal template for the "next ticket" run prompt and the Evidence section. Also let mode (b) in adk-tool-interface-design explicitly allow a one-sentence instruction fix when the instruction mandates the wrong tool.

## 7. Next prompt the skills told the user to type

None given. `adk-engineer/SKILL.md:40` says to "end with the run prompt for the next ready goal or ticket" but provides no wording. My suggestion, not from the skills: `/adk-engineer Please take ticket tickets/T-102.md and carry it out.`
