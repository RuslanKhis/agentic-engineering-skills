# Homeline assistant

Chat assistant for Homeline, a home-repair booking service. Customers book
plumbers and electricians, change visits and ask about past jobs. Built on
Google ADK 2.12; long-term memory (address, access notes, past jobs,
preferences) lives in Mem0 Platform through `homeline/memory/mem0_service.py`,
which we copied from Mem0's ADK integration guide.

```bash
pip install -e .
MEM0_API_KEY=... GOOGLE_CLOUD_PROJECT=... python -m homeline.main
python -m unittest discover -s tests -t .
```

google-adk and mem0ai are not installed in this environment, and there is no
network access or Mem0 key here; the tests that need the SDK skip.
