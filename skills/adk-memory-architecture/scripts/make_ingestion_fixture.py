"""Write four small synthetic PDFs with real bytes for ingestion qualification.

The pages are fictional planning material: a text page, a scanned page whose
only text layer is a running header, a parking-standards table and a site
plan with a scale bar. Output is deterministic: no timestamps, no randomness,
so repeated runs produce identical bytes.

`inventory.json` beside the PDFs records what this generator KNOWS it wrote
(the text placed in each text layer, image and vector operation counts). It
is generator knowledge, not an extraction result. A target project's own
extractor must produce its inventory from the bytes; compare the two to
measure that extractor, never substitute one for the other.

Standard library only. See references/document-ingestion.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import zlib


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "ingestion-fixture"
PAGE_WIDTH = 595
PAGE_HEIGHT = 842


def pdf_string(text: str) -> str:
    """Escape text for a PDF literal string (WinAnsi-compatible ASCII only)."""
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return f"({escaped})"


def text_op(x: float, y: float, text: str, size: int = 11) -> str:
    return f"BT /F1 {size} Tf {x:.1f} {y:.1f} Td {pdf_string(text)} Tj ET\n"


def build_pdf(content: str, extra_objects: list[bytes] | None = None,
              xobject_name: str | None = None) -> bytes:
    """Assemble a one-page PDF with Helvetica and optional image XObject."""
    extra_objects = extra_objects or []
    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    resources = "<< /Font << /F1 4 0 R >>"
    if xobject_name:
        resources += f" /XObject << /{xobject_name} 6 0 R >>"
    resources += " >>"
    objects.append(
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
        f"/Resources {resources} /Contents 5 0 R >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
                   b"/Encoding /WinAnsiEncoding >>")
    stream = content.encode("latin-1")
    objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
                   + stream + b"\nendstream")
    objects.extend(extra_objects)

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode("ascii") + body + b"\nendobj\n"
    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode("ascii")
    out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n").encode("ascii")
    return bytes(out)


TEXT_PAGE_LINES = [
    ("Policy H3 Residential extensions", 16),
    ("Extensions to dwellings are supported where the proposal respects the", 11),
    ("scale, form and materials of the host building and the character of the", 11),
    ("street. Rear extensions should not exceed a depth of 4.0 m for terraced", 11),
    ("dwellings or 6.0 m for detached dwellings unless the applicant shows that", 11),
    ("no material loss of daylight or outlook results to a neighbouring room.", 11),
    ("Side extensions are set back from the front elevation and keep a minimum", 11),
    ("1.0 m gap to the side boundary where a terracing effect would otherwise", 11),
    ("occur. Off-street parking is assessed against Table 2 of the Design SPD,", 11),
    ("which sets the minimum spaces by bedroom count and accessibility.", 11),
    ("Proposals that remove a parking space must show that the replacement", 11),
    ("provision meets that table or that the site lies within Zone A.", 11),
]

TABLE_ROWS = [
    ("Dwelling size", "Minimum spaces", "Cycle spaces", "Note"),
    ("1 bedroom", "1", "1", "Zone A: 0"),
    ("2-3 bedrooms", "2", "2", "see note 2"),
    ("4+ bedrooms", "3", "2", "Tandem spaces count once"),
]


def text_page() -> tuple[bytes, dict]:
    content = ""
    y = 780
    for line, size in TEXT_PAGE_LINES:
        content += text_op(60, y, line, size)
        y -= 20 if size == 11 else 30
    text = "\n".join(line for line, _ in TEXT_PAGE_LINES)
    return build_pdf(content), {"text": text, "image_count": 0, "vector_drawing_ops": 0}


def scanned_page() -> tuple[bytes, dict]:
    """A raster body standing in for a scan: dark bands as text lines, no glyphs."""
    width, height = 120, 160
    rows = bytearray()
    for row in range(height):
        band = 12 <= row <= 150 and (row % 8) in (2, 3)
        margin_left, margin_right = 10, 110
        for col in range(width):
            if band and margin_left <= col <= margin_right and (row // 8) % 5 != 4:
                rows.append(40)
            else:
                rows.append(235 if (row + col) % 7 else 225)
    image_data = zlib.compress(bytes(rows), 9)
    image_object = (b"<< /Type /XObject /Subtype /Image /Width 120 /Height 160 "
                    b"/ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode "
                    b"/Length " + str(len(image_data)).encode("ascii") + b" >>\nstream\n"
                    + image_data + b"\nendstream")
    header = "Synthetic Local Plan 2021 - page 7"
    content = text_op(60, 810, header, 9)
    content += "q 475 0 0 700 60 80 cm /Im1 Do Q\n"
    return (build_pdf(content, [image_object], "Im1"),
            {"text": header, "image_count": 1, "vector_drawing_ops": 0})


def table_page() -> tuple[bytes, dict]:
    content = text_op(60, 780, "Table 2 Parking standards (Design SPD)", 13)
    columns = [60, 200, 320, 420, 535]
    top, row_height = 740, 24
    vector_ops = 0
    content += "0.5 w\n"
    for index in range(len(TABLE_ROWS) + 1):
        y = top - index * row_height
        content += f"{columns[0]} {y} m {columns[-1]} {y} l S\n"
        vector_ops += 1
    bottom = top - len(TABLE_ROWS) * row_height
    for x in columns:
        content += f"{x} {top} m {x} {bottom} l S\n"
        vector_ops += 1
    lines = []
    for row_index, row in enumerate(TABLE_ROWS):
        y = top - row_index * row_height - 16
        for cell, x in zip(row, columns):
            content += text_op(x + 4, y, cell, 10)
        lines.append(" | ".join(row))
    note = "Note 2: within 400 m of a frequent bus stop the standard reduces by 1 space."
    content += text_op(60, bottom - 30, note, 10)
    lines.append(note)
    return build_pdf(content), {"text": "\n".join(lines), "image_count": 0,
                                "vector_drawing_ops": vector_ops}


def drawing_page() -> tuple[bytes, dict]:
    content = text_op(60, 800, "Proposed site plan - 14 Synthetic Road", 12)
    vector_ops = 0
    content += "1 w\n"
    # Site boundary, existing dwelling, proposed extension.
    for x, y, w, h in ((80, 200, 420, 520), (160, 420, 220, 200), (160, 330, 220, 90)):
        content += f"{x} {y} {w} {h} re S\n"
        vector_ops += 1
    # Dimension line for the extension depth.
    content += "400 330 m 400 420 l S\n"
    vector_ops += 1
    content += text_op(410, 370, "6.0 m", 10)
    # Scale bar: alternating filled segments.
    for index in range(4):
        x = 80 + index * 40
        fill = "0 g" if index % 2 == 0 else "1 g"
        content += f"{fill} {x} 150 40 8 re f 0 G {x} 150 40 8 re S\n"
        vector_ops += 2
    content += "0 g\n"
    content += text_op(78, 140, "0", 9) + text_op(158, 140, "5", 9) + text_op(238, 140, "10 m", 9)
    content += text_op(80, 120, "Scale 1:200 @ A3", 10)
    # North arrow.
    content += "520 760 m 520 800 l S\n510 790 m 520 800 l 530 790 l S\n"
    vector_ops += 2
    content += text_op(516, 805, "N", 10)
    content += text_op(170, 360, "Proposed extension", 9)
    content += text_op(170, 500, "Existing dwelling", 9)
    text = "\n".join([
        "Proposed site plan - 14 Synthetic Road", "6.0 m", "0", "5", "10 m",
        "Scale 1:200 @ A3", "N", "Proposed extension", "Existing dwelling"])
    return build_pdf(content), {"text": text, "image_count": 0,
                                "vector_drawing_ops": vector_ops}


BUILDERS = {
    "text-page.pdf": text_page,
    "scanned-page.pdf": scanned_page,
    "table-page.pdf": table_page,
    "drawing-page.pdf": drawing_page,
}


def write_fixture(output: Path) -> list[dict]:
    """Write the PDFs and inventory; return the inventory records."""
    output.mkdir(parents=True, exist_ok=True)
    inventory = []
    for filename, builder in BUILDERS.items():
        data, known = builder()
        (output / filename).write_bytes(data)
        inventory.append({"document": filename, "page": 1, **known})
    manifest = {
        "kind": "generator_knowledge_not_extraction_result",
        "note": "Text, image and vector counts are what make_ingestion_fixture.py wrote. "
                "Produce a separate inventory from your own extractor and compare.",
        "pages": inventory,
    }
    (output / "inventory.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                           encoding="utf-8")
    return inventory


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT,
                        help="directory for the PDFs and inventory.json")
    args = parser.parse_args()
    records = write_fixture(args.output)
    for record in records:
        print(f"{record['document']}: {len(record['text'])} chars written, "
              f"{record['image_count']} image(s), {record['vector_drawing_ops']} vector ops")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
