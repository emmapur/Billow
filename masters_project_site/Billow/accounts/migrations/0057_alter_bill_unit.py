# Generated by Django 4.1 on 2023-02-17 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0056_alter_bill_total_cost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bill", name="Unit", field=models.CharField(max_length=70),
        ),
    ]
