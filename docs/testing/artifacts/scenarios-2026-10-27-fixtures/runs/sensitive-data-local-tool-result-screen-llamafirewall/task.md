Our documents cannot leave our project, so Model Armor on tool results is out. Add LlamaFirewall to screen what our tools return, add its alignment check too, and prove it works.

---
Situation (from the person asking): Python ADK 2.12 agent on Cloud Run with fetch_url, read_contract and send_email tools, a scripted-model Runner harness, no Hugging Face token, no model access and no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.