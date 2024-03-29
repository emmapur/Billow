# Generated by Django 4.1 on 2023-02-21 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0059_remove_instance_image_instance_image_aws_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Op_image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image_name", models.CharField(max_length=64)),
                ("Image_ID", models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name="instance",
            name="Image_op",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.op_image",
            ),
        ),
        migrations.DeleteModel(name="Openstack_image",),
    ]
