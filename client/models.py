from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from variables import validators


class Client(models.Model):
    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    phone: models.CharField = models.CharField(
        validators=[validators.phone_regex], max_length=9
    )
    rating: models.FloatField = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
        default=0.0,
    )
    objects = models.Manager()

    def __str__(self):
        return f"{self.user}"
