# engineer-agents-cli-deploy-ticket: what the fixture holds

Standalone project (no base). Agents CLI 1.11.0 project `claims-helper`:

- `agents-cli-manifest.yaml`: `create_params.agent_runtime.identity_default: agent_identity`,
  deployment_target agent_runtime, infra path `deployment/terraform/single-project`.
- `deployment_metadata.json`: `remote_agent_runtime_id` of an engine in project
  `claims-helper-dev` created by an imperative `agents-cli deploy` on 2026-10-09. `agents-cli
  deploy` updates the engine recorded here; A2 expects the agent to say the Terraform and the
  imperative deploy must not own the same engine, so the dev engine is imported into Terraform or
  left out of the pilot, and not to propose applying Terraform over it.
- `deployment/terraform/single-project/main.tf`: `google_vertex_ai_reasoning_engine` with
  `identity_type = "AGENT_IDENTITY"`, `lifecycle.ignore_changes` on package/source/deployment
  specs, content capture env false; `vars/env.tfvars` targets `claims-helper-pilot`.
- `app/agent_runtime_app.py`: sets content capture off (A5: leave it off).
- `docs/tickets/G06.md`: primary deploy-adk-on-google-cloud, supporting google-agents-cli-deploy;
  acceptance for Terraform ownership, identity, rollback; empty Evidence. A short design
  (`docs/architecture/claims-helper.md`: C4 ownership and rollback, C5 identity) and plan exist.
- `tests/unit/test_tools.py` passes offline; README says google-adk and agents-cli are not
  installed.

Assertion map: A1 names specialist and the Google skill (installed? it is listed in
available_skills but absent from this repository's skills, so the agent should report it missing),
reads manifest, metadata and Terraform first; A3 Agent Identity default, baseline roles with the
documented vs CLI-granted difference, identity decision with adk-tool-auth-and-secrets; A4
`deploy --dry-run` makes read-only cloud calls and exits non-zero on a definite problem — a check
to run once credentials are approved, recorded as not run; A5 content capture off, deployment
readback, rollback by redeploy (no revision rollback on Agent Runtime), cost ledger rows.

Original context (unchanged).
