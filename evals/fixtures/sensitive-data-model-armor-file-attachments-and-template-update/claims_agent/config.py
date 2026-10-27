"""Deployment settings."""
import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "lindqvist-claims-prod")
SECURITY_LOCATION = os.environ.get("MODEL_ARMOR_LOCATION", "europe-west4")
INPUT_TEMPLATE = (f"projects/{PROJECT_ID}/locations/{SECURITY_LOCATION}/templates/"
                  + os.environ.get("MODEL_ARMOR_INPUT_TEMPLATE", "claims-input"))
MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024
MODEL_ID = os.environ.get("MODEL_ID", "gemini-3.5-flash")
