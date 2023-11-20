# Generated by Django 4.2.7 on 2023-11-20 21:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("offer", "0003_offer_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("In progress", "In progress"),
                    ("Done", "Done"),
                    ("Declined", "Declined"),
                    ("Under approval", "Under approval"),
                ],
                default="Pending",
                max_length=15,
            ),
        ),
    ]
