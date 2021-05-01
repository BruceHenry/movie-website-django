from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from movie.models import *
from django.http import HttpResponse, JsonResponse
import json
import math
import random
from movie.initializer import search_cache, search_index

#import sort value for dict
import operator

def add_seen(request, movie_id):
    print('oke')
    if request.is_ajax():
        history = Seen.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            movie = Popularity.objects.get(movieid_id=movie_id)
            weight = movie.weight
            movie.delete()
            # if user seen movie , popularity + 3
            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Seen(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('1')
        else:
            history.delete()
            return HttpResponse('0')


def add_expect(request, movie_id):
    if request.is_ajax():
        history = Expect.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            movie = Popularity.objects.get(movieid_id=movie_id)
            weight = movie.weight
            movie.delete()
            # add want to see movie , populartity +2
            new_record = Popularity(movieid_id=movie_id, weight=weight + 2)
            new_record.save()
            new_record = Expect(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('2')
        else:
            history.delete()
            return HttpResponse('0')



# turn of csrf post method in django
@csrf_exempt
def rate_movie(request):
    print('rate movie here ')
    if request.method == 'POST':
        print('rate movie here 2')
        if request.is_ajax():
            movie_id =request.POST.get('movieid')
            username = request.POST.get('username')
            print(movie_id)
            print(username)

            rate_score = request.POST.get('rate_score')
            movie = Movie.objects.get(movieid=movie_id)
            user = User.objects.get(username=username)
            try:
                rate_movie = User_Rate.objects.get(user=user, movie=movie)
                rate_movie.rate = int(rate_score)
                rate_movie.save()
                print(rate_movie)
                data = {'type': 'rated', 'rate_score':rate_score }
                print(data)
                return JsonResponse(data)
            except:
                rate_movie = User_Rate(movie=movie, user=user, rate=rate_score)
                rate_movie.save()
                print(rate_movie)
                data = {'type': 'rated' , 'rate_score':rate_score}
                print(data)
                return JsonResponse(data)

    return JsonResponse({'type':'error'})

@csrf_exempt
def review_movie(request):
    print('review movie here')
    if request.method == 'POST':
        print('rate movie here 2')
        if request.is_ajax():
            movie_id = request.POST.get('movieid')
            username = request.POST.get('username')
            content = request.POST.get('content')
            type = request.POST.get('type')

            if type =='review':
                try:
                    movie = Movie.objects.get(movieid=movie_id)
                    user = User.objects.get(username=username)

                    rate_movie = User_Rate.objects.get(user=user, movie=movie)
                    rate_movie.review = content
                    print(rate_movie)
                    rate_movie.save()

                except:
                    rate_movie = User_Rate(movie=movie, user=user, review=content)
                    rate_movie.save()
                    print(rate_movie)

                return JsonResponse({'mess':'success'})
            else:
                return JsonResponse({'mess':'error'})
    return JsonResponse({'mess':'error'})


@csrf_exempt
def reply_review(request):
    print('reply review here')
    if request.method == 'POST':
        print('reply review here 2')
        if request.is_ajax():
            data = {}
            review_id = request.POST.get('review_id')
            username = request.POST.get('username')
            content = request.POST.get('content')
            type = request.POST.get('type')

            if type == 'reply':
                try:
                    rate_movie = User_Rate.objects.get(id=int(review_id))
                    user = User.objects.get(username=username)
                    reply = ReplyToReview(user=user, review=rate_movie, content=content)
                    reply.save()
                    data['mess'] = 'succsess'
                    data['username'] = username
                    data['content'] = content
                    data['review_id'] = review_id

                    data['send_user_url'] = user.profile.get_absolute_url()
                    data['send_user_avatar']= user.profile.profile_picture.url
                    data['date_posted']  = 'just now'


                    return JsonResponse(data)
                except:
                    return JsonResponse({'mess':'error'})
    return JsonResponse({'mess':'error'})


@csrf_exempt
def add_tag(request):
    print('Add tag here ... ')
    if request.method == 'POST':
        print('Add tag here 2')
        if request.is_ajax():
            data = {}
            movieid = request.POST.get('movieid')
            username = request.POST.get('username')
            tags = request.POST.get('tag')
            type = request.POST.get('type')
            print(movieid)
            print(username)
            print(tags)

            movie = Movie.objects.get(movieid=movieid)
            user = User.objects.get(username=username)
            data = {}
            try:
                tag = MovieTags.objects.filter(movie=movie,user=user,tags=tags)
                if len(tag) > 0:
                    data['mess'] = 'error'
                    return JsonResponse(data)
                else:
                    tag = MovieTags(movie=movie, user=user, tags=tags)
                    tag.save()
                    data['mess'] = 'success'
                    data['tags'] = tags
                    data['count'] = MovieTags.objects.filter(movie=movie, tags=tags).count()
                    return JsonResponse(data)
            except:
                print('iam very sick !!!')
                return JsonResponse({'mess':'ERROR!!!'})











@csrf_protect
def detail(request, model, id):
    #set rate score
    items = []
    rate_score = 0
    try:
        if model.get_name() == 'movie' and id != 'None':
            try:
                d = Popularity.objects.get(movieid_id=id)
                weight = d.weight
                d.delete()
                new_record = Popularity(movieid_id=id, weight=weight + 1)
                new_record.save()
            except:
                new_record = Popularity(movieid_id=id, weight=1)
                new_record.save()
            label = 'actor'
            object = model.objects.get(movieid=id)
            records = Act.objects.filter(movieid_id=id)
            if request.user.get_username() != '':
                seen_list = [str(x).split('|')[1] for x in
                             Seen.objects.filter(username=request.user.get_username())]
                expect_list = [str(y).split('|')[1] for y in
                               Expect.objects.filter(username=request.user.get_username())]
                if id in seen_list:
                    object.flag = 1
                if id in expect_list:
                    object.flag = 2
            for query in records:
                for actor in Actor.objects.filter(actorid=query.actorid_id):
                    items.append(actor)
            # add rated movie for user
            review_form_flag = 1
            try:
                rate_movie = User_Rate.objects.get(movie=object, user=request.user)
                rate_score = rate_movie.rate
                print(rate_score)
                if rate_movie.review != None:
                    review_form_flag = -1
                reviews = User_Rate.objects.filter(movie=object).order_by('-date_posted')

            except:
                rate_score = 0
                reviews = User_Rate.objects.filter(movie=object).order_by('-date_posted')
                print(rate_score)


            # get tags from movie
            dict_tags ={}
            try:
                list_tags = MovieTags.objects.filter(movie=object)
                for tag in list_tags:
                    if tag.tags in dict_tags.keys():
                        dict_tags[tag.tags] +=1
                    else:
                        dict_tags[tag.tags] =1


            except:
                print('empty')
                dict_tags = {}


        if model.get_name() == 'actor':
            label = 'movie'
            object = model.objects.get(actorid=id)
            records = Act.objects.filter(actorid_id=id)
            for query in records:
                for movie in Movie.objects.filter(movieid=query.movieid_id):
                    items.append(movie)
    except:
        return render(request, '404.html')

    print(review_form_flag)
    return render(request, '{}_list.html'.format(label), {'items': items ,'dict_tags': dict_tags ,'number': len(items), 'object': object,'form_flag': review_form_flag , 'rate_score' : rate_score,'user':request.user, 'reviews':reviews})





def whole_list(request, model, page):
    if page is None:
        return render(request, '404.html')
    page = int(page)
    objects = model.objects.all()
    total_page = int(math.ceil(len(objects) / 10))
    if page > total_page:
        return render(request, '404.html')
    last_item_index = 10 * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(request, '{}_list.html'.format(model.get_name()), data)


def search(request, item, query_string, page):
    if item is None or query_string is None or page is None:
        return render(request, '404.html')
    query_string = query_string.replace("%20", " ")
    if item == 'movie':
        result = [search_index.data_in_memory['movie_dict'][movie_id] for movie_id in
                  search_index.search_movie(query_string)]
    elif item == 'actor':
        result = [search_index.data_in_memory['actor_dict'][actor_id] for actor_id in
                  search_index.search_actor(query_string)]
    else:
        return render(request, '404.html')
    page = int(page)
    total_page = int(math.ceil(len(result) / 10))
    if page > total_page and total_page != 0:
        return render(request, '404.html')
    last_item_index = 10 * page if page != total_page else len(result)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    return render(request, item + '_search.html',
                  {'items': result[10 * (page - 1):last_item_index], 'length': len(result),
                   'query_string': query_string, 'current_page': page, 'page_number': total_page, 'pages': pages})


def search_suggest(request, query_string):
    result = search_cache.get(query_string)
    if result is not None:
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    movie_list, actor_list = [], []
    search_result = search_index.search_suggest(query_string)
    for i, movie_id in enumerate(search_result[0]):
        movie = search_index.data_in_memory['movie_dict'].get(movie_id)
        movie_list.append({'movieid': movie.movieid, 'poster': movie.poster, 'title': movie.title})
        if i == 2:
            break
    for i, actor_id in enumerate(search_result[1]):
        actor = search_index.data_in_memory['actor_dict'].get(actor_id)
        actor_list.append({'actorid': actor.actorid, 'photo': actor.photo, 'name': actor.name})
        if i == 2:
            break
    result = {'movie': movie_list, 'actor': actor_list, 'text': query_string}
    search_cache.set(query_string, result)
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@csrf_protect
def seen(request, movie_id):
    if request.POST:
        try:
            d = Seen.objects.get(username=request.user.get_username(), movieid_id=movie_id)
            d.delete()
        except:
            return render(request, '404.html')
    records = Seen.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'seen.html', {'items': movies, 'number': len(movies)})


def expect(request, movie_id):
    if request.POST:
        try:
            d = Expect.objects.get(username=request.user.get_username(), movieid_id=movie_id)
            d.delete()
        except:
            return render(request, '404.html')
    records = Expect.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'expect.html', {'items': movies, 'number': len(movies)})


def top_movie(request):
    top_movie = Movie.objects.order_by('-rate')[:30]
    result = list(top_movie)
    # print(top_movie)

    top_movie = [result[i] for i in random.sample(range(len(result)), 11 )]

    return top_movie
