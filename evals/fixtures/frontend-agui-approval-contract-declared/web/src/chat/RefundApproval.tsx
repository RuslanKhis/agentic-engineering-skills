import { useHumanInTheLoop } from "@copilotkit/react-core";

// The agent asks before issue_refund runs; the customer answers here.
export function RefundApproval() {
  useHumanInTheLoop({
    name: "adk_request_confirmation",
    description: "Ask the customer to approve a refund before it is issued",
    parameters: [
      { name: "originalFunctionCall", type: "object", required: true },
      { name: "toolConfirmation", type: "object", required: false },
    ],
    render: ({ args, status, respond }) => {
      const call = (args.originalFunctionCall ?? {}) as { args?: { order_id?: string; amount_cents?: number } };
      const amount = ((call.args?.amount_cents ?? 0) / 100).toFixed(2);
      if (status !== "executing" || !respond) {
        return <p className="approval approval--done">Refund request for {call.args?.order_id}</p>;
      }
      return (
        <div className="approval" role="group" aria-label="Refund approval">
          <p>
            Refund £{amount} on order {call.args?.order_id}?
          </p>
          <button onClick={() => respond({ confirmed: true })}>Approve</button>
          <button onClick={() => respond({ confirmed: false })}>Decline</button>
        </div>
      );
    },
  });
  return null;
}
