# REPORT — T-202 Customers connect their own Gmail

**Specialist: `adk-tool-auth-and-secrets`**. T-202 is per-customer delegated
OAuth: consent, reading only the customer's own mailbox, and disconnect. That
is this skill's "End-user delegation … disconnect" branch. The ticket names no
primary skill. Supporting concern noted but not loaded: `adk-agent-security`
for the risk of reading untrusted email (deferred to T-104).

## 1. Skills invoked and reference files opened, in order

1. `adk-engineer` (invoked as `/adk-engineer`) — `.claude/skills/adk-engineer/SKILL.md`
2. `.claude/skills/adk-tool-auth-and-secrets/SKILL.md` (read directly; Skill tool not re-invoked)
3. `.claude/skills/adk-tool-auth-and-secrets/references/oauth-lifecycle.md`
4. `.claude/skills/adk-tool-auth-and-secrets/references/compatibility-and-evidence.md`
5. `.claude/skills/adk-tool-auth-and-secrets/references/validation.md`
6. `.claude/skills/adk-tool-auth-and-secrets/references/identity-and-output.md`
7. `.claude/skills/adk-system-designer/references/delivery-profiles.md` lines 105–140 only
   (found by grep for "Gmail", to size the estimate)
8. Ran `.claude/skills/adk-tool-auth-and-secrets/scripts/inspect_project.py . --expect-adk 2.8.0`
   with python3.11. Output is in `.adk-evidence/inspect_project.txt`.

Not opened: `adk-continuations.md`, `gcp-credentials.md`, `operations-runbook.md`,
`skill-validation.md`, `adk-engineer/references/composition.md` (no
`agents-cli-manifest.yaml` in the project).

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
|---|---|---|
| 1 | The ticket estimates 1–2 h, but real delegated OAuth plus Google verification of the restricted `gmail.readonly` scope is 8–16 h plus a wait of weeks. Should I expand the scope or split the ticket? | Split it. I built the offline slice under T-202 and wrote T-203 with its own estimate. |
| 2 | How do pilot customers sign in to the support app? Where is the verified principal created? The repo has no gateway. | The hosting gateway authenticates the customer and creates ADK sessions with `user_id` set to the verified principal. The tool reads `tool_context.session.user_id`. |
| 3 | Which sender or subject marks an "order confirmation" email? | `from:orders@acme.example subject:"order confirmation" newer_than:365d`. This is a placeholder constant (`ORDER_CONFIRMATION_QUERY`) to confirm. |
| 4 | Can the pilot run with the OAuth app in Testing mode (≤100 test users, refresh tokens expiring after 7 days) while verification is pending? | Probably yes for 30 customers. This is recorded in T-203 as something to check against current Google docs, because I did no network lookups. |
| 5 | Should the root agent get the tool even though it also has `send_email` to any address (an exfiltration path)? | Yes. The tool is wired in, but it fails closed until a service is configured. External rollout is blocked on T-104. |
| 6 | Where should refresh tokens live: Secret Manager or an encrypted DB column? And the connection index? | Not decided. Both are behind injected interfaces (`CredentialStore`, in-process index); the choice is in T-203. |
| 7 | How much of each email may reach the model? | The fixed query, at most 5 messages, and only the date/from/subject/snippet fields, each cut to 300 characters. Message bodies are never returned. |
| 8 | Is it acceptable to make `support_agent/__init__.py` import `root_agent` lazily? | Yes. The adk-engineer skill asks for this, and `support_agent.root_agent` still resolves through module `__getattr__`. |

## 3. Files written or changed; what is not finished

Written or changed:
- `support_agent/gmail_connections.py` (new). This is the connection index
  and consent transaction (PKCE S256, offline access, single-use 10-minute
  state bound to principal and browser cookie hash). It also covers:
  - scope and client checks, with nothing stored for a partial grant;
  - reuse of the old token when no refresh token comes back, but only for
    the same account and client;
  - revision-checked publish, with the losing credential retired;
  - disconnect: locally first, then revoke, then retire, with the revoke
    failure recorded;
  - `InvalidGrant` vs `ProviderUnavailable` handling;
  - result withheld if the connection changes during a read;
  - bounded, untrusted-marked results.
- `support_agent/tools.py`: added `read_order_confirmations(tool_context)`, which takes no model-supplied identity.
- `support_agent/agent.py`: tool added to `root_agent`, plus one instruction sentence.
- `support_agent/__init__.py`: lazy `root_agent`.
- `tests/test_gmail_connections.py` (new): 13 offline tests plus 1 tool-function test that needs httpx.
- `tickets/T-202.md`: status changed to partial and an Evidence section added.
- `tickets/T-203.md` (new): the remainder, estimated at 8–14 h plus the verification wait.
- `.gitignore` (new): `.adk-evidence/`. Also `.adk-evidence/inspect_project.txt` and `.adk-evidence/t202_unittest.txt`.

