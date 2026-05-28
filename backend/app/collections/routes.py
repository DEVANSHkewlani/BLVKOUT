from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.auth.roles import get_current_admin
from app.collections.schemas import (
    CollectionResponse,
    CollectionCreate,
    CollectionUpdate
)
from app.collections.service import (
    fetch_all_collections,
    fetch_active_collections,
    fetch_collection,
    create_new_collection,
    edit_collection,
    remove_collection
)


router = APIRouter()


@router.get(
    "/",
    response_model=List[CollectionResponse]
)
async def get_collections(
    db: Session = Depends(get_db)
):
    return fetch_all_collections(db)


@router.get(
    "/active",
    response_model=List[CollectionResponse]
)
async def get_active(
    db: Session = Depends(get_db)
):
    return fetch_active_collections(db)


@router.post(
    "/",
    response_model=CollectionResponse
)
async def create_collection_route(
    data: CollectionCreate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        return create_new_collection(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put(
    "/{collection_id}",
    response_model=CollectionResponse
)
async def update_collection_route(
    collection_id: UUID,
    data: CollectionUpdate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    collection = fetch_collection(db, collection_id)
    if not collection:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )
    return edit_collection(db, collection, data)


@router.delete("/{collection_id}")
async def delete_collection_route(
    collection_id: UUID,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    collection = fetch_collection(db, collection_id)
    if not collection:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )
    remove_collection(db, collection)
    return {"message": "Collection deleted successfully"}
