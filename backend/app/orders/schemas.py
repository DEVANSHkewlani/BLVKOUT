from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    total: Decimal
    items: Optional[Any] = []
    shipping_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
