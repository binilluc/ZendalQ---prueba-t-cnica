from django.core.exceptions import ValidationError

from tickets.models import Ticket


def ticket_create(
    *,
    title: str,
    description: str = "",
    priority: str = Ticket.Priority.MEDIUM,
    status: str = Ticket.Status.OPEN,
) -> Ticket:
    if status == Ticket.Status.CLOSED:
        raise ValidationError(
            {"status": "A ticket cannot be created directly with status 'closed'."}
        )

    ticket = Ticket(
        title=title, description=description, priority=priority, status=status
    )
    ticket.full_clean()
    ticket.save()
    return ticket


def ticket_update(*, ticket: Ticket, data: dict) -> Ticket:
    new_status = data.get("status")
    if new_status == Ticket.Status.OPEN and ticket.status == Ticket.Status.CLOSED:
        raise ValidationError(
            {
                "status": "A closed ticket cannot go back to 'open' directly; "
                "it must go through 'in_progress' first."
            }
        )

    for field, value in data.items():
        setattr(ticket, field, value)

    ticket.full_clean()
    ticket.save()
    return ticket
