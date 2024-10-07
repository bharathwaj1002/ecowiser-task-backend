# Generated by Django 5.1.1 on 2024-10-05 14:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("logo", models.ImageField(default="", upload_to="brands/")),
                ("name", models.CharField(max_length=25)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brands",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("picture1", models.ImageField(default="", upload_to="products/")),
                ("picture2", models.ImageField(default="", upload_to="products/")),
                ("picture3", models.ImageField(default="", upload_to="products/")),
                ("name", models.CharField(max_length=200)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.IntegerField()),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.brand"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Specification",
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
                ("key", models.CharField(max_length=100)),
                ("value", models.CharField(max_length=200)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specifications",
                        to="app.product",
                    ),
                ),
            ],
        ),
    ]