# Generated by Django 4.1 on 2023-03-01 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0064_delete_role"),
    ]

    operations = [
        migrations.RemoveField(model_name="key", name="key_name_ID",),
    ]
