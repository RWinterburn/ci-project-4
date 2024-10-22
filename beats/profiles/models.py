from django.db import models

# Create your models here.

# profiles/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the Django User model
    bio = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'
