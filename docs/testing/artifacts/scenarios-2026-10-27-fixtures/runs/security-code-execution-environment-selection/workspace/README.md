# Upload analyst

Lets Fjord Insurance's underwriting team ask questions about spreadsheets and CSV exports that
customers upload to the claims portal. The agent writes Python against the uploaded files and
runs it, then emails a short report.

- Google ADK 2.12.0 (`pyproject.toml`), Gemini on Vertex AI in `europe-west4`.
- Runs on Cloud Run in the `fjord-uw-prod` project (EU); uploads live in the
  `fjord-uw-uploads` bucket in the same project.
- `app/agent.py` builds the agent; `app/tools/` holds the tools.
- `deploy/service.yaml` is the Cloud Run service.

Customer uploads must not leave the EU project.

## Code execution decision

Model-written code runs in `AgentEngineSandboxCodeExecutor` against one named sandbox in
`fjord-uw-prod` / `europe-west4` (`SANDBOX_RESOURCE_NAME`, validated in `app/sandbox.py`; the service
refuses to start without it). Why, on google-adk 2.12.0 (source read, not executed):

- `UnsafeLocalCodeExecutor` ran the code inside the Cloud Run process: service-account token,
  metadata server, bucket access and the open network were all in the code's reach. Removed.
- `EnvironmentToolset` over Daytona sent customer files to a provider outside Google Cloud, which
  breaks the EU-project rule, and Daytona's public repo says it is no longer maintained. Removed,
  with the `daytona` dependency and its secret.
- The Agent Engine sandbox is a resource of our project, so the serving container's credentials are
  not reachable from the code, and naming the resource fixes project and region. The lazy path would
  pick the region from `GOOGLE_CLOUD_LOCATION`, hence the mandatory name.
- Fallback if the sandbox is unavailable in `europe-west4`: `CloudRunSandboxCodeExecutor(allow_egress=False)`
  (same container, same region), but only after a probe inside it shows `169.254.169.254` is
  unreachable and `google.auth.default()` fails. `GkeCodeExecutor` needs a GKE cluster we do not have.

`download_upload` stages the file in session state (`CodeExecutorContext`), not on the service disk.
`email_report` only sends to `REPORT_ALLOWED_DOMAINS` and sits behind `require_confirmation=True`.

Assumptions (no one to ask): the sandbox exists or can be created in `europe-west4` with no outbound
internet; `fjord.example` is the only legitimate recipient domain; the project id (not number) appears
in the resource name; sessions use in-memory storage (ADK confirmation is unsupported with
`DatabaseSessionService`/`VertexAiSessionService`); `File.content` takes base64 text.

Not provable offline: sandbox egress and credential reachability, and the `File` content encoding. Check
these once against the real sandbox before release.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk and the Daytona SDK are not installed in this environment; tests that need them skip.
