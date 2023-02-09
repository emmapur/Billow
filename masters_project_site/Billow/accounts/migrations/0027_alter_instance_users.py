# Generated by Django 4.1 on 2023-02-08 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0026_userprofile_delete_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instance",
            name="users",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.userprofile",
            ),
        ),
    ]