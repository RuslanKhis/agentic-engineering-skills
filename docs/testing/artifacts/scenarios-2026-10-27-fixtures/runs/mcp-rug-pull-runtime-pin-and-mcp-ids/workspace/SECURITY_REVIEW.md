# Security review: filings research agent (MCP surface)

Scope: `app/agent.py`, `app/inventory.py`, `scripts/check_mcp_inventory.py`, `mcp/ledgerline.tools.json`,
`.github/workflows/ci.yml`, `Dockerfile`, `pyproject.toml`, `tests/`. Pin: `google-adk==2.12.0`, `mcp==1.18.0`.
Findings use OWASP MCP Top 10 ids (MCP01:2025 to MCP10:2025, beta). Ids come from the adk-agent-security
skill's finding-to-id table and were **not** checked against the owasp.org entries (no network); confirm each
before quoting it to Security. No OWASP text is copied.

Evidence: everything below is `offline (source read)` of this repository. Nothing was executed:
the session had no shell, google-adk and mcp are not installed, and there is no network. The skill's
inspector (`inspect_security_surface.py`) and the unit tests were **not run** (`not run`). Statements about
ADK internals are taken from the skill's notes (2.12.0 source read 2026-10-24 by the skill's author) and
were not re-read here.

## Answer to Security: what if Ledgerline quietly changes a tool description after deploy?

Today, nothing stops it and nothing tells you promptly.

1. The agent lists tools from the live server and filters **by name only** (`app/agent.py:15`). A changed
   `description` or `inputSchema` on `search_filings` or `get_filing` passes the filter.
2. The new text reaches the model as part of the tool declaration. ADK 2.10.0+ wraps descriptions in
   untrusted-content markers (CHANGELOG, so it applies to the 2.12.0 pin; not re-verified). That marks the
   text as data. It does not stop a model being steered by it.
3. The only check is `scripts/check_mcp_inventory.py`, which runs on pull requests and on the Monday 05:00
   cron (`ci.yml:3-5`). The exposure window is up to a week plus however long until someone reads a red cron
   run. The job only reports; no step blocks a running deployment (no deploy workflow is in the repo).
4. `tool_list_cache_ttl_seconds=None` (`agent.py:16`) is not a pin. Whatever its exact semantics on 2.12.0
   (unverified), the definition the model sees is whatever the server returned at some point after deploy,
   never the reviewed one.
5. The CI check cannot prove what production sees. It is a different client at a different time; a server
   can serve different definitions to it. Only a check on the definitions the running agent receives
   proves anything.

What an attacker could achieve with a poisoned description: instruct the model to put conversation text or
extracted PDF content into the `query` / `filing_id` arguments (which Ledgerline receives by design), or to
call the unfiltered local PDF tools with chosen arguments. See F1, F2, F6.

## Findings (prioritised)

