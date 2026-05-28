from fastapi import Depends
from fastapi import HTTPException

from app.auth.dependencies import (
    get_current_user
)

from app.auth.config import (
    ADMIN_EMAIL
)


async def get_current_admin(
    current_user = Depends(get_current_user)
):

    if current_user.email != ADMIN_EMAIL:

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user