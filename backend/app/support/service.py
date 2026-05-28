from fastapi import HTTPException

from app.support.models import (
    SupportTicket
)

from app.support.repository import (

    create_support_ticket,

    get_user_tickets,

    get_all_tickets,

    get_ticket_by_id,

    update_ticket,

    delete_ticket
)

from app.user.repository import (
    get_user_by_auth_id
)


def create_ticket(
    db,
    ticket_data,
    current_user=None
):

    user_id = None

    if current_user:

        user = get_user_by_auth_id(
            db,
            current_user.id
        )

        if user:

            user_id = user.id

    ticket = SupportTicket(

        user_id=user_id,

        order_id=ticket_data.order_id,

        name=ticket_data.name,

        email=ticket_data.email,

        category=ticket_data.category,

        subject=ticket_data.subject,

        message=ticket_data.message,

        status="open"
    )

    return create_support_ticket(
        db,
        ticket
    )


def fetch_my_tickets(
    db,
    current_user
):

    user = get_user_by_auth_id(
        db,
        current_user.id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return get_user_tickets(
        db,
        user.id
    )


def fetch_all_tickets(
    db
):

    return get_all_tickets(db)


def fetch_single_ticket(
    db,
    ticket_id
):

    ticket = get_ticket_by_id(
        db,
        ticket_id
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


def update_support_ticket(
    db,
    ticket_id,
    update_data
):

    ticket = get_ticket_by_id(
        db,
        ticket_id
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    for key, value in update_data.model_dump(
        exclude_unset=True
    ).items():

        setattr(ticket, key, value)

    return update_ticket(
        db,
        ticket
    )


def remove_ticket(
    db,
    ticket_id
):

    ticket = get_ticket_by_id(
        db,
        ticket_id
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    delete_ticket(
        db,
        ticket
    )
