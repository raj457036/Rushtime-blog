from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserExtend)
admin.site.register(models.Follower)
# admin.site.register(models.Images)
# admin.site.register(models.Bookmarks)