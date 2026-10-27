"""Generate the memory-ingestion-scan-detection pack and its inventory (judge-only).

Four one-page PDFs from a fictional shopfront application to a fictional
borough: a policy text page, a scanned page whose only text layer is a
running header, a cycle-parking table drawn with vector rules, and a rear
elevation drawing with a written dimension and a scale bar. Deterministic
output (no timestamps, no randomness). Standard library only and written
independently of the memory skill's own generator, so the pack is not the
skill's worked example.

``write_pack(pack_dir, inventory_path)`` writes the PDFs into ``pack_dir``
and the inventory (what this generator placed on each page: text layer,
image count, vector operations and the route a correct qualification takes)
to ``inventory_path``. The committed copies are
evals/fixtures/memory-ingestion-scan-detection/pack/ (agent-visible) and
evals/graders/memory-ingestion-scan-detection/inventory.json (judge-only).

    python make_pack.py <pack_dir> <inventory_path>
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import zlib

WIDTH, HEIGHT = 842, 595  # A4 landscape


def _escape(text: str) -> str:
    return "(" + text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


def _show(x: float, y: float, text: str, size: float = 10.5, font: str = "F1") -> str:
    return f"BT /{font} {size:g} Tf 1 0 0 1 {x:g} {y:g} Tm {_escape(text)} Tj ET\n"


def _assemble(stream: str, image: bytes | None = None, image_size: tuple[int, int] = (0, 0)) -> bytes:
    """One-page PDF: catalog, pages, page, two Type1 fonts, content, optional grey image."""
    resources = "/Font << /F1 4 0 R /F2 5 0 R >>"
    if image is not None:
        resources += " /XObject << /Scan 7 0 R >>"
    content = stream.encode("latin-1")
    bodies = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {WIDTH} {HEIGHT}] "
         f"/Resources << {resources} >> /Contents 6 0 R >>").encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>",
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
    ]
    if image is not None:
        packed = zlib.compress(image, 9)
        bodies.append((f"<< /Type /XObject /Subtype /Image /Width {image_size[0]} /Height {image_size[1]} "
                       f"/ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode "
                       f"/Length {len(packed)} >>\nstream\n").encode("ascii") + packed + b"\nendstream")
    out = bytearray(b"%PDF-1.5\n%\xc7\xec\x8f\xa2\n")
    offsets = []
    for number, body in enumerate(bodies, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(bodies) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(bodies) + 1, xref)
    return bytes(out)


POLICY_TITLE = "DC7 Shopfronts and advertisements"
POLICY_LINES = [
    "New and replacement shopfronts in the Market Street conservation area keep the",
    "traditional elements of pilasters, fascia, stall riser and cornice, and use timber",
    "or painted metal frames. Internally illuminated box fascias are not acceptable;",
    "lettering is applied or hand-painted and may be lit by discreet trough lights.",
    "Roller shutters are fitted internally and are of an open lattice design; solid",
    "external shutters are refused unless the premises is a pharmacy open after 22:00.",
    "Fascia depth does not exceed 0.6 m or one fifth of the shopfront height, whichever",
    "is less. Projecting signs are limited to one per frontage and sit at fascia level.",
    "Cycle parking for staff and customers is provided in line with Table C1 of the",
    "Borough Transport SPD, or by a contribution where the pavement is under 2.5 m wide.",
]


def policy_page() -> tuple[bytes, dict]:
    stream = _show(70, 520, POLICY_TITLE, 15, "F2")
    y = 490.0
    for line in POLICY_LINES:
        stream += _show(70, y, line)
        y -= 17
    stream += _show(70, 60, "Example Borough Design Code 2024 - section 4", 8)
    text = "\n".join([POLICY_TITLE, *POLICY_LINES, "Example Borough Design Code 2024 - section 4"])
    return _assemble(stream), {"text": text, "image_count": 0, "vector_drawing_ops": 0,
                                "route": "text", "kind": "text"}


def scanned_page() -> tuple[bytes, dict]:
    """A raster body standing in for a photocopied page: grey ground, dark line bands, no glyphs."""
    width, height = 160, 112
    pixels = bytearray()
    for row in range(height):
        in_body = 14 <= row <= 100
        line_band = (row - 14) % 6 in (1, 2)
        paragraph_gap = ((row - 14) // 6) % 7 == 6
        for col in range(width):
            ink = in_body and line_band and not paragraph_gap and 12 <= col <= 148 - (row % 5) * 6
            speckle = (row * 31 + col * 17) % 23 == 0
            pixels.append(55 if ink else (205 if speckle else 238))
    header = "Example Borough Local Plan 2019 - page 12"
    stream = _show(60, 565, header, 8)
    stream += "q 720 0 0 504 60 40 cm /Scan Do Q\n"
    return (_assemble(stream, bytes(pixels), (width, height)),
            {"text": header, "image_count": 1, "vector_drawing_ops": 0,
             "route": "ocr_or_vision", "kind": "scanned body, header-only text layer"})


TABLE = [
    ("Use class", "Floor area", "Staff spaces", "Visitor spaces", "Notes"),
    ("Retail (E(a))", "up to 500 m2", "1 per 175 m2", "2 minimum", "Sheffield stands"),
    ("Retail (E(a))", "over 500 m2", "1 per 175 m2", "1 per 250 m2", "see note b"),
    ("Cafe (E(b))", "any", "1 per 100 m2", "1 per 40 m2", "see note b"),
    ("Hot food (sui generis)", "any", "1 per 100 m2", "2 minimum", "covered spaces"),
]
TABLE_NOTE = "Note b: where the footway is under 2.5 m wide a commuted sum replaces visitor spaces."


def table_page() -> tuple[bytes, dict]:
    title = "Table C1 Cycle parking for commercial units (Borough Transport SPD)"
    stream = _show(60, 540, title, 12, "F2")
    xs = [60, 230, 340, 470, 600, 780]
    top, step = 510, 26
    rules = 0
    stream += "0.6 w 0 G\n"
    for i in range(len(TABLE) + 1):
        y = top - i * step
        stream += f"{xs[0]} {y} m {xs[-1]} {y} l S\n"
        rules += 1
    bottom = top - len(TABLE) * step
    for x in xs:
        stream += f"{x} {top} m {x} {bottom} l S\n"
        rules += 1
    lines = [title]
    for r, row in enumerate(TABLE):
        y = top - r * step - 17
        for c, (cell, x) in enumerate(zip(row, xs)):
            stream += _show(x + 5, y, cell, 9.5, "F2" if r == 0 else "F1")
        lines.append(" | ".join(row))
    stream += _show(60, bottom - 28, TABLE_NOTE, 9.5)
    lines.append(TABLE_NOTE)
    return _assemble(stream), {"text": "\n".join(lines), "image_count": 0, "vector_drawing_ops": rules,
                                "route": "text_and_image", "kind": "table"}


def drawing_page() -> tuple[bytes, dict]:
    labels = []

    def label(x, y, text, size=9.0, font="F1"):
        labels.append(text)
        return _show(x, y, text, size, font)

    stream = label(60, 560, "Proposed rear elevation - 3 Example Mews", 13, "F2")
    ops = 0
    stream += "0.8 w 0 G\n"
    # Ground line, existing wall, new single-storey projection and a door opening.
    for x, y, w, h in ((100, 120, 600, 0.01), (140, 120, 300, 300), (440, 120, 180, 150), (500, 120, 60, 110)):
        stream += f"{x} {y} {w:g} {h:g} re S\n"
        ops += 1
    # Pitched roof of the projection.
    stream += "440 270 m 530 330 l 620 270 l S\n"
    ops += 1
    # Height dimension with ticks.
    stream += "650 120 m 650 270 l S 644 120 m 656 120 l S 644 270 m 656 270 l S\n"
    ops += 3
    stream += label(660, 190, "3.2 m to eaves")
    # Scale bar 0-4 m in alternating blocks.
    for i in range(4):
        shade = "0 g" if i % 2 == 0 else "1 g"
        stream += f"{shade} {100 + i * 45} 70 45 6 re f 0 G {100 + i * 45} 70 45 6 re S\n"
        ops += 2
    stream += "0 g\n"
    stream += label(97, 58, "0", 8) + label(187, 58, "2", 8) + label(275, 58, "4 m", 8)
    stream += label(100, 40, "Scale 1:100 @ A3")
    stream += label(470, 200, "New garden room")
    stream += label(220, 300, "Existing house")
    return _assemble(stream), {"text": "\n".join(labels), "image_count": 0, "vector_drawing_ops": ops,
                                "route": "text_and_image", "kind": "drawing",
                                "written_dimension": "3.2 m to eaves", "scale_statement": "Scale 1:100 @ A3"}


PAGES = {
    "01-design-code-dc7.pdf": policy_page,
    "02-local-plan-p12.pdf": scanned_page,
    "03-cycle-parking-table.pdf": table_page,
    "04-rear-elevation.pdf": drawing_page,
}


def write_pack(pack_dir: Path, inventory_path: Path) -> dict:
    """Write the four PDFs into pack_dir and the inventory to inventory_path; return the inventory."""
    pack_dir.mkdir(parents=True, exist_ok=True)
    pages = []
    for name, build in PAGES.items():
        data, known = build()
        (pack_dir / name).write_bytes(data)
        pages.append({"document": f"pack/{name}", "page": 1, **known})
    inventory = {
        "kind": "generator_knowledge_not_extraction_result",
        "note": "What make_pack.py placed on each page and the route a correct qualification "
                "takes. The scanned page's text layer is its running header only.",
        "pages": pages,
    }
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    return inventory


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    write_pack(Path(sys.argv[1]), Path(sys.argv[2]))
