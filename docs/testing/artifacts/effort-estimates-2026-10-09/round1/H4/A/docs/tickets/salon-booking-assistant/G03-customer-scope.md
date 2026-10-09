---
goal: G03
title: Customers see and change only their own bookings
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security (scripted forbidden-access test)]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate: 8-12 h
suggested_owner: Dev B (agent and Python)
status: ready
---

# G03 Customers see and change only their own bookings

## Outcome

The gateway derives customer_id from the verified website session and tools read it from trusted state only (D4, I1). Provisional on assumption A6; if G00 finds no server-verifiable login, stop and record the gap.

## Scope

- In: Auth dependency in app/gateway/main.py; Runner called with user_id = verified customer; session-ownership check on every call; trusted state key written only by the gateway; tools read customer_id from ToolContext state.
- Out: OTP or guest booking (later list), widget (G04).
- Depth: Build: verified identity with cross-customer denial tests. Floor: no tokens in logs or prompts.

## Acceptance

- [ ] Customer X listing or proposing on customer Y's appointment ID gets "not found" and no data from Y.
- [ ] Another customer's session ID → 403; expired or forged token → 401; no Runner call made.
- [ ] No tool declaration has a customer parameter, and the model cannot write the trusted state key.

Verification: pytest tests/test_identity.py (offline).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-customer-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
