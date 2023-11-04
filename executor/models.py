from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from variables import choices, validators


class Executor(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField()
    phone: models.CharField = models.CharField(
        validators=[validators.phone_regex], max_length=9
    )
    ownership: models.CharField = models.CharField(
        max_length=20, choices=choices.OWNERSHIP_CHOICES
    )
    area: models.CharField = models.CharField(
        max_length=20, choices=choices.AREA_CHOICES
    )
    rating: models.FloatField = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
        default=0.0,
    )
    description: models.TextField = models.TextField(max_length=350, default=None)
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.pk}: {self.name}, {self.ownership}, {self.area}, {self.date}, {self.rating}"
