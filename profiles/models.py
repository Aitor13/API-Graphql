from django.db import models
import logging
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from socialnetwork import settings_dev


logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
    friends = models.ManyToManyField("CustomUser", blank=True)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"


class FollowRequests(models.Model):
    to_user = models.ForeignKey("CustomUser", related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey("CustomUser", related_name='from_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
	    return "Request created from {}, to {}".format(self.from_user.username, self.to_user.username)

