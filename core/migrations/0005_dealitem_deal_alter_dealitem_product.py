# Generated by Django 4.2.4 on 2023-09-24 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_remove_deal_products_dealitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="dealitem",
            name="deal",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="core.deal",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dealitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deal_items",
                to="core.product",
            ),
        ),
    ]
