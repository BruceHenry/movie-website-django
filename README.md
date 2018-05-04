# MovieHunter
This is a movie website using **Django** as backend framework and SQLite as database.

For the current version, the following features are implemented, 
- **Search Engine** including inverted index and LRU cache
- User Management
- Login via Facebook (**OAuth** with Facebook API)
- **Recommender** according to user's taste

I deployed the website at [https://baohan08.pythonanywhere.com/](https://baohan08.pythonanywhere.com/).

***

## Index of Contents
1. [Data and Database](#data-and-database)
2. [Search Engine and Cache](#search-engine)
3. [Recommender](#recommender)
4. [Deployment Instructions](#deployment-instructions)


<a name="data-and-database"></a>

## Data and Database 
I got 5000+ movie_ids from this [movie dataset](https://www.kaggle.com/oxanozaep/imdb-eda/data). With these movie_ids, I utilized a python lib called [imdbpie](https://pypi.org/project/imdbpie/) to collect other columns of data. Currently, there are about 3000 movies in the database.

To make it easy to deploy, SQLite is chosen as database. The database file is `movie.db` in the root directory.


<a name="search-engine"></a>

## Search Engine and Cache

### Approaches
- An Inverted Permuterm Index in B-Tree Structure
- LRU Cache for Frequent Query
- Results Sorted by Rating


<a name="recommender"></a>

## Recommender

- **Item-based** : Do the item-based recommendation based on users’ seens and expects


<a name="deployment-instructions"></a>

## Deployment Instructions
1. Install [**Python 3**]( https://www.python.org/) in your computer, and make sure to set environment variable correctly.
2. Install **Django** and **Sklearn** for the Python environment. The easiest way is to use pip by running `pip install django` and `pip install sklearn` in a terminal.
3. Open a terminal, input command: `python manage.py runserver 8080`
4. Open your web browser, input `localhost:8080` in the address bar.
- P.S. If you fail running `python manage.py runserver 8080`, try another port numbers, like 8081 or 8000.
