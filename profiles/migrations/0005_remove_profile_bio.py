# Generated by Django 4.2 on 2024-12-13 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]