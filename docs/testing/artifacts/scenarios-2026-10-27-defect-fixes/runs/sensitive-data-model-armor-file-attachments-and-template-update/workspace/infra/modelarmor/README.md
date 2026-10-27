# Model Armor configuration

- `input-template.json` is the input template `claims-input` in
  `europe-west4`, owned by this team. Apply changes with
  `python scripts/apply_template.py` after review.
- The organisation's Model Armor floor setting is owned and changed by Platform
  Security (#platform-security). Ask them before relying on what it enforces.
  Since September they require the Agent Platform enforcement block on every
  project in the claims folder.
- Uploads: customers may attach PDFs and Word documents. Every file is screened
  against `claims-input` before the model sees it (`claims_agent/screening.py`).
  Model Armor file screening takes 69 bytes to 4 MB, so larger documents are
  refused at upload even though the general limit is 10 MB. Photos are refused:
  the template has no image modality, so an image could not be screened. Turning
  one on is a template change for this team to decide, not part of this change.
- `scripts/apply_template.py` updates only
  `template_metadata.multi_language_detection.enable_multi_language_detection`
  (with an update mask) so nothing else in the live template is rewritten. Use
  `--dry-run` first. If the update is refused, stop and ask Platform Security
  whether the floor setting conflicts; do not retry.
- Before release, one approved live canary is still needed: screen a synthetic
  PDF and a synthetic DOCX carrying an SDP finding and expect `MATCH_FOUND`. It
  settles `MODEL_ARMOR_BYTE_ENCODING` (`raw` default vs `base64`; a wrong choice
  reads as a silent `NO_MATCH_FOUND`), whether file results report all four
  `filter_results` keys (`screen_file` withholds if one is missing), and whether
  multi-language detection applies to extracted file text.
