# Generated by Django 5.1.2 on 2024-11-29 12:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumentals', '0004_beat_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beat',
            name='slug',
        ),
        migrations.AddField(
            model_name='beat',
            name='beat_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
