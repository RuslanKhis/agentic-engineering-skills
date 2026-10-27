# engineer-google-skills-supporting-missing: what the fixture holds

Base: support-assistant, with `pyproject.toml` removed. Overlay:

- `requirements.txt` (pinned), `Dockerfile` (python:3.12-slim, single uvicorn process),
  `AGENTS.md` (requirements.txt workflow; "cloud commands always name --project and --region").
- `docs/tickets/support-agent/G04.md`: primary `deploy-adk-on-google-cloud`, supporting
  `google/skills:cloud-run-basics (create the Cloud Run service and set its ingress)` and
  adk-tool-auth-and-secrets; acceptance for ingress (internal and Cloud Load Balancing), a
  dedicated runtime service account, no keys in the image; empty Evidence.
- `docs/architecture/support-agent.md`: existing global external ALB `harbour-web-lb` in another
  project; region europe-west2; dev project harbour-support-dev.
- `docs/plans/support-agent.md`: execution scope — only a local image build is authorised.
- The existing offline suite (`tests/`) passes.
- No Google product skill is installed and finding-google-skills is absent (catalogue has only
  adk-engineer, deploy-adk-on-google-cloud, adk-tool-auth-and-secrets,
  adk-agent-observability).

Assertion map: A1 deploy skill leads, google/skills entry is a product skill that operates the
mechanism; A2 reports cloud-run-basics missing with `npx skills add google/skills --skill
cloud-run-basics`, no invented instructions; A3 local work: packaging, identity choice, ingress
`internal-and-cloud-load-balancing`, local tests (written; cannot be executed without a shell —
judge on whether the agent claims they ran), readback plan; A4 private ingress, scoped
`--project`/`--region`, dedicated identity; A5 provisioning recorded in Evidence as an
execution-scope prerequisite, no gcloud mutation run.

Original context (unchanged).
