# Generated by Django 4.1 on 2023-01-05 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_alter_instance_id_instance"),
    ]

    operations = [
        migrations.RemoveField(model_name="instance", name="flavor",),
    ]
