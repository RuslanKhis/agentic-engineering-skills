We copied the CaMeL-style before_tool_callback from the security skill. A reviewer says an injected email can still make our agent delete a file or archive a thread. Is our gate really doing what CaMeL does, and what do we change?

---
Situation (from the person asking): An ADK 2.12 mail agent with search_mail, send_email, delete_file and a new archive_thread tool added last sprint; capability_gate from injection-patterns copied verbatim; no plan step; no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.