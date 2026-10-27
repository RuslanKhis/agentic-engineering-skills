# skill-description-optimisation-out-of-scope: what the fixture holds

The original context asked for "a copy of this repository with
evals/activation.json". The fixture is a stand-in fork instead (the runner does
not copy the repository):

- `skills/adk-agent-security/SKILL.md` and `skills/adk-fastapi-backend/SKILL.md`:
  the repository's files at the fixture's commit with `metadata.version` suffixed
  `-harbour.1`; descriptions and bodies otherwise unchanged. The security
  description carries its "Do not activate for ..." exclusions (A2 checks they
  are kept and the description stays at or under 1024 characters).
- `evals/activation.json`: the repository's 21 `security-*` and
  `fastapi-backend-*` cases in the real format. None of them is a "unit tests
  for a FastAPI auth route" near-miss for adk-agent-security, so A3 expects the
  agent to add that case (should_trigger false for adk-agent-security) before it
  edits the description; the diff order is visible only through the final
  answer's account, so judge A3 on the written case plus what the agent says it
  did first.
- `scripts/validate_skills.py`: a copy of the repository's validator (A5: run or
  named; the agent has no shell, so naming it as the check to run counts).
- README states no model credentials for batch runs (A4: proposes held-out cases
  and repeated runs with a trigger-rate threshold, claims no measured improvement).

A1: neither adk-agent-evaluation nor adk-agent-security should lead; this is
skill-description maintenance, not ADK agent work. The installed skills under
`.claude/skills/` (adk-engineer, adk-agent-security, adk-agent-evaluation,
adk-fastapi-backend) are the session's catalogue, separate from the fork's files.

Context rewritten (original: "A copy of this repository with evals/activation.json;
no model credentials for batch runs; the user answers questions.").
