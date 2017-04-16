from django.contrib import admin
from movie.models import *


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'movieid', 'rate')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'actorid')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
