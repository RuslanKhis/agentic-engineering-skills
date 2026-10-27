# ADR 0012: Check conditions against waivers in their reasons

Date: 2026-10-19
Status: accepted

## Context

A condition required visibility splays that its own reason said were waived. (PA-2026-0204)

## Decision

Add a code check that fails a draft whose condition requires what its reason says is waived.

## Verification

Re-ran PA-2026-0204 on the new version: decision now matches the officer's label. Other development cases not re-run (cost).
