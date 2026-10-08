I've written the architecture document and the implementation plan for the support agent; both are marked **draft**. You weren't available, so I answered the 14 design questions myself as a plausible product owner. Each one is recorded in the design with the decision it controls, so a real product owner can confirm or correct it. No code was written, nothing was installed, and no cloud or network commands were run.

**The central decision: no model can trigger a refund or send an email.** An agent that reads customer emails and also holds a "create refund" tool could be talked into a refund by the email text itself. So the design splits reading from acting:

- **Two model steps with no tools:** one classifies the email, the other writes the reply draft.
- **Refunds are ordinary code.** It applies the policy (under 200 EUR automatic, larger ones need a support lead) and records each refund so retries can't refund twice.
- **Staff approve and send every reply** during the pilot.
- **Billing questions go to the Java team's agent over A2A (agent-to-agent protocol).** Only a short summary is sent, and its answer is treated as information, never as an approval.
- **Weekly releases** go through a fixed test set of 200 labelled emails plus a 24-hour canary, and the image, prompts and models roll back together.
- **Model choice:** I'm using `gemini-3.8-flash` for both steps and `gemini-3.5-flash` to grade test runs. ADK's default grading model, `gemini-2.5-flash`, retires on Vertex AI on 2026-10-20 (11 days from now), so the design overrides it.

**Decisions still open:**
- **OD1:** does the billing team actually expose A2A, with what authentication and response-time target? If not, the call becomes a plain REST request.
- **OD2:** does the payments service accept an idempotency key and let us look a refund up by it? The refund-at-most-once guarantee depends on this.
- **OD3:** are the chosen Gemini models available in an EU region on Vertex AI, and at what price? I couldn't look this up, so the cost estimate is only a formula.
- **OD4:** which ADK version to pin. The specialist skills were checked against 2.8.0, but A2A works better on 2.10–2.11.
- **OD5:** all 14 assumed product-owner answers need confirming.
- **OD6:** can the Gmail-to-Pub/Sub intake keep all data in the EU?

**Checks:** both documents' relative links resolve. Nothing that imports `google.adk` could run, and there is no application code to test. The design is about 6–7 printed pages, longer than the skill's two-to-four-page guidance for a pilot, because refunds and the remote billing agent each brought in failure cases.

REPORT.md has the friction log with pointers into the skill files. I rated the process 4/5; the three changes that would help most:
1. A "user unavailable" mode for logging assumed answers.
2. An index to the 341-line design reference.
3. One table of version conflicts and risky defaults, such as the retiring grading model.

The next goal I recommend is G02, refunds executed exactly once. It's the money guarantee, and it needs no model and no ADK install, so it can run locally now:

```text
/adk-engineer Carry out G02 (Execute an eligible refund exactly once) from docs/plans/support-agent.md.
Read docs/architecture/support-agent.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-operational-guardrails.
Work locally against a fake Payments server, verify the boundary, lost-response,
concurrency, approval-binding and kill-switch cases, and update
the plan with actual evidence and remaining blockers.
```

Files are in the repository root:
- `docs/architecture/support-agent.md`
- `docs/plans/support-agent.md`
- `REPORT.md`