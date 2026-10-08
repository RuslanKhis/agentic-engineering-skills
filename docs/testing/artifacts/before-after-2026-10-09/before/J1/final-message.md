I've written the architecture document and an implementation plan for the support agent, plus `REPORT.md`; no code was written. Both documents are marked **draft**. Every product answer in them is an assumption I made, because you weren't available.

**Design decisions:**
- **No model can issue a refund.** One agent reads the email but has no tools; it only returns a structured claim (intent, order reference, reason). Ordinary code then identifies the customer, loads the order from PostgreSQL, applies the ≤200 EUR policy and makes the refund call. The refund amount always comes from the order, never from the email.
- **Duplicate refunds are blocked by a ledger.** Each order line can have at most one refund record. Spend caps and an off switch are checked when the record is created. If a refund call times out, its status is checked later; it is never sent again.
- **Billing questions go to the other team's Java agent through code, not through the model.** It runs over A2A (the agent-to-agent protocol) or REST with a 30-second timeout, and only minimal customer data is sent. Its answer is treated as data. On timeout or error, the ticket goes to a human on the billing team.
- **Customer identity comes from a verified sender address.** Email has no OIDC login, so the customer must be an account whose email matches a sender with a DMARC pass. Unverified senders get knowledge-base answers only, with no account actions.
- **The pilot only drafts replies.** A human sends every reply, which keeps the remaining security risk acceptable. Hosting is Cloud Run with Cloud Tasks, and everything stays in an EU region.
- **Weekly releases pass a gate.** All parts of a release (code image, prompts, pinned model, policy version, knowledge-base version, eval set) ship and roll back as one unit. The gate fails on any wrong auto-refund or forbidden action, or on intent accuracy dropping more than 3 points. Then 20% of traffic gets the new version for 24 hours before full rollout.

**Questions I would have asked:** all 17 are in §3 of the design, each with my assumed answer and the decision it settles. Your examples are used as given: 2k emails/day, EU customers, existing OIDC login and PostgreSQL, refunds under 200 EUR auto-approvable. Six questions stay open (§10). The ones that matter most are:
- whether the refunds API supports idempotency keys and status lookup;
- whether the billing team's agent actually speaks A2A;
- whether the helpdesk passes on the DMARC result.

Turning on auto-refunds depends on the first and third; local work does not.

**Checks:** I confirmed that the links between the two documents resolve and that every decision and open-question ID is defined. No tests ran, because no code exists and `google.adk` isn't installed. Nothing provider-related is verified: model ID, EU availability, prices and ADK API behaviour need the network, so they're marked provisional and assigned to a discovery goal (G00).

`REPORT.md` contains the friction log with file:line pointers; I rated the skill 3/5. The main friction:
- I had about 950 lines of reference reading before writing anything useful.
- The examples and template assume an assignment judged on predictions, which fits a design review poorly.
- There is no place to record questions when the user can't answer.
- There is no guidance on identity for channels without a login, like email.

The skills give no ready-to-type next prompt, only a template. Filled in for the next ready goal (G03, the refund policy and ledger, local only):

```text
Use adk-engineer to continue G03 "Refund policy and ledger, local" from docs/plans/customer-support-agent.md.
Read docs/architecture/customer-support-agent.md and preserve its accepted decisions (D3, D4, invariants I1, I2).
Use safe-api-tool-calls and adk-operational-guardrails.
Work within local code and a local PostgreSQL container only (no payments API, no cloud), verify the G03 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

Files are in `docs/`:
- architecture/customer-support-agent.md
- plans/customer-support-agent.md