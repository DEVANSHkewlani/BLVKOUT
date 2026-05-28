from sqlalchemy.orm import Session

from app.user.models import User

def get_user_by_auth_id(
    db: Session,
    auth_user_id: str
):

    return db.query(User).filter(
        User.id == auth_user_id
    ).first()


def create_user(
    db: Session,
    user
):

    db.add(user)

    db.commit()

    db.refresh(user)

    return user

def update_profile(
    db: Session,
    profile
):

    db.commit()

    db.refresh(profile)

    return profile