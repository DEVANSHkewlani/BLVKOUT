from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from uuid import UUID

from app.core.database import get_db

from app.auth.dependencies import (
    get_current_user,
    get_optional_user
)

from app.auth.roles import (
    get_current_admin
)

from app.support.schemas import (

    SupportTicketCreate,

    SupportTicketUpdate,

    SupportTicketResponse
)

from app.support.service import (

    create_ticket,

    fetch_my_tickets,

    fetch_all_tickets,

    fetch_single_ticket,

    update_support_ticket,

    remove_ticket
)


router = APIRouter()


# PUBLIC CONTACT ROUTE

@router.post(
    "/ticket",
    response_model=SupportTicketResponse
)
async def create_support_ticket_route(

    ticket_data: SupportTicketCreate,

    db: Session = Depends(get_db),

    current_user = Depends(
        get_optional_user
    )
):

    return create_ticket(
        db,
        ticket_data,
        current_user
    )


# USER ROUTES

@router.get(
    "/my-tickets",
    response_model=list[SupportTicketResponse]
)
async def get_my_support_tickets(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return fetch_my_tickets(
        db,
        current_user
    )


# ADMIN ROUTES

@router.get(
    "/tickets",
    response_model=list[SupportTicketResponse]
)
async def get_all_support_tickets(

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    return fetch_all_tickets(db)


@router.get(
    "/tickets/{ticket_id}",
    response_model=SupportTicketResponse
)
async def get_single_ticket(

    ticket_id: UUID,

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    return fetch_single_ticket(
        db,
        ticket_id
    )


@router.put(
    "/tickets/{ticket_id}",
    response_model=SupportTicketResponse
)
async def update_ticket_route(

    ticket_id: UUID,

    update_data: SupportTicketUpdate,

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    return update_support_ticket(
        db,
        ticket_id,
        update_data
    )


@router.delete("/tickets/{ticket_id}")
async def delete_ticket_route(

    ticket_id: UUID,

    admin_user = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    remove_ticket(
        db,
        ticket_id
    )

    return {
        "message": "Ticket deleted successfully"
    }
