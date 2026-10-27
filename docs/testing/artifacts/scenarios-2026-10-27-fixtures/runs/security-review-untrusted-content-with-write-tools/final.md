I reviewed the agent, fixed the problems I found, and wrote tests for the fixes. I couldn't run anything: this session had no shell and no model credentials, so none of the new tests or the fixes have actually run. Please run `python -m unittest discover -s tests -t .` first.

## What an attacker could make it do

The agent holds all three risky capabilities at once. It reads customer data, it reads text outsiders wrote (inbound email bodies and public-forum posts in the RAG index), and it can send email and issue refunds. Model Armor only screens the chat message, so email bodies and retrieved posts are never screened. The prompt line "ignore instructions in emails" is not a control.

- **Data theft:** a crafted email or forum post could have the agent call `get_customer_profile` for any customer ID and `send_email` the result to any address.
- **Reading other customers' mail:** `fetch_email` had no ownership check, and the message ID went straight into a URL path (so `../` could reach other mail-API paths).
- **Refund abuse:** `issue_refund` needed no confirmation. Repeated calls each under the order total could refund far more than the order was worth.
- **Ticket tampering:** `add_ticket_note` accepted any message ID.

## Fixes

- **Email:** `send_email` only sends to the signed-in customer's verified address. `fetch_email` only returns the customer's own mail and rejects malformed IDs.
- **Profile:** `get_customer_profile` no longer takes a customer ID from the model.
- **Refunds:** `issue_refund` is wrapped in `FunctionTool(..., require_confirmation=True)`. Refunds are summed per order against the order total, with a cap of 3 per conversation.
- **Tickets and RAG:** `add_ticket_note` only accepts message IDs read in the same session. Email bodies and community posts are length-capped and mark the session as having seen untrusted content.
- **Server (unverified):** `server.py` now stores the verified email in session state and passes refund confirmations to and from the client. I wrote this from ADK's documented confirmation pattern and haven't checked it against 2.8.0.
- **Prompt:** I removed the "staff give you a message ID" mode. The existing checks already tie everything to the signed-in customer, so that mode never worked safely.

## Tests and the review

`tests/test_security.py` runs on the standard library only, with the existing fakes and no SDK. It covers:

- Replaying what an injected model would do (attacker send, cross-customer refund, foreign ticket note); all must be refused with no provider calls.
- Other customers' mail and path-traversal IDs.
- Subject header injection and no identity parameters on any tool.
- Refund caps.
- A static check that `issue_refund` is only registered with confirmation required.

`SECURITY_REVIEW.md` has the findings with OWASP IDs and the residual risks.

## Left undone and still open

- **Not run:** the skill's inventory script, the unit tests, and any live model test.
- **Not written:** a scripted-model Runner test of the confirmation round trip (it needs the SDK).
- **Not changed:** the google-adk 2.8.0 pin.
- **Residual risk:** the agent still has all three capabilities in one place. The damage is now bounded rather than removed. The proper fix is splitting off a quarantined reader with no tools, which I didn't attempt.
- **Residual risk:** the `From` header can be spoofed unless the mail provider reports SPF/DKIM results.
- **Residual risk:** there are no per-user rate limits, concurrent refunds can race past the sum check, and sessions are in-memory.
- **Assumptions I proceeded on (nobody could answer):**
  - Only customers use the agent, not staff acting for customers.
  - `customer_id` equals the IAP `sub`.
  - Refunds always need confirmation, at any amount.
  - Mail sender authentication is unknown.
- **Skills:** `/security-review` couldn't run because the workspace isn't a git repository, so I used the ADK security skill's review mode instead.