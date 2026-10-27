I've finished the redesign and written it up; no application code was touched.

The new design is in `docs/architecture/design-revised.md`. I also added a one-line "superseded in part" pointer to the status line of `proposal.md`.

**What was wrong against your three requirements**
- **Customer isolation:**
  - The browser sends `tenant_id` and `traveller_id` in the request body, so anyone can edit them.
  - Search pulls the top 20 chunks across every customer and filters afterwards. That sends other customers' chunks through the service and starves the caller's results as the index grows.
  - Nothing checks `booking_ref` against the caller's tenant.
- **Approval:** the only approval is a prompt telling the model to ask. The model can call the write with different values than were approved, and nothing is recorded.
- **Lost replies:** each retry mints a fresh `operation_id`, so a lost reply followed by a retry can charge twice. After three timeouts the tool says the system didn't answer, though the change may have happened.

**The fixes**
- **Identity:** tenant and traveller come from the verified OIDC token. Sessions are tied to the traveller who created them.
- **Retrieval:** the tenant filter goes inside the index query, with a per-document access check before any text reaches the model. I recorded one index per customer as the fallback if the vector store can't filter that way.
- **Approval:**
  - The model gets a read-only `propose_change` tool.
  - The server stores the exact change and shows it as an approval card in the browser.
  - The traveller's click is recorded and is single-use and time-limited, and the server executes the write. The model is never in the write path.
- **Lost replies:**
  - The operation ID is created and saved before the first send, then reused.
  - Until the provider confirms it supports idempotency or lookup, the design never resends blindly. It checks the booking state and otherwise marks the change "unknown", tells the traveller it isn't confirmed, and hands it to an operator.

**Assumptions I proceeded on (nobody to ask)**
- The OIDC token is verifiable, and tenant comes from a claim or a directory lookup.
- The vector store supports filtering inside the query.
- Itineraries and bookings are visible only to the traveller they belong to, while policies are visible to the whole company.
- The provider does not support idempotency or lookup until it answers.
- A price difference can be fetched before the write.
- Approvals expire after 15 minutes.
- A Tidewater operator handles unknown outcomes.

The document lists each of these with the decisions that depend on it.

**Left undone**
- The provider's answer is still the blocker for automating retries.
- Logging and approval-record retention is still open, and needs Omar Haddad.
- I did not check the `gemini-3.5-flash` model ID against a lifecycle table.
- The plan estimates (about 37 hours for phase 1) are summed by hand, not run through the schedule script.
- No independent review has been done, so the design is a draft.
- No tickets were written, and nothing was run or sent externally.