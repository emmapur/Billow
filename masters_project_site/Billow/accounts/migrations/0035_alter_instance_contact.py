# Generated by Django 4.1 on 2023-02-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0034_alter_instance_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instance",
            name="contact",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]