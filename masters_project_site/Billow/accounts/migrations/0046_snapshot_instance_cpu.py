# Generated by Django 4.1 on 2023-02-11 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0045_alter_snapshot_instance_flavor"),
    ]

    operations = [
        migrations.AddField(
            model_name="snapshot_instance",
            name="CPU",
            field=models.CharField(max_length=64, null=True),
        ),
    ]