# Pinecrest delivery assistant

Chat assistant for Pinecrest Grocers' home delivery. Customers book delivery
slots, ask about orders and substitutions. Built on google-adk 2.12.0 with
Vertex AI Memory Bank (memory revisions on, the default) for what customers
tell it about themselves: delivery address and access notes, substitution
preferences, dietary needs.

- `pinecrest/agent.py`: agent with `PreloadMemoryTool`, `book_slot`,
  `order_status`.
- `pinecrest/memory_config.py`: Memory Bank topics and generation settings.
- `jobs/nightly_generate.py`: nightly pass that generates memories from the
  previous day's sessions.
- `eval/memory_gold.jsonl` and `eval/score_recall.py`: the memory gold set and
  its scorer (offline, against saved recall outputs).

```bash
python -m unittest discover -s tests -t .
python eval/score_recall.py eval/memory_gold.jsonl eval/recall_outputs.jsonl
```

google-adk and the Vertex AI SDK are not installed here; there is no network
or Google Cloud access in this environment.
