# MovieHunter
This is a movie website using **Django** as backend framework and SQlite as database. 

For the current version, the following features are implemented, 
- Search Engine
- User Management
- Login via Facebook (OAuth with Facebook API)
- Recommender
- Cache

We deployed the website on a Digital Ocean server at [http://zijun-xu.com](http://zijun-xu.com).

***

## Index of Contents
1. [Data and Database](#data-and-database)
2. [Search Engine](#search-engine)
3. [Recommender](#recommender)
4. [Deployment Instructions](#deployment-instructions)


<a name="hello-world"></a>

## Data and Database 
We downloaded a raw [movie dataset](https://www.kaggle.com/oxanozaep/imdb-eda/data) which contains 5000+ movies and features from IMDB. With movieid, we utilized python lib to collect the features we want from IMDB. Finally, we inserted about 3000 movies into database.

To make it easy to deploy, SQLite is used as database. The database file is "movie.db" in the root directory.


<a name="search-engine"></a>

## Search Engine

### Our Idea
- Permuterm Index : B-Tree
- Transform users’ queries into Wildcard queries
- Return sorted results

### Detail
For each token, add wild-card between each character respectively. 

Return the results that contain all the tokens or contain at least one token of the query.

Sort: 
- Result movies are sorted by ratings.                                             
- Result actors are sorted by number of movies they act.    
- Search “*token” and “token*” first.

Return the results that contain all the tokens in the query first.


<a name="recommender"></a>

## Recommender

- **Item-based** : Do the item-based recommendation based on users’ seens and expects
- **Content-based** : Do the content-based recommendation based on movies’ plots(tf-idf and euclidean distance)

![image](/img/recommender.jpg)


<a name="deployment-instructions"></a>

## Deployment Instructions
1. Install [**Python 3**]( https://www.python.org/) in your computer, and make sure to set environment variable correctly.
2. Install **Django** and **Sklearn** for the Python environment. The easiest way is to use pip by running `pip install django` and `pip install sklearn` in a terminal.
3. Open a terminal, input command: `python manage.py runserver 8080`
4. Open your web browser, input `localhost:8080` in the address bar.
- P.S. If you fail running `python manage.py runserver 8080`, try another port numbers, like 8081 or 8000.
