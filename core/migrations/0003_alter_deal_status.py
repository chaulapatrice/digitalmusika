# Generated by Django 4.2.4 on 2023-09-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="status",
            field=models.CharField(
                choices=[
                    ("unassigned", "Unassigned"),
                    ("assigned", "Assigned"),
                    ("accepted", "Accepted"),
                    ("completed", "Completed"),
                    ("closed", "Closed"),
                ],
                default="unassigned",
                max_length=45,
            ),
        ),
    ]
