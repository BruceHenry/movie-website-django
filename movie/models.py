from django.db import models
from django.contrib.auth.models import User

#add timezones
from django.utils import timezone
import humanize
import datetime as dt


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


class Actor(models.Model):
    actorid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    photo = models.URLField()

    def __str__(self):
        return self.actorid + '|' + self.name

    @staticmethod
    def get_name():
        return 'actor'


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

    # def save(self, *args, **kwargs):
    #     created = not self.pk
    #     super().save(*args,**kwargs)
    #     if created:
    #         Activity.objects.create(review=self, user = self.user, type = 3)

    def total_likes(self):

        return self.likes.count()


    def total_reply(self):
        return ReplyToReview.objects.filter(review = self).count()

    def get_all_reply(self):
        #order by count like =>>> good
        replys = ReplyToReview.objects.filter(review = self).order_by('-date_posted')

        return replys


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


class MovieTags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)
    tags =  models.CharField(max_length=150)


    def __str__(self):
        return str(self.movie) + '|' + str(self.tags)


class User_Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username + '|' + str(self.content) + '|' + str(self.date_posted)


