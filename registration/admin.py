from django.contrib import admin
from . import models
# Register your models here.

class UserExtendAdmin(admin.ModelAdmin):
    list_display=('user','date_of_birth','gender', 'protected')
    search_fields=('aboutMe','gender')
    list_filter=('protected','gender')

admin.site.register(models.UserExtend, UserExtendAdmin)
admin.site.register(models.Images)
admin.site.register(models.Bookmarks)