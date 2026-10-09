# Support agent

Internal customer-support assistant built on Google ADK. Deployed on Cloud Run
(europe-west1) with the API-key backend (GOOGLE_GENAI_USE_VERTEXAI unset).
Reads inbound customer emails through the `fetch_email` tool, searches the
knowledge base, looks up and refunds orders, and hands billing questions to
the billing sub-agent. Weekly releases from `main` through GitHub Actions
(unit tests only). Known issues are tracked in tickets/.
