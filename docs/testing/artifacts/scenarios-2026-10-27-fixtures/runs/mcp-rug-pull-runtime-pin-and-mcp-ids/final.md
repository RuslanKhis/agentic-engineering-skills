I've written the review to `SECURITY_REVIEW.md` and changed no code. I couldn't run the skill's inspector or the unit tests because this session has no shell.

**If Ledgerline quietly changes a tool description after deploy:**
- **Allowlist:** it checks names only (`app/agent.py:15`), so the changed text reaches the model.
- **CI check:** it runs only on pull requests and the Monday cron, and it reports rather than blocks. The exposure window is up to about a week.
- **`tool_list_cache_ttl_seconds=None`:** this isn't a pin. I couldn't verify what it does on ADK 2.12.0, but either way the model sees whatever the server returned after deploy.
- **CI client:** CI is a different client at a different time, so it can't prove what production sees.

**Findings (OWASP MCP ids):**
- **F1, High (MCP03):** there's no run-time pin. The fix is a `tool_filter` predicate that admits a tool only if its live definition hashes to the committed manifest. A sketch is in the document and is untested.
- **F2, High (MCP02):** the PDF MCP server runs inside the agent container with no `tool_filter` and no recorded definitions. It also handles untrusted PDFs. Moving it to its own service is the fix.
- **F3–F9, Medium to Info:** these cover:
  - the PDF server's version and dependencies;
  - weaknesses in the CI check;
  - one shared static Ledgerline token;
  - the untrusted-content, private-data and egress mix;
  - missing audit logging;
  - tag-pinned images and actions;
  - no recorded owner for the Ledgerline server.

**Questions I couldn't ask, and what I assumed** (all six are in the document):
- **Deploys:** nothing deploys from `main` or waits on the CI job.
- **PDF server:** it reads files and handles untrusted input.
- **`app/server.py`:** it exists outside this repo.
- **`LEDGERLINE_TOKEN`:** it's one shared secret.
- **Ledgerline notice:** Ledgerline gives no notice before changing tools.
- **TTL semantics:** unknown, so the findings are written to hold either way.

**Left undone:**
- Inspector and tests not run.
- No fix applied and no tests written.
- OWASP ids not checked against owasp.org (no network); confirm before quoting them to Security.
- ADK internals taken from the skill's notes, not re-read.
- Serving layer not reviewed, because `app/server.py` is missing from the repo.