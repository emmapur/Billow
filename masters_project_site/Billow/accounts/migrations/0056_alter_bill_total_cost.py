# Generated by Django 4.1 on 2023-02-16 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0055_alter_instance_total_cost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bill",
            name="total_cost",
            field=models.CharField(max_length=64, null=True),
        ),
    ]
