# ADR 0014: Repair missing schema fields once

Date: 2026-10-25
Status: accepted

## Context

The writer omitted gaps and a condition's reason_id. (PA-2026-0205)

## Decision

Re-ask the writer once with the validation errors when required fields are missing.

## Verification

Re-ran PA-2026-0205 on the new version: decision now matches the officer's label. Other development cases not re-run (cost).
