# Situation: observability-handover-and-postmortem

Standalone project: claims agent on Cloud Run (`deploy/deploy.sh`) with a Secret Manager secret,
model pinned to gemini-2.5-flash in `claims_agent/agent.py` (A4: copy its retirement date from the
model lifecycle table with read date), two alert policies under `monitoring/` both notifying the
Brightlane agency mailing list (A2: must move to a client channel), `docs/operations/access.md`
listing agency-held access (A3: transfer per item with verification and removal of agency access).
A1 (handover from the template with support tiers and RACI one accountable per row) and A4
postmortem template graded from the files written. Context unchanged.
