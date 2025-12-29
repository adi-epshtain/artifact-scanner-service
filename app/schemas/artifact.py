import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import ScanResult, ScanStatus


class ArtifactCreateRequest(BaseModel):
    """Request schema for creating a new artifact."""
    name: str
    type: str
    source: str


class ArtifactStatusResponse(BaseModel):
    """Response schema for artifact status."""
    id: uuid.UUID
    status: ScanStatus
    result: ScanResult
    exit_code: Optional[int]


class ArtifactCreateResponse(BaseModel):
    """Response schema for artifact creation."""
    id: uuid.UUID
    status: ScanStatus


class ArtifactResponse(BaseModel):
    """Full artifact response schema."""
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

