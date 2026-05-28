from fastapi import HTTPException

from slugify import slugify

from app.policies.models import Policy

from app.policies.repository import (

    get_all_policies,

    get_policy_by_slug,

    get_policy_by_id,

    create_policy,

    update_policy,

    delete_policy
)


def fetch_policies(
    db
):

    return get_all_policies(db)


def fetch_policy(
    db,
    slug
):

    policy = get_policy_by_slug(
        db,
        slug
    )

    if not policy:

        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    return policy


def create_new_policy(
    db,
    policy_data
):

    slug = slugify(
        policy_data.title
    )

    existing_policy = get_policy_by_slug(
        db,
        slug
    )

    if existing_policy:

        raise HTTPException(
            status_code=400,
            detail="Policy already exists"
        )

    new_policy = Policy(

        title=policy_data.title,

        slug=slug,

        content=policy_data.content,

        is_active=policy_data.is_active
    )

    return create_policy(
        db,
        new_policy
    )


def edit_policy(
    db,
    policy_id,
    update_data
):

    policy = get_policy_by_id(
        db,
        policy_id
    )

    if not policy:

        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    for key, value in update_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(policy, key, value)

    return update_policy(
        db,
        policy
    )


def remove_policy(
    db,
    policy_id
):

    policy = get_policy_by_id(
        db,
        policy_id
    )

    if not policy:

        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    delete_policy(
        db,
        policy
    )