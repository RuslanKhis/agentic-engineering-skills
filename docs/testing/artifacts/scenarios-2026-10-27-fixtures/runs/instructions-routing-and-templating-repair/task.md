Our ADK coordinator misroutes refund questions to the billing agent and the root instruction raises KeyError on a JSON example. Fix both and give us a test that renders the instruction and a check that the right sub-agent is chosen.

---
Situation (from the person asking): Python ADK 2.8.0 project with a chat-mode coordinator, three sub-agents whose descriptions are one or two words, an instruction string containing a JSON example with simple keys, and a profile state key written by a tool. No model credentials are available.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.