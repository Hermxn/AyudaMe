from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from client.models import Client
from variables import choices


class Order(models.Model):
    title: models.CharField = models.CharField(max_length=150)
    description: models.TextField = models.TextField(max_length=350, default=None)
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    area: models.CharField = models.CharField(
        max_length=15, choices=choices.AREA_CHOICES
    )
    rating: models.FloatField = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
        default=0.0,
    )
    client: models.ForeignKey = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client"
    )
    executor: models.ForeignKey = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="executor",
        null=True,
        blank=True,
    )
    offer: models.IntegerField = models.IntegerField(null=True, blank=True)
    status: models.CharField = models.CharField(
        max_length=15,
        choices=choices.STATUSES,
        default="Pending",
    )
    objects = models.Manager()

    def __str__(self):
        return f"{self.pk}, {self.date}, {self.title}, {self.description}, {self.client}, {self.executor}, {self.status}"
