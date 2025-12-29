import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.artifact import Artifact
from app.models.enums import ScanResult, ScanStatus


async def create_artifact(
    session: AsyncSession,
    name: str,
    type: str,
    source: str,
    status: ScanStatus,
    result: ScanResult,
    exit_code: Optional[int] = None,
    error_message: Optional[str] = None,
) -> Artifact:
    """Create a new artifact in the database."""
    artifact = Artifact(
        name=name,
        type=type,
        source=source,
        status=status,
        result=result,
        exit_code=exit_code,
        error_message=error_message,
    )
    session.add(artifact)
    await session.commit()
    await session.refresh(artifact)
    return artifact


async def get_artifact_by_id(
    session: AsyncSession,
    artifact_id: uuid.UUID,
) -> Optional[Artifact]:
    """Get an artifact by its ID."""
    result = await session.execute(
        select(Artifact).where(Artifact.id == artifact_id)
    )
    return result.scalar_one_or_none()


async def update_artifact(
    session: AsyncSession,
    artifact_id: uuid.UUID,
    name: Optional[str] = None,
    type: Optional[str] = None,
    source: Optional[str] = None,
    status: Optional[ScanStatus] = None,
    result: Optional[ScanResult] = None,
    exit_code: Optional[int] = None,
    error_message: Optional[str] = None,
) -> Optional[Artifact]:
    """Update an artifact by its ID."""
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if type is not None:
        update_data["type"] = type
    if source is not None:
        update_data["source"] = source
    if status is not None:
        update_data["status"] = status
    if result is not None:
        update_data["result"] = result
    if exit_code is not None:
        update_data["exit_code"] = exit_code
    if error_message is not None:
        update_data["error_message"] = error_message

    if not update_data:
        return await get_artifact_by_id(session, artifact_id)

    await session.execute(
        update(Artifact)
        .where(Artifact.id == artifact_id)
        .values(**update_data)
    )
    await session.commit()
    return await get_artifact_by_id(session, artifact_id)

