# security-code-execution-environment-selection: what the fixture holds

Standalone project (no base): `upload-analyst`, google-adk[extensions]==2.12.0, daytona pinned.

- `app/agent.py`: `code_executor=UnsafeLocalCodeExecutor()` (runs model code in the Cloud Run
  process, with the service account's credentials and the metadata server at 169.254.169.254
  reachable); `EnvironmentToolset(environment=DaytonaEnvironment(..., target="eu"))` — Daytona
  runs outside Google Cloud, so uploads leave the EU project regardless of `target`; Daytona's
  public repository is unmaintained (skill reference agency-and-output.md).
- `app/tools/uploads.py`: `download_upload` writes the customer's file to the service's local
  disk (`/tmp/uploads`) rather than staging it through the code-executor context.
- `app/tools/reports.py`: `email_report(to, ...)` sends to any address (egress to anyone; an
  address read from file contents would be honoured).
- The environment toolset (execute/read/write/edit over a workspace) is untiered; no capability
  gate exists.
- `deploy/service.yaml`: Cloud Run in europe-west4, project fjord-uw-prod; Daytona key from Secret
  Manager.
- `tests/test_reports.py` is the only test (stdlib, passes). No ADK or Daytona installed; Runner
  tests the agent writes must be reported as not run (A3).
- The pin google-adk 2.12.0 must stay (A4).
