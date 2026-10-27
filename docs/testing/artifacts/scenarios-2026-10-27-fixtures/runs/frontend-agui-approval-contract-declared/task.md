Our CopilotKit frontend asks users to approve refunds, but since we upgraded the JavaScript client the next message is refused until the approval is answered some other way. Can you fix approvals? And which version of the approval protocol are we actually on?

---
Situation (from the person asking): An ADK 2.12 agent behind ag-ui-adk with emit_interrupt_outcome left at its default, a CopilotKit app on @ag-ui/client 1.0 that answers approvals with useHumanInTheLoop tool messages, require_confirmation on the refund tool. No network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.