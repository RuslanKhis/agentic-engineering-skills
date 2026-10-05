# Qualify document ingestion before the first model call

Read this when the corpus arrives as PDFs, scans, drawings or tables rather
than clean text, and the answer depends on what those pages actually contain.
A page whose text layer holds only a running header is a scan, whatever the
extractor returns. Decide per page what the model will see, and keep that
decision with the case. [Local-document coverage](local-document-coverage.md)
diagnoses misses afterwards; this reference prevents the first class of them.

## Produce an ingestion report before any model call

Run the target's extractor over every page once, then qualify the result:

```bash
"$PYTHON" "$SKILL_DIR/scripts/qualify_ingestion.py" --inventory /path/to/inventory.json
"$PYTHON" "$SKILL_DIR/scripts/qualify_ingestion.py" --pdf /path/to/document.pdf   # needs pypdf
```

Set `PYTHON` to the project's interpreter and `SKILL_DIR` to this installed
skill. The inventory is a list of page records from your extractor:
`document`, `page`, `text`, `image_count` and, where known, `vector_drawing_ops`.
The report gives each page its character count, alphanumeric ratio, density
class (`text`, `low_density`, `image_only`), table and drawing hints, the
written dimensions and scale statements found in the text layer, and a route.
Its summary lists low-density pages, image-only pages, table and drawing
candidates, reading-order anomalies (missing, duplicate or out-of-order page
numbers) and the number of images a full visual pass would send.

The report is an input, not a log entry. Store it beside the case so the
officer, the reviewer stage and the drafting model can all see which pages
were read as text, which were rendered, and which were never read at all.
Exit code 0 means a report was produced; the report itself is information.
Exit 2 means the PDF route is blocked because `pypdf` is absent: supply the
inventory from the extractor the project already uses.

## Route scanned and low-density pages

Classify by the text the extractor returned, not by the file's claim to be
text-based:

| Observation | Class | Route |
| --- | --- | --- |
| Empty text layer with an image | `image_only` | OCR or vision pass |
| Fewer characters than the threshold, or a low alphanumeric ratio | `low_density` | OCR or vision pass |
| Enough legible characters, no table or drawing hints | `text` | Text |
| Table or drawing hints at any density | as observed | Text and image together |

Header-only extraction counts as low density: thirty characters with a
perfect alphanumeric ratio is still a scan. The defaults (200 characters,
ratio 0.5, eight vector operations with a written dimension) follow the
text-density and alphanumeric-ratio heuristics that
[pdf-inspector](https://instagit.com/firecrawl/pdf-inspector/how-to-detect-pdf-text-vs-scanned-pdf-inspector/)
uses to separate text pages from scans (pattern reviewed 6 October 2026).
Calibrate them on the supplied corpus: sort pages by character count, look at
the pages around the threshold, and record the values chosen with the case.

Label every piece of text the model receives by origin: `native` for the
extractor's text layer, `ocr` for an OCR pass, `vision` for a model's reading
of a rendered page. Keep the label through retrieval and citation so a
conclusion drawn from OCR output can be traced back to the pass that produced
it. OCR confidence and legibility ride along as fields, never as prose.

## Choose text, image or both per page

- Send the rendered page image when the page has drawings, tables or low
  text density. Send the text layer alone otherwise.
- Send both when the model flags a page as unclear, and record that flag.
- Record the choice per page in the report; a later stage can then tell
  whether a missing fact was on a page the model never saw.

Rendering resolution is a per-corpus decision. Drawings need enough pixels to
read dimension labels; table pages need enough to keep cell boundaries. Pick
one resolution per page class from a sample, keep it in configuration, and
record it with the report.

## Size the image budget from the corpus

Measure once on the supplied data before choosing caps:

```text
pages_per_case         = median and maximum pages across the development cases
visual_pages_per_case  = pages routed ocr_or_vision or both, from the report
images_per_call        = provider limit or the number the model reads reliably
calls_for_visual_pass  = ceil(visual_pages_per_case / images_per_call)
cost_of_visual_pass    = calls_for_visual_pass × (image tokens + prompt tokens) × rate
```

Fill the template with observed values and current provider prices, dated.
If a full visual pass for the largest case exceeds the allowance, choose which
page classes are rendered first (drawings cited by the decision, then tables,
then scans) and record the pages left unread as unresolved evidence rather than
as absent provisions.

## Reconstruct tables and read drawings

For tables, reconstruct rows before asking for values: cell text in reading
order, a header row, continuation markers such as "see note 2" joined to the
note they cite. A model asked for "the parking standard for three bedrooms"
should receive the row, not the page. Verify the reconstruction on the fixture
table page and on two real dense tables from the corpus.

For drawings, extract written dimensions and scale statements as separate
fields (the report already does this for the text layer) and let the model
reason about them. A value estimated from pixels is an estimate: label it as
`pixel_estimate` with the scale assumption used, alongside any written
dimension. [Govern the visual branch](local-document-coverage.md#govern-the-visual-branch)
explains why these are different evidence types and how an unreviewed image
stays unresolved.

## Run the fixture

The fixture directory `assets/ingestion-fixture/` holds four synthetic one-page
PDFs with real bytes and an [inventory](../assets/ingestion-fixture/inventory.json),
produced by [`make_ingestion_fixture.py`](../scripts/make_ingestion_fixture.py):

| File | What it is | Expected route |
| --- | --- | --- |
| `text-page.pdf` | A fictional residential-extension policy citing an SPD table | `text` |
| `scanned-page.pdf` | A running header plus a raster body with no glyphs | `ocr_or_vision` |
| `table-page.pdf` | A parking-standards table with a continued note | `both` |
| `drawing-page.pdf` | A site plan with a scale bar, "Scale 1:200" and a written 6.0 m dimension | `both` |

`inventory.json` beside them is what the generator knows it wrote, not an
extraction result. Run the project's extractor over the PDFs, qualify its
output, and compare with the committed inventory to see what the extractor
dropped. The [tests](../tests/test_ingestion_qualification.py) establish the
classification rules, deterministic generation and the pypdf path when that
package is installed:

```bash
"$PYTHON" -m pytest "$SKILL_DIR/tests/test_ingestion_qualification.py" -q -p no:cacheprovider
```

They run no OCR engine, send no image to a model and claim no domain review of
the fictional policy. A passing suite shows that the routing logic behaves as
described; whether a real OCR pass reads the corpus legibly is measured on the
corpus.

## Completion

Every page in the case has a density class, a route and an origin label for
its text, recorded in a report retained with the case. Low-density pages are
never passed to the model as text pages. Thresholds and rendering resolution
were calibrated on the supplied corpus and recorded. Pages left unread because
of the image budget appear as unresolved evidence in the report.
