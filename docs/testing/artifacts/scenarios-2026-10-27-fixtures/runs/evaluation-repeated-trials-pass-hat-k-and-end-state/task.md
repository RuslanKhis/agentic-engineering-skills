Our booking agent passes the eval set on Monday and fails on Tuesday with no code change. Give us a reliability number we can gate on and a way to grade bookings that doesn't break every time the model picks a different but correct order of calls.

---
Situation (from the person asking): An ADK 2.12 agent with a scripted-model test harness and an in-memory booking backend fixture, an eval set of 40 cases, a nightly CI job, no model access in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.