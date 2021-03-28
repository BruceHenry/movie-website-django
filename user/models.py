from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

#add unique Email 
User._meta.get_field('email')._unique = True

class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=140)  
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='images/', blank=True)
    birthday = models.DateField(verbose_name=("Birthday"), null=True)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)

