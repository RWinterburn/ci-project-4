# Generated by Django 5.1.2 on 2024-12-05 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_profile_bio_profile_address_line_1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='address_line_1',
            new_name='street_address1',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='address_line_2',
            new_name='street_address2',
        ),
    ]
