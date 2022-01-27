from django.contrib import admin
from profiles.models import FollowRequests, CustomUser

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(FollowRequests)