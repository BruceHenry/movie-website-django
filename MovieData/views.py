from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *


@csrf_protect
def index(request):
    if request.POST:
        if request.POST.get('Search'):
            content = request.POST.get('title')
            return redirect('/movie/search/' + content)
    else:
        data = {}
        if request.user.is_authenticated():
            data = {'username': request.user.get_username()}
        movies = Popularity.objects.all().order_by('-weight')
        temp_list = []
        for movie in movies[:5]:
            try:
                temp = {}
                temp['movieid'] = movie.movieid_id
                temp['poster'] = Movie.objects.get(movieid=movie.movieid_id).poster
                temp_list.append(temp)
            except:
                continue
        data['list'] = temp_list
        return render(request, 'base.html', data)
