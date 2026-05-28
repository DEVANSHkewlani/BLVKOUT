from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.user.schemas import (
    UserResponse,
    UserUpdate
)

from app.user.service import (
    get_or_create_user,
    edit_user
)


router = APIRouter()


@router.get("/me")
async def get_me(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return get_or_create_user(
        db,
        current_user
    )

@router.put(
    "/me",
    response_model=UserResponse
)
async def update_my_user(

    update_data: UserUpdate,

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    user = get_or_create_user(
        db,
        current_user
    )

    return edit_user(
        db,
        user,
        update_data
    )