from django.contrib import admin
from movie.models import *


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'movieid', 'rate')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'actorid')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Seen)
admin.site.register(Expect)
admin.site.register(Popularity)
admin.site.register(User_Rate)
admin.site.register(ReplyToReview)
admin.site.register(MovieTags)

admin.site.register(User_Search)

