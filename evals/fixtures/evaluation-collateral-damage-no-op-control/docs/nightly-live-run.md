# Nightly live run

Every night at 02:00 the GitHub Actions workflow `nightly-live` runs the 30 cases in
`eval_cases/cases.json` against the real model (gemini-3.5-flash on Vertex AI) and the real MCP
servers: the filesystem server over a copy of last week's receipts and the GitHub server against
the `finance-approvals-staging` repository.

Recorded today: the pass rate per case and overall, the date, and the model name. Results go to
the `nightly-results` artifact.

Staging incident, 2026-10-16: during a manual staging session the agent changed emp-102's approver
while filing a claim. The nightly run that night was 30/30 green.
