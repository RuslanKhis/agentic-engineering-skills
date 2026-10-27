# Design: claims helper

Status: accepted 2026-09-30 (pilot design)

- Hosting: Agent Runtime (europe-west1), created and deployed with Agents CLI; pilot project
  `claims-helper-pilot`, dev project `claims-helper-dev`.
- Users: 15 claims handlers through the internal portal's agent panel.
- Telemetry: Cloud Trace with message content capture off.

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | the agent never changes a claim | agent | tool list | read-only tools only | no tool to call | evidenced: local, G02 |
| C2 | R1 | answers cite the claim they came from | agent | instruction | response check | handler sees no citation | evidenced: local, G03 |
| C3 | R2 | prompts and replies are not stored in traces | project | telemetry config | capture flag off | content absent | evidenced: local, G04 |
| C4 | R3 | one tool owns each cloud resource and the pilot can return to the last working version | project | Terraform and deploy CLI | ownership journal, readback | manual recovery | planned: G06 |
| C5 | R3 | the agent acts under its own identity with only the roles it needs | project | IAM | Agent Identity or a dedicated service account | permission denied | planned: G06 |
