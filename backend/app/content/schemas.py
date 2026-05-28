from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict
from datetime import datetime


class SiteContentItem(BaseModel):
    key: str
    value: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SiteContentBulkUpdate(BaseModel):
    """Accepts a dict of key: value pairs to upsert"""
    items: Dict[str, str]
