from pydantic import BaseModel

from uuid import UUID

from typing import Optional


class UserResponse(BaseModel):

    id: UUID

    email: str

    full_name: Optional[str]

    avatar_url: Optional[str]

    phone: Optional[str]

    role: str

    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):

    full_name: Optional[str] = None

    avatar_url: Optional[str] = None

    phone: Optional[str] = None