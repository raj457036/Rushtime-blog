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
        ('o', 'Others')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=genders)
    aboutMe  = models.CharField(max_length=255, blank=True)
    # settings
    protected = models.CharField(max_length=1, choices=protection_level, default='1')

    def __str__(self):
        return self.user.username

    def get_followers(self):
        return self.user.followers.all()

    def get_following(self):
        try:
            f = self.user.owner.first().fusers.all()
        except Exception:
            f = []
        return f

    def get_profile_pics(self):
        return self.images.filter(img_type='0').order_by('-datetime')

    def get_bookmarks(self):
        return self.user.bookmarks.values_list('o_id', flat=True)

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




class Follower(models.Model):
    # users that i am following
    fusers = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='followers')
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owner', on_delete=models.CASCADE)


    @classmethod
    def add_follow(cls, current_user, fuser):
        follow_obj, created = Follower.objects.get_or_create(
            current_user = current_user
        )

        follow_obj.fusers.add(fuser)

    @classmethod
    def remove_follow(cls, current_user, fuser):
        follow_obj, created = Follower.objects.get_or_create(
            current_user = current_user
        )

        follow_obj.fusers.remove(fuser)

    def __str__(self):
        return self.current_user.username


@receiver(post_init, sender=Follower)
def check_followers(sender, instance, **kwargs):
    if instance.current_user in instance.fusers.all():
        instance.fusers.remove(instance.current_user)
        raise ValidationError(u"You cannot follow yourself.")
    instance.save()


class Bookmarks(models.Model):
    b_type = (('1', 'Post'),('2','Images'))

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