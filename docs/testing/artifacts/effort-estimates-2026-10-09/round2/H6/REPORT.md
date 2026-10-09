# REPORT: T-202, customers connect their own Gmail

**Specialist: `adk-tool-auth-and-secrets`.** The ticket is about end-user delegated OAuth: each customer
connects only their own mailbox and can disconnect it. That is the "Tool identity, credentials, Secret Manager or delegated OAuth"
row (`.claude/skills/adk-engineer/SKILL.md:76`), and the specialist's description names consent, refresh and disconnect flows and
cross-user access bugs. The ticket names no `Primary skill`. Supporting skill (scoped, not loaded in full): `adk-agent-security`,
because the agent now reads untrusted email *and* can send email and hand off refunds (`adk-engineer/SKILL.md:71`).

## 1. Skills invoked and reference files opened, in order

1. `adk-engineer` (`/adk-engineer` command): `.claude/skills/adk-engineer/SKILL.md` (provided in full by the command)
2. `.claude/skills/adk-tool-auth-and-secrets/SKILL.md`
3. `.claude/skills/adk-tool-auth-and-secrets/references/oauth-lifecycle.md`
4. `.claude/skills/adk-tool-auth-and-secrets/references/compatibility-and-evidence.md`
5. `.claude/skills/adk-tool-auth-and-secrets/references/identity-and-output.md`
6. `.claude/skills/adk-tool-auth-and-secrets/references/validation.md`
7. `.claude/skills/adk-tool-auth-and-secrets/references/adk-continuations.md` (first 40 lines, the whole file)
8. Helper run: `.claude/skills/adk-tool-auth-and-secrets/scripts/inspect_project.py . --expect-adk 2.8.0`
9. Grep only, to choose the supporting skill and get line pointers: `.claude/skills/adk-agent-security/SKILL.md` (description and lines 51 and 68)

Not opened: `adk-engineer/references/composition.md` (no `agents-cli-manifest.yaml`), `gcp-credentials.md`,
`operations-runbook.md` (no cloud work allowed), `skill-validation.md`, `assets/public_text.py` (response projection is not part of this change).

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
|---|---|---|
| 1 | How do customers sign in to the support app, and what is the verified principal? Nothing in the repo shows a customer-facing gateway (the README says "internal assistant"). | A gateway outside this repo verifies the customer and creates ADK sessions with `user_id` set to that verified principal. The tool trusts `tool_context.session.user_id` only. Building the gateway is T-203. |
| 2 | The estimate is 1-2 h, but the acceptance needs a gateway, durable stores and Google's restricted-scope process. Should I expand the scope or slice it? | Slice it, as `adk-engineer/SKILL.md:130-135` instructs: the broker, tool, wiring and offline tests. The remainder is tickets/T-203.md (6-10 h plus calendar time). |
| 3 | What should the agent see from an email: the full body, or extracted fields only? | Extracted fields only: sender, date, subject (capped at 150 characters) and order IDs regex-extracted in code. This is enough to answer "about an order" via `get_order`, and it keeps untrusted bodies away from an agent that has `send_email`. |
| 4 | Gmail scope? | `gmail.readonly` only. `gmail.metadata` cannot read bodies or use `q` search, so it cannot find order IDs. This is a Google *restricted* scope. |
| 5 | Pilot in 3 weeks: Testing mode or verification? | Testing mode with the 30 customers added as test users for the pilot. In parallel, a person decides whether to start verification. From my own knowledge, not from the skills, and not checked online: Testing-mode refresh tokens expire after 7 days, and restricted scopes need a security assessment. Recorded as an unverified constraint in T-203. |
| 6 | Where do refresh tokens and connection records live? | Behind `TokenStore`, connection-index and transaction-store interfaces with in-memory implementations for now. The production store (Firestore plus Secret Manager or KMS) is T-203. |
| 7 | Which agent gets the tool? | `root_agent` only, which is where customers ask about orders. Not refunds or billing. |
| 8 | Can `support_agent/__init__.py` change? The eager `from .agent import root_agent` made every test, including the existing one, fail without google-adk. | Yes. It now uses a PEP 562 lazy `__getattr__`, so `from support_agent import root_agent` and attribute access still work. Not verified with `adk web` or Cloud Run. |
| 9 | Should an unconnected customer get a consent link in chat? | No. The tool returns `authorization_required` and the agent points the customer to their account page. Consent starts only from an authenticated app action (application-broker contract, `adk-continuations.md:7`). |

## 3. Files written or changed; what is not finished

Written or changed:
- `support_agent/gmail_connect.py` (new): consent transactions (single use, PKCE S256, browser binding, principal/client/redirect checks,
  granted-scope check, offline access); a connection index with revision compare-and-set; coordinated refresh (transient error keeps consent,
  `invalid_grant` affects only the failing revision, a stale refresh cannot reactivate, rotating refresh retires the old token); local-first
  disconnect, then revoke, with failures queued; an httpx `GoogleOAuthProvider` (not run live); `configure()`/`get_connections()`.
- `support_agent/gmail_tools.py` (new): the `find_order_confirmations(order_id="", tool_context=None)` tool.
- `support_agent/agent.py`: tool added to `root_agent.tools`, plus one instruction sentence about `authorization_required`.
- `support_agent/__init__.py`: lazy `root_agent`.
- `tests/test_gmail_connect.py`, `tests/test_gmail_tools.py` (new, unittest-style so they run without pytest).
- `tickets/T-202.md`: status and an Evidence section. `tickets/T-203.md`: new follow-up ticket.
- `.gitignore` (new): `.adk-evidence/`. `.adk-evidence/`: inspector and test output.