Not finished (all in T-203):
- the real Google provider adapter (code exchange, ID-token validation, refresh, revoke);
- the Gmail API reader;
- a Secret Manager credential store;
- a persistent connection index shared across Cloud Run instances;
- an access-token cache;
- gateway connect/callback/disconnect routes with cookie and CSRF protection, and callback query strings kept out of logs;
- reconciliation of `pending_revocations`;
- OAuth client, consent screen and test users or verification (only a person can do these).

The security review of reading mail plus `send_email` is T-104.

## 4. Checks run and checks not run

Run:
- `python3.11 .claude/skills/adk-tool-auth-and-secrets/scripts/inspect_project.py . --expect-adk 2.8.0`:
  exit 0, `static_pins_match`, no observations. This is a static inventory, not a security verdict.
- `python3.11 -m unittest tests.test_gmail_connections -v`: **13 passed, 1 skipped**
  (`ToolFunctionTests` was skipped because httpx is not installed). These are offline,
  with doubles for Google OAuth, the credential store and Gmail only.
- `python3.11 -m py_compile support_agent/*.py`: OK.

Not run:
- `tests/test_tools.py` (existing), because httpx is not installed.
- `ToolFunctionTests`, skipped because httpx is absent.
- Anything that imports `google.adk`: agent construction, tool-declaration
  generation (whether ADK injects `tool_context` and exposes no parameters),
  and Runner dispatch. Whether `ToolContext.session.user_id` works on 2.8.0 is
  **not verified** in this environment.
- Real Google consent, token exchange, refresh, revocation or Gmail calls; restart; multiple replicas.
- `pytest`. It is only installed for Python 3.9 here, below the project's `>=3.11`. The new tests are `unittest`-style, so pytest in CI will collect them.

Human effort still owed for this change: about 1–1.5 h to review
`gmail_connections.py` and the tests, and to run `pytest` with the project's
dependencies installed (check that the tool declaration exposes no
parameters). It is not usable by customers until T-203 and T-104 are done.

## 5. Friction log

- **Helpful:** `.claude/skills/adk-engineer/SKILL.md:130-135`. The estimate rule
  ("If it is clearly larger … say so first … propose the remainder as a new
  ticket") gave a clear course of action when 1–2 h clearly didn't fit.
- **Unsure / had to dig:** the 8–16 h figure and the "Gmail verification takes
  weeks" fact live only in `.claude/skills/adk-system-designer/references/delivery-profiles.md:118-133`.
  That is a skill I wasn't routed to, and I found it by grep. The auth skill
  itself (`adk-tool-auth-and-secrets/SKILL.md`, `references/oauth-lifecycle.md`)
  never mentions sizing or restricted-scope verification.
- **Unsure:** `.claude/skills/adk-engineer/SKILL.md:39-44` says to end with "the
  run prompt for the next ready goal", but gives no template. The other tickets
  (T-101..T-105) have no status field, so "next ready" was ambiguous. I chose
  the T-203 follow-up I created.
- **Heavier than needed for a 1–2 h pilot:** `.claude/skills/adk-tool-auth-and-secrets/references/oauth-lifecycle.md:51-53`
  and `references/validation.md:5-14` list a production test matrix (replicas,
  rotating refresh races, restart with populated stores). I covered the cases
  that fit the slice and named the rest as unverified.
- **Helpful:** `.claude/skills/adk-tool-auth-and-secrets/references/identity-and-output.md:11`
  names `ToolContext.session.user_id` as an acceptable accessor, which saved a
  version-check detour (still unverified here).
- **Helpful:** `.claude/skills/adk-engineer/SKILL.md:144-150` (keep `google.adk`
  out of `__init__`, report SDK tests as not run). This led directly to the lazy
  `__init__` and the stdlib-only module that made the tests runnable.
- **Minor friction:** `.claude/skills/adk-engineer/SKILL.md:106-108` says to use
  any 3.11+ interpreter for helpers. That worked (`python3.11`), but the only
  pytest available was on 3.9, so I switched the tests to `unittest`.
- **Unsure:** `.claude/skills/adk-tool-auth-and-secrets/SKILL.md:41` says "Mock
  success cannot clear it". It was clear what to report, but the line between
  offline doubles (allowed) and imitating the SDK (`adk-engineer/SKILL.md:148-150`)
  needed judgement for the tool-function test. I labelled it a plain function
  call, not ADK evidence.

## 6. Next prompt the skills told the user to type

None given verbatim. `adk-engineer/SKILL.md:39-44` instructs ending with a run
prompt for the next ready ticket but provides no exact text. The prompt I
composed, following that instruction:

> Please take ticket tickets/T-203.md and carry it out with adk-tool-auth-and-secrets. First run the T-202 tests with the project's dependencies installed (`pip install -e . pytest && pytest`) and report the SDK-dependent checks that were marked not run.
