import asyncio
import random
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.dal.artifact_dal import create_artifact, get_artifact_by_id, update_artifact
from app.models.enums import ScanResult, ScanStatus


async def trigger_artifact_scan(
    session: AsyncSession,
    name: str,
    type: str,
    source: str,
) -> uuid.UUID:
    """Create a new artifact with PENDING status and trigger scan."""
    artifact = await create_artifact(
        session=session,
        name=name,
        type=type,
        source=source,
        status=ScanStatus.PENDING,
        result=ScanResult.NONE,
    )
    
    # Start scan asynchronously (fire and forget)
    asyncio.create_task(run_artifact_scan(session, artifact.id))
    
    return artifact.id


async def run_artifact_scan(
    session: AsyncSession,
    artifact_id: uuid.UUID,
) -> None:
    """Run the scan process for an artifact."""
    # Update status to RUNNING
    await update_artifact(
        session=session,
        artifact_id=artifact_id,
        status=ScanStatus.RUNNING,
    )
    
    # Simulate scan work
    await asyncio.sleep(random.uniform(1.0, 3.0))
    
    # Randomly decide scan outcome
    outcome = _determine_scan_outcome()
    
    if outcome["status"] == ScanStatus.COMPLETED:
        await update_artifact(
            session=session,
            artifact_id=artifact_id,
            status=ScanStatus.COMPLETED,
            result=outcome["result"],
            exit_code=outcome["exit_code"],
        )
    else:
        await update_artifact(
            session=session,
            artifact_id=artifact_id,
            status=ScanStatus.FAILED,
            result=ScanResult.NONE,
            exit_code=outcome["exit_code"],
            error_message="Scan process failed",
        )


def _determine_scan_outcome() -> dict:
    """Randomly determine scan outcome."""
    rand = random.random()
    
    if rand < 0.6:
        # 60% chance: CLEAN
        return {
            "status": ScanStatus.COMPLETED,
            "result": ScanResult.CLEAN,
            "exit_code": 0,
        }
    elif rand < 0.9:
        # 30% chance: PROBLEM
        return {
            "status": ScanStatus.COMPLETED,
            "result": ScanResult.PROBLEM,
            "exit_code": 1,
        }
    else:
        # 10% chance: FAILED
        return {
            "status": ScanStatus.FAILED,
            "result": ScanResult.NONE,
            "exit_code": 2,
        }



