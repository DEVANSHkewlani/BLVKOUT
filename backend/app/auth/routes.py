from fastapi import APIRouter
from fastapi import Depends

from app.auth.dependencies import (
    get_current_user
)

from app.auth.roles import (
    get_current_admin
)


router = APIRouter()


@router.get("/me")
async def get_me(
    current_user = Depends(get_current_user)
):

    return current_user


@router.get("/admin")
async def admin_dashboard(
    admin_user = Depends(get_current_admin)
):

    return {
        "message": "Welcome Admin"
    }