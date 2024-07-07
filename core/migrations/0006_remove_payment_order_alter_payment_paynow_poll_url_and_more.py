# Generated by Django 4.2.4 on 2024-07-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.AlterField(
            model_name='payment',
            name='paynow_poll_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paynow_redirect_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
