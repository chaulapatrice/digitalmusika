# Generated by Django 4.2.4 on 2023-10-30 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_alter_deal_assignee"),
    ]

    operations = [
        migrations.CreateModel(
            name="Withdrawal",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("inbucks_qrcode", models.ImageField(upload_to="withdrawals")),
                ("paid", models.BooleanField(default=False)),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
