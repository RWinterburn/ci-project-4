from django.db import models 
from django.conf import settings
from instrumentals.models import Beat



class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.beat.title} x {self.quantity}"