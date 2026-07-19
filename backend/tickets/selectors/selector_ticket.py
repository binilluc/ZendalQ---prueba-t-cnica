from django.db.models import Count, QuerySet

from tickets.models import Ticket


def ticket_list(*, filters: dict | None = None) -> QuerySet[Ticket]:
    filters = filters or {}
    queryset = Ticket.objects.all()

    status = filters.get("status")
    if status:
        queryset = queryset.filter(status=status)

    priority = filters.get("priority")
    if priority:
        queryset = queryset.filter(priority=priority)

    return queryset.order_by("-created_at")


def ticket_stats() -> dict[str, int]:
    counts = dict(Ticket.objects.values_list("status").annotate(count=Count("id")))
    return {choice: counts.get(choice, 0) for choice, _ in Ticket.Status.choices}
