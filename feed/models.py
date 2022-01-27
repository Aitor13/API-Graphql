from django.db import models
import logging
from profiles.models import CustomUser
# Create your models here.

logger = logging.getLogger(__name__)

class Feed(models.Model):
    
    STATE_CHOICES = [
        ('PUB', 'Public'),
        ('PRO', 'Protected'),
        ('PRI', 'Private')]
    
    feed = models.CharField(max_length=254)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=3, choices=STATE_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.feed} -- {self.visibility}'