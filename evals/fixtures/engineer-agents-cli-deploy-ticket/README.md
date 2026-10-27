# claims-helper

Claims helper agent for the home-insurance claims team, created with Agents CLI 1.11.0
(`agents-cli-manifest.yaml`). Dependencies are managed with uv (`uv.lock`).

- Agent: `app/agent.py`; Agent Runtime entry point: `app/agent_runtime_app.py`.
- Infrastructure: `deployment/terraform/single-project/` (generated; `vars/env.tfvars` names the
  pilot project).
- `deployment_metadata.json` was written by an `agents-cli deploy` to our dev project on
  2026-10-09 while we tried things out.
- Tests: `uv run pytest tests/unit` (the unit tests also run with
  `python -m unittest discover -s tests -t .`).

google-adk and agents-cli are not installed in this checkout's environment.
