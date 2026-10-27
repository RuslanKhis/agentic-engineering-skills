Our CI has no GCP credentials. Add an offline check that fails the build if any test run leaks personal data or credentials into model requests, session events, logs or tool calls, and tell us whether it can replace the SDP tests.

---
Situation (from the person asking): Python ADK 2.12 agent with scripted-model Runner tests, network egress blocked in CI after dependency install, Python 3.12, SDP and Model Armor used in production.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.