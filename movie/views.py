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
from django.contrib.auth.decorators import login_required

from user.models import Activity

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
                # print(rate_movie)
                data = {'type': 'rated', 'rate_score':rate_score }
                # print(data)
                return JsonResponse(data)
            except:
                rate_movie = User_Rate(movie=movie, user=user, rate=rate_score)
                rate_movie.save()
                # print(rate_movie)
                data = {'type': 'rated' , 'rate_score':rate_score}
                # print(data)
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
                    # every one create 1 review => create here !!!
                    Activity.objects.create(review = rate_movie, user = request.user, type = 3)
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
def movie_detail(request, model, id):
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
                    print(actor)
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

    except:
        return render(request, '404.html')

    # print(review_form_flag)
    return render(request, 'movie_detail.html', {'items': items  ,'number': len(items), 'object': object , 'rate_score' : rate_score,'user':request.user, 'reviews':reviews})

@csrf_exempt
def actor_detail(request, model, id):
    items = []
    if model.get_name() == 'actor':
        label = 'movie'
        object = model.objects.get(actorid=id)
        records = Act.objects.filter(actorid_id=id)
        for query in records:
            for movie in Movie.objects.filter(movieid=query.movieid_id):
                items.append(movie)

    return render(request, 'movie_list_all.html', {'items': items, 'number': len(items), 'object': object})



def movie_whole_list(request, model, page):
    if page is None:
        return render(request, '404.html')
    page = int(page)
    #movie
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
    # print(objects)
    objects =  objects[ 2:]
    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(request, 'movie_list_all.html'.format(model.get_name()), data)



def actor_whole_list(request, model, page):
    if page is None:
        return render(request, '404.html')
    page = int(page)
    #actor
    objects = model.objects.all()
    print(objects)
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
    # print(objects)
    # objects =  objects[ 2:]

    # for actor in objects[10 * (page - 1):last_item_index]:
    #     print(actor.photo)

    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(request, 'actor_list_all.html', data)

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
    # print(result)
    print(query_string)
    #save to the db search
    #search_query = User_Search(content=query_string, user = request.user)
    #search_query.save()


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

@login_required
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


# get favourite movie of user
def favourite_movie(user):
    try:
        # filter with source code https://stackoverflow.com/questions/10040143/how-to-do-a-less-than-or-equal-to-filter-in-django-queryset
        # list_movie = User_Rate.objects.filter(user=request.user, rate_gte=4)
        # print(user)
        # tinh trung binh luot rate
        user_rate = User_Rate.objects.filter(user=user)
        count = User_Rate.objects.filter(user=user).count()
        sum_rate = 0
        for rate in user_rate:
            sum_rate += rate.rate
        medium = sum_rate/count
        # print(medium)
        list_rate_good = User_Rate.objects.filter(user=user, rate__gte=medium)
        print('list movieid liked : ')
        list_movie = [rate.movie.movieid for rate in list_rate_good]
        # print(list_movie)

    except:
        list_movie = []

    return list_movie

import pandas as pd
import numpy as np

def get_recommend_by_jaccard(movieid):
    # get data file
    mv_genres = pd.read_csv('data/data_movie.csv')
    mv_tags = pd.read_csv('data/genome_scores_data.csv')
    mv_tags_desc = pd.read_csv('data/genome-tags.csv')

    print(mv_tags.head())
    print(mv_genres.head())
    print(mv_tags_desc.head())

    movie = {}
    movie = pd.DataFrame(data=movie)

    movie['imdbId'] = mv_genres['movieid']
    movie['movieId'] = mv_genres['movielenid']

    #prepare
    mv_tags_denorm = mv_tags.merge(mv_tags_desc, on='tagId').merge(movie, on='movieId')
    mv_tags_denorm['relevance_rank'] = mv_tags_denorm.groupby("movieId")["relevance"].\
        rank(method="first",ascending=False).astype('int64')

    mv_tags_list = mv_tags_denorm[mv_tags_denorm.relevance_rank <= 50].groupby(['movieId', 'imdbId'])['tag'].apply(lambda x: ','.join(x)).reset_index()
    mv_tags_list['tag_list'] = mv_tags_list.tag.map(lambda x: x.split(','))

    #example

    target_movie_id = movieid

    # print(target_movie_id)

    target_tag_list = mv_tags_list[mv_tags_list.imdbId == target_movie_id].tag_list.values[0]
    mv_tags_list_sim = mv_tags_list[['movieId', 'imdbId', 'tag_list', 'tag']]
    mv_tags_list_sim['jaccard_sim'] = mv_tags_list_sim.tag_list.map(
        lambda x: len(set(x).intersection(set(target_tag_list))) / len(set(x).union(set(target_tag_list))))
    # print(f'Movies most similar to {target_movie_id} based on tags:')

    recommend_movie = mv_tags_list_sim.sort_values(by='jaccard_sim', ascending=False).head(12)['imdbId']

    recommend_movie = recommend_movie[1:]


    return list(recommend_movie)


