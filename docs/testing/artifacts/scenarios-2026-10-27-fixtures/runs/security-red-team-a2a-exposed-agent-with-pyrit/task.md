Our ADK claims agent is exposed over A2A on Cloud Run behind IAM. We want PyRIT to red-team it through A2A and to test whether a poisoned uploaded document makes it file a payout. Set it up.

---
Situation (from the person asking): Python ADK 2.12.0, agent served with to_a2a under /a2a/claims, a2a-sdk 1.2.3. PyRIT 1.1.0 is the latest PyPI release. Tools: read_document, file_payout (require_confirmation), send_email. No model credentials in CI.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.