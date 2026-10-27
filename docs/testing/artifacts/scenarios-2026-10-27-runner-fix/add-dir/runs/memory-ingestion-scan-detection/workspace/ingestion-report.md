# Ingestion report: pack/

Method: I read the raw PDF content streams by hand, because the shell was disabled and I could not run `qualify_ingestion.py` (it also needs pypdf, which I could not confirm). Character counts are hand tallies, not extractor output. Thresholds are the skill defaults (200 chars, alnum ratio 0.5, 8 vector ops). They were not calibrated on this corpus. All text is labelled `native`. Full detail is in `ingestion-report.json`.

| Page | Chars (approx) | Class | Route | Origin | Status |
| --- | --- | --- | --- | --- | --- |
| text-page.pdf | ~860 | text | text | native | Ready for the model. It cites SPD Table 2, which is on another page. |
| scanned-page.pdf | 34 (header only) | image_only | ocr_or_vision | none yet | **Unresolved.** The body is a 120x160 px gray raster and has not been read. |
| table-page.pdf | ~240 | text, with table hint | text and image | native | Rows reconstructed from the text layer (see below). The image pass is pending. |
| drawing-page.pdf | ~100 | low_density, with drawing hint | text and image | native | The written dimension and scale were captured. The geometry was not read visually. |

## Table 2 reconstruction (native text)
| Dwelling size | Min spaces | Cycle spaces | Note |
| --- | --- | --- | --- |
| 1 bedroom | 1 | 1 | Zone A: 0 |
| 2-3 bedrooms | 2 | 2 | see note 2 |
| 4+ bedrooms | 3 | 2 | Tandem spaces count once |

Note 2: within 400 m of a frequent bus stop the standard reduces by 1 space.

## Drawing
- Written dimension: `6.0 m`, beside the proposed extension.
- Scale statement: `Scale 1:200 @ A3`. The scale bar is labelled 0, 5 and 10 m.
- There are no pixel estimates. Any value measured from pixels must be labelled `pixel_estimate` with the 1:200 assumption.

## Summary
- Low density or image-only: scanned-page and drawing-page.
- A full visual pass would send 3 images (scanned, table, drawing).
- Reading order: each file is one page. The scanned header says "page 7", so the pack is an excerpt and pages 1-6 are missing. This is not a defect in the pack, but answers must not claim to cover the whole Local Plan.
- Unresolved evidence: the scanned-page body. Do not pass its header to the model as if it were the page. Any answer that depends on it must say the page was not read.

## Questions I could not ask, and the assumptions I used
1. Should the scanned page be OCR'd or sent to a vision model once one exists? I assumed it stays unresolved for now.
2. Is the pack meant to be complete? I assumed it is an excerpt, given "page 7".
3. What image budget and render resolution should apply? I set none. I suggest 150-200 dpi for the table and 200-300 dpi for the drawing, to be confirmed on a sample.
