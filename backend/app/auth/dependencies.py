from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from typing import Optional

from app.auth.config import supabase


security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional)
) -> Optional[dict]:
    if not credentials:
        return None
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception:
        return None



async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        user_response = supabase.auth.get_user(
            token
        )

        user = user_response.user

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid user"
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )