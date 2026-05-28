from pydantic import BaseModel

from uuid import UUID

from typing import Optional

from datetime import datetime


class PolicyBase(BaseModel):

    title: str

    content: str

    is_active: bool = True


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):

    title: Optional[str] = None

    content: Optional[str] = None

    is_active: Optional[bool] = None


class PolicyResponse(PolicyBase):

    id: UUID

    slug: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True
