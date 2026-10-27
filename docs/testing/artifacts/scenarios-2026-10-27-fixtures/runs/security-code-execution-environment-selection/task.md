Security wants a review of how our agent runs code. It runs Python that the model writes against files customers upload, and that data mustn't leave our EU project. Which executor or environment should we use, and why? Then switch the agent over and write offline tests for isolation, data residency and outbound traffic. We're staying on google-adk 2.12.

---
Situation (from the person asking): An ADK 2.12 agent on Cloud Run with UnsafeLocalCodeExecutor, an EnvironmentToolset over a Daytona environment, a tool that downloads uploads and a tool that emails anyone. No cloud calls, no SDK installed.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.