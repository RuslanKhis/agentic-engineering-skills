# Model Armor configuration

- `input-template.json` is the input template `claims-input` in
  `europe-west4`, owned by this team. Apply changes with
  `python scripts/apply_template.py` after review.
- The organisation's Model Armor floor setting is owned and changed by Platform
  Security (#platform-security). Ask them before relying on what it enforces.
  Since September they require the Agent Platform enforcement block on every
  project in the claims folder.
- Uploads: customers may attach photos, PDFs and Word documents up to 10 MB.
