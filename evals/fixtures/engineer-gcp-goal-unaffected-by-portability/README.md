# Coastline claims assistant

Assistant for Coastline Insurance policyholders reporting and following up
home-insurance claims. Google ADK 2.12.0 on Cloud Run, Gemini through
Vertex AI, claims in Firestore. Design: `docs/architecture/claims.md`; plan:
`docs/plans/claims.md`.

```bash
python -m unittest discover -s tests -t .
```

google-adk is not installed in this environment; there is no network or
Google Cloud access here.
