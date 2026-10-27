Deploy our ADK assistant's FastAPI backend and React app to Cloud Run behind IAP for the pilot group.

---
Situation (from the person asking): An ADK 2.12 web app built from the designer's web defaults: one FastAPI app with the Runner in process, /api behind a verified-principal dependency, the SPA served by app.frontend(); no cloud credentials in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.