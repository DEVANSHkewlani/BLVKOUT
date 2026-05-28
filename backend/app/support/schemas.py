from pydantic import BaseModel
from pydantic import EmailStr

from uuid import UUID

from typing import Optional

from datetime import datetime


class SupportTicketCreate(BaseModel):

    name: str

    email: EmailStr

    category: str

    order_id: Optional[UUID] = None

    subject: str

    message: str

class SupportTicketUpdate(BaseModel):

    status: Optional[str] = None

    admin_reply: Optional[str] = None



class SupportTicketResponse(BaseModel):

    id: UUID

    user_id: Optional[UUID]

    name: str

    email: EmailStr

    category: str

    order_id: Optional[UUID]

    subject: str

    message: str

    status: str

    admin_reply: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True
