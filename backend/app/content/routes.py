from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.auth.roles import get_current_admin
from app.content.schemas import (
    SiteContentItem,
    SiteContentBulkUpdate
)
from app.content.service import (
    fetch_all_content,
    bulk_upsert_content
)


router = APIRouter()


@router.get(
    "/",
    response_model=List[SiteContentItem]
)
async def get_all_site_content(
    db: Session = Depends(get_db)
):
    """Public: returns all site content key-value pairs"""
    return fetch_all_content(db)


@router.put("/")
async def update_site_content(
    payload: SiteContentBulkUpdate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin only: bulk upsert site content"""
    results = bulk_upsert_content(db, payload.items)
    return {
        "message": f"Updated {len(results)} content entries",
        "count": len(results)
    }