from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def get_recommend_by_cosine(list_movie_id):

    mv_genres = pd.read_csv('data/data_movie.csv')
    mv_tags = pd.read_csv('data/genome_scores_data.csv')
    mv_tags_desc = pd.read_csv('data/genome-tags.csv')

    # print(mv_tags.head())
    # print(mv_genres.head())
    # print(mv_tags_desc.head())

    movie = {}
    movie = pd.DataFrame(data=movie)

    movie['imdbId'] = mv_genres['movieid']
    movie['movieId'] = mv_genres['movielenid']

    # prepare
    mv_tags_denorm = mv_tags.merge(mv_tags_desc, on='tagId').merge(movie, on='movieId')
    mv_tags_denorm['relevance_rank'] = mv_tags_denorm.groupby("movieId")["relevance"]. \
        rank(method="first", ascending=False).astype('int64')

    mv_tags_list = mv_tags_denorm[mv_tags_denorm.relevance_rank <= 50].groupby(['movieId', 'imdbId'])['tag'].apply(
        lambda x: ','.join(x)).reset_index()
    mv_tags_list['tag_list'] = mv_tags_list.tag.map(lambda x: x.split(','))

    #model
    model = Doc2Vec.load('model/model_version1')
    mv_tags_vectors = model.dv.vectors

    #generate movie recommendation for user
    # compute user vector as an average of movie vectors seen by that user
    user_movie_vector = np.zeros(shape=mv_tags_vectors.shape[1])

    # remove data with not tag in data
    for movieid in list_movie_id:
        if mv_tags_list[mv_tags_list["imdbId"] == movieid].empty:
            # print(movieid)
            list_movie_id.remove(movieid)

    # print(list_movie_id)

    for movie_id in list_movie_id:

        mv_index = mv_tags_list[mv_tags_list["imdbId"] == movie_id].index.values[0]
        user_movie_vector += mv_tags_vectors[mv_index]

    user_movie_vector /= len(list_movie_id)

    #  find movies similar to user vector to generate movie recommendations

    print('Movie Recommendations:')

    sims = model.docvecs.most_similar(positive=[user_movie_vector], topn=30)
    results = []
    for i, j in sims:
        movie_sim = mv_tags_list.loc[int(i), "imdbId"].strip()
        if movie_sim not in list_movie_id:
            # print(movie_sim)
            results.append(movie_sim)

    return results

from django.utils import timezone
import humanize
import datetime as dt
from datetime import timedelta

@login_required
@csrf_exempt
def get_search_value(request):
    print('Get search value here ... ')
    data = {}
    if request.method == 'POST':
        if request.is_ajax():
            user_id = request.POST.get('user_id')
            content = request.POST.get('content')
            keyup_now = request.POST.get('keyup_now')

            user = User.objects.get(id=user_id)
             
            try:
                all_sessions = User_Search.objects.all()
                print('len all_sessions:', len(all_sessions))
                all_search_value = [session.content for  session in  all_sessions]

                #search in all_search_value , which the best similarity 
                sort_search_value = sorted(all_search_value , key = lambda value: jaccard_similarity(content, value)[0])
                
                best_similarity_session_content = sort_search_value[-1]
                jaccard_value = jaccard_similarity(content, best_similarity_session_content)[0]
                list_key_recommend = jaccard_similarity(content, best_similarity_session_content)[1]
                print(jaccard_value)
                print(list_key_recommend)
                # if jaccard similarity > 0.5 
                if jaccard_value > 0.5:
                    list_key_success = []
                    for key_recommend in list_key_recommend :
                        if key_recommend.find(keyup_now) != -1 and len(key_recommend) > len(keyup_now):
                            list_key_success.append(key_recommend)
                            print('2')
                            print('Exactly recommend key :', key_recommend)
                        
                    if len(list_key_success) > 0:
                        #recommend for last search by diffrent user ....
                        longest_key = max(list_key_success, key=len)
                        data['mess'] = 'success'
                        data['check_recommend'] = 'true'
                        data['key_recommend'] = longest_key

                else:
                    data['mess'] = 'success'
                    data['check_recommend'] = 'false'
                    data['key_recommend'] = 'false'
            except:
                data['mess'] = 'false'
                data['check_recommend'] = 'false'
                data['key_recommend'] = 'false'
            
            
            #save search value to database 
            
            try:
                now_user_session = User_Search.objects.filter(user=user).latest('date_posted')
                if content.find(now_user_session.content) != -1:
                    now_user_session.content = content
                    now_user_session.save()
                else:
                    new_user_session = User_Search(user=user, content=content)
                    new_user_session.save()
            except:
                # first user create session 
                new_user_session = User_Search(user=user, content=content)
                new_user_session.save()


    return JsonResponse(data)

                

def jaccard_similarity(text1, text2):
    list1 = text1.split(',')

    list2 = text2.split(',')
    # print(text1, text2, len(set(list1).intersection(set(list2))) / len(set(list1).union(set(list2))), set(list2) - set(list1) )
    return (len(set(list1).intersection(set(list2))) / len(set(list1).union(set(list2))), set(list2) - set(list1))


def action_movie(request):
    all_action_movie = Movie.objects.order_by('-rate')[:200]
    results = []
    for movie in all_action_movie:
        if check_genres(movie, 'Action'):
            results.append(movie)
    return [results[i] for i in random.sample(range(len(results)), 11 )]
    

def comedy_movie(request):
    all_action_movie = Movie.objects.order_by('-rate')[:200]
    results = []
    for movie in all_action_movie:
        if check_genres(movie, 'Comedy'):
            results.append(movie)
    return [results[i] for i in random.sample(range(len(results)), 11 )]

def check_genres(movie, genre):
    if movie.genres.find(genre)!=-1:
        return True
    return False