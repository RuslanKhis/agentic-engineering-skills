"""Push infra/modelarmor/input-template.json to Model Armor.

Usage: python scripts/apply_template.py
"""
import json
from pathlib import Path

from google.cloud import modelarmor_v1

TEMPLATE_FILE = Path(__file__).resolve().parents[1] / "infra" / "modelarmor" / "input-template.json"


def main() -> None:
    spec = json.loads(TEMPLATE_FILE.read_text())
    client = modelarmor_v1.ModelArmorClient()
    template = modelarmor_v1.Template(spec)
    updated = client.update_template(request=modelarmor_v1.UpdateTemplateRequest(template=template))
    print(f"updated {updated.name}")


if __name__ == "__main__":
    main()
