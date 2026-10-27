# Acceptance criteria (agreed 2026-10-06, before any run)

Submission readiness needs every gate below, each with its own evidence:

1. Transport and schema: every prediction is valid against the draft schema through the normal
   route.
2. Source support: every reason's citations support it under the review rubric.
3. Fresh end-to-end: at least one clean, fresh case through the normal route (writer, review,
   export) on the frozen version, with its latency recorded.
4. Outcome agreement: predicted decision matches the officer's reference decision on at least
   6 of the 8 reference cases (disagreements are reported, not re-run until they agree).
5. Officer UI and export: the fixture journey passes in the UI.
6. Full regression on the frozen snapshot passes.

Latency: p50 end-to-end under 10 minutes per case on an uninterrupted run.
