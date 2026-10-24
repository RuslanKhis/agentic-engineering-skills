# Model Armor and DLP samples alignment — 24 October 2026

Source note: [comparison](../research/model-armor-dlp-samples-comparison-2026-10-24.md).

## Changed journey

`protect-adk-sensitive-data`: screening file attachments with Model Armor,
and changing one field of an existing template safely.

## Fresh-agent trial

A fresh agent with only the skill package added Model Armor screening of PDF
and Word attachments to a synthetic ADK 2.12 claims agent and switched on
multi-language detection in an existing europe-west4 template without
changing anything else, offline, in its own environment (Python 3.11,
google-adk 2.12.0, google-cloud-modelarmor 0.7.1 from PyPI, pytest), with
sockets and DNS blocked.

Result: 42 tests passed (screening logic and request shape; seven through
the real 2.12.0 `Runner` with a scripted model and doubles built from the
real Model Armor message types; eight for the template script against real
field-mask merge behaviour). The plugin screens in `on_user_message_callback`
before the message is saved, re-checks file parts before each model call,
allows a file only on a clean, complete verdict, and runs ahead of the stock
plugin. The template script is a dry run unless given approval and the exact
template name, updates one field with `update_mask` and `request_id`, and
reads the template back. The skill's own inspector and tests passed.
Pending live: the `MATCH_FOUND` canary, the nested mask, and whether the
language setting applies to files.

Ease: 3 of 5. The verdict rules and plugin ordering carried the work; the
two specific asks were mostly answered from SDK source.

## Frictions and fixes (same day)

All facts below were checked in google-adk 2.12.0 and
google-cloud-modelarmor 0.7.1 on 2026-10-24.

1. Multi-language detection was absent. Fixed: the template field, the
   request-level metadata and the precedence question.
2. No nested mask format. Fixed: a dotted path example, with live
   confirmation still required.
3. The stock plugin's attachment gap was unstated. Fixed: it screens text
   parts only; a file-only message skips screening.
4. No ADK seam named for attachments. Fixed: `on_user_message_callback`,
   which runs before the message is saved, plus a model-call re-check.
5. Base64 or raw bytes. Not changed: the skill keeps the live canary as the
   only way to decide.
6. Two 2.12 claims were wrong or incomplete. Fixed: the config requires at
   least one of the three templates (not a tool-output template), and
   `deidentify_sensitive_data` substitutes de-identified text while the
   session keeps the original.
7. `modalities` unexplained. Fixed.
8. No file-type mapping. Fixed: the eight byte types, mapping from checked
   leading bytes, and that a file SDP match is a block. The trial's claim
   about legacy `.doc` files was not verified and not added.
9. Required filter result keys. Fixed: the five documented keys; the trial
   reported an undocumented virus-scan key, which was not added.
10. Running the bundled tests could write cache files into the skill. Fixed:
    the commands use `python -B`.
11. The floor guidance assumed ownership. Fixed: no read or write without
    the owner's grant; a refused update stops and is handed over.

## Limits

No call reached Model Armor; every live behaviour above is pending an
approved canary.
