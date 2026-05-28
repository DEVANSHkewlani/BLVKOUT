from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy.types import TIMESTAMP

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

import uuid

from app.core.database import Base


class WishlistItem(Base):

    __tablename__ = "wishlist_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
