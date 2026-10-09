---
goal: G03
title: We know which EU region gives us the model, sessions, storage and screening we need
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-model-and-output-contracts, protect-adk-sensitive-data]
blocked_by: []
phase: 1
profile: production
estimate: 16-24 h
status: ready
---

# G03 We know which EU region gives us the model, sessions, storage and screening we need

## Outcome

A dated residency and availability note picks the region and lists every data recipient (Vertex, Cloud Run, Cloud SQL, GCS, Cloud Tasks, Logging, Trace, Model Armor, SDP) with its EU location, quota and price source. Implements D6, D9, D10, I7 in the design.

## Scope

- In: `docs/integration/eu-residency.md` with URLs and access dates; selected region; Vertex quota for the model in that region; dated prices for the cost formula in the design.
- Out: Provisioning (G16).
- Depth: Discovery: stops when a region is chosen with evidence or no compliant region exists (escalate to the user).
- Route: Official Google Cloud documentation pages and, if authorised, read-only `gcloud` quota inspection in the target project.
- Prerequisites: Network access for documentation; optionally read access to the target GCP project.
- Supporting skills:
  - `adk-model-and-output-contracts`: `gemini-3.8-flash` availability, quotas and pricing on the Vertex EU endpoint
  - `protect-adk-sensitive-data`: Model Armor and SDP EU endpoints and residency of each recipient
- Execution scope: Documentation lookup (network) and optional read-only project inspection; no resource creation.

## Acceptance

- [ ] Every recipient in the design's data table has an EU location with a dated source.
- [ ] `gemini-3.8-flash` is confirmed available on a Vertex EU regional endpoint, or the note names the alternative model and the decision D10 must change.
- [ ] Forbidden: no resources created; no global endpoint chosen.

Verification: Document review; the chosen region becomes a single config value consumed by G16.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-eu-residency-discovery.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
