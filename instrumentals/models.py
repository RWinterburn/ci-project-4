from django.db import models
from django.conf import settings
import uuid


class Beat(models.Model):
    title = models.CharField(max_length=100)
    beat_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    producer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to='static/covers/', blank=True, null=True)
    audio_file = models.FileField(upload_to='static/audio/', blank=True, null=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title




class Producer(models.Model):
    name = models.CharField(max_length=100)
    years_producing = models.PositiveIntegerField()  
    main_instrument = models.CharField(max_length=100)  
    software = models.CharField(max_length=100)  
    def __str__(self):
        return self.name



