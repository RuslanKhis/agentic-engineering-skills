"""Push the multi-language detection setting from infra/modelarmor/input-template.json.

Usage: python scripts/apply_template.py [--dry-run]

Only the fields in UPDATE_MASK are written. An update without a mask overwrites the whole
template, so everything else in the live template is left as it is. If the service refuses
the update, do not retry: the organisation floor setting (Platform Security) may be the cause.
"""
import json
import sys
import uuid
from pathlib import Path

TEMPLATE_FILE = Path(__file__).resolve().parents[1] / "infra" / "modelarmor" / "input-template.json"
UPDATE_MASK = ["template_metadata.multi_language_detection.enable_multi_language_detection"]


def build_request(modelarmor_v1, text: str):
    template = modelarmor_v1.Template.from_json(text)  # the file is camelCase JSON
    flag = template.template_metadata.multi_language_detection.enable_multi_language_detection
    if flag is not True:
        raise SystemExit("template file does not enable multi-language detection; nothing to apply")
    # Same file and mask give the same id, so a retry within the service's 60 minutes is a repeat.
    request_id = str(uuid.uuid5(uuid.NAMESPACE_URL, template.name + "|" + ",".join(UPDATE_MASK) + "|" + str(flag)))
    return modelarmor_v1.UpdateTemplateRequest(
        template=template, update_mask={"paths": UPDATE_MASK}, request_id=request_id)


def main(argv=None, client=None, modelarmor_v1=None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if modelarmor_v1 is None:
        from google.cloud import modelarmor_v1
    request = build_request(modelarmor_v1, TEMPLATE_FILE.read_text())
    if "--dry-run" in argv:
        print(f"would update {request.template.name}: {', '.join(UPDATE_MASK)} (request {request.request_id})")
        return
    client = client or modelarmor_v1.ModelArmorClient()
    updated = client.update_template(request=request)
    after = updated.template_metadata.multi_language_detection.enable_multi_language_detection
    print(f"updated {updated.name}: multi-language detection = {after}")
    if after is not True:
        raise SystemExit("read-back does not show multi-language detection enabled")


if __name__ == "__main__":
    main()
