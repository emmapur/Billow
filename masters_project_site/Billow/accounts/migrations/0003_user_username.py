# Generated by Django 4.1 on 2022-12-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_user_email_remove_user_password_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(default=1, max_length=64, unique=True),
            preserve_default=False,
        ),
    ]