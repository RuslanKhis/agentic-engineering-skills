# portability-ticket-carried-out: what the fixture holds

Context unchanged. Standalone overlay (no base): an accepted design `docs/architecture/claims.md`
(Cloud Run, Gemini via Vertex AI, Agent Platform sessions and Memory Bank, Vertex AI Search,
Firestore and Cloud Storage, Identity Platform; R1-R6, C1-C6, D1-D6; scope gate names AWS and
Azure as targets and LangGraph as the framework to compare), a plan `docs/plans/claims.md`
(G01-G02 verified_local, G03-G06 ready build goals, G07 portability ready) and the ticket
`docs/tickets/claims/G07.md`. A little code under `claims/` for G01-G02.

| Assertion | What to check |
| --- | --- |
| A1 reads design and plan first | evidence of both in the answer or the document's citations |
| A2 writes docs/portability/claims.md from the template with every section | the 15 sections of the skill's template |
| A3 classification per component citing design IDs | e.g. Memory Bank (D1), sessions (D2), Vertex AI Search (D3), Firestore/Storage (D4), Gemini (D5), Cloud Run and Identity Platform (D6) |
| A4 five dimensions | cloud, agent framework, model, service, deployment, each assessed or "not a concern" with a reason |
| A5 AWS, Azure, frameworks with ADK first, official sources with read dates | the session has no network: sources from the skill's references with their dates are acceptable; fresh reads cannot happen |
| A6 relative effort words, no hours, prices or dates | |
| A7 runs check_portability.py | no shell in the run: credit naming the command with `--design` and `--plan` and saying it was not run |
| A8 design, other goals and code unchanged; no Terraform, IAM, manifests | workspace diff: only docs/portability/claims.md (and possibly G07's Evidence) may change |
