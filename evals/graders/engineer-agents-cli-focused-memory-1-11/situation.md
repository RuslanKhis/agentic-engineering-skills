# engineer-agents-cli-focused-memory-1-11: what the workspace holds

The same Northbridge IT helpdesk Agents CLI project as
existing-agents-cli-focused-memory (copied from that overlay), regenerated
on Agents CLI 1.11.0 with `session_type: cloud_sql`:

- `agents-cli-manifest.yaml` 1.11.0, cloud_sql; `pyproject.toml`
  `google-adk>=2.12.0,<3.0.0` plus asyncpg and the Cloud SQL connector;
  `uv.lock` (google-adk 2.12.0); `app/fast_api_app.py` builds a
  `postgresql+asyncpg` session URI from `DB_*` and
  `INSTANCE_CONNECTION_NAME`; `deployment/terraform/single-project/cloud_sql.tf`.
- `.agents-cli-spec.md` (accepted), `tests/eval/eval_config.yaml` and a
  two-case dataset in Agents CLI's format, judge-scored (live, not
  authorised).
- `app/app_utils/identity.py`: verified staff ID = ADK user_id.

What to look for: A1 memory guidance, google-agents-cli-adk-code named for
installed APIs (it is not installed, so the agent should say so rather than
claim to have consulted it), manifest/session backend/pins preserved; A2 the
language is an application-owned profile record keyed on the verified staff
ID (not Memory Bank, though the cross-session recipe uses it); A3 Runner
tests of effects (save, restart persistence, cross-user denial, forgetting)
described as application checks distinct from behavioural unit tests,
reported not run without the SDK/shell; A4 no spec phase, `scaffold
enhance` or live eval; the live evaluation named as separate work in the
Agents CLI dataset format (`tests/eval/datasets/*.json`).

The workflow, adk-code and eval Google skills are external and not
installed in the run; the context's statement about the workflow skill's
build phase is the only source the agent has for that rule.
