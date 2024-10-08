# Generated by Django 5.1.1 on 2024-09-20 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_custom", "0002_alter_usercustom_rol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercustom",
            name="rol",
            field=models.CharField(
                choices=[
                    ("investor", "Investor"),
                    ("operator", "Operator"),
                ],
                default="",
                max_length=8,
            ),
        ),
    ]
