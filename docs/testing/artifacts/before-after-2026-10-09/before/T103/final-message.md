I've moved all four agents to `gemini-3.8-flash` and written `REPORT.md`, but the change is not ready to ship: there is no quality evidence yet. Merging it to `main` would release an untested model swap, which is exactly the silent quality drop T-103 asks us to avoid. It's uncommitted in the working tree, and I've recorded it as **NO-GO** until an old-versus-new comparison has run.

**Specialist:** I used `adk-release-engineering`, because the toolkit's routing table sends model deprecation notices there and its model-migration mode fits the ticket. The change also touched model settings, so I used `adk-model-and-output-contracts` for those. The comparison itself belongs to `adk-agent-evaluation`, which I couldn't apply because the project has no evaluation set.

**Decision for you: the backend.** The README says production uses an API key, not Vertex. The 20 October date in Google's email is the Vertex retirement date; for API-key users Google lists gemini-2.5-pro as limited to existing users with no shutdown date. If the README is right, the hard deadline may not apply to production, so please confirm the backend before treating 20 October as a cutover.

**Changes:**
- **`support_agent/agent.py`:** one `MODEL_ID = "gemini-3.8-flash"` constant, used by all four agents.
  - I picked it because Google names it as the replacement, it is stable, and no retirement is announced.
  - The triage agent's old thinking setting (`thinking_budget`) becomes `thinking_level="medium"`, since the old one is deprecated on Gemini 3 models.
  - I removed the two `temperature=0.2` settings, because Google recommends the default of 1.0 on Gemini 3.
  - Prompts are unchanged.
- **`tests/test_model_pins.py`** (new): reads the agent source without importing google-adk. It checks that every agent uses the constant, that no 2.x model or alias remains, and that neither old setting comes back.
- **`docs/releases/T-103-model-upgrade.md`** (new): the filled upgrade checklist, with the empty comparison table and the steps needed to reach GO.
- **`PROMPT_CHANGELOG.md`** (new): a row for the current release and one for this candidate.

**Checks:**
- The new pin test passes on the change and fails 3 of 3 on the original code. pytest isn't installed, so I called the test functions directly with Python 3.12.
- The skills' two scanning scripts ran with Python 3.12. The release-inventory one crashed under the default Python 3.9 first.
- **Not run:** `tests/test_tools.py` (it imports google-adk, which isn't installed), any live model call or comparison, a load test and a staged rollout.

**Still to do before it ships:**
- Build a development set from de-identified real emails, plus a holdout.
- Run gemini-2.5-pro against gemini-3.8-flash on that set, then the holdout once.
- Roll out on Cloud Run as a no-traffic tagged revision and step traffic up.

`REPORT.md` also lists seven questions I'd have asked, with the assumption I took for each. Two matter most: whether moving from a Pro model to a Flash model is acceptable, and whether CI runs at all, since `.github_workflows_ci.yml` sits at the repo root rather than in `.github/workflows/`.

**Skills feedback:** I rated it 3/5. The routing and content were good. The main friction:
- The scanning scripts crash under Python 3.9 instead of saying they need 3.11+.
- They also scan the installed skills, so about 130 of roughly 150 findings came from skill files, not this project.
- The migration guide has no path for a project with no evaluation set facing a deadline.

The skills gave no next prompt for you to type.