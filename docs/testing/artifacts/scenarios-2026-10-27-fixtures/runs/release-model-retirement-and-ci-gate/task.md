Our Gemini model retires in three weeks and our GitHub Actions only run unit tests. Plan the model upgrade and add an eval gate that blocks regressions without being flaky.

---
Situation (from the person asking): ADK 2.8.0 project with a 40-case evalset, no eval config, judge model unset, model ID gemini-2.5-pro in three places, Cloud Run deployment, prompts as Python constants.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.