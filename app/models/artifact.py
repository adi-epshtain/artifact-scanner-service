import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.models.enums import ScanResult, ScanStatus


# Short explanationdd:
# The GUID class is a custom SQLAlchemy type decorator that ensures the UUID (GUID)
# is handled as a string in the database (for SQLite compatibility), and transparently
# converts between Python's uuid.UUID objects and their string representation
# when reading from or writing to the database.

class GUID(TypeDecorator):
    """Platform-independent GUID type for SQLite compatibility."""
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        # Always store as a string of length 36 (UUID canonical form)
        return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        # Convert UUID to string before storing to DB
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        # Convert back to UUID object when loading from DB
        if value is None:
            return value
        return uuid.UUID(value)


class Base(DeclarativeBase):
    pass


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ScanStatus] = mapped_column(
        SQLEnum(ScanStatus),
        nullable=False,
    )
    result: Mapped[ScanResult] = mapped_column(
        SQLEnum(ScanResult),
        nullable=False,
    )
    exit_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

