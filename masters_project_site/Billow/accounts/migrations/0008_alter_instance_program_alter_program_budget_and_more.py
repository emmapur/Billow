# Generated by Django 4.1 on 2022-12-21 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_alter_image_image_id_alter_image_image_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instance",
            name="program",
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="program", name="budget", field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="program",
            name="program_name",
            field=models.CharField(max_length=64),
        ),
    ]
