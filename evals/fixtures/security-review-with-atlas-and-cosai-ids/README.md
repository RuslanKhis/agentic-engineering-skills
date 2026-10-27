# Operations assistant

Internal assistant for Tamsin Logistics' operations staff, on Google ADK 2.12 (Cloud Run).

- Mail: `search_mail`, `send_mail` (staff mailbox via the Gmail API).
- Drive: `read_drive_file`, `share_drive_file`.
- Knowledge: `search_corpus` over the shared operations corpus. Any member of the
  `ops-staff` group can add documents to the corpus bucket; `corpus/ingest.py` indexes new
  uploads nightly.
- Ticketing: the vendor's MCP server (`https://mcp.deskline.example/mcp`), all its tools.
- `app/server.py` runs the agent for each chat message.

Our security team tracks findings against MITRE ATLAS and the CoSAI Risk Map.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk is not installed in this environment and there is no network.
