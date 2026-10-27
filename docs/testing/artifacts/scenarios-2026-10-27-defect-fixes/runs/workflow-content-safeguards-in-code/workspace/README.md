# Planning decision assistant

Drafts a recommended decision on a householder planning application for a
planning officer. Each case runs four stages:

1. **source** – load the application documents and the local-plan policies
   into numbered source spans (`pipeline/sources.py`);
2. **writer** – the model drafts a decision with reasons, conditions,
   citations, conflicts and gaps (`pipeline/stages.py`, `pipeline/prompts.py`);
3. **review** – a second model call checks every claim against the cited
   spans and lists findings;
4. **export** – an accepted draft is written as the officer's report.

Between writer and review, `pipeline/safeguards.py` checks the draft in plain code (no model,
no cloud service): a condition that requires what a reason says is waived, a reason that rests
on an instruction written in a source document or cites no local-plan policy, and a decision
that disagrees with its conditions. A blocked draft stops with `StageFailed("consistency")`
before any paid review. The exported report repeats each gap once, ranks those closest to the
decision first, shows five and gives a count for the rest (the full list stays in the writer
checkpoint).

Every stage result is saved as a checkpoint (`pipeline/checkpoints.py`) with
a manifest under `runs/<run-id>/`. Paid model calls go through
`pipeline/model.py`, an OpenAI-compatible chat-completions adapter (our
provider is reached through an OpenAI-compatible gateway), and are charged
against the campaign ledger in `campaign/ledger.json`
(`pipeline/ledger.py`).

`pipeline/workflow.py` runs a case in plain Python. `pipeline/adk_app.py`
wires the same stages as a Google ADK app for the served route; it is the
only module that imports `google.adk`.

## Running

```bash
python -m pipeline.workflow --case cases/dev/PA-2026-0141   # paid: needs PROVIDER_API_KEY
python -m unittest discover -s tests -t .                  # offline
```

The unit tests use `tests/doubles.py` (a scripted transport that counts
sends) and never reach the provider. google-adk and the provider SDKs are
not installed in this environment.
