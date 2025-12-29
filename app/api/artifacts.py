import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.core.database import SessionDep, async_session_factory
from app.dal.artifact_dal import create_artifact, get_artifact_by_id
from app.models.enums import ScanResult, ScanStatus
from app.schemas.artifact import (
    ArtifactCreateRequest,
    ArtifactCreateResponse,
    ArtifactResponse,
)
from app.services.artifact_service import run_artifact_scan

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post(
    "/",
    response_model=ArtifactCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_artifact_endpoint(
    request: ArtifactCreateRequest,
    background_tasks: BackgroundTasks,
    session: SessionDep,
) -> ArtifactCreateResponse:
    """Create a new artifact and trigger scan."""
    artifact = await create_artifact(
        session=session,
        name=request.name,
        type=request.type,
        source=request.source,
        status=ScanStatus.PENDING,
        result=ScanResult.NONE,
    )
    
    # Trigger scan in background with new session
    async def run_scan_with_session():
        async with async_session_factory() as bg_session:
            await run_artifact_scan(bg_session, artifact.id)
    
    background_tasks.add_task(run_scan_with_session)
    
    return ArtifactCreateResponse(
        id=artifact.id,
        status=artifact.status,
    )


@router.get("/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact_endpoint(
    artifact_id: uuid.UUID,
    session: SessionDep,
) -> ArtifactResponse:
    """Get artifact by ID."""
    artifact = await get_artifact_by_id(session, artifact_id)
    
    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact not found",
        )
    
    return ArtifactResponse(
        id=artifact.id,
        name=artifact.name,
        type=artifact.type,
        source=artifact.source,
        status=artifact.status,
        result=artifact.result,
        exit_code=artifact.exit_code,
        error_message=artifact.error_message,
        created_at=artifact.created_at,
        updated_at=artifact.updated_at,
    )

