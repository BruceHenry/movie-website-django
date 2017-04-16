from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index(request):
    if request.POST:
        # if request.POST.get('Search Movie'):
        #     content = request.POST.get('title')
        #     return redirect('/movie/movie_search/' + content)
        # if request.POST.get('Search Actor'):
        #     content = request.POST.get('title')
        #     return redirect('/movie/actor_search/' + content)
        if request.POST.get('Search'):
            content = request.POST.get('title')
            return redirect('/movie/search/' + content)
    else:
        data = {}
        if request.user.is_authenticated():
            data = {'username': request.user.get_username()}
        return render(request, 'base.html', data)