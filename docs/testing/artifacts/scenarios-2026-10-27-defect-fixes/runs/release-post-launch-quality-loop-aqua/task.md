Please do ticket G07. After launch we need to keep an eye on quality in production and turn problems that keep coming back into eval cases. The ticket says to use google/adk-recipes:agents-cli-aqua as well.

---
Situation (from the person asking): An Agents CLI project on google-adk>=2.12.0 writing BigQuery Agent Analytics rows, with a production design (contracts for a CI gate and weekly production quality) and a release manifest. The agents-cli-aqua skill is not installed; no network or credentials.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.