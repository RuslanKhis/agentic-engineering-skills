I added the Snyk Agent Scan to the adoption checklist and to CI, and left the existing steps and jobs unchanged. None of it has been run: the shell was disabled in this session and there's no network. The new unit tests, the CI job and the scanner itself are all untested.

**What changed**
- **`mcp-scan/freightline-shipping.json`** is new. It holds the agent's exact `npx -y @freightline/shipping-mcp@3.4.1` command in the `mcpServers` shape, with no credentials.
- **`tests/test_mcp_scan_config.py`** is new. It reads `app/agent.py` without importing it and checks four things:
  - the scanned command equals the agent's command;
  - the scan config has no `env`;
  - the scanned package matches the version in the recorded manifest;
  - there is exactly one `StdioServerParameters` call.
- **`.github/workflows/ci.yml`** has a new `mcp-scan` job.
  - It runs on its own, in the same Node-capable container as the definition check.
  - It installs `snyk-agent-scan==0.6.9`.
  - It runs `scan --ci --dangerously-run-mcp-servers` on the config. Only this job gets `SNYK_TOKEN`.
  - Exit 0 passes and exit 1 blocks. Any other exit code, or a missing token, is reported as NOT RUN and fails the job, so it can't pass silently.
- **`docs/security/mcp-adoption.md`** gains step 8, the scan. Sign-off is now step 9 and includes the scan result. The new step says:
  - the scan supplements the allow-list and the definition check and doesn't replace them;
  - the command is reviewed before the scanner executes it;
  - the data-handling decision is recorded;
  - CI keys on the exit code and the pinned version, not on output fields;
  - any ignore flag needs Priya's approval.
- **`README.md`** lists the new files.

**Questions I couldn't ask, and what I assumed**
1. **Can Freightline tool names and descriptions go to Snyk's API?** `scan` uploads them, with secrets redacted. I assumed yes, because the definitions are in our repo and the config has no credentials. The doc makes the PR author record that decision. Please confirm with the platform team.
2. **How should the scanner be installed?** The skill's guidance is `uvx snyk-agent-scan@0.6.9`. I used a pinned `pip install` instead, because I couldn't verify a `uv` version to pin offline. Switch to `uvx` if you prefer it.
3. **Do fork PRs matter?** They get no secrets, so the scan job fails there as NOT RUN. I treated that as correct.

**Left undone**
- **Test run:** run `python -m unittest discover -s tests -t .` first.
- **First CI run:** it needs to confirm three things I took from documentation and haven't run. They are the `snyk-agent-scan` command name, that the config path works as a positional argument, and that the server starts and lists tools without `FREIGHTLINE_API_KEY`. The existing definition check already lists tools without the key.
- **Signing and sandboxing:** I didn't add signed-binary verification for the scanner. I also didn't sandbox the stdio server beyond the ephemeral container, and in production it still runs inside the agent's container.