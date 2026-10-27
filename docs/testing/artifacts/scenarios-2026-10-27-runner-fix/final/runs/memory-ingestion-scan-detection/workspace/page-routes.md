# Per-page route (pack/)

| Page | Density | Route | Text origin | Model sees |
| --- | --- | --- | --- | --- |
| text-page.pdf p1 | text | text | native | text layer only |
| scanned-page.pdf p7 | low_density (34 chars, header only) | ocr_or_vision | native header only | NOT as text; body unread until OCR or vision runs |
| table-page.pdf p1 | text, table | both | native | reconstructed rows plus rendered page |
| drawing-page.pdf p1 | low_density, drawing | both | native | text fields (6.0 m, Scale 1:200 @ A3) plus rendered page |

## Questions I could not ask, and the assumptions I used
1. Is "page 7" in the scan's header its true page number? Assumed yes: a folio of a longer plan, with pages 1-6 not supplied.
2. Which interpreter or extractor should I use? Assumed none: the shell was disabled, so the script did not run and I applied its rules by hand.
3. Should the default thresholds stand? Assumed yes. Four pages cannot calibrate them, and no page sits near a threshold. The drawing page (about 115 chars) is below 200 but is routed `both` by its scale statement.

## Not done
- `qualify_ingestion.py` was not executed, so the character counts marked "approx" are estimates and the image and vector-op counts are unmeasured.
- No OCR, no vision, no rendering. The scanned page's content is unknown.
- No image-budget or cost sizing (no provider limits or prices supplied).
- Table row reconstruction and drawing dimension checks were not implemented.
- Re-run the script once a shell or an inventory from a real extractor is available, and diff its output against this report.
