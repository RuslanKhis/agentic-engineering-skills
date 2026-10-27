Customers can now attach PDFs and Word files to our ADK claims agent. Screen every attachment with Model Armor before the model sees it, and switch on multi-language detection in our existing input template without changing anything else in it. Write the code and offline tests; do not touch the cloud.

---
Situation (from the person asking): Python ADK 2.12 agent with google-cloud-modelarmor 0.7.1 pinned, an input template in europe-west4, attachments up to 10 MB, an organisation floor setting managed by another team. No credentials or network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.