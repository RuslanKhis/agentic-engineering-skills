# Claims assistant

Helps policyholders of Lindqvist Mutual report and follow up home-insurance
claims. Python, Google ADK 2.12, FastAPI on Cloud Run in `europe-west4`.

- `claims_agent/agent.py`: the ADK agent and its callbacks.
- `claims_agent/screening.py`: Model Armor screening of what the customer types,
  against the input template in `infra/modelarmor/input-template.json`.
- `claims_agent/attachments.py`: customer uploads (photos, PDFs, Word files),
  passed to the model with the next message.
- `claims_agent/server.py`: the HTTP routes.
- `scripts/apply_template.py`: pushes the template JSON to Model Armor.

Model Armor floor settings for the organisation are owned by Platform Security,
not this team (see `infra/modelarmor/README.md`).

Tests: `python -m unittest discover -s tests -t .` — offline, with an SDK-shaped
double for the Model Armor client. Neither google-adk nor google-cloud-modelarmor
is installed in this environment, and there are no credentials or network.
