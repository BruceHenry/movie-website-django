from django.conf.urls import url
from . import views
from . import models
from django.urls import include, path


urlpatterns = [
    url(r'^movie_all/(?P<page>\d*)', views.movie_whole_list, {'model': models.Movie}, name='movie_whole_list'),
    url(r'^actor_all/(?P<page>\d*)', views.actor_whole_list, {'model': models.Actor}, name='actor_whole_list'),
    url(r'^movie_detail/(?P<id>.*)', views.movie_detail, {'model': models.Movie}, name='movie_detail'),
    url(r'^actor_detail/(?P<id>.*)', views.actor_detail, {'model': models.Actor}, name='actor_detail'),
    url(r'^search/(?P<item>.*)/(?P<query_string>.*)/(?P<page>\d*).*', views.search, name='search'),
    url(r'^seen/(?P<movie_id>.*)', views.seen, name='seen'),
    url(r'^add_seen/(?P<movie_id>.*)', views.add_seen, name='seen'),
    url(r'^expect/(?P<movie_id>.*)', views.expect, name='expect'),
    url(r'^add_expect/(?P<movie_id>.*)', views.add_expect, name='expect'),
    url(r'^search_suggest/(?P<query_string>.*)', views.search_suggest, name='search_suggest'),

    # Viet lai view cho movie detail , tu do them rate va review vao
    # Voi actor thi chua can
    # Lam man share fb cho movie

    # viet function cho moive share ....

    # path('detail/<str:movie_id>/', views.movie_detail, name='movie-detail'),
    #ajax send data
    path('review_movie/', views.review_movie, name='review-movie'),
    path('reply_review/', views.reply_review, name='reply-review'),
    path('rate_movie/', views.rate_movie, name='rate-movie'),
    path('top_movie/', views.top_movie, name='top_movie'),
    path('add_tag/', views.add_tag, name='add-tag'),

    #get comunity tags
    path('favourite_movie/', views.favourite_movie, name='favourite-movie'),

    # path('comunity_tags/', views.)
]
