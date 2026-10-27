# model-output-schema-with-tools-hardening: what the fixture holds

Standalone project (no base). `pyproject.toml` pins `google-adk==2.8.0`;
`.env.example` uses the API-key backend (`GOOGLE_GENAI_USE_VERTEXAI=FALSE`) and
`gemini-3.5-flash`. README says google-adk is not installed and there are no
model credentials.

- `extractor/agent.py`: one LlmAgent with `output_schema=ClaimExtraction`,
  `output_key="extraction"` and two tools (`lookup_policy`, `lookup_repairer`).
  On the API-key backend 2.8.0 combines output_schema with tools through the
  `set_model_response` workaround tool; on Vertex it sets the native response
  schema (A1 wants this explained plus a request-capture test showing which
  path ran — there is no request capture in tests today).
- The instruction says "Return ONLY the JSON object" (prompt-level hope for a
  structural problem).
- Sampling/thinking: `temperature=0.1` set (Gemini 3 default should be kept, A4)
  and thinking configured twice — `BuiltInPlanner(thinking_config=...budget 1024)`
  and `generate_content_config.thinking_config(thinking_level="low")` (A4: one place).
- `extractor/schema.py`: `ClaimExtraction` has twelve top-level fields with nested
  optionals (Party, Vehicle, Incident with nested third_party Party, Repairer), no
  refusal/insufficient-information shape (A2: reduce to the decision the model owns,
  first-class refusal; identifiers such as claim_reference/policy number copied in
  code rather than generated).
- `extractor/pipeline.py`: reads `session.state["extraction"]`, `json.loads` it
  if a string, `model_validate` — no owned boundary, no attempt budget, no explicit
  failure outcome; prose or fenced JSON raises (A3).
- A2 "runs the schema checker": the agent has no shell; naming
  check_response_schema.py and reporting it as not run is the gradeable behaviour.
- A4 also expects the development-set comparison handed to adk-agent-evaluation.

Tests: tool tests run on the standard library; schema tests skip without pydantic.
Context unchanged from scenarios.json.
