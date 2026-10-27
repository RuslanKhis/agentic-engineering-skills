# travel-desk-agent

Travel desk assistant for Oakmere staff: answers travel-policy questions and
drafts booking requests from an employee's trip details. Generated with
Agents CLI 1.11.0 (`agents-cli-manifest.yaml`); dependencies are managed with
uv (`uv.lock`). Deployed to Cloud Run with the generated Terraform in
`deployment/terraform/`.

Employees type names, passport details and travel dates into the chat, so
prompts are personal data. After the privacy review in October we switched off
message-content capture in tracing (`.env`).

Local tests: `python -m unittest discover -s tests -t .` (the unit tests use
the standard library only). google-adk is not installed in this environment.
