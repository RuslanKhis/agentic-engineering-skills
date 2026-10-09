# REPORT — T-202 Customers connect their own Gmail

Specialist: **`adk-tool-auth-and-secrets`**, because the ticket is delegated end-user
OAuth (consent, per-customer token ownership, disconnect). The ticket named no
`Primary skill`, so I chose it from the routing table. Concerns noted but not loaded:
`adk-agent-security` (T-104: untrusted email text reaches an agent that can send mail)
and `protect-adk-sensitive-data` (email bodies are personal data).

## 1. Skills invoked and reference files opened, in order

1. `adk-engineer` (invoked by the user via `/adk-engineer`): `.claude/skills/adk-engineer/SKILL.md`
2. `.claude/skills/adk-tool-auth-and-secrets/SKILL.md`
3. `.claude/skills/adk-tool-auth-and-secrets/references/oauth-lifecycle.md`
4. `.claude/skills/adk-tool-auth-and-secrets/references/identity-and-output.md`
5. `.claude/skills/adk-tool-auth-and-secrets/references/validation.md`
6. `.claude/skills/adk-tool-auth-and-secrets/references/compatibility-and-evidence.md`
7. `.claude/skills/adk-tool-auth-and-secrets/references/adk-continuations.md`
8. `.claude/skills/adk-tool-auth-and-secrets/references/gcp-credentials.md`: headings plus the "Inspect" and "Implement custody" sections only
9. Ran `.claude/skills/adk-tool-auth-and-secrets/scripts/inspect_project.py`

Not opened: `operations-runbook.md`, `skill-validation.md`, `assets/public_text.py`. No
cloud work was in scope, and the change does not alter the public response contract.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
|---|---|---|
| 1 | The README calls this an *internal* support tool. Do pilot customers chat with the agent directly, and what verified identity becomes the ADK session `user_id`? | Customers use an authenticated customer portal, and its gateway sets `user_id` to the verified customer ID. The tool trusts only `tool_context.session.user_id`. |
| 2 | Does a web layer exist (portal or gateway) where the connect, callback and disconnect routes belong? | Not in this repo. I wrote framework-neutral service methods and listed the routes as unfinished. |
| 3 | Which Gmail scope is acceptable? Has the company started Google OAuth verification for a restricted scope? | `gmail.readonly` plus `openid`, the minimum that can read message bodies. Verification has not started, so the pilot runs in Testing mode: up to 100 test users, and refresh tokens expire every 7 days. Flagged as a pilot risk. |
| 4 | Which sender addresses send ACME order confirmations? | They are configurable through `gmail_tool.configure(..., confirmation_senders=...)`. The tool searches only those senders plus the order ID. |
| 5 | Where should connection metadata and refresh tokens live (Firestore, Cloud SQL, Secret Manager per customer)? | Storage sits behind interfaces (`ConnectionIndex`, `ConsentStore`, `TokenVault`). Only in-memory implementations exist. I recommend Firestore plus Secret Manager, but did not build them. |
| 6 | Should the agent read mail only when the customer asks about an order, or also proactively? | Only on request, for one order ID, at most 3 emails of 2,000 characters each. |
| 7 | Can one customer connect several Gmail accounts? | No. One connection per customer, and reconnecting replaces it (the old token is revoked and destroyed). |
| 8 | Must T-104 (security review) finish before the pilot? | Recommended, not assumed done. The ticket records it as a pilot prerequisite. |
| 9 | Is it acceptable to make `support_agent/__init__.py` lazy? | Yes. `from support_agent import root_agent` still works via `__getattr__`. I did not run the ADK loader to confirm it. |

## 3. Files written or changed; what is not finished

Written or changed:
- `support_agent/gmail_oauth.py` (new): connection service, records, provider/store interfaces, in-memory stores.
- `support_agent/gmail_tool.py` (new): the `read_order_confirmations` tool and the Gmail client interface.
- `support_agent/gmail_http.py` (new): httpx adapters for the Google token, revoke and userinfo endpoints and the Gmail API.
- `support_agent/agent.py`: imports `gmail_tool`, adds the tool to `support_root`, and adds one instruction sentence.
- `support_agent/__init__.py`: lazy `root_agent`, so ADK-free tests can import the package.
- `tests/test_gmail_connection.py` (new, 19 tests) and `tests/test_gmail_http.py` (new, 3 tests that skip without httpx).
- `tickets/T-202.md`: status line and an Evidence section.
- `.gitignore` (new): `.adk-evidence/` and `__pycache__/`.
- `.adk-evidence/inspect_project.json`: the inspector's output.

Not finished (the ticket's Evidence lists these as pilot prerequisites):
- Persistent index, consent store and token vault (Firestore and Secret Manager adapters).
- HTTP routes for connect (with CSRF protection), callback (binding cookie, and query strings kept out of logs) and disconnect, plus `configure()` at start-up with the client secret loaded from Secret Manager.
- The Google OAuth client and consent screen, and verification for the restricted scope.
- A verified customer identity in the session.
- The T-104 security review: untrusted email content now reaches the root agent, which holds `send_email` and can hand off to refunds.
- Left out on purpose at pilot depth: a reconciliation worker for `pending_cleanup`, cross-replica cache invalidation, pagination, sensitive-data screening of email text, and secret-access audit logs.

## 4. Checks run and not run

Run:
- `python3.11 -m unittest tests.test_gmail_connection tests.test_gmail_http`: **22 ran, OK, 3 skipped** (httpx is not installed for 3.11).
- `python3 -m pytest -q -p no:cacheprovider tests` on **Python 3.9.13**, which has httpx and pytest 7.1.2: **23 passed**. That includes the existing `test_tools.py` and the httpx adapter tests. This is supplementary only, because the project needs Python 3.11 or later.
- `python3.11 -m py_compile support_agent/*.py`: OK. This compiles `agent.py` but does not import it.
- `python3.11 .claude/skills/adk-tool-auth-and-secrets/scripts/inspect_project.py . --expect-adk 2.8.0`: exit 0, `static_pins_match`, no observations, `security_verdict: not_assessed`.

Not run:
- Anything that imports `google.adk`: building the agent, ADK injecting `tool_context` and keeping it out of the tool declaration, whether `ToolContext.session.user_id` exists on 2.8.0, and Runner orchestration with a substituted model.
- `test_tools.py` under Python 3.11, because httpx is missing there.
- Real Google consent, token exchange, refresh, revoke, userinfo and Gmail calls.
- Restart with persistent stores, and behaviour across replicas.
- Exporter and log canary checks.
- The project's CI workflow.

## 5. Friction log

- **Unclear: what is the "next ready" ticket?** `.claude/skills/adk-engineer/SKILL.md:36-44` says to end with the run prompt for "the next ready goal or ticket". Only T-202 has `status: ready`. T-101 to T-105 have no status or prerequisites, so "ready" can't be decided. I chose T-104 because this change makes it more urgent.
- **Unclear: a ticket with no `Primary skill`, design or acceptance cases.** `adk-engineer/SKILL.md:33-38` assumes linked design, plan and acceptance cases. T-202 has four sentences, so I invented the acceptance cases (the tests) myself. The routing table at `adk-engineer/SKILL.md:56-78` made the specialist choice quick.
- **Unclear: the identity source.** `references/identity-and-output.md:7-11` requires a verified principal, but the repo has no gateway, and the README says the tool is internal. The skill correctly says to record this rather than invent it (`adk-tool-auth-and-secrets/SKILL.md:23`). I recorded it.
- **Unclear: does making `__init__.py` lazy break `adk web`/`api_server` loading?** `adk-engineer/SKILL.md:137-140` tells you to keep `google.adk` out of `__init__.py`. It doesn't mention that the existing package eagerly imports `agent`, or how to change that safely. I used a module `__getattr__`, which is unverified with the 2.8.0 loader.
- **Heavier than needed at pilot depth:** `references/oauth-lifecycle.md:35-51` (refresh races, losing-version reconciliation, replica invalidation, a long list of edge-case tests) is written for production. `adk-engineer/SKILL.md:118-128` gives permission to cut, but I still had to pick which invariants to keep myself. A short "pilot floor for delegated OAuth" list in the specialist would have saved time.
- **Heavier than needed:** `references/validation.md:43-47` (Calendar semantics) and `compatibility-and-evidence.md` provenance tables don't apply to a Gmail feature, but they're interleaved with guidance that does.
- **Missing:** nothing in the skills mentions that Google's *restricted* scopes (Gmail) need verification and a security assessment, or that Testing-mode refresh tokens expire after 7 days. Both are central to a three-week, 30-customer pilot. `references/oauth-lifecycle.md:21` only links Google's generic web-server flow.
- **Genuinely helpful:**
  - `references/oauth-lifecycle.md:15-19`: browser binding, single-use state and the "copied URL in another browser" case.
  - `references/oauth-lifecycle.md:29`: an omitted refresh token is reused only for the same account and client.
  - `references/oauth-lifecycle.md:41`: a resource 401 is not grounds to erase consent.
  - `references/oauth-lifecycle.md:45-47`: disconnect locally first.
  - `references/identity-and-output.md:13`: model-visible declarations must not choose identity.
  - The inspector ran cleanly and stated its limits. Each of the five rules above became a test.
- **Helpful:** `adk-engineer/SKILL.md:105-108` (`.adk-evidence/` and the Python 3.11 helper rule) was clear, and resolved the system 3.9 vs 3.11 question at once.

## 6. Next prompt

No prompt was given verbatim. `adk-engineer/SKILL.md:40-44` tells the agent to *compose* a final run prompt ("end with the run prompt for the next ready goal or ticket … written so the user can paste it"). The one I composed:

> Please take ticket tickets/T-104.md and carry it out, treating the new Gmail tool from T-202 (support_agent/gmail_tool.py: customer email text reaching support_root, which also holds send_email and transfers to refunds_agent) as in scope.
