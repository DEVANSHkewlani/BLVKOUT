from sqlalchemy.orm import Session

from app.support.models import (
    SupportTicket
)


def create_support_ticket(
    db: Session,
    ticket
):

    db.add(ticket)

    db.commit()

    db.refresh(ticket)

    return ticket


def get_user_tickets(
    db: Session,
    user_id
):

    return db.query(
        SupportTicket
    ).filter(
        SupportTicket.user_id == user_id
    ).all()


def get_all_tickets(
    db: Session
):

    return db.query(
        SupportTicket
    ).order_by(
        SupportTicket.created_at.desc()
    ).all()


def get_ticket_by_id(
    db: Session,
    ticket_id
):

    return db.query(
        SupportTicket
    ).filter(
        SupportTicket.id == ticket_id
    ).first()


def update_ticket(
    db: Session,
    ticket
):

    db.commit()

    db.refresh(ticket)

    return ticket


def delete_ticket(
    db: Session,
    ticket
):

    db.delete(ticket)

    db.commit()
