# REPORT: T-103 "gemini-2.5-pro is retiring"

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-engineer` (invoked by the user with `/adk-engineer`): `.claude/skills/adk-engineer/SKILL.md`
2. `.claude/skills/adk-release-engineering/SKILL.md` (specialist, read directly from the sibling directory)
3. `.claude/skills/adk-release-engineering/references/model-migration.md`
4. `.claude/skills/adk-release-engineering/assets/model-upgrade-checklist.md`
5. `.claude/skills/adk-release-engineering/assets/PROMPT_CHANGELOG.md`
6. `.claude/skills/adk-release-engineering/scripts/inventory_release_refs.py`, run but not read (first with Python 3.9, which crashed; then with 3.12)
7. `.claude/skills/adk-release-engineering/references/ci-eval-gates.md`, first 58 lines
8. `.claude/skills/adk-model-and-output-contracts/SKILL.md`, grepped rather than read in full (secondary specialist)
9. `.claude/skills/adk-model-and-output-contracts/references/model-selection.md`
10. `.claude/skills/adk-model-and-output-contracts/references/reasoning-and-sampling.md`
11. `.claude/skills/adk-model-and-output-contracts/scripts/audit_model_config.py`, run but not read
12. `.claude/skills/adk-release-engineering/assets/eval-gate.github-actions.yml`, read but not adopted
13. `.claude/skills/adk-agent-evaluation/`: directory listing only

Not opened: release-engineering `compatibility.md`, `versioning.md`, `staged-rollout.md`, `validation.md`, `production-feedback.md`; all of the adk-agent-evaluation references.

## 2. Specialist chosen and why

**Primary: `adk-release-engineering`.** The adk-engineer routing table maps "Model deprecation notices, prompt and model version pinning, eval gates in CI, canary or rollback" to it (`adk-engineer/SKILL.md:66`). Its mode (c), model migration, fits the ticket's two requirements: replace a retiring model, and do it without silently dropping quality, given that CI runs only unit tests.

**Secondary: `adk-model-and-output-contracts`.** The change crosses into model choice and thinking/temperature settings (`adk-engineer/SKILL.md:63`). The triage agent's `thinking_budget` and the 0.2 temperatures have to change on Gemini 3. **`adk-agent-evaluation`** owns the side-by-side, which could not run here, so it is named as the next owner and was not applied.

## 3. Files changed, and what is not finished

Changed (uncommitted, working tree only):
- `support_agent/agent.py`
  - Added a single `MODEL_ID = "gemini-3.8-flash"` constant, used by all four agents (it replaces four `"gemini-2.5-pro"` literals).
  - triage_agent: `thinking_budget=2048, temperature=0.2` became `thinking_level="medium"`, with temperature at its default.
  - root: removed `temperature=0.2`.
  - Prompts are unchanged.
- `tests/test_model_pins.py` (new): an AST-based pin test that doesn't import google.adk. It checks that every agent uses `MODEL_ID`, that the model is not 2.x and not an alias, and that no `thinking_budget` or `temperature` remains.
- `docs/releases/T-103-model-upgrade.md` (new): the filled model-upgrade checklist and go/no-go record, currently **NO-GO pending evidence**.
- `PROMPT_CHANGELOG.md` (new): a back-filled baseline row plus the rc-T103 candidate row, with prompt hashes from the inventory helper.

**Not finished:**
- **No quality evidence.** There is no development set, holdout, eval config or scripted-model test in the repo, so the old-vs-new side-by-side the ticket's "without silently dropping quality" requires has not run. Merging this to `main` (weekly release, unit tests only) would ship the swap unevaluated. **Do not merge until the side-by-side in the release record is done.**
- No live eval tier was added to CI. The eval-gate workflow asset needs an eval set, expectations, Workload Identity Federation (WIF) and project variables that don't exist here. A placeholder workflow would either fail every push or pass vacuously.
- No staged rollout was performed or scripted, because there is no deploy config in the repo and no cloud access.
- Not committed (the user wasn't available to approve).

### Questions I would have asked (assumptions taken)

1. **Backend.** README says production uses the API-key backend (Gemini API), but the email's 2026-10-20 date is the Vertex date. On the Gemini API, 2.5 is "limited" with no shutdown date. *Assumed:* migrate anyway; treat 10-20 as the deadline in case Vertex is used anywhere.
2. **Flash vs Pro tier.** Is dropping from a Pro tier to Flash acceptable? *Assumed:* `gemini-3.8-flash`, the replacement Google names on both pages. The only Pro option is a preview, which the skill treats as a production finding.
3. **Thinking level for triage.** *Assumed:* `medium`, the model default. I chose it over `low`, which the skill suggests for classification, so quality is not reduced while there is no data.
4. **Owner and approver** of the model change and traffic steps: unknown.
5. **Is the side-by-side expected before 10-20?** If evaluation can't happen in time, ship with a canary, or ask Google for an extension?
6. **CI file location.** `.github_workflows_ci.yml` sits at the repo root, not in `.github/workflows/`. Is CI actually running?
7. **Real email samples.** May real, de-identified inbound emails be used to build the development set (personal-data concern)?

## 4. Checks

Run:
- `inventory_release_refs.py --project . --dry-run` with Python 3.12: exit 0. It found 4× `gemini-2.5-pro` and 4 prompt literals in `support_agent/agent.py`, and no judge, eval set or deploy config. With the default `python3` (3.9) it **crashed** with `ModuleNotFoundError: tomllib`.
- `audit_model_config.py --project . --dry-run` with Python 3.12: exit 0. It reported `model_limited` ×4, `temperature_below_default` at lines 35 and 46, and `schema_with_tools_path_depends_on_backend` at line 35 (left as is: out of scope).
- `tests/test_model_pins.py`, all three functions, called directly with Python 3.12 (pytest isn't installed): **PASS** on the change. On the stashed baseline they **FAIL** (3/3), so the test actually discriminates.
- `ast.parse` of the edited `support_agent/agent.py`: OK.

Not run:
- `tests/test_tools.py` and any import of `support_agent`: they need google.adk, which isn't installed.
- pytest itself (not installed; no install allowed).
- Scripted-model tests, `adk conformance test`, `AgentEvaluator` and any live model call: none exist, and there was no network or credentials.
- Load test and canary.
- Re-reading the Google deprecation pages (no network). Dates come from the skill snapshot dated 2026-10-07/08.

## 5. Friction log

1. **Helpful:** the routing table pointed straight at the right specialist with no ambiguity: "Model deprecation notices" (`.claude/skills/adk-engineer/SKILL.md:66`). Line 63 (model selection, thinking settings) made it clear a second skill was involved.
2. **Unsure what to type:** the inventory helper says "Python 3.11+" and then shows `python ...` (`.claude/skills/adk-release-engineering/SKILL.md:22-25`). Here `python3` is 3.9, and the script dies at import (`.claude/skills/adk-release-engineering/scripts/inventory_release_refs.py:12`, `import tomllib`) with a traceback instead of a version message. I had to hunt for a 3.12 interpreter. The same pattern appears at `.claude/skills/adk-model-and-output-contracts/SKILL.md:22-25`.
3. **Heavier than needed:** `--project .` also scans the installed skills under `.claude/skills/`. Of about 150 signal entries, 130 came from the skills' own tests and assets, and the output (41 KB) overflowed the tool. Even the manifest's `judge_models`, `eval_configs` and `prompts` were polluted by skill fixtures, which could mislead someone into thinking the project has a judge pinned to 3.8-flash. The JSON was also followed by `exit=0` text, so `json.load` failed. `.claude` is not in the excluded directories (see the `limits` in the output; `SKILL.md:25`).
4. **Assumed something I couldn't provide:** the model-migration reference (`.claude/skills/adk-release-engineering/references/model-migration.md:35-41`) and the checklist assume a frozen development set and a judge. The project has neither, and the reference has no path for "no eval set exists and the deadline is in 11 days". I had to decide myself to prepare the change and mark it NO-GO.
5. **Helpful:** the backend split between the two calendars (`.claude/skills/adk-release-engineering/references/model-migration.md:21`) made me notice that README's API-key backend may make the Vertex date irrelevant. That is the most important finding for the user.
6. **Helpful:** the thinking-level table (`.claude/skills/adk-model-and-output-contracts/references/reasoning-and-sampling.md:11`) shows 3.8-flash has no `minimal` level. Lines 19 and 25 gave concrete reasons to drop `thinking_budget` and the 0.2 temperature.
7. **Helpful:** the checklist asset (`.claude/skills/adk-release-engineering/assets/model-upgrade-checklist.md:3`), especially "not run is valid, blank is not". It made the release record honest and quick to write.
8. **Unsure:** two sibling skills each tell you to run their own helper, and the release skill hands off lifecycle status to the other skill's audit script (`.claude/skills/adk-release-engineering/SKILL.md:28`). It wasn't clear whether both were needed. They overlap; the audit added the temperature and schema findings.
9. **Heavier than needed / assumed:** the eval-gate workflow asset (`.claude/skills/adk-release-engineering/assets/eval-gate.github-actions.yml:43-61`) has about 8 `<PATH>`/`<PIN>` placeholders and assumes `requirements.txt`, WIF and an installed checker path. It can't be adopted without an eval set, so I left it out.
10. **Unsure:** the instruction to "keep pins unchanged unless a version decision is requested" (`.claude/skills/adk-release-engineering/SKILL.md:14`) clashes with the requirement for evidence before go. I resolved it by changing the pin in the working tree but recording NO-GO.
11. **Read before useful work:** 2 SKILL.md files + 2 references + 2 assets + 2 more references for settings, about 8 documents before the first edit.

## 6. Rating: 3 / 5

The routing and the content were right and specific. The friction was mechanical (interpreter, noisy scan), and there was no path for the very common case of a project with no eval set.

The three changes that would help most:
1. Make the helpers exclude `.claude/` and other skill install directories by default, print only project findings (or have a `--summary` mode), and exit with a clear "needs Python 3.11+" message instead of a `tomllib` traceback.
2. Add a "no eval set yet + hard deadline" branch to `model-migration.md`: prepare the pin, mark NO-GO, define the minimum dev-set size and which cases to bootstrap, and decide whether a canary can stand in. Point to the exact adk-agent-evaluation reference to start from.
3. Merge or clearly sequence the two audit helpers (release inventory and model audit) into one command for the deprecation scenario.

## 7. Next prompt the skills told the user to type

None given. The only literal command in the skills is the install line for a missing specialist (`npx skills@latest add RuslanKhis/agentic-engineering-skills --skill <specialist-name>`, `.claude/skills/adk-engineer/SKILL.md:88`). It didn't apply, because every specialist was installed.
