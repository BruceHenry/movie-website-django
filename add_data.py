from imdbpie import Imdb
import sqlite3


def execute_sql(s):
    con = sqlite3.connect('movie.db')
    with con:
        cur = con.cursor()
        cur.execute(s)


def single_quote(s):
    if len(s) == 0:
        return 'None'
    if s.find('\'') != -1:
        return s.replace("\'", "\'\'")
    else:
        return s


movie_list = []
movie_genres = {}
actor_set = {}

with open('data.csv') as f:
    for row in f.readlines()[1:]:
        columns = row.split(',')
        movie_id = columns[0].split('/')[4]
        genres = columns[1][:-1]
        movie_list.append(movie_id)
        movie_genres[movie_id] = genres

imdb = Imdb()
movie_count = 0
for movie_id in movie_list:
    try:
        title = imdb.get_title(movie_id)
        sql = (
            '''INSERT INTO movie_movie VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'''.format(
                movie_id,
                single_quote(str(title['base']['title'])),
                title['base']['year'],
                title['base']['runningTimeInMinutes'],
                movie_genres[movie_id],
                title['ratings']['rating'],
                single_quote(title['base']['image']['url']),
                single_quote(str(title['plot']['outline']['text'])),
                single_quote(str(imdb.get_title_videos(movie_id)['videos'][0]['encodings'][0]['play']))
            ))
        execute_sql(sql)
        movie_count += 1
        print("Insert movie: " + movie_id, movie_count)
    except Exception as e:
        print('Movie Insert Failure: ' + movie_id, e)
        continue

    actors = imdb.get_title_credits(movie_id)
    actor_length = len(actors['credits']['cast'])
    print('Add Actors: ', end='')
    for actor in actors['credits']['cast'][:5 if actor_length > 5 else actor_length]:
        actor_id = actor['id'].split('/')[2]
        try:
            if actor_id not in actor_set:
                sql = ('INSERT INTO movie_actor VALUES (\'{}\',\'{}\',\'{}\')'.format(
                    actor_id,
                    single_quote(str(actor['name'])),
                    single_quote(str(actor['image']['url']))))
                execute_sql(sql)
                actor_set[actor_id] = ''
                print(actor_id + ' success; ', end='')
            else:
                print(actor_id + ' existed; ', end='')
            sql = (
                'INSERT INTO movie_act(actorid_id, movieid_id) VALUES (\'{}\',\'{}\')'.format(actor_id,
                                                                                              movie_id))
            execute_sql(sql)
        except Exception as e:
            print(actor_id + ' failure', e, '; ', end='')
    print('\n')
