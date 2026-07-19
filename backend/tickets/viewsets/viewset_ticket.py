from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response

from tickets.selectors import ticket_list, ticket_stats
from tickets.serializers import TicketSerializer
from tickets.services import ticket_create, ticket_update


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        return ticket_list(filters=self.request.query_params.dict())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ticket = ticket_create(**serializer.validated_data)
        except DjangoValidationError as exc:
            raise DRFValidationError(exc.message_dict) from exc

        return Response(
            self.get_serializer(ticket).data, status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, *args, **kwargs):
        ticket = self.get_object()
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            ticket = ticket_update(ticket=ticket, data=serializer.validated_data)
        except DjangoValidationError as exc:
            raise DRFValidationError(exc.message_dict) from exc

        return Response(self.get_serializer(ticket).data)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        return Response(ticket_stats())
