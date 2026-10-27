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

Memory is opt-in, saved only on explicit request, per engineer, and can be listed, corrected and erased. See
`docs/memory-design.md` (design, assumptions, gaps) and `docs/memory-wishlist.md` (the ask). Recall now goes through
`fieldline/memory_adk.py:recall_instruction` instead of `PreloadMemoryTool`, so consent and forgotten-fact filtering
apply in every deployment. Consent and erasure: `python -m fieldline.memory_admin grant|withdraw|list|sweep <user_id>`.

```bash
python -m unittest discover -s tests -t .
```

google-adk is not installed in this environment; there is no network and no
Google Cloud credentials. Tests that need the SDK skip.
