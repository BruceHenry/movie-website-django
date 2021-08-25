# MovieHunter
This is a movie website using **Django** as backend framework and SQLite as database.

For the current version, the following features are implemented, 
- **Search Engine** including inverted index and LRU cache
- User Management
- Login via Facebook (**OAuth** with Facebook API)
- **Recommender** according to user's taste

This website is deployed at [http://movie.hbao.blog](http://movie.hbao.blog).

***

## Index of Contents
1. [Data and Database](#data-and-database)
2. [Search Engine and Cache](#search-engine)
3. [Recommender](#recommender)
4. [Deployment Instructions](#deployment-instructions)


<a name="data-and-database"></a>

## Data and Database 
5000+ movie_ids from this [movie dataset](https://www.kaggle.com/oxanozaep/imdb-eda/data) are the origin data source. With these movie_ids, I utilized a python lib called [imdbpie](https://pypi.org/project/imdbpie/) to collect other columns of data. 

Currently, there are about **3000 movies** in the database.

To make it easy to deploy, SQLite is chosen as database. The database file is `movie.db` in the root directory.


<a name="search-engine"></a>

## Search Engine and Cache

- **Search Index**: Built an inverted index structure with wildcard to enable vague search.
- **Rank**: Movie search results are sorted by rating, while actor search results are sorted by the number of movies acted.
- **Cache**: Implemented a LRU Cache to record search result to make search suggestion faster.


<a name="recommender"></a>

## Recommender

An **item-based** recommender is implemented.

According to movies in user's movie list, movies with **same genres** will be recommended for each user. If user's movie list is empty or the number of movies to recommend is not sufficient, movies with highest ratings will be recommended instead.

The final recommendation is **randomly** chosen from a set of candidate movies, so the result will be slightly different each time.


<a name="deployment-instructions"></a>

## Deployment Instructions
1. Install [**Python 3**]( https://www.python.org/) in your computer, and make sure to set environment variable correctly.
2. Install **Django** for the Python environment. The easiest way is to use pip by running `pip install django`.
3. Open a terminal, input command: `python manage.py runserver 8080`
4. Open your web browser, input `localhost:8080` in the address bar.
- P.S. If you fail running `python manage.py runserver 8080`, try another port numbers, like 8081 or 8000.
