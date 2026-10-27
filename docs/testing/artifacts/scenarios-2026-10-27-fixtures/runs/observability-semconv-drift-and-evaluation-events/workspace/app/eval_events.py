"""Emit judge scores as ``gen_ai.evaluation.result`` log events attached to the evaluated span's trace.

Spans are immutable once exported, so the score travels as a log record whose trace context is the evaluated
span. The event and its attributes are Development status in the GenAI conventions (semantic-conventions-genai
commit 9ffc7e0, read 2026-10-22); the judge attributes use our own namespace because the conventions define none.
"""
from __future__ import annotations

import re

EVENT_NAME = "gen_ai.evaluation.result"
_TRACE_ID = re.compile(r"^[0-9a-f]{32}$")
_SPAN_ID = re.compile(r"^[0-9a-f]{16}$")


def build_event(row: dict, rubric_version: str) -> dict | None:
    """Map one judge_scores row to an event, or None when the row has no usable trace context."""
    trace_id, span_id = str(row.get("trace_id", "")).lower(), str(row.get("span_id", "")).lower()
    if not (_TRACE_ID.match(trace_id) and _SPAN_ID.match(span_id)):
        return None
    attributes = {
        "gen_ai.evaluation.name": row["metric"],
        "gen_ai.evaluation.score.value": row["score"],
        "gen_ai.evaluation.score.label": row["label"],
        "support.judge.model": row["judge_model"],
        "support.judge.rubric_version": rubric_version,
    }
    return {"event_name": EVENT_NAME, "trace_id": int(trace_id, 16), "span_id": int(span_id, 16),
            "attributes": attributes}


def emit_events(rows: list[dict], rubric_version: str, emit) -> int:
    """Call ``emit(event)`` for each mappable row; return how many rows were skipped."""
    skipped = 0
    for row in rows:
        event = build_event(row, rubric_version)
        if event is None:
            skipped += 1
        else:
            emit(event)
    return skipped


def otlp_emitter():
    """Return ``(emit, flush)`` that send events through OTLP/HTTP using OTEL_EXPORTER_OTLP_* settings."""
    from opentelemetry._logs import LogRecord
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.trace import TraceFlags

    import os

    provider = LoggerProvider(resource=Resource.create(
        {"service.name": os.environ.get("OTEL_SERVICE_NAME", "support-assistant")}))
    provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    logger = provider.get_logger("support.nightly_judge")

    def emit(event: dict) -> None:
        logger.emit(LogRecord(event_name=event["event_name"], trace_id=event["trace_id"],
                              span_id=event["span_id"], trace_flags=TraceFlags(TraceFlags.SAMPLED),
                              attributes=event["attributes"]))

    return emit, provider.force_flush
