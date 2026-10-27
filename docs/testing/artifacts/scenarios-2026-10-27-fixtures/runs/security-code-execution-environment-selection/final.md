I switched the agent to `AgentEngineSandboxCodeExecutor` pinned to one sandbox in `fjord-uw-prod`, `europe-west4`. **I couldn't run the new tests because Bash is disabled in this session.** I checked them by reading only, so please run `python3 -I -m unittest discover -s tests -t .` before merging. google-adk stays at 2.12.0.

## Why this executor
- **`UnsafeLocalCodeExecutor`** ran model code inside the Cloud Run process. That put the service account token, the metadata server, bucket access and the open network within the code's reach.
- **`EnvironmentToolset` over Daytona** sent customer files to a provider outside Google Cloud, which breaks the EU-project rule. Daytona's public repo also says it is no longer maintained. It was a second code-running surface as well.
- **Agent Engine sandbox** is a resource in our own project, so the serving container's credentials aren't reachable from the code. Naming the sandbox resource fixes its project and region. Without a name, ADK picks the region from `GOOGLE_CLOUD_LOCATION`, so `app/sandbox.py` requires `SANDBOX_RESOURCE_NAME` and the service refuses to start without a valid one.
- **Fallback** if the sandbox isn't available in `europe-west4`: `CloudRunSandboxCodeExecutor(allow_egress=False)`. Use it only after a probe inside it shows the metadata server is unreachable and `google.auth.default()` fails.

## Changes
- **`app/agent.py`:** the new executor replaces the Unsafe executor and the Daytona toolset. `email_report` now sits behind `require_confirmation=True`.
- **`app/tools/uploads.py`:**
  - Uploads are staged into session state for the sandbox, not onto the service disk.
  - `upload_id` must match `up-<digits>`.
  - Uploads are capped at 25 MB.
  - The tool returns a file name rather than a path.
- **`app/tools/reports.py`:** only one recipient at `REPORT_ALLOWED_DOMAINS` is accepted (default `fjord.example`). Subject headers can't be injected.
- **`pyproject.toml` and `deploy/service.yaml`:** the `daytona` dependency and its secret are gone. `service.yaml` now has `SANDBOX_RESOURCE_NAME` as a placeholder that fails validation until you fill it in.
- **Tests:** `tests/test_isolation.py`, `tests/test_residency.py` and `tests/test_outbound.py`. They use AST and text checks plus fakes, and they block sockets and DNS.

## Questions I couldn't ask, and what I assumed
1. Does the sandbox exist, or can it be created, in `europe-west4` with no internet access? I assumed yes.
2. Is `fjord.example` the only legitimate recipient domain? I assumed yes.
3. Does the resource name use the project ID rather than the project number? I assumed the ID.
4. Are sessions in memory? ADK confirmation doesn't work with `DatabaseSessionService` or `VertexAiSessionService`, so I assumed in-memory.
5. Does `File.content` take base64 text? I read nothing to confirm this, so it is a guess.

## Left undone
- **Tests not run.** Nothing was executed, and the new tests have never passed.
- **No live proof of isolation.** I haven't checked that the sandbox has no outbound network or can't reach credentials. That needs a probe against the real sandbox, and I didn't create any cloud resources.
- **Real SDK not exercised.** The real ADK executor and `File` encoding path were never run. The Runner-level test that the executor receives the staged file name needs the SDK installed.
- **Sandbox grants not set up.** I didn't create the sandbox or grant the service account permissions to use it.
- **Further hardening not done:**
  - `download_upload` still lets any signed-in underwriter fetch any upload, because there is no per-user check.
  - There is no VPC egress control on Cloud Run.
  - `email_report` still gives the agent all three legs of the lethal trifecta (private data, untrusted content, outbound send). The domain allowlist and confirmation reduce that risk but don't remove it.