| # | Sev | MCP id | Finding | Where | Observable check that shows the fix | Owner skill |
|---|-----|--------|---------|-------|-------------------------------------|-------------|
| F1 | High | MCP03 | No run-time pin. Allowlist is names only; changed definitions are served to the model until the next CI run. | `app/agent.py:15`, `ci.yml:3-5` | Scripted test: a fake tool whose description differs from the manifest is withheld by the filter and a mismatch is logged; a matching one is admitted. | adk-agent-security (tool-supply-chain item 3) |
| F2 | High | MCP02, MCP05 (confirm) | Local PDF MCP server runs as a stdio child of the agent process in the same Cloud Run container, so it holds the container's identity and network reach (plausibly the metadata server; inference, not tested). It has **no `tool_filter`**, no prefix, no recorded definitions. It handles analyst-attached, untrusted PDFs. | `app/agent.py:19-23`, `Dockerfile:6` | Inspector shows no `mcp_unfiltered` or `mcp_stdio_transport` for it; or it is a separate Cloud Run service with its own minimal service account behind Streamable HTTP. | adk-agent-interoperability / deploy-adk-on-google-cloud |
| F3 | Medium | MCP03, MCP04 | The PDF server's behaviour and tool definitions change with any version bump of `pdf-extract-mcp`; `==0.9.2` pins the version but not file hashes or transitive deps, and its definitions are not in any manifest. | `pyproject.toml:9`, `Dockerfile:5` | Lock file with hashes (`pip install --require-hashes`), plus a committed manifest of the PDF tools checked by the same predicate. | adk-agent-security |
| F4 | Medium | MCP03 | The CI check is weaker than it looks: point-in-time, alert-only, only name/description/inputSchema hashed (`outputSchema`, `annotations` not covered), and the listing is pre-filtered to the two allowed names so added tools are invisible to it. Its hash format is also not the interoperability skill's manifest format, so there is no parity test. | `scripts/check_mcp_inventory.py:29`, `app/inventory.py:9` | Keep CI as a second line, but fail the build/block deploy on diff; add parity test against `mcp_tool_inventory.py` output. | adk-agent-interoperability |
| F5 | Medium | MCP01, MCP07 | One static bearer token from the environment, read at import time, is shared by every analyst. Server sees a single principal; rotation needs a restart. `header_provider` is not used. Also the same token is used in CI on `pull_request`, where a PR can change the script that reads it. | `app/agent.py:13`, `ci.yml:26` | Token from Secret Manager; per-user or at least per-environment credential; CI token scoped read-only to `tools/list`. | adk-tool-auth-and-secrets |
| F6 | Medium | MCP06, MCP10 | Trifecta shape: untrusted content (filing text from a third party, attacker-controlled PDFs), private data (analyst conversation and attachments), and egress (model-chosen `query` sent to an external operator). No `before_tool_callback`, no taint labelling. Both tools look read-only, which limits impact. | `app/agent.py:25-31` | Adversarial case: poisoned filing text asks to send PDF contents via `search_filings`; scripted-model test asserts the call is refused or arguments are not tainted. | adk-agent-security (injection-patterns, adversarial-testing) |
| F7 | Low | MCP08 | No record of which tools were listed, admitted or withheld, or tool calls made. | `app/agent.py` (no callbacks/plugins) | A log line per withheld tool and per call, visible in Cloud Logging in a test run. | adk-agent-security |
| F8 | Low | MCP04 | Build and CI supply chain: base image and `actions/*@v4` are tag-pinned, not by digest/SHA; container runs as root (no `USER`); `pip install .` without hashes. | `Dockerfile:1,5`, `ci.yml:10-14` | Digest/SHA pins; non-root user. | deploy-adk-on-google-cloud |
| F9 | Info | MCP09 | Ledgerline is documented in the README, so it is registered informally. No owner, contract term or change-notification channel is recorded for the server. | `README.md:6-7` | A line naming the owner and whether Ledgerline gives notice of tool changes. | (owner decision) |

Other observations: `Dockerfile:8` runs `app.server:app`, but `app/server.py` is not in the repo, so the
serving surface (auth, `--no-allow-unauthenticated`, user identity) was not reviewed. The `mcp/` manifest is
not copied into the image (`Dockerfile:3-4`), which a run-time pin needs.

## Recommended fix for F1 (not applied; this review changed no code)

Make `tool_filter` a predicate that admits a tool only if its name is allowlisted **and** its live
definition hashes to the committed manifest entry. Fail closed per tool, log the mismatch, and treat
re-approval as a manifest change reviewed in a PR. Sketch, untested:

```python
import logging
from app.inventory import tool_hash

log = logging.getLogger(__name__)

def pinned_filter(manifest: dict, allow: set[str]):
    want = {t["name"]: t["sha256"] for t in manifest["tools"]}

    def predicate(tool, readonly_context=None) -> bool:
        if tool.name not in allow:
            return False
        live = tool.raw_mcp_tool.model_dump(by_alias=True, mode="json", exclude_none=True)
        if want.get(tool.name) != tool_hash(live):
            log.error("mcp definition changed, tool withheld: %s", tool.name)
            return False
        return True

    return predicate
```

Needs: (a) `COPY mcp ./mcp` in the Dockerfile; (b) `tool_filter=pinned_filter(...)` in `app/agent.py`;
(c) a unit test with fake tool objects (match, changed description, changed schema, unlisted name);
(d) a parity test that `tool_hash` equals the interoperability skill's hash on the same definition;
(e) an alert on the withheld log line, since failing closed removes search for analysts until re-approved.
Residual risk: a matching hash proves the definition, not what the server does with the arguments.

## Questions nobody could answer in this session, and the assumption used

1. Does anything deploy automatically from main, or gate on the `mcp-inventory` job? Assumed no and no.
2. What does `tool_list_cache_ttl_seconds=None` do on 2.12.0 (cache forever or never cache)? Unverified;
   the findings hold either way.
3. Does `pdf-extract-mcp` read paths or fetch URLs from model arguments, and which tools does it expose?
   Unknown; assumed it reads files and handles untrusted input. F2's MCP05 id depends on this.
4. Where does `app/server.py` live, and is the service authenticated? Assumed it exists elsewhere.
5. Is `LEDGERLINE_TOKEN` a Secret Manager reference or a plain env var, and is it per user? Assumed one shared secret.
6. Does Ledgerline commit to notice before changing tools? Assumed no.

## Left undone

Inspector and unit tests not run; no code changed; OWASP ids not confirmed against the source entries;
no scripted-model or adversarial tests written; the serving layer was not reviewed.
