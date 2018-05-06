import re
from movie.models import *
from movie.binarytree import binary_tree

data_in_memory = {'movie_dict': {}, 'actor_dict': {}, 'movie_list': [], 'actor_list': []}


def load_data_from_db():
    global data_in_memory
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        data_in_memory['movie_dict'][movie.movieid] = movie
        data_in_memory['movie_list'].append(movie)
    actor_objects = Actor.objects.all()
    for actor in actor_objects:
        data_in_memory['actor_dict'][actor.actorid] = actor
        data_in_memory['actor_list'].append(actor)


def _permute(term):
    x = term + "$"
    return [x[i:] + x[:i] for i in range(len(x))]


def tokenize(text):
    clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
    tokens = clean_string.split()
    return tokens


def index_dir():
    global permuterm_index
    permuterm_index = binary_tree()
    movie_objects = data_in_memory['movie_list']
    for movie in movie_objects:
        for term in tokenize(movie.title):
            for permuted_term in _permute(term):
                if permuted_term not in permuterm_index:
                    permuterm_index[permuted_term] = set()
                if movie.movieid not in permuterm_index[permuted_term]:
                    permuterm_index[permuted_term].add(movie.movieid)
    actor_objects = data_in_memory['actor_list']
    for actor in actor_objects:
        for a_term in tokenize(actor.name):
            for a_permuted_term in _permute(a_term):
                if a_permuted_term not in permuterm_index:
                    permuterm_index[a_permuted_term] = set()
                if actor.actorid not in permuterm_index[a_permuted_term]:
                    permuterm_index[a_permuted_term].add(actor.actorid)
    # return permuterm_index


def rating_dir():
    global rating_dic
    rating_dic = {}
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        rating_dic[movie.movieid] = movie.rate


def get_rating(id):
    return rating_dic[id]


def get_act_num(id):
    records = Act.objects.filter(actorid_id=id)
    return len(records)


def _rotate(term):
    x = term + "$"
    if "*" not in term:
        return x
    n = x.index("*") + 1
    return (x[n:] + x[:n])


def add_Wild_Card(term):
    tokens = []
    n = len(term)
    for i in range(1, n):
        tokens.append(term[:i] + "*" + term[i:])
    return tokens


def wildcard_search(text):
    result = []
    intersection_movies, union_movies = set(), set()
    intersection_actors, union_actors = set(), set()
    suggest_movies, suggest_actors = set(), set()
    movie_objects = data_in_memory['movie_list']
    for movie in movie_objects:
        intersection_movies.add(movie.movieid)
    actor_objects = data_in_memory['actor_list']
    for actor in actor_objects:
        intersection_actors.add(actor.actorid)
    for token in tokenize(text):
        result_movies, result_actors = set(), set()
        search_token_1 = _rotate("*" + token)
        search_token_2 = _rotate(token + "*")
        for id in list(crawl_tree(permuterm_index.root, search_token_1)) + list(
                crawl_tree(permuterm_index.root, search_token_2)):
            result_movies.add(id) if id[:2] == "tt" else result_actors.add(id)
        tokens = add_Wild_Card(token)
        for t in tokens:
            search_token = _rotate(t)
            for id in list(crawl_tree(permuterm_index.root, search_token)):
                suggest_movies.add(id) if id[:2] == "tt" else suggest_actors.add(id)

        intersection_movies = intersection_movies.intersection(result_movies)
        union_movies = union_movies.union(result_movies)
        intersection_actors = intersection_actors.intersection(result_actors)
        union_actors = union_actors.union(result_actors)

    union_movies = union_movies - intersection_movies
    union_actors = union_actors - intersection_actors
    suggest_movies = suggest_movies - intersection_movies - union_movies
    suggest_actors = suggest_actors - intersection_actors - union_actors
    result.append(
        sorted(intersection_movies, key=get_rating, reverse=True) + sorted(union_movies, key=get_rating, reverse=True) +
        sorted(suggest_movies, key=get_rating, reverse=True))
    result.append(sorted(intersection_actors, key=get_act_num, reverse=True) + sorted(union_actors, key=get_act_num,
                                                                                      reverse=True) +
                  sorted(suggest_actors, key=get_act_num, reverse=True))
    return result


def search_suggest(text):
    result = []
    intersection_movies = set()
    intersection_actors = set()
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        intersection_movies.add(movie.movieid)
    actor_objects = Actor.objects.all()
    for actor in actor_objects:
        intersection_actors.add(actor.actorid)
    for token in tokenize(text):
        result_movies, result_actors = set(), set()
        search_token_1 = _rotate("*" + token)
        search_token_2 = _rotate(token + "*")
        for id in list(crawl_tree(permuterm_index.root, search_token_1)) + list(
                crawl_tree(permuterm_index.root, search_token_2)):
            result_movies.add(id) if id[:2] == "tt" else result_actors.add(id)

        intersection_movies = intersection_movies.intersection(result_movies)
        # union_movies = union_movies.union(result_movies)
        intersection_actors = intersection_actors.intersection(result_actors)
        # union_actors = union_actors.union(result_actors)

    # union_movies = union_movies - intersection_movies
    # union_actors = union_actors - intersection_actors
    result.append(sorted(intersection_movies, key=get_rating, reverse=True))
    result.append(sorted(intersection_actors, key=get_act_num, reverse=True))
    return result


def crawl_tree(node, term):
    if not node:
        return set()
    if ('*' in term and node.key.startswith(term[:-1])) or term == node.key:
        x = node.data
    else:
        x = set()
    return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))
