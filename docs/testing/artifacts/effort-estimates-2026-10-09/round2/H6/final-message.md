I built the code side of T-202 and tested it offline, but customers can't connect Gmail yet. The ticket needs much more than its 1–2 h estimate. I built the largest useful piece and wrote the rest up as a new ticket, `tickets/T-203.md`.

**Specialist: `adk-tool-auth-and-secrets`**, because the ticket is about customers giving the agent access to their own Gmail, with connect, disconnect and "only their own mailbox". That is the skill's core subject. I also used `adk-agent-security`: the agent now reads untrusted email and can also send email and hand off refunds.

**Why the estimate doesn't fit:**
- **No customer sign-in:** there is no sign-in or web gateway in this repo for customers to connect from.
- **Nothing durable or shared:** there is no lasting, shared storage for Gmail tokens.
- **Google approval:** read access to Gmail is a "restricted" permission at Google. Opening it to the public needs Google's verification and a security assessment, which takes weeks.

**What's built** (details in the ticket's Evidence section):
- **Connection handling** (`support_agent/gmail_connect.py`): starting and finishing the Google consent step safely, so a link can't be reused, copied to another browser or completed by a different customer.
  - It refreshes Google tokens; a temporary Google outage doesn't disconnect anyone.
  - Disconnect blocks access in the app first, then revokes at Google.
- **The tool** (`support_agent/gmail_tools.py`): `find_order_confirmations(order_id)`.
  - The mailbox owner always comes from the signed-in session; the model can't choose whose mailbox to read.
  - It returns only sender, date, subject and the order IDs found in each email, never the email body.
- **Agent wiring** (`support_agent/agent.py`): the tool is added to `root_agent`, plus one instruction sentence.
- **Package import** (`support_agent/__init__.py`): `root_agent` now loads lazily. Before this, even the existing test couldn't run without google-adk installed.
- **Tests:** `tests/test_gmail_connect.py` and `tests/test_gmail_tools.py`.

**Checks:**
- **New tests:** 26 passed, 1 skipped, on Python 3.11 against a fake Google. The first run caught a real bug: "confirmation" was being read as an order ID. I fixed it and reran.
- **Existing test:** `test_tools.py` now passes; before my change it failed to load. I could only run it on Python 3.9 (the only interpreter here with pytest), which is below the project's 3.11 minimum.
- **Not run:**
  - The test that checks the model sees only `order_id` (skipped, google-adk isn't installed).
  - A real ADK Runner test.
  - Any live Google or Gmail call.
  - Whether `adk web` or Cloud Run still finds `root_agent` through the lazy import.

**Not safe for the pilot yet:**
- **Storage is in memory:** connections are lost on restart and break with more than one Cloud Run instance.
- **Security risk:** the agent that reads customer mailboxes also has `send_email`. Email subjects are written by outsiders and can carry instructions, so leaving out bodies narrows the risk but doesn't remove it. This should block launch until the existing security review ticket (T-104) covers it.

**Human effort still owed:**
- **Review (about 1–1.5 h):** check the connect, refresh and disconnect logic, and check the fields shown to the model.
- **Verify:** run the full tests with google-adk 2.8.0 on Python 3.11, and confirm the deployed app still loads `root_agent`.
- **Person-only:** create the OAuth client and consent screen in Google Cloud Console. Also choose between leaving the app in Google's Testing mode and applying for verification:
  - **Testing mode:** you add the 30 pilot customers as test users. I believe customers would then have to reconnect weekly, but I couldn't confirm that here.
  - **Verification:** takes weeks.

`REPORT.md` has the questions I would have asked and the answers I assumed, plus the friction log. The skills gave no ready-made next prompt; they told me to write one. Here it is:

> /adk-engineer Please take ticket tickets/T-203.md and carry it out. Customers sign in with <your identity provider>; use <Firestore / Cloud SQL> for the connection index and Secret Manager for refresh tokens; the pilot uses OAuth Testing mode with the 30 customers as test users. Also run the T-202 tests marked not run (tests/test_gmail_tools.py::AdkDeclarationTest and full pytest) with google-adk 2.8.0 on Python 3.11.