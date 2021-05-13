from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# add lib for Profile user with signals 
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify

# add exception for user -> to profile 
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

#add unique Email 
# User._meta.get_field('email')._unique = True

# add os to display url image avatar 
import os

#add timezones
from django.utils import timezone
import humanize
import datetime as dt

# user's activity 
from movie.models import User_Rate

# human time 
from django.contrib.humanize.templatetags import humanize


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
    # slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length=255, blank=True)

    # def slug(self):
    #     return slugify(self.id)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return "/user/detail/{}".format(self.id)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

class PostToUser(models.Model):
    content = models.TextField(max_length=240)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserComment')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ToUser')
    likes = models.ManyToManyField(User, related_name='likes', blank = True)
    reports = models.ManyToManyField(User, related_name='reports', blank = True)

    def __str__(self):
        return self.content
    
    def save(self, *args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            Activity.objects.create(post=self, user = self.author, type = 2)

    #def get_absolute_url(self):
    #    return reverse('beets:beets-detail', kwargs={'pk': self.pk})

    def total_likes(self):

        return self.likes.count()

    def total_reports(self):
        return self.reports.count()

    def total_comments(self):
        return CommentToPost.objects.filter(post = self).count()

    def get_all_reply(self):

        replys = CommentToPost.objects.filter(post = self).order_by('-date_posted')

        return replys

class CommentToPost(models.Model):
    content = models.TextField(max_length=240)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PostToUser, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content



class Follow(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

    def __str__(self):
        return str(self.user1) + '|' + str(self.user2)

    # Override the save() method of your User model or extended Usermodel
    # link https://stackoverflow.com/questions/52196365/django-automatically-create-a-model-instance-when-another-model-instance-is-cr/52196467
    
    def save(self, *args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            Activity.objects.create(follow=self, user = self.user1, type = 1)

class Activity(models.Model):
    follow = models.ForeignKey(Follow, on_delete = models.CASCADE, blank=True, null=True)
    review = models.ForeignKey(User_Rate, on_delete = models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(PostToUser, on_delete = models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField() # 1 follow, 2 post , 3 review
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Activity by '+ str(self.user) + str(self.type)

    def get_date(self):
        return humanize.naturaltime(self.date_posted)

