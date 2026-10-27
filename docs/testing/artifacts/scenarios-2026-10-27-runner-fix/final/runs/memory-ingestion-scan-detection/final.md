I wrote the ingestion report and the per-page route, but I couldn't run the qualification script. The shell is disabled in this session, so I read each page's text layer with the Read tool and applied the script's rules by hand. The counts are derived by hand and not machine-checked. The character counts for the text, table and drawing pages are estimates, and image and vector-operation counts are unmeasured.

| Page | Class | Route |
| --- | --- | --- |
| `text-page.pdf` | text | **text** |
| `scanned-page.pdf` (printed page 7) | low density: 34 characters, running header only | **OCR or vision** |
| `table-page.pdf` | text, with table hints | **both** |
| `drawing-page.pdf` | low density, with a scale statement | **both** |

- **Scanned page:** its body has no text, so it must not go to the model as a text page. Its content is unknown until OCR or vision runs, so treat it as unresolved evidence rather than "no provisions".
- **Table page:** reconstruct the rows before querying. The "see note 2" cell links to the 400 m bus-stop note. The last cell's text overflows its border, so check it in the render.
- **Drawing page:** the written dimension is 6.0 m and the scale is 1:200 @ A3. Keep those apart from any estimate taken from pixels. The drawing is routed `both` because of the scale statement, not its low character count.
- **Reading order:** the scan's header says page 7, but the file has one page. I assumed it is page 7 of a longer plan whose other pages weren't supplied. The script would flag pages 1–6 as missing if it used that number as the page number.

**Questions I couldn't ask, and what I assumed:**
- Is the "page 7" header the true page number? I assumed yes.
- Which extractor should I use? I assumed none, because the shell was disabled.
- Should the default thresholds stand? I assumed yes. Four pages can't calibrate them, and no page sits near a threshold.

**Left undone:**
- The script was not run, so re-run it on a real inventory and compare the output with this report.
- No OCR, no vision and no page rendering, so no model has seen the rendered table or drawing.
- No image-budget or cost sizing, because no provider limits or prices were given.
- No table row reconstruction.
- No comparison of the drawing's 6.0 m with Policy H3's 6.0 m detached limit.

Files are in the working directory:
- ingestion-report.json
- page-routes.md