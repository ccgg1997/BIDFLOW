# Generated by Django 5.1.1 on 2024-09-19 20:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='start_date',
            field=models.DateField(default=datetime.date(2024, 9, 19)),
        ),
    ]
