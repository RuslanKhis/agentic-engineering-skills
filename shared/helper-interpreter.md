<!--
Where helpers resolve from, which Python runs them, and how to run a project's
tests when no interpreter meets its pin. Moved here from adk-engineer's
SKILL.md so each specialist installed alone carries it. Edit here, then run
scripts/sync_shared.py.
carriers: adk-engineer, adk-agent-evaluation, adk-agent-instructions, adk-agent-interoperability, adk-agent-observability, adk-agent-security, adk-fastapi-backend, adk-frontend-integration, adk-memory-architecture, adk-model-and-output-contracts, adk-operational-guardrails, adk-release-engineering, adk-sql-agent-engineering, adk-tool-auth-and-secrets, adk-tool-interface-design, adk-workflow-design, deploy-adk-on-google-cloud, optimise-adk-on-google-cloud, protect-adk-sensitive-data, safe-api-tool-calls
-->

## Helper scripts and interpreters

`$SKILL_DIR` is the directory that contains the skill's `SKILL.md`; resolve its
helper scripts, references and assets relative to it, even when the installer
uses symlinks. The helpers need Python 3.11 or later. If the project's
interpreter is older, run the helper alone with any available 3.11+
interpreter, say which one ran, and change nothing in the project: no new
interpreter pin and no installs. Helper output kept as evidence goes in
`.adk-evidence/` at the project root (create it and add it to `.gitignore`);
the helpers never scan it, nor the installed skill folders.

Run the project's own tests with the project's interpreter and runner. When no
interpreter at hand meets the project's `requires-python`, run the tests with
the newest one available, say which one ran and that it is below the pin, and
install nothing; the tests the pin matters for are `not run`. When the only
interpreter that meets the pin lacks the project's test runner, run what the
standard-library runner can collect there and the rest on the older
interpreter, and report both runs by interpreter. Write new tests so the
standard-library runner can collect them (`unittest`-style classes, which
pytest collects as well, so a project's pytest job is unaffected) when that is
the runner that will see them. For a `tests/` directory without `__init__.py`
the command is `PYTHONPATH=. python -m unittest discover -s tests`, since
`discover -t .` refuses a start directory that is not a package.
