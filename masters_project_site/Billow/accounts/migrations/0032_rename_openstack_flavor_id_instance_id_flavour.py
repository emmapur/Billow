# Generated by Django 4.1 on 2023-02-09 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0031_remove_instance_network_userprofile_program_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="instance",
            old_name="openstack_flavor_id",
            new_name="id_flavour",
        ),
    ]
