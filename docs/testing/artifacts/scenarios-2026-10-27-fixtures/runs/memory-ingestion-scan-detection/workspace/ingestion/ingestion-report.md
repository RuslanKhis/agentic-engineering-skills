# Ingestion report: planning pack (4 PDFs, 1 page each)

Method: no shell was available, so `qualify_ingestion.py` was not run. I read the uncompressed content streams directly and applied the skill's rules by hand. Character counts are approximate. No OCR or vision pass ran. Machine-readable version: `page-routes.json`.

| Document | Class | Route | Text origin | What it is |
| --- | --- | --- | --- | --- |
| 01-design-code-dc7.pdf p1 | text (~860 chars) | **text** | native | Prose policy DC7 (shopfronts). Cites Table C1 of the Transport SPD. |
| 02-local-plan-p12.pdf p1 | low_density (~41 chars) | **ocr_or_vision** | native header only | **Scan.** Header plus one 160x112 px grayscale raster over the page. Body unread. |
| 03-cycle-parking-table.pdf p1 | text (~450 chars), table | **both** (text + image) | native | Ruled 5-column table, 4 rows, with Note b. Probably the SPD Table C1 that page 01 cites. |
| 04-rear-elevation.pdf p1 | low_density (~100 chars), drawing | **both** (text + image) | native | Vector rear elevation with written "3.2 m to eaves", scale bar and "Scale 1:100 @ A3". |

Summary: 4 pages. 2 low-density (02, 04), 0 image-only, 1 table candidate (03), 1 drawing candidate (04), no reading-order anomalies. A full visual pass is 3 images, so no image cap is needed.

## Findings to act on
- **02 is a scan.** Don't send it to the model as text; the header would look like a complete page. Its raster is about 16 px/inch at print size, so OCR or vision may read it poorly. Until it has been read, the Local Plan p12 content is unresolved evidence and not an absent provision.
- **03 table:** rebuild rows from cell coordinates (use class, floor area, staff, visitor, notes). Join "see note b" to Note b (a commuted sum replaces visitor spaces where the footway is under 2.5 m). The stock table heuristic may miss this page, so I set the route myself.
- **04 scale is inconsistent.** The page is A4-sized but says @A3, and the scale bar does not match 1:100 at 1:1 print. Use the written 3.2 m. Don't measure from pixels; if one is needed, label it `pixel_estimate` with the scale assumption.
- Cross-reference: 01 depends on the Transport SPD Table C1, which appears to be page 03. Please confirm.

## Assumptions (no one to ask)
1. Questions: is 03 the Table C1 that 01 cites? Is a higher-resolution source of 02 available? Is the 04 scale statement authoritative? Proceeding on: yes to the first, no and no to the others (treated as unresolved/unreliable).
2. Skill default thresholds kept (200 chars, 0.5 alnum ratio, 8 vector ops). Four pages cannot calibrate them; 02 (41) and 04 (100) sit well below 200 and 01 (860) and 03 (450) well above, so no page is near the threshold.
3. Rendering resolution not chosen, since nothing was rendered.

## Left undone
Script not executed; no OCR, rendering or vision; table rows not reconstructed; thresholds and resolution not calibrated; the char counts and alnum ratios are estimates and should be re-run with the script when a shell is available (`qualify_ingestion.py --pdf` needs pypdf).
