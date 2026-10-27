// Approval card for ADK's adk_request_confirmation call (refunds use require_confirmation).
// The card only asks; the gateway re-checks that the call is pending for this user's session and
// the tool runs server-side. Money is integer cents.
import { makeAssistantToolUI } from "@assistant-ui/react";

interface ConfirmationArgs {
  originalFunctionCall?: { name?: string; args?: { order_id?: string; amount_cents?: number; reason?: string } };
}

export function formatCents(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`;
}

export const RefundApproval = makeAssistantToolUI<ConfirmationArgs, { confirmed: boolean }>({
  toolName: "adk_request_confirmation",
  render: ({ args, result, addResult }) => {
    const call = args.originalFunctionCall;
    const a = call?.args ?? {};
    const amount = typeof a.amount_cents === "number" ? formatCents(a.amount_cents) : "an amount";
    if (result) {
      return <p role="status">{result.confirmed ? "Refund approved." : "Refund declined."}</p>;
    }
    return (
      <section className="approval-card" role="group" aria-label="Approve refund">
        <h3>Approve this refund?</h3>
        <p>
          Refund {amount} on order {a.order_id ?? "(unknown)"}
          {a.reason ? ` — “${a.reason}”` : ""}.
        </p>
        <button type="button" onClick={() => addResult({ confirmed: true })}>Approve refund</button>
        <button type="button" onClick={() => addResult({ confirmed: false })}>Decline</button>
      </section>
    );
  },
});
