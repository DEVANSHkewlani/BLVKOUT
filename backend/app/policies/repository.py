from sqlalchemy.orm import Session

from app.policies.models import Policy


def get_all_policies(
    db: Session
):

    return db.query(Policy).filter(
        Policy.is_active == True
    ).all()


def get_policy_by_slug(
    db: Session,
    slug: str
):

    return db.query(Policy).filter(
        Policy.slug == slug
    ).first()


def get_policy_by_id(
    db: Session,
    policy_id
):

    return db.query(Policy).filter(
        Policy.id == policy_id
    ).first()


def create_policy(
    db: Session,
    policy
):

    db.add(policy)

    db.commit()

    db.refresh(policy)

    return policy


def update_policy(
    db: Session,
    policy
):

    db.commit()

    db.refresh(policy)

    return policy


def delete_policy(
    db: Session,
    policy
):

    db.delete(policy)

    db.commit()
