# Generated by Django 5.0.6 on 2024-05-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trading_platform", "0004_alter_apikey_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stock",
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
                ("name", models.CharField(max_length=128, verbose_name="Stock Name")),
                ("active", models.BooleanField(default=True, verbose_name="Active")),
            ],
            options={
                "verbose_name": "Stock",
                "verbose_name_plural": "Stocks",
            },
        ),
    ]
