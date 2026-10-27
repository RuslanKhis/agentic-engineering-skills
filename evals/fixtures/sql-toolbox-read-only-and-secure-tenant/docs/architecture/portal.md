# Design: customer portal revenue agent

Status: accepted 2026-10-12

- Customers sign in to the portal through IAP; the portal backend (`portal/`) maps the signed-in
  email to a customer account (`portal/directory.json` in development).
- The agent reaches BigQuery only through MCP Toolbox for Databases (`tools.yaml`), run as a
  sidecar with the identity `portal-toolbox@fernhill-analytics.iam.gserviceaccount.com`.

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a customer sees only their own account's figures | customer | portal identity | to be decided in G03 | refusal | planned: G03 |
| C2 | R2 | nothing the agent does can change warehouse data | warehouse | Toolbox and IAM | to be decided in G03 | refusal | planned: G03 |
