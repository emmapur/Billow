# Generated by Django 4.1 on 2023-02-09 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0030_userprofile_team_name_alter_instance_network"),
    ]

    operations = [
        migrations.RemoveField(model_name="instance", name="network",),
        migrations.AddField(
            model_name="userprofile",
            name="program_name",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.program",
            ),
        ),
    ]