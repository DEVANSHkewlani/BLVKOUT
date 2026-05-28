from app.user.repository import (
    update_profile
)
from app.user.models import User

from app.user.repository import (
    get_user_by_auth_id,
    create_user
)

from app.auth.config import ADMIN_EMAIL

def get_or_create_user(
    db,
    current_user
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    if user:
        # Self-healing: if the user exists but has a customer role and matches ADMIN_EMAIL, promote them to admin
        if user.email == ADMIN_EMAIL and user.role != "admin":
            user.role = "admin"
            db.commit()
            db.refresh(user)
        return user

    # Auto-assign admin role if email matches ADMIN_EMAIL
    role = "admin" if current_user.email == ADMIN_EMAIL else "customer"

    new_user = User(

        id=current_user.id,

        email=current_user.email,

        full_name=current_user.user_metadata.get(
            "full_name"
        ),

        avatar_url=current_user.user_metadata.get(
            "avatar_url"
        ),

        role=role,

        is_active=True
    )

    return create_user(
        db,
        new_user
    )

def edit_user(
    db,
    user,
    update_data
):

    for key, value in update_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(user, key, value)

    return update_profile(
        db,
        user
    )