from django.db import models

from client.models import Client
from order.models import Order
from variables import choices


class Offer(models.Model):
    order: models.ForeignKey = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="offers"
    )
    executor: models.ForeignKey = models.ForeignKey(Client, on_delete=models.CASCADE)
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    price: models.IntegerField = models.IntegerField()
    comment: models.TextField = models.TextField(max_length=150, null=True)
    status: models.CharField = models.CharField(
        max_length=15,
        choices=choices.STATUSES,
        default="Pending",
    )
    objects = models.Manager()

    class Meta:
        unique_together = ("order", "executor")

    def __str__(self):
        return f"{self.pk}: {self.executor}, {self.order}, {self.date}, {self.price}"
