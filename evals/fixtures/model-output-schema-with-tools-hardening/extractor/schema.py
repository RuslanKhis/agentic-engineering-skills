"""The record the claims queue accepts."""
from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Party(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Vehicle(BaseModel):
    registration: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


class Incident(BaseModel):
    occurred_on: Optional[date] = None
    location: Optional[str] = None
    description: Optional[str] = None
    third_party: Optional[Party] = None
    police_reference: Optional[str] = None


class Repairer(BaseModel):
    repairer_id: Optional[str] = None
    name: Optional[str] = None
    estimate_pence: Optional[int] = None


class ClaimExtraction(BaseModel):
    claim_reference: str = Field(description="The claim reference from the email subject, e.g. CLM-2026-04411")
    policy_number: Optional[str] = None
    policy_status: Optional[Literal["active", "lapsed", "not_found"]] = None
    claimant: Optional[Party] = None
    vehicle: Optional[Vehicle] = None
    incident: Optional[Incident] = None
    injuries_reported: Optional[bool] = None
    repairer: Optional[Repairer] = None
    claim_type: Literal["collision", "theft", "glass", "fire", "other"]
    fault_admitted: Optional[bool] = None
    urgency: Literal["routine", "priority", "urgent"]
    missing_information: list[str] = Field(default_factory=list)
