from django.db import models
from django.contrib.auth.models import User

#add timezones
from django.utils import timezone
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
import user.models 

from django.contrib.humanize.templatetags import humanize



class Movie(models.Model):
    movieid = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    length = models.CharField(max_length=10)
    genres = models.CharField(max_length=100)
    rate = models.IntegerField(default=0)
    poster = models.URLField(default='')
    plot = models.CharField(max_length=500)
    trailer = models.URLField(default='')
    #addd
    movielenid = models.IntegerField(default=0)
    youtubeid = models.CharField(max_length=500)

    def __str__(self):
        return self.movieid + '|' + self.title

    @staticmethod
    def get_name():
        return 'movie'
    #add get_average for movie
    def get_average(self):
        sum = 0
        count = 0
        for rate in  User_Rate.objects.filter(movie = self):
            sum += rate.rate
            count +=1
        return sum/count


class Actor(models.Model):
    actorid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    photo = models.URLField()

    def __str__(self):
        return self.actorid + '|' + self.name

    @staticmethod
    def get_name():
        return 'actor'
    
    def get_simple_name(self):
        if len(self.name) > 12:
            if len(self.name.split()[0]) < len(self.name.split()[1]):
                return self.name.split()[1]
            return self.name.split()[0]
        else:
            return self.name


class Act(models.Model):
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)
    actorid = models.ForeignKey('Actor', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.actorid.actorid + '|' + self.movieid.movieid


class Seen(models.Model):
    username = models.CharField(max_length=150)
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '|' + self.movieid.movieid


class Expect(models.Model):
    username = models.CharField(max_length=150)
    movieid = models.ForeignKey('Movie', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '|' + self.movieid.movieid


class Popularity(models.Model):
    movieid = models.ForeignKey('Movie', default=' ', on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.movieid.movieid + '|' + str(self.weight)

class User_Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    review = models.CharField(max_length=500, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)

    def __str__(self):
        return self.movie.movieid + '|' + str(self.user.username) + '|' + str(self.rate) + '|' + str(self.review)

   
    def total_likes(self):

        return self.likes.count()


    def total_reply(self):
        return ReplyToReview.objects.filter(review = self).count()

    def get_all_reply(self):
        #order by count like =>>> good
        replys = ReplyToReview.objects.filter(review = self).order_by('-date_posted')

        return replys
    
    def get_absolute_url(self):
        return "/movie/movie_detail/{}".format(self.movie.movieid)

    def get_date(self):
        return humanize.naturaltime(self.date_posted)



class ReplyToReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(User_Rate, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='reply_likes', blank=True)

    def total_likes(self):

        return self.likes.count()

    def __str__(self):
        return self.user.username + '|' + str(self.review) + '|' + str(self.content)

    def get_date(self):
        return humanize.naturaltime(self.date_posted)
    


# create notification if follow created
@receiver(post_save, sender=ReplyToReview)
def create_notification4(sender, instance, created, **kwargs):
    if created:
        if instance.user != instance.review.user:
            user.models.Notification.objects.create(reply_to_review = instance, user = instance.review.user, user2=instance.user ,type=4)


class MovieTags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)
    tags =  models.CharField(max_length=150)


    def __str__(self):
        return str(self.movie) + '|' + str(self.tags)
    def count_tag(self):
        return MovieTags.objects.filter(movie=self.movie, tags=self.tags).count()



class User_Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username + '|' + str(self.content) + '|' + str(self.date_posted)


