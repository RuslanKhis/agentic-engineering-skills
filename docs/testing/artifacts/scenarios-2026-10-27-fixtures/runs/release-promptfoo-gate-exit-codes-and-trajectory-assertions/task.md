The platform team standardised on Promptfoo for agent evals. Wire our ADK agent into it so the nightly job asserts on tool trajectories and native spans, and tell us exactly how the job should read Promptfoo's result.

---
Situation (from the person asking): An ADK 2.12 agent, Node and Python on the runner, a model key available only in the nightly job, no model access in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.