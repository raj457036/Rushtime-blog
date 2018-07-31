from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_init, pre_delete, post_delete
from django.dispatch import receiver
from django.forms import ValidationError
from cloudinary import models as cmodels
from post.models import Post
import cloudinary

# Create your models here.
class UserExtend(models.Model):
    protection_level = (
        ('1', 'No One allowed'),
        ('2', 'only followers'),
        ('3', 'everyone')
    )
    genders = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    post_type_choice = (
        ('1','Public'),
        ('2','Only folowers'),
        ('3','Private')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=genders)
    aboutMe  = models.CharField(max_length=255, blank=True)
    avatar = models.SmallIntegerField(default=1)
    # settings
    protected = models.CharField(max_length=1, choices=protection_level, default='1')
    Post_Type = models.CharField(max_length=1, choices=post_type_choice, default='1')
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)  #userextend.followers.all
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True) #userextend.following.all
    def __str__(self):
        return self.user.username


    def get_followers(self):
        return self.follower.all()

    def get_following(self):
        return self.following.all()

    def get_profile_pics(self):
        return self.images.filter(img_type='0').order_by('-datetime')

    def get_bookmarks(self):
        return self.user.bookmarks.values_list('o_id', flat=True)

    def get_avatar_url(self, stat=False):
        v = ''
        if self.gender == 'm':
            v='male'
        else:
            v='female'
        if stat:
            return f'/static/registration/Avatars/{v}/{self.gender}({self.avatar}).svg'
        return f'registration/Avatars/{v}/{self.gender}({self.avatar}).svg'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_UserExtend(sender, instance, created, **kwargs):
    if created:
        UserExtend.objects.create(user = instance)
    instance.userextend.save()


class Images(models.Model):
    imgType = (
        ('0', 'Profile Pic'),
        ('1', 'Post Pic'),
        ('2', 'Article Pic'),
        ('3', 'Banner Pic')
    )
    user = models.ForeignKey(UserExtend, on_delete=models.CASCADE, related_name='images')
    img = cmodels.CloudinaryField('image')
    img_type = models.CharField(max_length=1, choices=imgType, default='1')
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.img.public_id

@receiver(pre_delete, sender=Images)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.img.public_id)


class Bookmarks(models.Model):
    b_type = (('1', 'Post'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    bookmark_type = models.CharField(max_length=1, choices=b_type, default='1')
    o_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.bookmark_type + "  " + str(self.o_id)

@receiver(pre_delete, sender=Post)
def fix_bookmark(sender, instance, **kwargs):
    p = Bookmarks.objects.filter(o_id=instance.pk)
    if len(p) > 0:
        p.first().delete()

