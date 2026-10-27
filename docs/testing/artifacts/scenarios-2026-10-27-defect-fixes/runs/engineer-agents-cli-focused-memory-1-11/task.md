In this Agents CLI project, remember each user's preferred response language between conversations. Keep the scaffold, the Cloud SQL session backend and the dependency pins. Offline tests only.

---
Situation (from the person asking): An Agents CLI 1.11.0 project scaffolded on google-adk>=2.12.0 with session_type cloud_sql, an accepted .agents-cli-spec.md, uv.lock and tests/eval/eval_config.yaml. The workflow skill's build phase says not to write behavioural unit tests. No live calls are authorised.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.