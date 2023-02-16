# Generated by Django 4.1 on 2023-02-16 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0051_instance_total_cost_snapshot_instance_daily_cost_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snapshot_instance",
            name="CPU",
            field=models.DecimalField(decimal_places=2, default=2.88, max_digits=10),
            preserve_default=False,
        ),
    ]
