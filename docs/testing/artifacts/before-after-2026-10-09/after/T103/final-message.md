I've moved all four agents from `gemini-2.5-pro` to `gemini-3.8-flash`. The ticket also asks that quality doesn't silently drop, and that part isn't proven: the old-vs-new comparison has not run, so this is a candidate and the go/no-go is still pending.

**Specialist: `adk-release-engineering`**, because the ticket is a model deprecation notice that needs a version pin and an eval gate in CI ("Our CI only runs unit tests"). Supporting skills: `adk-model-and-output-contracts` to pick the replacement model and its settings, and `adk-agent-evaluation` for the eval-set format and its strict results checker.

**Changes**
- **Model:** all four agents read `AGENT_MODEL` from the new `support_agent/models.py`. I picked `gemini-3.8-flash` because it's stable, has no retirement date announced, and Google lists it as the replacement. There is no stable Gemini 3 Pro model, only a preview.
- **Settings:** the triage agent's `thinking_budget=2048` became `thinking_level="medium"`, because Gemini 3 deprecates `thinking_budget` and Vertex can reject it with a 400 error. I removed `temperature=0.2` from triage and root, following Google's advice to leave it at 1.0 on Gemini 3. The prompts are unchanged.
- **Tests:** `tests/test_model_pins.py` checks that the model is pinned, isn't retiring, isn't a `-latest`/`-preview` alias, and that `thinking_budget` is gone. It runs without ADK installed.
- **Live eval gate:** `tests/eval/test_ci_gate.py` plus `evals/` hold two draft read-only cases (an order lookup and an invoice question routed to billing), run 3 times each.
- **CI:** `.github_workflows_ci.yml` has a new opt-in `live-eval` job, triggered by the `run-live-eval` label or a manual run. If no eval results are produced, the job fails rather than passing.
- **Records:** a filled go/no-go checklist in `docs/releases/T-103-model-upgrade.md`, a row in `PROMPT_CHANGELOG.md`, an Evidence section in the ticket, and `REPORT.md`.

**Checks**
- The pin tests ran: 3 passed. The live gate was skipped, as intended without `EVAL_LIVE=1`.
- Running the results checker on an empty CSV exits 1, so a skipped live eval blocks the gate.
- **Not run:** `tests/test_tools.py` (needs google-adk), the live gate itself, checking the eval-set files with ADK 2.8.0, the old-vs-new comparison, and any canary. I also couldn't re-read Google's deprecation pages (no network), so the dates come from the skill's 2026-10-07 snapshot.

**Questions I'd have asked** (all recorded in `REPORT.md`):
- **Which backend does production use?** The README says the API key (Gemini API), but Google's email is about Vertex. I migrated anyway, since 2.5 is limited to existing users on the Gemini API.
- **Is Flash acceptable in place of Pro?** I assumed yes, since the only Gemini 3 Pro is a preview.
- **Can CI reach the internal tool services?** I assumed not, so the live job is opt-in.
- **Is there a test setup for `issue_refund`?** It posts real refunds, so I left refund cases out of the live eval.
- **Should `.claude/` be committed?** The CI job uses the results checker from `.claude/skills/adk-agent-evaluation`, which is currently untracked.

**Before 20 October:** run `live-eval` on `main` to get a baseline, then on this branch, and compare. Don't deploy until that passes, and roll out through a no-traffic Cloud Run revision first. Rolling back to `gemini-2.5-pro` only works until 20 October.

**Rating and friction:** I gave it 3/5. Picking the specialist was immediate. The friction:
- The inventory helper needed Python 3.11+, and the default `python3` here is 3.9.
- It also scanned the installed skills in `.claude/`, which buried the project's four model IDs in 31 KB of noise.
- The CI template assumes a Vertex backend.
- Nothing warns that a live eval with write tools makes real refunds and sends real emails.

**Next prompt from the skills:** none given. `adk-engineer` says to end with one but supplies no wording.