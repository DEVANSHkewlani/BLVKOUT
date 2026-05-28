from pydantic import BaseModel

from uuid import UUID

from datetime import datetime


class WishlistResponse(BaseModel):

    id: UUID

    user_id: UUID

    product_id: UUID

    created_at: datetime

    class Config:
        from_attributes = True