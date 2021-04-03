from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# add lib for Profile user with signals 
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField

# add exception for user -> to profile 
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

#add unique Email 
User._meta.get_field('email')._unique = True

# add os to display url image avatar 
import os

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=140, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    profile_picture = models.ImageField(upload_to='image/', default='image/avatar.png')
    birthday = models.DateField(verbose_name=("Birthday"), null=True)
    slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return "/users/detail/{}".format(self.slug)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

