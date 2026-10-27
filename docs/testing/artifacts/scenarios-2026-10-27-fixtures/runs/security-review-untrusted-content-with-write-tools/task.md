Review our ADK support agent before launch. It reads inbound customer emails through a tool, searches a RAG index, and can issue refunds and send emails. Tell us what an attacker could make it do and give us tests that prove the fixes.

---
Situation (from the person asking): Python ADK 2.8.0 project: one chat-mode agent with eight FunctionTools including fetch_email, search_docs, issue_refund and send_email, no before_tool_callback, refund tool without require_confirmation, Model Armor plugin on user input only. No model credentials available.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.