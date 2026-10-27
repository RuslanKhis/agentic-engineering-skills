# Fieldline assistant

Assistant for Fieldline's mobile-network maintenance engineers. An engineer
on a site visit asks about the site (equipment, access, hazards), logs what
they did, and gets reminders of how they like to work. Several engineers
cover the same sites on a rota.

- `fieldline/agent.py`: the agent; `PreloadMemoryTool` loads relevant
  memories into each turn.
- `fieldline/services.py`: sessions in a database (`DatabaseSessionService`);
  memory is Vertex AI Memory Bank when deployed and `InMemoryMemoryService`
  in tests and locally.
- `fieldline/tools.py`: `get_site` and `log_visit`.
- `deploy/deploy.sh`: Cloud Run deployment with the Memory Bank URI.

Nothing writes to memory yet, so preload always finds nothing in production.
See `docs/memory-wishlist.md` for what the product owner wants remembered.

```bash
python -m unittest discover -s tests -t .
```

google-adk is not installed in this environment; there is no network and no
Google Cloud credentials. Tests that need the SDK skip.
