# Ingestion report: pack/ (4 one-page PDFs)

Machine-readable version: `ingestion-report.json`. Qualified before any model call. No OCR, vision or model call was run.

**Provenance caveat:** `qualify_ingestion.py` was not executed (no shell in this session, and `pypdf` availability is unchecked). I applied its documented rules to the text, image and path operators read straight from the PDF bytes. Character counts marked "approx" are hand counts. Re-run the script before relying on exact values.

## Per-page route

| Page | Chars | Density | Hints | Route | Text origin |
| --- | --- | --- | --- | --- | --- |
| text-page.pdf p1 | approx 800 | text | none | **text** | native |
| scanned-page.pdf p1 | 34 (alnum 0.96) | low_density | 1 embedded image | **ocr_or_vision** | native header only; body unread |
| table-page.pdf p1 | approx 205-280 | text (near threshold) | table | **both** | native |
| drawing-page.pdf p1 | approx 95 | low_density | drawing; "Scale 1:200"; "6.0 m" | **both** | native |

- Text-layer dimensions: text page 1.0 m, 4.0 m, 6.0 m. Drawing page 6.0 m, plus 10 m (scale-bar label, not a building dimension). Table page 400 m (bus-stop distance, not a drawing dimension).
- Scanned page: the text layer is only a running header over a 120x160 grey raster. It is a scan despite the perfect alphanumeric ratio.
- Table page: needs row reconstruction. "see note 2" must be joined to "Note 2: ... reduces by 1 space". The text page cites this table as Table 2 of the Design SPD, so the two pages are linked.
- Drawing page: it has 10 path operators by my count (generator says 14; both are at least 8). Fall back to the scale statement if the extractor doesn't report vector counts. The "6.0 m" label is not tied to a specific element here, because that needs the image.

## Summary

- Low density: scanned p1, drawing p1. Image-only: none (the scan has a header, so it is not empty).
- Reading-order anomalies: none.
- Full visual pass: 3 images (scan, table, drawing), so 1 call if the provider accepts 3 or more images.
- **Unresolved evidence:** the scanned page body has never been read. The visual half of the table and drawing routes has not been executed.

## Questions I would have asked, and assumptions made

1. Which extractor will the real pipeline use? Assumed a pypdf-style text layer. The shipped `inventory.json` is generator knowledge, not an extraction, so I did not use it as evidence. It differs from the real PDFs: it uses `|` separators and omits the table caption.
2. Is a hand-applied qualification acceptable when the script can't run? Assumed yes, flagged above.
3. Are the defaults (200 chars, 0.5 ratio, 8 ops) acceptable? Kept them. Four pages cannot calibrate them. The table page sits close to 200 characters and its route doesn't depend on that, while the drawing page is under 200 and is routed by its scale statement.
4. Rendering resolution and the image-per-call limit are unset. Nothing was rendered or costed.
5. Is `pack/` identical to the skill's `ingestion-fixture/`? Assumed so, because the text and structure matched. I did not do a byte comparison.
