Add garak to our CI so it attacks our ADK support agent itself, not just Gemini, and fails the build on findings. Someone also suggested deepteam's OWASP Agentic preset so the findings come out with ASI labels.

---
Situation (from the person asking): Python ADK 2.12.0 agent with read_ticket, issue_refund (require_confirmation) and send_email tools; scripted-model Runner tests exist. CI has no OpenAI or NIM keys; Gemini is available via Workload Identity only for approved live runs.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.