"""Observe one session read without recording its identifiers or exceptions.

This importable component does not configure a provider, exporter, HTTP server
or session backend. Pass the tracer and service already owned by the calling
process. It preserves the backend's result and exception, including cancellation.

The policy covers only this custom span. Parent spans, native ADK instrumentation,
resource attributes and application logs need their own content policy at the
final export boundary. Message-capture flags alone are not that policy.
"""

import asyncio

from opentelemetry.trace import Status, StatusCode


async def load_session_safely(
    tracer,
    service,
    *,
    app_name: str,
    user_id: str,
    session_id: str,
    store_kind: str,
):
    """Return the session while exposing only a fixed operation and safe labels.

    ``store_kind`` must be ``managed`` or ``postgresql`` and should describe the
    backend the application actually wired. This function does not select or
    construct it. Invalid labels fail before a span or backend read is started.
    Apply the caller's bounded timeout and cancellation policy outside this read;
    the component does not add retries or change storage behaviour.
    """
    if type(store_kind) is not str or store_kind not in {"managed", "postgresql"}:
        raise ValueError("Unsupported store label")
    with tracer.start_as_current_span(
        "session.load",
        record_exception=False,
        set_status_on_exception=False,
    ) as span:
        span.set_attribute("session.store", store_kind)
        try:
            session = await service.get_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
            )
        except BaseException as error:
            category = (
                "timeout" if isinstance(error, TimeoutError) else
                "cancelled" if isinstance(error, asyncio.CancelledError) else
                "session_error"
            )
            span.set_attribute("error.type", category)
            span.set_status(Status(StatusCode.ERROR))
            raise
        span.set_attribute("session.found", session is not None)
        return session
