# Generated by Django 4.2 on 2024-12-13 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumentals', '0006_alter_beat_audio_file_alter_beat_cover_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('years_producing', models.PositiveIntegerField()),
                ('main_instrument', models.CharField(max_length=100)),
                ('software', models.CharField(max_length=100)),
            ],
        ),
    ]