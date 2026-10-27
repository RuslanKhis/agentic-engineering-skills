# Harbour fork of the agentic engineering skills

Our team's fork of the Agentic Engineering skills collection for Google ADK.
This is a sparse checkout: only the two skill packages we change in this fork
(`skills/adk-agent-security`, `skills/adk-fastapi-backend`, `SKILL.md` only),
the activation cases for them and the package validator. The other skills and
their references are unchanged from upstream and are not checked out here.

- Activation cases: `activation.json` in the `evals` folder (one object per prompt: `skill`,
  `prompt`, `should_trigger`, `rationale`, `split` of `dev` or `heldout`).
- Package check: `python scripts/validate_skills.py --root .`

We have no model credentials for batch selection runs in this environment.
