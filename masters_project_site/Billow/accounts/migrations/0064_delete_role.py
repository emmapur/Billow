# Generated by Django 4.1 on 2023-03-01 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0063_rename_image_aws_image"),
    ]

    operations = [
        migrations.DeleteModel(name="role",),
    ]
