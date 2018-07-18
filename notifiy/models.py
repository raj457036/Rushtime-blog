from django.db import models
from django.contrib.auth import settings
# Create your models here.

type_of_notice = (
    ('1','Post'),
    ('2','Comment'),
    ('3','Reply'),
    ('4', 'Follow')
)


class Notice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notice')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='sender')
    text = models.CharField(max_length=512)
    category = models.CharField(max_length=1, choices=type_of_notice)
    date_time = models.DateTimeField(auto_now_add=True)
    c_id = models.PositiveIntegerField()
    viewed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    
    # def follow_request(self, user, message, c_id):
    #     pass