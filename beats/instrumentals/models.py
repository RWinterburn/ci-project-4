from django.db import models

# Create your models here.

class Beat(models.Model):
    title = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)