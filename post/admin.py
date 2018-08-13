from django.contrib import admin
from . import models
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','created_on','draft','user','visibility','post_topic')
    search_field = ('title',)
    list_filter = ('visibility','draft','user','created_on','post_topic')

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, )
admin.site.register(models.reply, )
admin.site.register(models.PostLikers, )