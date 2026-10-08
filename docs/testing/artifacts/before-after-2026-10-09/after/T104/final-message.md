**Specialist: `adk-agent-security`**, because T-104 is a pre-release security review of an agent that reads untrusted customer email and can both refund money and send mail. The routing table points exactly that case to this skill, and the ticket doesn't name a primary skill. Other skills (auth, guardrails, API safety, data protection, deployment, frontend, instructions) are named as owners of specific findings but weren't loaded.

**Verdict:** the agent was not safe to open to external customers, and it still isn't launch-ready until the open questions below are answered and the SDK tests have run. I fixed the two critical paths and the high-severity ones in code.

**The review** is in `docs/security/T-104-security-review.md`. It has 15 findings, each with file:line, OWASP ID, where it's enforced, how to check the fix, and an owner. The two critical ones:
- **F1:** the root agent read raw email and could `send_email` to any address the model chose. One injected email could send order data to an attacker.
- **F2:** `issue_refund` had no human step and no amount limit, and it took the customer's `user_id` from the model.

Order lookups also weren't limited to the customer's own orders, and model-supplied IDs went straight into URL paths.

**Changes made:**
- **New `support_agent/security.py`:** a check that runs before every tool call and refuses when unsure. It blocks:
  - identity arguments such as `user_id` and `to`;
  - malformed IDs;
  - refunds outside 0 to `REFUND_LIMIT_EUR` (default 100);
  - mail when the session has no address written by the application.

  It logs every refusal and labels email and knowledge-base results as third-party text.
- **`tools.py`:**
  - The customer identity comes from the session, not the model.
  - Orders are filtered to the session user.
  - Mail goes only to `state["user:email"]`.
  - IDs are checked before they go into URLs.
  - Refunds check that the customer owns the order and that the amount is within the order total.
- **`agent.py`:**
  - Only the triage agent reads raw mail now.
  - Triage can't hand the conversation to another agent.
  - Refunds need user confirmation (`require_confirmation=True`).
  - Every agent gets the new checks.
- **`__init__.py`:** loads `root_agent` lazily, so the policy tests import without the SDK.
- **`tickets/T-104.md`:** Evidence section filled in.

**Checks:**
- **Inventory (before vs after):** write tools with no gate went from 3 to 0, and the model-supplied identity finding went from 1 to 0. Every agent is still flagged for the "lethal trifecta" (private data, untrusted content and a way out). The tool can't see that the mail recipient is now fixed by the session; the review explains this.
- **`tests/test_security_policy.py`:** 7 of 7 passed. pytest isn't installed, so I called the test functions directly with python3.11.
- **Not run:**
  - `tests/test_security_runner.py` (needs google-adk); its use of the 2.8.0 API is unverified.
  - `tests/test_tools.py` (needs httpx).
  - A live red-team.
  - Checks against the deployed service's authentication and IAM.

**Behaviour changes to accept before merging:**
- Refunds now pause for confirmation, so the front end must show ADK's confirmation request or refunds will stall.
- Refunds above the limit are refused rather than sent to staff.
- The application must write the customer's address into session state when the session starts.

**Still open:**
- Refunds have no idempotency key, so a retry could refund twice.
- Customer emails go to Gemini through the API-key backend rather than Vertex AI; Legal should decide.
- I couldn't check from the repo whether the Cloud Run service requires authentication, or how the UI renders model output.
- Upgrading google-adk to 2.11.0 is a decision for you.

I logged each assumption as Q1–Q8 in the review. The main ones: the session user is the external customer, and their ID matches `customer_id` in the orders system; and order responses include `customer_id` and `amount_eur`. Nothing was committed.

`REPORT.md` covers the skills and files read, the friction log with pointers into `.claude/skills/...`, and a 3/5 rating. The biggest frictions:
- The inspector also scanned `.claude/`.
- It missed callbacks passed as `**kwargs`.
- Its trifecta check flags too much.
- The review mode asks you to read all 8 reference files first.

**Next prompt:** the skills gave none to quote. `adk-engineer` says to end with one but gives no wording. My suggestion: `Please take ticket tickets/T-101.md and carry it out.`