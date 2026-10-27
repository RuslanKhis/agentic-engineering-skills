I've written the ingestion report and the per-page route, but I did it by hand, not with the skill's `qualify_ingestion.py`. There was no shell in this session. I read the uncompressed content streams of the four PDFs and applied the skill's routing rules myself. The character counts and alphanumeric ratios are my estimates, not extractor output.

| Page | Class | Route |
| --- | --- | --- |
| 01-design-code-dc7 | text, about 860 characters | text |
| 02-local-plan-p12 | low density, about 41 characters | OCR or vision |
| 03-cycle-parking-table | text, ruled table | text and image |
| 04-rear-elevation | low density, vector drawing | text and image |

- **02 is the scan.** Its text layer is only the running header "Local Plan 2019 - page 12". The body is a single 160x112 px grayscale image, so OCR or vision may read it poorly. Until it is read, its content is unresolved evidence, not an absent provision.
- **03 is a table.** Each cell is a separate text run, so rows need rebuilding from the cell positions. It probably holds the Table C1 that page 01 cites. The stock script's table check may not catch this page, so I set the route by reading it.
- **04 is a drawing.** It carries a written "3.2 m to eaves" and "Scale 1:100 @ A3". The page is A4-sized and the scale bar doesn't match 1:100, so use the written dimension and don't measure from pixels.

There are no reading-order problems. A full visual pass would be 3 images.

**Questions I couldn't ask, and what I assumed:**
- **Table C1:** is page 03 the Table C1 that 01 cites? I assumed yes.
- **Page 02 source:** is a higher-resolution source available? I assumed not.
- **Page 04 scale:** is its scale statement authoritative? I assumed not.

I kept the skill's default thresholds (200 characters, 0.5 alphanumeric ratio, 8 vector operations). Four pages are too few to calibrate them, and no page sits near a threshold.

**Left undone:**
- Running the script (`--pdf` needs pypdf).
- OCR, rendering and vision.
- Table row reconstruction.
- Choosing a rendering resolution.
- Calibrating the thresholds.

Files are in `ingestion/`:
- `ingestion-report.md`
- `page-routes.json`