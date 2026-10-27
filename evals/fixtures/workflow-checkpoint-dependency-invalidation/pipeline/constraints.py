"""Site constraints stage: looks the address up in the council's constraint layers.

Independent of the application documents and of the writer; the export lists the
constraints beside the decision. The layers file is versioned by the GIS team.
"""
from __future__ import annotations

import json
from pathlib import Path

LAYERS = Path(__file__).resolve().parent.parent / "cases" / "constraint-layers.json"


def load_layers(path: Path = LAYERS) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def site_constraints(address: str, layers: dict | None = None) -> dict:
    layers = layers or load_layers()
    hits = [layer["name"] for layer in layers["layers"] if address in layer["addresses"]]
    return {"address": address, "layers_version": layers["version"], "constraints": hits}
