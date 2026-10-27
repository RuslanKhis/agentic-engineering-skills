"""Deployment settings."""
import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "lindqvist-claims-prod")
SECURITY_LOCATION = os.environ.get("MODEL_ARMOR_LOCATION", "europe-west4")
INPUT_TEMPLATE = (f"projects/{PROJECT_ID}/locations/{SECURITY_LOCATION}/templates/"
                  + os.environ.get("MODEL_ARMOR_INPUT_TEMPLATE", "claims-input"))
MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024
# Model Armor file screening accepts 69 bytes to 4 MB; a file outside that cannot be screened.
SCREENABLE_FILE_MIN_BYTES = 69
SCREENABLE_FILE_MAX_BYTES = 4 * 1024 * 1024
SCREEN_FILE_TIMEOUT_S = float(os.environ.get("MODEL_ARMOR_FILE_TIMEOUT_S", "30"))
# "raw" or "base64": how bytes go into ByteDataItem.byte_data. Unresolved until the live canary
# in infra/modelarmor/README.md has run; a wrong choice reads as a silent NO_MATCH_FOUND.
BYTE_DATA_ENCODING = os.environ.get("MODEL_ARMOR_BYTE_ENCODING", "raw")
MODEL_ID = os.environ.get("MODEL_ID", "gemini-3.5-flash")
