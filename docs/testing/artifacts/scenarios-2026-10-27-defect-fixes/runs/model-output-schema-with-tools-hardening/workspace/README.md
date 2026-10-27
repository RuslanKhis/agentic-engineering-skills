# Claim intake extractor

Reads a motor-insurance claim email and its attachment text and produces a
structured `ClaimExtraction` record for the claims queue. Built on Google ADK
2.8.0 with the Gemini API-key backend (`GOOGLE_GENAI_USE_VERTEXAI=FALSE`).

- `extractor/agent.py`: two-step extraction. `claim_gatherer` (tools, writes plain notes) then
  `claim_formatter` (`output_schema`, no tools). On the API-key backend ADK 2.8.0 does not send a
  response schema to an agent that has tools (it adds a `set_model_response` tool instead), so the
  schema sits on the tool-free agent.
- `extractor/probe.py`: `before_model_callback` that records, per request, whether the schema and
  `set_model_response` were present; this is how to prove the path (log line `model request ...`).
- `extractor/pipeline.py`: bounded retry (3 attempts, error fed back) returning an
  `ExtractionResult` with `status` "ok" or "failed"; it never raises on bad model output.
- `extractor/schema.py`: the `ClaimExtraction` Pydantic model.
- `extractor/tools.py`: `lookup_policy` and `lookup_repairer`, backed by local
  reference data in `extractor/reference.py`.
- `samples/`: three anonymised claim emails used for manual checks.

Tests: `python -m unittest discover -s tests -t .` (tool tests run on the standard
library; schema tests skip when pydantic is not installed). google-adk is not
installed in this environment and there are no model credentials.
