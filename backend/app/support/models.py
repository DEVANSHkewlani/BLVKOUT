from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from sqlalchemy.sql import func

from sqlalchemy.types import TIMESTAMP

from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.core.database import Base


class SupportTicket(Base):

    __tablename__ = "support_tickets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    subject = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    status = Column(
        String,
        default="open"
    )

    admin_reply = Column(
        Text,
        nullable=True
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
    category = Column(
        String,
        nullable=False
    )
    
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=True
    )
