# Model Armor and DLP samples compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [GoogleCloudPlatform/python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
at commit `3db968f` (Apache-2.0), sparse-cloned on 24 October 2026 to
`model_armor/` and `dlp/` only and read, never run, with the Model Armor
`service.proto` from googleapis and four Model Armor documentation pages
last updated 2026-10-22.

**Maintenance.** The repository is active; the `model_armor` folder itself
changes rarely, and its samples pin `google-cloud-modelarmor` 0.2.8, older
than this toolkit's pin.

**Conclusion.** The memo called these the canonical calls; they are useful
and partly unsafe to copy. The PDF sample base64-encodes bytes that the Go
sample sends raw, and its only test sends a benign file, so it cannot tell
the two apart; the update samples omit `update_mask`, which on the API means
every field is overwritten, so copying the floor-settings sample silently
drops an organisation's integrated services. The sensitive-data skill now
carries the file-screening contract with an encoding canary, the
`update_mask` and `request_id` rules, and the fields an effective-policy
audit must read back.

## Method

Each fact was checked in the proto (the overwrite rule, the 60-minute
request id, `INSPECT_ONLY`, `data_residency_compliant`, `byte_data_type`
required) and the documentation pages before editing. One scenario case
covers the journey; the fresh-agent trial is in the
[testing record](../testing/model-armor-dlp-samples-alignment-2026-10-24.md).

## Drift corrected

None in the skill; it had no file-screening or update-mask guidance.

## Imported, by specialist

- **protect-adk-sensitive-data.** Production policy: the file request shape,
  required type, size limits and the live `MATCH_FOUND` canary. Cloud
  lifecycle: `request_id` and `update_mask` on every template and floor
  update, read-back after update. Model Armor: `enforcement_type`,
  `data_residency_compliant`, per-service floor modes, floor precedence, a
  refused create as a possible floor conflict, and the unresolved question
  of `INSPECT_ONLY` on direct calls; the samples' confidence level left to
  the policy owner. Compatibility: the dated source entry.

- **From the trial.** The attachment seam (`on_user_message_callback`), the
  stock plugin's text-only screening, `deidentify_sensitive_data` and the
  corrected template-requirement rule for 2.12.0, `modalities`,
  multi-language detection, the byte types, the filter result keys and the
  rule for a floor owned by another team.

## Routed, not copied

None; Google's `model-armor` product skill is already routed.

## Vendored assets

None; paraphrase only.

## Left out, with reasons

- The DLP snippets' `locations/global` and default endpoint: weaker than the
  skill's regional rule.
- Samples that print responses (screened content to stdout), per-call
  clients without deadlines or retries, the mixed transports and the 0.2.8
  pin.
- The live snippet tests: paid calls against a real project.

## Limits

Nothing was executed; the encoding question is settled only by the live
canary the skill now asks for.
