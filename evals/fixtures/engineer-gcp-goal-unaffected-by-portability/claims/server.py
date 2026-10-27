"""FastAPI entrypoint on Cloud Run; the policyholder ID comes from the verified Identity Platform token."""
from __future__ import annotations

import os

from fastapi import Depends, FastAPI, Header, HTTPException
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.cloud import firestore
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from claims.agent import root_agent
from claims.firestore_repo import FirestoreClaims
from claims.tools import use_repository

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west2")
ENGINE_ID = os.environ["AGENT_ENGINE_ID"]

use_repository(FirestoreClaims(firestore.Client(project=PROJECT)))
runner = Runner(app_name="coastline_claims", agent=root_agent,
                session_service=VertexAiSessionService(project=PROJECT, location=LOCATION,
                                                       agent_engine_id=ENGINE_ID))
app = FastAPI()


def policyholder(authorization: str = Header(...)) -> str:
    try:
        claims = id_token.verify_firebase_token(authorization.removeprefix("Bearer "),
                                                google_requests.Request(), audience=PROJECT)
    except ValueError:
        raise HTTPException(status_code=401)
    return claims["sub"]
