I wrote the ingestion report and the per-page route, but I didn't run the skill's `qualify_ingestion.py`. Bash was disabled in this session, so I applied its rules by hand to the raw PDF bytes, read with Grep. Character counts for the text, table and drawing pages are approximate hand counts. The scanned page's 34 characters and its image details are exact, taken from the raw bytes.

**Routes**

| Page | Route | Why |
| --- | --- | --- |
| `text-page.pdf` | text | About 800 characters of native text. |
| `scanned-page.pdf` | ocr_or_vision | The text layer is only the header "Synthetic Local Plan 2021 - page 7" (34 characters). The body is one embedded raster image, so it must never go to the model as a text page. |
| `table-page.pdf` | both | A ruled four-column grid. The "2-3 bedrooms" row points to note 2, so the note should be joined to the row before any question is asked. |
| `drawing-page.pdf` | both | It has a scale statement ("Scale 1:200 @ A3"), a scale bar (0, 5, 10 m) and a written "6.0 m". |

- **Unread body:** the scanned page's body is unresolved evidence, not an absent provision. It is a 120×160 gray image stretched to about 18 dpi, so even a future OCR pass may struggle.
- **Visual pass:** a full visual pass would send 3 images.
- **Drawing dimensions:** by the scale bar, 90 pt on the drawing is about 5.6 m. By 1:200 at A3 it is about 6.4 m. The written 6.0 m is not attributed to anything in the text layer. I treat both pixel figures as estimates that do not override the written dimension.

**Questions I couldn't ask, and what I assumed**
- **Larger Local Plan:** I assumed the pack is just these four files and that "page 7" stands alone.
- **The 6.0 m dimension:** I left it unattributed rather than assuming it is the extension depth.
- **Table 2 and Zone A:** I treated the pack's table as the "Table 2" the text page cites, by title match. Zone A is undefined anywhere in the pack.

**Left undone**
- Running `qualify_ingestion.py` and confirming my hand-derived numbers against its output.
- OCR or vision on the scanned page, and decoding the embedded image.
- Calibrating the thresholds, which are still the defaults. Four pages is too few to calibrate on.
- Rendering the pages to images.

Files are in the working directory:
- `ingestion-report.json`
- `page-routes.md`