# Generated by Django 4.1.3 on 2023-06-11 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0009_alter_order_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 6, 11, 13, 54, 20, 34937)
            ),
        ),
    ]
