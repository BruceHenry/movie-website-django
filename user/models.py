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
# from movie.models import User_Rate, ReplyToReview

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
    full_name = models.CharField(max_length=140, null=True)
    # social network
    twitter_link = models.CharField(max_length=140, null=True)
    facebook_link = models.CharField(max_length=140, null=True)
    google_link = models.CharField(max_length=140, null=True)
    linkedln_link = models.CharField(max_length=140, null=True)
    instagram = models.CharField(max_length=140, null=True)



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

    def total_likes(self):

        return self.likes.count()

    def total_reports(self):
        return self.reports.count()

    def total_comments(self):
        return CommentToPost.objects.filter(post = self).count()

    def get_all_reply(self):
        replys = CommentToPost.objects.filter(post = self).order_by('-date_posted')
        return replys

    def get_date(self):
        return humanize.naturaltime(self.date_posted)

class CommentToPost(models.Model):
    content = models.TextField(max_length=240)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PostToUser, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_date(self):
        return humanize.naturaltime(self.date_posted)

# create notification if post created
@receiver(post_save, sender=PostToUser)
def create_notification(sender, instance, created, **kwargs):
    if created:
        if instance.to_user != instance.author:
            Notification.objects.create(post = instance, user = instance.to_user, user2=instance.author ,type=2)



# create notification if post created
@receiver(post_save, sender=CommentToPost)
def create_notification2(sender, instance, created, **kwargs):
    if created:
        if instance.post.author != instance.author:
            Notification.objects.create(reply_to_post = instance ,user = instance.post.author, user2=instance.author ,type=3)


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

# create notification if follow created
@receiver(post_save, sender=Follow)
def create_notification3(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(follow = instance, user = instance.user2, user2=instance.user1 ,type=1)


class Activity(models.Model):
    follow = models.ForeignKey(Follow, on_delete = models.CASCADE, blank=True, null=True)
    review = models.ForeignKey("movie.User_Rate", on_delete = models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(PostToUser, on_delete = models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField() # 1 follow, 2 post , 3 review
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.type ==3:
            return str(self.user)+ ' review ' + str(self.review.movie.title)
        if self.type ==1:
            return str(self.user) + ' follow '
        if self.type ==2:
            return str(self.user) + ' post'



    def get_date(self):
        return humanize.naturaltime(self.date_posted)

# add notigications
class Notification(models.Model):
    #to user 
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    #from_user
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', blank=True, null=True)
    NOTIFICATION_TYPES = ((1,'follow'), (2,'post'), (3, 'reply post'), (4, 'reply review'), (5, 'report'), (6, 'like review'), (7, 'like post'))
    date_posted = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)
    type = models.IntegerField(choices=NOTIFICATION_TYPES)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(PostToUser, on_delete=models.CASCADE, blank=True, null=True)
    reply_to_review = models.ForeignKey("movie.ReplyToReview", on_delete=models.CASCADE, blank=True, null=True)
    reply_to_post = models.ForeignKey(CommentToPost, on_delete=models.CASCADE, blank=True, null=True)
    review = models.ForeignKey("movie.User_Rate", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.type == 1:
            return str(self.user2) + ' follow you' 
        if self.type == 2:
            return str(self.user2) + ' just posted on your wall' 
        if self.type == 4:
            return str(self.user2) + ' just replied to the review about {} movie'.format(self.reply_to_review.review.movie.title) 
        if self.type == 3:
            return str(self.user2) + ' just replied to your post'
        if self.type == 6:
            return str(self.user2) + ' liked your review  about {}'.format(self.review.movie.title)
        if self.type == 7:
            return str(self.user2) + ' liked your post'
    
    def get_date(self):
        return humanize.naturaltime(self.date_posted)
    
    def get_link(self):
        if self.type == 1:
            return self.user2.profile.get_absolute_url()
        if self.type == 2:
            return self.user.profile.get_absolute_url()
        if self.type == 4:
            return self.reply_to_review.review.get_absolute_url()
        if self.type == 3:
            return self.reply_to_post.post.to_user.profile.get_absolute_url()
        if self.type == 6:
            return self.review.get_absolute_url()
        if self.type == 7:
            return self.post.to_user.profile.get_absolute_url()


class UserSeenNotifycation(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, blank=True, null=True, related_name='noti')
    # to user ( user get this notification)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name= 'user_get_that_noti')
    is_seen = models.BooleanField(default=False)

    def get_all_noti_not_seen(self):
        return UserSeenNotifycation.objects.filter(user = self.user, is_seen = False)
    
    def count_not_seen(self):
        return UserSeenNotifycation.objects.filter(user = self.user, is_seen = False).count()

    def __str__(self):
        return str(self.user.username) + '|' + str(self.notification)

            
# create user_seen after notification create
@receiver(post_save, sender=Notification)
def create_notification_seen(sender, instance, created, **kwargs):
    if created:
        UserSeenNotifycation.objects.create(user = instance.user, notification = instance)


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

def create_new_folow_notifications(sender, **kwargs):
    
	notify = kwargs['instance']
	print(notify.user.username)
	channel_layer = get_channel_layer()
	room_name = 'noti_' + str(notify.user.id)
	my_dictionary = {
		'sender': notify.user2.username,
		'to_user': notify.user.username,
		'date': str(notify.get_date()),
		'is_seen': notify.is_seen,
        'noti': str(notify),
        'sender_image': notify.user2.profile.profile_picture.url,
        'link': notify.get_link()
	}

	# print(my_dictionary)
	message = json.dumps(my_dictionary, default=str)
	
	async_to_sync(channel_layer.group_send)(
		room_name, {
            'type': 'chat_message',
            'message': message
		}
	)

post_save.connect(create_new_folow_notifications, sender=Notification)