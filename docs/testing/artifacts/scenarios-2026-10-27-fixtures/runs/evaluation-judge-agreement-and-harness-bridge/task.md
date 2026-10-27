We have two LLM judges and a set of 60 human-labelled traces; the judges disagree more than we expected. Tell us how to measure agreement properly, and whether we can run our ADK agent under Inspect to reuse its repeated-trial reducers without rewriting the agent.

---
Situation (from the person asking): An ADK 2.12 agent, two judge prompts on gemini models, 60 labelled traces with ordinal 1-5 ratings, a scripted-model harness, no model access in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.