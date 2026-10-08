# REPORT — T-104 Security review before launch to external customers

Paths under `.claude/skills/` are abbreviated `S=` for `.claude/skills/adk-agent-security/`
and `E=` for `.claude/skills/adk-engineer/`.

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-engineer` (invoked by the user as `/adk-engineer`): `E/SKILL.md` (loaded with the command).
2. Specialist `adk-agent-security`: `S/SKILL.md` (read from the sibling directory, as `E/SKILL.md:76-79` instructs).
3. `S/references/compatibility.md`
4. `S/references/validation.md`
5. `S/assets/threat-model-checklist.md`
6. `S/scripts/inspect_security_surface.py`: ran it, `--help`, and read lines 640-710 to diagnose a false negative.
7. `S/references/threat-model.md`
8. `S/references/agency-and-output.md`
9. `S/references/injection-patterns.md`
10. `S/references/adversarial-testing.md`
11. `S/references/tool-supply-chain.md`: lines 1-60 only.
12. `S/assets/adversarial-cases.json`: case list only.

Not opened: `S/references/sources.md`; `E/references/composition.md` (not needed: the repo has no `agents-cli-manifest.yaml`).

## 2. Specialist chosen and why

**`adk-agent-security`, mode (f) "Security review".**
- The ticket is a pre-release security review of an agent that reads untrusted content (customer emails) and can act (refunds, outbound mail). That is word for word the `adk-engineer` routing row at `E/SKILL.md:64` ("…excessive agency… or a pre-release security review"). The specialist's own description also matches: "Use when an agent reads untrusted content and can act … or for a security review".
- I chose mode (f) because Legal asked for a review, and `S/SKILL.md:73` says "Change nothing unless asked".
- Other specialists are named as owners of individual findings but were not loaded: `adk-tool-auth-and-secrets`, `adk-operational-guardrails`, `safe-api-tool-calls`, `adk-agent-instructions`, `deploy-adk-on-google-cloud`, `adk-agent-observability`, `adk-release-engineering`, `protect-adk-sensitive-data`.

## 3. Files changed / not finished

Changed:
- **Added** `docs/security/T-104-security-review.md`. It contains:
  - the agent and tool inventory with tool tiers;
  - 9 prioritised findings (S1–S9) with `file:line`, OWASP LLM/ASI IDs, enforcement point, observable check, evidence label and owning skill;
  - per-agent trifecta worksheets;
  - a remediation plan;
  - residual risks;
  - open questions with the answers I assumed.
- **Added** `REPORT.md` (this file).
- No source, test or config files were modified.

Not finished (out of scope for a review, or blocked):
- None of the fixes are implemented (S1–S3 are launch blockers).
- No scripted-model Runner tests or adversarial suite were written. They cannot run without google-adk, and mode (f) is review-only.
- There is no "after" inventory because nothing changed.
- No deployment or perimeter checks: there is no deploy config in the repo, and I have no cloud access.
- The UI renderer was not reviewed because there is none in the repo.

Side effect to note: I first wrote the inspector output to `/tmp/t104-security-before.json`, as `S/references/validation.md:10` suggests. That is outside the allowed directory, so I deleted it straight away. A scratch copy, `.review-scratch/`, was created inside the cwd and deleted again. `__pycache__` folders from compile checks were removed.

## 4. Checks run and not run

| Check | Command | Result |
| --- | --- | --- |
| Security inventory, system Python | `python3 S/scripts/inspect_security_surface.py --project .` | **Failed**: `ModuleNotFoundError: No module named 'tomllib'` (python3 is 3.9.13) |
| Security inventory, Python 3.12 | `/opt/homebrew/bin/python3.12 -I S/scripts/inspect_security_surface.py --project .` | rc=0, `partial: false`, `adk_pins: at_or_above_cve_floor`. **But** no trifecta and no write-tool findings for `support_agent/` (false negative, see friction F4). It also reported 7 `unauthenticated_exposure_hint` rows and 4 other rows about `.claude/skills/` itself (noise) |
| Inventory on a scratch copy with `tools.x` rewritten to bare names | same script on `.review-scratch/` | `trifecta_present: 3` (support_root, refunds_agent, billing_agent), `write_tool_without_gate: 5`, `identity_parameter_review: 1` (issue_refund), `egress_capable_tool: 12`, `untrusted_content_source: 9`. Each row was then checked by hand against `tools.py`; billing_agent and the fetch_email "write" flag are heuristic over-flags (explained in the review) |
| Syntax compile | `python3.12 -I -m py_compile support_agent/*.py tests/*.py` | ok |
| Project unit tests | `python3 -m pytest -q -p no:cacheprovider tests` | **Collection error.** `tests/test_tools.py` imports `support_agent`, whose `__init__` imports `google.adk`, which is not installed. Reported as **not run** |

Not run:
- Scripted-model Runner tests for gates: none exist, and google-adk is not installed.
- Offline adversarial suite: not written.
- Live red team: needs approval plus a model and project.
- Declaration-hash test: not applicable (no MCP/OpenAPI).
- Deployment auth and alerting checks: no config, no cloud access.
- The skill's own test suite (`S/tests/`): not needed for this ticket.

## 5. Friction log

| # | Kind | Pointer | Note |
| --- | --- | --- | --- |
| F1 | Helpful | `E/SKILL.md:64` | The routing row names "pre-release security review" explicitly, so picking the specialist took seconds. |
| F2 | Assumed something I lacked | `S/SKILL.md:37-42` | It says "with an available Python 3.11+ interpreter" and gives the command as `python …`. `python3` here is 3.9, so it crashed on `import tomllib` (`S/scripts/inspect_security_surface.py:24`). I had to search for another interpreter. A `tomli` fallback, or a clear version error message, would help. |
| F3 | Unsure what to type | `S/SKILL.md:41`, `S/references/validation.md:10` | `$SKILL_DIR` is never defined. I guessed `.claude/skills/adk-agent-security`. |
| F4 | Instruction assumed something false (most serious) | `S/scripts/inspect_security_surface.py:644-650` (only `ast.Call`/`ast.Name` handled in `describe_tool`) | The common `from . import tools; tools=[tools.fetch_email, …]` form gives `kind: "other"` for every tool, so all trifecta legs come back false. A reviewer who trusts `S/SKILL.md:44-54` would see a clean report on the most dangerous agent in the repo. I only caught it by reading the code, then confirmed it with a rewritten scratch copy. |
| F5 | Noise | `S/scripts/inspect_security_surface.py:27` (`EXCLUDED`) | `.claude/` is not excluded, so the inventory scanned 131 files, mostly the skills' own tests and assets. It reported 15 extra agents and 11 findings that have nothing to do with the project. There is no `--exclude` flag (`--help`). |
| F6 | Instruction assumed something I could not provide | `S/references/validation.md:10,12` | It writes the inventory to `/tmp/…`, which conflicts with the session's "only change files in the cwd" rule. Accepting an output path, or defaulting to stdout, would avoid this. |
| F7 | Heavier than needed | `S/SKILL.md:73` | Mode (f) says "Use all references": 8 references plus 2 assets, about 1,200 lines, before writing a word. `tool-supply-chain.md`, and most of `compatibility.md` and `adversarial-testing.md`, do not apply to a repo with no MCP, A2A or executor. A "skip if the inventory shows no MCP/A2A/executor" note would save a lot of reading. |
| F8 | Heuristic over-flagging | `S/SKILL.md:53` | Every `httpx.get` to an internal host is flagged as egress, and `fetch_email` is flagged as `write`, so billing_agent shows a false trifecta. The doc does say to confirm every row by hand, which is right, but it doubles the work. |
| F9 | Validation unreachable in review mode | `S/SKILL.md:119-125`, `S/references/validation.md:38-49` | The finish step asks for scripted-model Runner tests "for each structural change" and an offline suite. In mode (f) nothing changes, and here google-adk is absent. It is unclear what the minimum finish is for a review-only run. I used the evidence-label table instead. |
| F10 | Unsure | `S/SKILL.md:60-62` vs session rules | "Ask only for decisions the source cannot settle" lists four questions, but the user was unavailable. I recorded them as assumptions in the review's Open questions. The skill gives no guidance for running without a user. |
| F11 | Helpful | `S/assets/threat-model-checklist.md:13-44` | The ASI and LLM tables with an owning skill per row made it quick to attach OWASP IDs and owners to findings. |
| F12 | Helpful | `S/references/injection-patterns.md:25-49`, `S/references/agency-and-output.md:8-14,60-67` | The quarantined-reader recipe, the tool tier table and the "identity never from the model" rule fit the findings directly and gave concrete fixes. |
| F13 | Helpful | `S/references/compatibility.md:32-42` | The CVE and version-floor table let me assess the 2.8.0 pin without going online. |

## 6. Rating and top three changes

**Rating: 3 / 5.** Routing and the reference content were very good. The inspector's false negative on a common import style (F4) is a real hazard for a security tool, and the Python and `$SKILL_DIR` setup cost several turns.

Three changes that would help most:
1. **Fix the inspector so it resolves `module.function` tool references** (`ast.Attribute` in `describe_tool`, and when resolving function definitions), with a test for the `from . import tools` pattern. When tools stay unresolved, report a finding or `partial: true` instead of a clean trifecta.
2. **Exclude `.claude/` (and other skill install directories) by default, add `--exclude`, and support Python 3.9/3.10** (a `tomli` fallback or a regex pin parse). Define `$SKILL_DIR` in `SKILL.md`.
3. **Give mode (f) a lighter, conditional reading list and a review-only finish definition.** For example: always read threat-model + agency-and-output + the checklist; read supply-chain/A2A/executor references only when the inventory shows them. Also state the minimum validation for a no-change review.

## 7. Next prompt the skills told the user to type

None given. Neither `E/SKILL.md` nor `S/SKILL.md` gives a literal next prompt. The only literal command offered is the install line at `E/SKILL.md:88` (`npx skills@latest add RuslanKhis/agentic-engineering-skills --skill <specialist-name>`), which applies only when a specialist is missing; it was not missing here.
