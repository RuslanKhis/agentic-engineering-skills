I wrote the handover document and the incident-writeup template for Kestrel's IT team. Nothing was run, checked against the live project, or changed in existing files. Everything comes from reading the repo.

**Files (both new):**
- `docs/operations/claims-intake/handover.md`: contracts, system map, support tiers and RACI, alerts, runbook entries, access transfer, recurring owners, known limits, hypercare exit checklist.
- `docs/operations/claims-intake/postmortem-template.md`: a blameless template pre-filled for this agent. It includes triggers, harm categories, affected-users queries using Cloud Logging and sessions (BigQuery once a table exists), the notification decision (Kestrel decides, Brightlane tells them), and the regression case.

**What the IT team needs to know first:**
1. **The pinned model may already be retired.** `agent.py` pins `gemini-2.5-flash`. A note in the installed evaluation skill says it retired on Vertex on 2026-10-20. I couldn't verify that offline, and the model lifecycle table isn't installed. Someone with project access should check today and send a test request, because the service may already be failing.
2. **Both alerts email only Brightlane's on-call list.** After 2026-11-17 nobody at Kestrel would be told.
3. **There is no alert for telemetry stopping or for quality drops, and there is no route for handlers to report wrong answers.**
4. **The 5xx alert isn't a ratio.** It is named "> 2%" but filters the 5xx request count with no denominator. I recorded this in the handover and did not edit the alert files.
5. **Brightlane holds Owner on the project, repo admin, and secret rotation.** The transfer table is written but empty of dates.
6. **Other gaps:**
   - Only one behavioural rule is written down, and nothing tests it.
   - `policy-api-token` is injected but no code reads it, so production may not match the repo.
   - No session store or telemetry settings are in `deploy.sh`, so sessions may be in-memory.

**Questions I couldn't ask, and what I assumed (also listed at the end of the handover):**
- **Q1:** There is no support contract after 2026-11-17, and Brightlane's access ends then.
- **Q2:** Only "never promise a payout" is an agreed contract. Two more contracts (cover answers come from `check_cover`; no personal data in logs or traces) are proposals.
- **Q3:** The deployed build is the repo's `1.2.0`.
- **Q4:** Production uses the repo's one-record policy dictionary.
- **Q5:** Support hours and response targets are left blank, not invented.
- **Q6:** The RACI assignments for Kestrel's product owner and data protection officer are proposals, and no names are given.
- **Q7:** No feedback route exists yet.

**Left undone:**
- Confirming that the alerts are deployed and enabled, and checking IAM, the secret, the session store and the telemetry settings.
- Rehearsing the runbook entries.
- The model retirement date.
- Fixing the alerts or channels.
- Writing an evaluation set.
- Writing a postmortem for a past incident (none was requested).