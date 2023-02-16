# Generated by Django 4.1 on 2023-02-15 18:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0049_alter_bill_bill_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="daily_usage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("instance_name", models.CharField(max_length=64)),
                ("total_cost", models.CharField(max_length=64)),
            ],
        ),
    ]