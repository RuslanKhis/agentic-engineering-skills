I've written the ingestion report and per-page route, but I couldn't run the skill's `qualify_ingestion.py` because this session has no shell. Instead I applied its documented rules by hand to the text, image and drawing operators in the PDF bytes of `pack/*.pdf`. Re-run the script before relying on exact figures.

| Page | Route | Why |
| --- | --- | --- |
| `text-page.pdf` | **text** | About 800 characters of native text, no table or drawing hints. |
| `scanned-page.pdf` | **ocr_or_vision** | The text layer is a 34-character running header over an embedded image, so it is a scan despite the clean header. |
| `table-page.pdf` | **both** | Table hint. Its rows need reconstructing, with "see note 2" joined to the note it cites. |
| `drawing-page.pdf` | **both** | Has the "Scale 1:200" statement and the written "6.0 m". The "10 m" on the scale bar is a scale label, not a building dimension. |

- **Visual pass:** it would send 3 images.
- **Unread:** the body of the scanned page. It is recorded as unresolved evidence, not as absent content.
- **Reading order:** no anomalies.
- **Extractor evidence:** the shipped `inventory.json` is generator knowledge, so I didn't use it as extraction evidence. It differs from the real PDFs: it adds `|` separators and omits the table caption.

The report states these assumptions, in place of questions I couldn't ask:
- The real pipeline uses a text layer like pypdf's.
- The default thresholds (200 characters, 0.5 alphanumeric ratio, 8 vector operations) are kept, since four pages can't calibrate them.
- `pack/` matches the skill's fixture; I did not compare the bytes.

Left undone:
- No OCR, vision, rendering or model call.
- No render resolution or image-per-call limit chosen, and no cost estimate.
- No pixel estimate from the drawing, and no judgement on what the "6.0 m" label measures. That needs the image.
- Script re-run and byte comparison with the fixture.

Files are in the workspace root:
- `ingestion-report.json`
- `ingestion-report.md`