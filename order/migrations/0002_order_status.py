# Generated by Django 4.2.7 on 2023-11-14 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("In progress", "In progress"),
                    ("Done", "Done"),
                ],
                default="Pending",
                max_length=15,
            ),
        ),
    ]
