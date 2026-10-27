import os

from google.adk.cli.fast_api import get_fast_api_app

from app.app_utils.telemetry import setup_telemetry

setup_telemetry()

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = get_fast_api_app(
    agents_dir=os.path.dirname(AGENT_DIR),
    web=False,
    otel_to_cloud=True,
    session_service_uri=None,
)
app.title = "travel-desk-agent"


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}
