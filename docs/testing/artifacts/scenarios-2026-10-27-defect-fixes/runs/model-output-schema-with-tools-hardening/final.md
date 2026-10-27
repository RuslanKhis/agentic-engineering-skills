I restructured the agent and added a retry boundary and tests, but nothing has been run. This session had no shell, `google-adk` isn't installed, and I made no network calls.

**Diagnosis.** On the API-key backend, ADK 2.8.0 doesn't send a response schema to an agent that has tools. It adds a `set_model_response` tool instead, and the model can answer in prose or fenced JSON. A bad answer then raises when `output_key` is saved. This comes from the skill's reference notes, which cite 2.8.0 source. I haven't confirmed it against your installed ADK.

**What changed**
- **`extractor/agent.py`**: the work is split in two.
  - **`claim_gatherer`** has the two tools and writes plain notes to `claim_notes`.
  - **`claim_formatter`** has `output_schema` and `output_key="extraction"` and no tools, so it should get the native `response_schema`.
  - A `SequentialAgent` runs them in order.
  - I removed the `BuiltInPlanner(thinking_budget=1024)`, which overrode `thinking_level` on a Gemini 3 model.
  - I also removed `temperature=0.1`, since the Gemini 3 default is 1.0.
- **`extractor/pipeline.py`**: `extract()` now returns an `ExtractionResult` and no longer raises on bad model output. It makes up to 3 attempts, each in a fresh session with the validation error fed back. It accepts fenced JSON, and returns `status="failed"` with the last error if all attempts fail. Callers must handle that result instead of a bare `ClaimExtraction`.
- **`extractor/probe.py`**: a `before_model_callback` that records, for every model request, whether `response_schema` is set, the MIME type and the tool names. It also logs a `model request ...` line. This is how you prove which path ran.
- **`tests/test_pipeline.py`**:
  - Retry tests use a fake runner and cover a first-try pass, fenced JSON, prose then valid, exhausted attempts and a bad enum.
  - A scripted-model test asserts the gatherer has tools and no schema, and the formatter has the schema, JSON MIME type and no `set_model_response`.
- **`README.md`**: updated to describe the new layout.

**Status**
- **Tests:** not run (`not run`). They skip without `pydantic` and `google-adk`, and the first two classes need ADK for `types.Content` too.
- **Helper scripts:** I didn't run `audit_model_config.py` or `check_response_schema.py`.
- **Live path proof:** the real path on your backend is unproven until the probe's log line or the scripted test runs with ADK installed. For the scripted test, run it once with `GOOGLE_GENAI_USE_ENTERPRISE` unset and a dummy `GOOGLE_API_KEY`, then once with it enabled.
- **Scripted-model test:** I haven't run it, so my guesses about 2.8.0's `BaseLlm` and `LlmResponse` APIs may need adjusting.

**Questions I couldn't ask, and what I assumed**
1. **Retry location:** is an extra gatherer+formatter run per retry acceptable cost-wise? I assumed yes, with a budget of 3.
2. **Failure record:** should the queue get a failure record instead of `status="failed"`? I assumed the caller handles it and left `ClaimExtraction` unchanged.
3. **Hybrid option:** would you rather move to the enterprise backend and keep one agent? I assumed not, since that needs project, IAM and billing changes.
4. **Formatter thinking level:** I set `thinking_level="low"` on both agents without measuring. It needs checking on a labelled set.

**Left undone**
- No development-set comparison of schema validity, accuracy and wrong-valid-schema rates.
- No `max_output_tokens` sizing or finish-reason handling (a `MAX_TOKENS` result would just be retried).
- `.env.example` is unchanged and still uses the deprecated `GOOGLE_GENAI_USE_VERTEXAI` name.