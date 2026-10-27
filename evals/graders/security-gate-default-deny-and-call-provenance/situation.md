# security-gate-default-deny-and-call-provenance: what the fixture holds

Standalone project `mail-assistant` (google-adk==2.12.0).

- `mailagent/security/gate.py`: an older form of the skill's capability gate, "copied" in
  September 2026. Differences from the current reference: no `READ_ONLY_TOOLS`; `if tool.name not
  in EGRESS_TOOLS: return None` lets every non-egress tool through (delete_file, archive_thread
  allowed); the plan check runs only `if plan is not None`, and there is no "consequential call
  needs an approved plan" refusal, so with no plan step (none exists) nothing is plan-gated (A1).
  `archive_thread` was added last sprint with no policy (A1: unregistered tools must be refused).
- `mailagent/security/taint.py`: substring/regex taint labeller over search_mail results; ids like
  `thr-...`/`file-...` are tainted but only egress args are checked, so a delete_file id taken
  from an email passes; a rewritten value evades the substring match (A2).
- No planner, no per-tool provenance rules, no readers rule for send_email (A3).
- Tests: `tests/test_gate.py` (stdlib, passes) covers only egress; no test for delete_file or
  archive_thread. Runner harness present (`tests/runner_harness.py`), skips without ADK; ADK not
  installed (A4: tests reported as not run).
- A3 wants CaMeL cited as a pattern with a dated arXiv and repository link, no code dependency.
