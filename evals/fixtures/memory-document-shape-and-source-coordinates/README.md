# Policy review

Answers planning officers' compliance questions against the council's
Development Management Policies (DMP) and has a second model check the
draft before it goes to the officer.

Route (see `review_app/pipeline.py`): an offline job extracts the policy
PDFs into records (`extract/records.jsonl`, `extract/manifest.json`); for a
question the retriever selects a pack of records; `review_app/grouping.py`
turns the pack into units; the writer agent drafts findings citing units;
the reviewer agent accepts or rejects. Each stage's output is an envelope
saved through `review_app/storage.py` under `runs/<run_id>/`.

`runs/run-0412/` is a retained run the reviewer rejected (its
`manifest.json` lists the envelopes). The writer and reviewer are ADK
agents; google-adk is not installed here and no model calls are
authorised. The original PDFs and page images are not in this repository.

```bash
python -m unittest discover -s tests -t .
```
