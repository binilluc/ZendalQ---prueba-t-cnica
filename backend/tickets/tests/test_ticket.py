from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.models import Ticket


class TicketCreationTests(APITestCase):
    def test_cannot_create_ticket_directly_closed(self):
        """Business rule: a ticket cannot be created with status=closed."""
        url = reverse("ticket-list")
        response = self.client.post(
            url, {"title": "Broken printer", "status": Ticket.Status.CLOSED}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_create_ticket_defaults_to_open(self):
        url = reverse("ticket-list")
        response = self.client.post(url, {"title": "Broken printer"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Ticket.Status.OPEN)


class TicketStatusTransitionTests(APITestCase):
    """Covers the closed -> open business rule required by the exercise."""

    def setUp(self):
        self.ticket = Ticket.objects.create(
            title="Server down", status=Ticket.Status.CLOSED
        )
        self.url = reverse("ticket-detail", args=[self.ticket.id])

    def test_closed_ticket_cannot_go_back_to_open_directly(self):
        response = self.client.patch(self.url, {"status": Ticket.Status.OPEN})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)

    def test_closed_ticket_can_go_to_in_progress(self):
        response = self.client.patch(
            self.url, {"status": Ticket.Status.IN_PROGRESS}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.IN_PROGRESS)


class TicketListingTests(APITestCase):
    def setUp(self):
        Ticket.objects.create(title="A", priority=Ticket.Priority.LOW)
        Ticket.objects.create(title="B", priority=Ticket.Priority.HIGH)
        Ticket.objects.create(
            title="C", priority=Ticket.Priority.HIGH, status=Ticket.Status.IN_PROGRESS
        )

    def test_filter_by_status_and_priority(self):
        url = reverse("ticket-list")
        response = self.client.get(url, {"priority": Ticket.Priority.HIGH})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(t["priority"] == "high" for t in response.data))

    def test_list_is_ordered_by_created_at_descending(self):
        url = reverse("ticket-list")
        response = self.client.get(url)

        titles = [t["title"] for t in response.data]
        self.assertEqual(titles, ["C", "B", "A"])


class TicketStatsTests(APITestCase):
    def test_stats_groups_by_status(self):
        Ticket.objects.create(title="A")
        Ticket.objects.create(title="B")
        Ticket.objects.create(title="C", status=Ticket.Status.IN_PROGRESS)

        url = reverse("ticket-stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"open": 2, "in_progress": 1, "closed": 0},
        )
