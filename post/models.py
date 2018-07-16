from django.db import models
from django.conf import settings
from notifiy.models import Notice
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=300)
    sub_title = models.CharField(max_length=150, blank=True)
    head_img = models.ImageField(verbose_name="Title Image" ,null=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)
    upvote = models.PositiveIntegerField(default=0)
    share = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def add_upvote(self, username):
        self.upvote = models.F('upvote') + 1
        Upvoter.objects.create(post=self, user = username)
        self.save()

    def remove_upvote(self, username):
        self.upvote = models.F('upvote') - 1
        Upvoter.objects.filter(post=self, user=username).delete()
        self.save()

    def all_likers(self):
        l = [i.users_id for i in self.likers.all()]
        return l

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
    likes = models.PositiveIntegerField(default=0)
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