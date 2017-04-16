from imdbpie import Imdb
import sqlite3


def insert(s):
    con = sqlite3.connect('movie.db')
    with con:
        cur = con.cursor()
        cur.execute(s)


def single_quote(s):
    if len(s) == 0:
        return 'None'
    if s.find('\'') != -1:
        ss = s.split("\'")
        new = ''
        for x in ss:
            new = new + "\'" + "\'" + x
        return new[2:]
    else:
        return s


imdb = Imdb()
imdb = Imdb(anonymize=True)  # to proxy requests

top250 = []
top250 = imdb.top_250()
for item in top250:
    title = imdb.get_title_by_id(item['tconst'])
    if len(title.trailers) > 0:
        trailer_url = title.trailers[0]['url']
    else:
        trailer_url = 'None'
    new_movie = (
        '''INSERT INTO movie_movie VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'''.format(
            item['tconst'],
            single_quote(str(item['title'])),
            item['year'],
            title.release_date,
            item['rating'],
            single_quote(item['image']['url']),
            single_quote(str(title.plot_outline)),
            single_quote(str(trailer_url)),
        ))
    try:
        print("Insert movie:" + new_movie)
        insert(new_movie)
    except:
        print("The movie is already in the database!")
        continue

    for actor in title.cast_summary:
        new_act = (
            'INSERT INTO movie_act(actorid_id, movieid_id) VALUES (\'{}\',\'{}\')'.format(actor.imdb_id, item['tconst']))

        print("Insert act:" + new_act)
        insert(new_act)

        person = imdb.get_person_by_id(actor.imdb_id)
        new_actor = ('INSERT INTO movie_actor VALUES (\'{}\',\'{}\',\'{}\')'.format(actor.imdb_id, actor.name,
                                                                                   single_quote(str(person.photo_url))))
        try:
            insert(new_actor)
            print("Insert actor:" + new_actor)
        except:
            continue
