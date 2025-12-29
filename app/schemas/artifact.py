import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import ScanResult, ScanStatus


class ArtifactCreateRequest(BaseModel):
    name: str
    type: str
    source: str


class ArtifactCreateResponse(BaseModel):
    id: uuid.UUID
    status: ScanStatus


class ArtifactResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    source: str
    status: ScanStatus
    result: ScanResult
    exit_code: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime

