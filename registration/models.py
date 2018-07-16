from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.forms import ValidationError

# Create your models here.
class Images(models.Model):
    imgType = (
        ('0', 'Profile Pic'),
        ('1', 'Post Pic'),
        ('2', 'Article Pic'),
        ('3', 'Banner Pic')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = models.ImageField()
    img_type = models.CharField(max_length=1, choices=imgType, default='1')
    def __str__(self):
        return self.img.name


class UserExtend(models.Model):
    protection_level = (
        ('1', 'No One allowed'),
        ('2', 'only followers'),
        ('3', 'everyone')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1)
    aboutMe  = models.CharField(max_length=255, blank=True)
    Profile_pic = models.OneToOneField(Images, on_delete=models.CASCADE, null=True, blank=True)
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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_UserExtend(sender, instance, created, **kwargs):
    if created:
        UserExtend.objects.create(user = instance)
    instance.userextend.save()





class Follower(models.Model):
    # users that i am following
    fusers = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='followers')
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owner', on_delete=models.CASCADE)


    @classmethod
    def add_follow(cls, current_user, fuser):
        follow_obj, created = Following.objects.get_or_create(
            current_user = current_user
        )

        follow_obj.fusers.add(fuser)

    @classmethod
    def remove_follow(cls, current_user, fuser):
        follow_obj, created = Following.objects.get_or_create(
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
