# Generated by Django 5.1.2 on 2024-12-04 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_remove_orderlineitem_product_orderlineitem_beat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_metadata',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_payment_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_payment_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]