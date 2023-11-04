# Generated by Django 4.2.7 on 2023-11-04 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("executor", "0001_initial"),
        ("order", "0002_alter_order_executor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="executor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="executor",
                to="executor.executor",
            ),
        ),
    ]
