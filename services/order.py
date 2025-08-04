from typing import List
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    ticket_objs = [
        Ticket(
            movie_session_id=t["movie_session"],
            order=order,
            row=t["row"],
            seat=t["seat"]
        )
        for t in tickets
    ]

    Ticket.objects.bulk_create(ticket_objs)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
