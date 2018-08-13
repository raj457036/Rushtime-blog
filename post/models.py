from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.db.models import F
from django.conf import settings
from notifiy.models import Notice
from django.core.validators import validate_comma_separated_integer_list
from cloudinary import models as cmodels
import cloudinary
from django.utils.html import strip_tags

POST_TOPICS = (('0', 'PERSONAL'),('1', 'FUTURE'), ('2', 'CULTURE'), ('3', 'TECH'), ('4', 'ENTREPRENEURSHIP'), ('5', 'SELF'), ('6', 'POLITICS'), ('7', 'DESIGN'), ('8', 'SCIENCE'), ('9', 'POPULAR'))



# Create your models here.
class Post(models.Model):
    POST_VISIBILITY_CHOICE = (
        ('1','Public'),
        ('2','Only folowers'),
        ('3','Private')
    )
    DEFAULT_TOPIC = 1

    title = models.CharField(max_length=300)
    sub_title = models.CharField(max_length=150, blank=True)
    head_img = cmodels.CloudinaryField('images')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)
    upvote = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=1, choices=POST_VISIBILITY_CHOICE, default='1')
    post_tags = models.CharField(max_length=255, help_text='Tags seperated with a space')
    post_topic= models.CharField(max_length=1, choices=POST_TOPICS, default=0)
    def __str__(self):
        return self.title

    def add_upvote(self, username):
        self.upvote = models.F('upvote') + 1
        PostLikers.objects.create(post=self, user = username)
        self.save()

    def remove_upvote(self, username):
        self.upvote = F('upvote') - 1
        PostLikers.objects.filter(post=self, user=username).delete()
        self.save()

    def all_likers(self):
        l = [i.users_id for i in self.likers.all()]
        return l

    def get_read_time(self):
        time = len(strip_tags(self.content).split(' ')) / 255
        return round(time)

    def get_comments_count(self) :
        return len(self.comment_set.all())

    def get_short_story(self):
        return strip_tags(self.content)[:200]+'...'

    def save(self):
        super().save()
        followers = self.user.userextend.get_followers()
        text = self.user.get_full_name() + " just posted."
        print(followers)
        for u in followers:
            if self.created_on == self.updated_on:
                Notice.objects.create(user=u.current_user,sender=self.user,text=text, category='1', c_id=self.pk)


class Comment(models.Model):
    who = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.who.username

    def save(self):
        super().save()
        text= " commented on your Post."
        if (self.post.user != self.who) and (self.created_on == self.updated_on):
            Notice.objects.create(user=self.post.user,sender=self.who,text=text, category='2', c_id=self.pk)

class reply(models.Model):
    who = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.who.username

    def save(self):
        super().save()
        text= self.who.get_full_name() + " Just replied on your Post."
        if self.comment.post.user != self.who and self.created_on == self.updated_on:
            Notice.objects.create(user=self.comment.post.user,sender=self.who,text=text, category='3', c_id=self.pk)

class PostLikers(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='likers')
    users_id = models.IntegerField()

    def __str__(self):
        return str(self.users_id)