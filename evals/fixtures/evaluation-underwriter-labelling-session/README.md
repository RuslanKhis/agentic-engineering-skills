# Claims triage agent

An ADK agent that triages incoming motor claims for Kestrel Mutual's underwriters: it reads the
first notice of loss, flags fraud indicators, decides whether the claim can be fast-tracked and
writes a short triage note.

- `triage/agent.py` builds the agent; `triage/prompts.py` holds the instruction.
- `labels/` holds the first labelling batch: two underwriters' verdicts (`experts.csv`) and an
  LLM judge's verdicts on the same cases (`judge.jsonl`); `labels/criteria.md` defines the
  criteria.
- `cases/` holds the 24 claims of the batch (synthetic).

No cloud access from this environment.
