from fastapi import FastAPI

from app.api.artifacts import router as artifacts_router
from app.core.database import engine
from app.models import Base


async def init_db():
    """Initialize database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(
    title="Artifact Scanner Service",
    on_startup=[init_db],
)

app.include_router(artifacts_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "OK"}

