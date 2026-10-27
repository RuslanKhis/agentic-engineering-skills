T-202 is only partly done: I built the part that can be tested offline, but I couldn't run any tests. No shell tool was available this session, so `tests/test_gmail.py` is written but not run.

**Specialist:** `adk-tool-auth-and-secrets`, because this is per-customer delegated OAuth (consent, owner-scoped tokens, disconnect). I got there through the `adk-engineer` router.

**Estimate:** the ticket's 1-2 hours doesn't cover the whole job. The missing pieces are the Google OAuth provider, token storage, HTTP routes with browser binding, and console setup.
- **Verification wait:** `gmail.readonly` is a restricted scope, so Google's verification is a calendar wait. Someone should start it now.
- **Testing status:** in Google's Testing status, refresh tokens expire after 7 days.
- **Next ticket:** I proposed T-203 for the remainder, at roughly 6-10 hours plus the verification wait.

**What I built, with no change to the agent or routes:**
- **Connection flow:** `app/connections.py` handles consent, disconnect and per-user tokens.
  - **Consent:** the transaction is single-use, short-lived, and bound to the signed-in user and browser. It accepts only the read-only scope.
  - **Disconnect:** it removes local access first, then revokes with Google and retires the stored token. A failed revoke is reported as `revocation_pending`.
- **Storage:** two new tables in `app/store.py` hold connection metadata and a secret reference only, never a token.
- **Gmail tool:** `app/clients/gmail.py` is a GET-only client, and `app/tools/gmail.py` adds `find_order_email`. It reads the user from `tool_context.user_id` and returns only from, subject, date and a snippet.

**Left undone:**
- **Agent wiring:** `find_order_email` is not in the agent's tool list, and there are no HTTP routes or prompt changes.
- **Google and Secret Manager:** there is no real Google OAuth client or Secret Manager store, only interfaces and fakes.
- **Console setup:** the consent screen, web client, redirect URI, test users and scope verification are for a person to do.
- **Refresh handling:** a withdrawn grant makes the tool ask the customer to reconnect, but nothing marks the stale connection yet.
- **Live runs:** nothing was exercised against Google, and nothing needing the ADK SDK was run, since it isn't installed.

**Questions I couldn't ask, and what I assumed:**
- **Testing-status consent:** I assumed it's acceptable for the pilot, with the 30 customers added as test users and reconnecting weekly. Jon decides on verification.
- **Token storage:** I assumed one Secret Manager secret per customer. None was created.
- **Gmail account ownership:** I assumed a customer may connect any Gmail account they can consent to, and the connected account is shown back to them.

The ticket's Evidence section records all of this. It lists about 1 hour of human effort still owed to run the tests and review the code, plus the console steps. Status is `in_progress`.

**Next step:** run `python -m unittest discover -s tests -t .`, then ask me to run T-203.