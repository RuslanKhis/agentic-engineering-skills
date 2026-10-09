I used **`adk-tool-auth-and-secrets`** as the specialist. T-202 is about customers giving the agent access to their own Gmail and being able to take it back, and this skill covers exactly that: consent, keeping each customer's credential separate, refresh and disconnect. The ticket didn't name a specialist, so I picked it from the routing table.

The code for connecting, reading and disconnecting is written and passes its offline tests. It can't go to the 30 pilot customers yet: there is nowhere permanent to store connections, and the web pages and Google setup customers need to connect don't exist.

**What I built**
- **`support_agent/gmail_oauth.py`:** the connect, refresh and disconnect logic.
  - Connecting uses a one-time, 10-minute link tied to the customer and their browser. Every rejected attempt is stopped before anything is sent to Google.
  - Gmail access is read-only, and a connection is refused if the customer unticks the Gmail permission.
  - Each customer's long-lived token sits in a separate store; the connection record holds only a reference to it.
  - Disconnecting blocks access immediately, even if Google's revoke call fails; the failure is recorded for later cleanup.
- **`support_agent/gmail_tool.py`:** a tool, `read_order_confirmations(order_id, tool_context)`.
  - Whose mailbox it reads comes from the session's user ID, never from anything the model passes in.
  - It searches only the configured ACME confirmation senders for that one order ID, and returns at most 3 emails of 2,000 characters each.
- **`support_agent/gmail_http.py`:** the calls to Google and Gmail. Error messages never include response contents.
- **`support_agent/agent.py`:** the tool is added to the root agent with one new instruction sentence.
- **`support_agent/__init__.py`:** now loads the agent only on demand, so tests run without ADK. `from support_agent import root_agent` still works in theory, but I haven't checked it against ADK's own loader.

**Checks**
- **Python 3.11:** 22 new tests ran with no failures, but 3 of them were skipped because `httpx` isn't installed for 3.11.
- **Python 3.9:** all 23 tests pass, including the existing one. This is extra evidence only, since the project requires 3.11.
- **Not run:**
  - anything that imports `google.adk`, so I haven't confirmed ADK fills in `tool_context` or exposes the session's user ID in version 2.8.0;
  - any real Google sign-in or Gmail call;
  - restarts or multiple running instances.

**Blocking the pilot** (recorded in the ticket's Evidence section):
1. **No permanent storage:** connections and tokens are only held in memory, so a restart loses them and separate instances don't share them.
2. **No web pages or start-up wiring:** the connect, callback and disconnect routes don't exist, nor does the start-up wiring that loads the OAuth client secret.
3. **No customer sign-in:** there is no verified customer identity anywhere in this repo, and the README calls this an internal tool.
4. **Google's rules for Gmail access:** reading Gmail needs Google's approval. Without it, at most 100 test users can connect and must reconnect every 7 days, which matters for a three-week pilot.
5. **Security review (T-104):** customers' email text now reaches an agent that can also send mail and hand off to refunds.

The 9 questions I would have asked you, with my assumed answers, are in `REPORT.md` along with the friction log. The skills didn't give a ready-made next prompt to quote; they said to write one. I chose T-104 over T-101 because this change makes the security review more urgent:

> Please take ticket tickets/T-104.md and carry it out, treating the new Gmail tool from T-202 (support_agent/gmail_tool.py: customer email text reaching support_root, which also holds send_email and transfers to refunds_agent) as in scope.