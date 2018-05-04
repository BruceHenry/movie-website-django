from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import random


@csrf_protect
def index(request):
    if request.POST:
        if request.POST.get('Search'):
            content = request.POST.get('title')
            return redirect('/movie/search/' + content)
    else:
        data = {}
        if request.user.is_authenticated:
            data = {'username': request.user.get_username()}

            recommendations = set()
            seens_and_expects = set()
            seens = Seen.objects.filter(username=request.user.get_username())
            if len(seens) != 0:
                find_recommendations(recommendations, seens)
                for seen in seens:
                    seens_and_expects.add(seen.movieid.movieid)
                    recommendations.remove(seen.movieid.movieid)
            else:
                expects = Expect.objects.filter(username=request.user.get_username())
                if len(expects) != 0:
                    find_recommendations(recommendations, expects)
                    for expect in expects:
                        seens_and_expects.add(expect.movieid.movieid)
                        recommendations.remove(expect.movieid.movieid)

            recommendation = []
            if len(recommendations) < 5:
                high_rates = Movie.objects.exclude(movieid__in=seens_and_expects).order_by('-rate')[:50]
                supplies = random.sample(list(high_rates), 5 - len(recommendations))
                for supply in supplies:
                    recommendations.add(supply.movieid)
                for movieid in recommendations:
                    try:
                        temp = {'movieid': movieid, 'poster': Movie.objects.get(movieid=movieid).poster}
                        recommendation.append(temp)
                    except:
                        continue
            else:
                for movieid in random.sample(recommendations, 5):
                    try:
                        temp = {'movieid': movieid, 'poster': Movie.objects.get(movieid=movieid).poster}
                        recommendation.append(temp)
                    except:
                        continue
            data['recommendations'] = recommendation

        popular_movies = Popularity.objects.all().order_by('-weight')
        popular = []
        for movie in popular_movies[:5]:
            try:
                temp = {'movieid': movie.movieid_id, 'poster': Movie.objects.get(movieid=movie.movieid_id).poster}
                popular.append(temp)
            except:
                continue
        data['popular'] = popular

        return render(request, 'base.html', data)


def find_recommendations(recommendations, user_favorite):
    for seen_or_expect in user_favorite:
        cur = Movie.objects.get(movieid=seen_or_expect.movieid.movieid)
        if cur.plot is None or cur.plot == '':
            continue
        movies = Movie.objects.filter(genres=cur.genres)
        elements = []
        corpus = []
        for movie in movies:
            if movie.plot is not None and movie.plot != '':
                elements.append({'movieid': movie.movieid})
                corpus.append(movie.plot)

        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus).todense())
        weight = tfidf.toarray()

        cur_vector = []
        for i in range(len(elements)):
            elements[i]['vector'] = weight[i].reshape(1, -1)
            if elements[i]['movieid'] == seen_or_expect.movieid.movieid:
                cur_vector = elements[i]['vector']

        for element in elements:
            dist = euclidean_distances(cur_vector, element['vector'])
            element['dist'] = dist[0, 0]
        elements = sorted(elements, key=lambda e: e['dist'])

        for i in range(0, min(10, len(elements))):
            recommendations.add(elements[i]['movieid'])
