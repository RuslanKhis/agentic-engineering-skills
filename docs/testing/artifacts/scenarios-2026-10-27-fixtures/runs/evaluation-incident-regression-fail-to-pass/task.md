Last week our refund agent issued two refunds when a customer said 'yes' twice. We merged a fix. Turn this into a regression case CI keeps, and tell us exactly when the case counts as passing.

---
Situation (from the person asking): An ADK 2.12 refund agent with issue_refund and lookup_order tools, an in-memory backend fixture, scripted-model Runner tests for eligible refund and foreign-order denial, the fix merged as one commit on top of a known base commit, no model access in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.