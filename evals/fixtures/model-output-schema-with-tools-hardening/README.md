# Claim intake extractor

Reads a motor-insurance claim email and its attachment text and produces a
structured `ClaimExtraction` record for the claims queue. Built on Google ADK
2.8.0 with the Gemini API-key backend (`GOOGLE_GENAI_USE_VERTEXAI=FALSE`).

- `extractor/agent.py`: the extraction agent (output_schema plus two lookup tools).
- `extractor/schema.py`: the `ClaimExtraction` Pydantic model.
- `extractor/tools.py`: `lookup_policy` and `lookup_repairer`, backed by local
  reference data in `extractor/reference.py`.
- `extractor/pipeline.py`: runs the agent for one claim and hands the record to
  the queue.
- `samples/`: three anonymised claim emails used for manual checks.

Tests: `python -m unittest discover -s tests -t .` (tool tests run on the standard
library; schema tests skip when pydantic is not installed). google-adk is not
installed in this environment and there are no model credentials.
