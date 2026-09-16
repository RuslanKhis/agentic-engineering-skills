"""Optional current-result boundary for a narrow formatter; requires Pydantic 2.

Adapt this component into the target application only when its task needs this
contract. The limits come from an illustrative Chapter 4 handoff, not universal
ADK defaults. They bound the child input after the producer has already limited
query work and result materialisation. They do not authorise SQL, make data
trusted, persist results or identify the selected result on the caller's behalf.

Pass a plain dictionary to ``parse_formatting_input`` for a validated model or
``encode_formatting_input`` for the exact compact UTF-8 JSON sent to a child.
Both raise only ``FormattingInputError("invalid_formatting_input")`` for invalid
payloads, without the original validation exception in their exception chain.
Direct Pydantic validation is available for framework integration; report a
fixed public error rather than logging its ``errors()`` output or raw payload.
"""

import json
from typing import Annotated, Self

from pydantic import (
    BaseModel, BeforeValidator, ConfigDict, Field, ValidationError, model_validator,
)


MAX_PREVIEW_BYTES = 64 * 1024
ColumnName = Annotated[str, Field(min_length=1, max_length=128)]
CellText = Annotated[str, Field(max_length=1_000)]


def _plain_cell(value: object) -> object:
    # Pydantic's strict float still accepts some numeric objects such as Decimal.
    # The handoff contract preserves only plain JSON scalar types, without such
    # conversion losing precision before its encoded-byte check.
    if type(value) not in (str, int, float, bool, type(None)):
        raise ValueError("cells must be plain JSON scalar types")
    return value


Cell = Annotated[CellText | int | float | bool | None, BeforeValidator(_plain_cell)]


class FormattingInputError(ValueError):
    """Fixed public failure that contains no supplied preview or identifiers."""


def _compact_json(payload: dict) -> bytes:
    return json.dumps(
        payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"),
    ).encode("utf-8")


class FormattingInput(BaseModel):
    """Strict preview with an inclusive 64 KiB encoded JSON ceiling.

    Empty rows are valid: the caller can return an empty-result response without
    a model call. Lists remain mutable Python values, so ``canonical_bytes`` checks
    their current contents again immediately before constructing a handoff.
    """

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        allow_inf_nan=False,
        hide_input_in_errors=True,
        revalidate_instances="always",
    )

    correlation_id: str = Field(
        min_length=16, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$",
    )
    columns: list[ColumnName] = Field(min_length=1, max_length=64)
    rows: list[list[Cell]] = Field(max_length=20)

    @model_validator(mode="after")
    def check_preview(self) -> Self:
        if len(set(self.columns)) != len(self.columns):
            raise ValueError("column names must be unique")
        if any(len(row) != len(self.columns) for row in self.rows):
            raise ValueError("every row must match the column count")
        encoded = _compact_json(self.model_dump(mode="python"))
        if len(encoded) > MAX_PREVIEW_BYTES:
            raise ValueError("formatting input exceeds the byte limit")
        return self

    def canonical_bytes(self) -> bytes:
        """Recheck mutable contents and return the exact bounded UTF-8 payload."""
        return encode_formatting_input({
            "correlation_id": self.correlation_id,
            "columns": self.columns,
            "rows": self.rows,
        })


def parse_formatting_input(payload: object) -> FormattingInput:
    """Validate a plain decoded object without changing it or leaking errors.

    This accepts a decoded dictionary, not a JSON string, DataFrame or existing
    model instance. Bound any raw input before decoding it. Pydantic copies the
    validated lists; callers should still construct and pass the current result.
    """
    if type(payload) is dict:
        try:
            result = FormattingInput.model_validate(payload)
        except (ValidationError, ValueError, TypeError, OverflowError):
            pass
        else:
            return result
    # Raising outside the handler avoids retaining input-bearing exceptions as
    # __context__, including in diagnostics that inspect exception chains.
    raise FormattingInputError("invalid_formatting_input")


def encode_formatting_input(payload: object) -> bytes:
    """Return validated compact JSON; UTF-8 bytes include escaping overhead."""
    validated = parse_formatting_input(payload)
    return _compact_json(validated.model_dump(mode="python"))
