# Generated by Django 4.1 on 2023-03-01 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0061_instance_state_snapshot_instance_state"),
    ]

    operations = [
        migrations.RemoveField(model_name="instance", name="id_flavour",),
        migrations.RemoveField(model_name="snapshot_instance", name="id_flavour",),
    ]
