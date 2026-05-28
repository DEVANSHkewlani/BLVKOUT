from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text

from sqlalchemy.sql import func

from sqlalchemy.types import TIMESTAMP

from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.core.database import Base


class Policy(Base):

    __tablename__ = "policies"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(
        String,
        nullable=False
    )

    slug = Column(
        String,
        unique=True,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
