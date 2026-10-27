This project was set up with Agents CLI. I need a language preference that users save themselves, that survives restarts and that they can delete. Don't touch the spec, the generated wiring or the deployment setup; just this feature and its local tests.

---
Situation (from the person asking): An adopted Agents CLI project contains agents-cli-manifest.yaml, uv.lock, an accepted specification, generated serving entrypoints and an application-owned user identity. The user has chosen its existing lifecycle and requests a focused follow-up change. No external service calls or deployment are authorized.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.