from pydantic import BaseModel

from uuid import UUID

from typing import Optional

from datetime import datetime


class AddToCartSchema(BaseModel):

    product_id: UUID

    qty: int = 1

    size: Optional[str] = None

    color: Optional[str] = None


class UpdateCartSchema(BaseModel):

    qty: int


class CartResponse(BaseModel):

    id: UUID

    user_id: UUID

    product_id: UUID

    qty: int

    size: Optional[str]

    color: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True