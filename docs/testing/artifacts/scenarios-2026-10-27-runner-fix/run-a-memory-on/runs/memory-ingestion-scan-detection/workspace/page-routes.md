# Per-page route (pack/)

Hand-derived from the raw PDF bytes. The skill's `qualify_ingestion.py` was not run because there was no shell. Details are in `ingestion-report.json`.

| Page | Density | Route | Text origin | Send to model |
| --- | --- | --- | --- | --- |
| text-page.pdf p1 | text | text | native | Text layer only |
| scanned-page.pdf p1 | low_density (34 chars, header only) | ocr_or_vision | native header only | Rendered image once an OCR or vision pass exists. **Unresolved now.** Never send as a text page. |
| table-page.pdf p1 | text, table | both | native | Reconstructed rows with note 2 joined, plus the rendered page |
| drawing-page.pdf p1 | low_density, drawing | both | native | Text layer (Scale 1:200, 6.0 m, 10 m) plus the rendered page |

## Gaps
- No OCR or vision is available, so scanned-page.pdf body content is unread and must be reported as unresolved evidence, not as absent provisions. The embedded image is about 18 dpi, so a re-scan may be needed.
- A full visual pass would send 3 images.
- The 6.0 m written dimension and the scale bar disagree slightly with the 1:200 statement. Treat any pixel measurement as `pixel_estimate`.
- Thresholds are defaults and are not calibrated.
