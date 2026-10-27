# Upload analyst

Lets Fjord Insurance's underwriting team ask questions about spreadsheets and CSV exports that
customers upload to the claims portal. The agent writes Python against the uploaded files and
runs it, then emails a short report.

- Google ADK 2.12.0 (`pyproject.toml`), Gemini on Vertex AI in `europe-west4`.
- Runs on Cloud Run in the `fjord-uw-prod` project (EU); uploads live in the
  `fjord-uw-uploads` bucket in the same project.
- `app/agent.py` builds the agent; `app/tools/` holds the tools.
- `deploy/service.yaml` is the Cloud Run service.

Customer uploads must not leave the EU project.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk and the Daytona SDK are not installed in this environment; tests that need them skip.
