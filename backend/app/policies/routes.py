from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from uuid import UUID

from app.core.database import get_db

from app.auth.roles import (
    get_current_admin
)

from app.policies.schemas import (

    PolicyCreate,

    PolicyUpdate,

    PolicyResponse
)

from app.policies.service import (

    fetch_policies,

    fetch_policy,

    create_new_policy,

    edit_policy,

    remove_policy
)


router = APIRouter()


# PUBLIC ROUTES

@router.get(
    "/",
    response_model=list[PolicyResponse]
)
async def get_policies(
    db: Session = Depends(get_db)
):

    return fetch_policies(db)


@router.get(
    "/{slug}",
    response_model=PolicyResponse
)
async def get_policy(
    slug: str,
    db: Session = Depends(get_db)
):

    return fetch_policy(
        db,
        slug
    )


# ADMIN ROUTES

@router.post(
    "/",
    response_model=PolicyResponse
)
async def create_policy_route(

    policy_data: PolicyCreate,

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    return create_new_policy(
        db,
        policy_data
    )


@router.put(
    "/{policy_id}",
    response_model=PolicyResponse
)
async def update_policy_route(

    policy_id: UUID,

    update_data: PolicyUpdate,

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    return edit_policy(
        db,
        policy_id,
        update_data
    )


@router.delete("/{policy_id}")
async def delete_policy_route(

    policy_id: UUID,

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    remove_policy(
        db,
        policy_id
    )

    return {
        "message": "Policy deleted successfully"
    }