Not finished (all in T-202 Evidence and T-203):
- No gateway, sign-in or connect/callback/disconnect HTTP routes; no cookie or CSRF handling; callback URLs not scrubbed from access logs.
- Stores are in memory only, so they break with more than one Cloud Run instance or after a restart. No Secret Manager wiring for the client secret, and no revocation-reconciliation worker.
- No real ADK Runner test; no live Google consent/refresh/revoke or Gmail check.
- No per-customer Gmail call budget.
- Security: `root_agent` now combines private mailbox data, attacker-controlled subjects and `send_email`. This is narrowed but not removed, and is a T-104 blocker before external customers.
- Google Cloud Console steps (OAuth client, consent screen, test users) are person-only.

## 4. Checks run and not run

Run:
- `python3.11 -m unittest tests.test_gmail_connect tests.test_gmail_tools -v`: **26 passed, 1 skipped**, offline with fake Google
  provider and HTTP transport (`.adk-evidence/unittest_py311.txt`). The first run failed one test: the subject word "confirmation" was being extracted as an
  order ID. Fixed by requiring a digit in an order ID; the rerun is green.
- `python3 (3.9) -m pytest -q tests/test_tools.py`: **1 passed**. Run the same way before my change, it **failed at collection**
  (google-adk missing via the eager `__init__`). Python 3.9 is below the project's `>=3.11`; I used it only because it has pytest and httpx.
- Running the full `pytest tests` on 3.9 fails collecting `test_gmail_tools.py` (`dict | None` needs 3.10+). This is expected on an unsupported interpreter, not a project failure.
- `python3.11 -m py_compile support_agent/*.py tests/*.py`: OK.
- Inspector `--expect-adk 2.8.0`: exit 0, `complete: true`, `static_pins_match`, no observations (`.adk-evidence/inspect_project.txt`). This is not a security verdict.

Not run:
- `AdkDeclarationTest` (checks the model-visible schema is only `order_id`; skipped because google-adk is not installed).
- Real ADK Runner orchestration with a model double. Also unverified: that ADK 2.8.0 hides a `tool_context` parameter with a `None` default, and the `ToolContext.session.user_id` accessor on 2.8.0.
- Loading `root_agent` through the lazy `__init__` with `adk web`, `adk api_server` or Cloud Run.
- Any live Google OAuth, Gmail API or revoke call; restart and multi-replica cases; the existing CI (`pip install -e . pytest && pytest`).

## 5. Friction log

- **Helpful:** `adk-engineer/SKILL.md:130-135`. The estimate rule names "a calendar wait such as provider verification", and it is exactly what
  turned a 1-2 h ticket into a slice plus T-203. Without it I would have quietly overrun.
- **Helpful:** `adk-engineer/SKILL.md:145-151`. "Keep `google.adk` imports out of package `__init__.py` files" pointed directly at the
  existing defect that blocked even the current test.
- **Helpful:** `adk-tool-auth-and-secrets/references/oauth-lifecycle.md:51`. The concrete case list became the test list almost one-to-one.
- **Helpful:** `oauth-lifecycle.md:41`. Resource 401 versus token-endpoint `invalid_grant` shaped the tool's retry and keep-consent behaviour.
- **Unsure:** the ticket has no `Primary skill`, and three table rows plausibly fit: `adk-engineer/SKILL.md:71` (security), `:75` (personal data)
  and `:76` (OAuth). I resolved it by "connects/disconnects" → `:76`. A tie-break hint for "OAuth to a personal-data provider" would help.
- **Unsure / gap:** nothing in `adk-tool-auth-and-secrets` mentions Google's restricted-scope verification or Testing-mode limits. All examples are
  Calendar (`validation.md:22`, `validation.md:43-47`, `oauth-lifecycle.md:41`). The Gmail constraints in this report come from my own knowledge
  and are unverified here.
- **Unsure:** `adk-tool-auth-and-secrets/SKILL.md:41` says to implement the full browser and lifecycle requirements for real delegated OAuth. That conflicts
  in size with a 1-2 h ticket at pilot depth (`adk-engineer/SKILL.md:120-128`), and it was unclear which governs. I took the engineer's profile rule
  and listed the omitted controls.
- **Unsure:** the contract for testing the tool function with a plain object carrying `session.user_id`. `adk-engineer/SKILL.md:150` forbids "hand-built
  stand-ins" for the SDK. I treated a direct function call as a tool-function test (allowed at `:146`) and labelled ADK dispatch as not run.
  The line between the two could be stated.
- **Heavier than needed:** `compatibility-and-evidence.md` (41 lines) is mostly book-campaign provenance. Only lines 5-9 (version contract) mattered here.
- **Heavier than needed:** `validation.md:49-72` (validating the skill package itself) sits in the same file as project validation, so I had to read past it.
- **Minor:** `adk-engineer/SKILL.md:107` says helpers need Python 3.11+. The default `python3` was 3.9, and an `-I` unittest-discover run failed
  because `tests/` is not a package. Running module names directly worked.
- **Minor:** `adk-engineer/SKILL.md:40-45` says to end with "the run prompt for the next ready goal or ticket". T-101 to T-105 have no status or
  prerequisite fields, so "next ready" could not be determined. I used the follow-up rule instead.

## 6. Next prompt

None given verbatim by the skills. `adk-engineer/SKILL.md:40-45` tells the agent to compose one; the one I composed is:

> /adk-engineer Please take ticket tickets/T-203.md and carry it out. Customers sign in with <your identity provider>; use <Firestore / Cloud SQL> for the connection index and Secret Manager for refresh tokens; the pilot uses OAuth Testing mode with the 30 customers as test users. Also run the T-202 tests marked not run (tests/test_gmail_tools.py::AdkDeclarationTest and full pytest) with google-adk 2.8.0 on Python 3.11.
