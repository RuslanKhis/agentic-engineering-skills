/adk-engineer Carry out docs/tickets/support/G01.md.

---
Situation (from the person asking): A five-ticket proof of concept under docs/tickets/support/ (save and forget a reply language, streamed replies, honest failed replies, a journey check, a review presentation). While implementing G01 I found that forgetting must also clear the copy of the language cached in session state, which the design's C2 does not say, and we decided forget should be a soft delete kept for 30 days. The work took me about six hours against the 2-3 hour estimate. ADK is not installed.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.