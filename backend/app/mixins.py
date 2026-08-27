import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from .common import get_datetime_utc


class IDMixin(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class CreatedAtMixin(SQLModel):
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )


class UpdatedAtMixin(SQLModel):
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
