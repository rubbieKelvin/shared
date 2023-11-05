# Generated by Django 4.2.7 on 2023-11-05 17:40

from django.db import migrations, models
import shared.apps.authentication.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CallbackInformation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "code",
                    models.CharField(
                        default=shared.apps.authentication.models.default_code_gen,
                        max_length=12,
                    ),
                ),
                ("token", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
