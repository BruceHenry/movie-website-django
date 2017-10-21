# Movie-Django

This is a movie website, using Django as backend, SQlite as database. Features like search, user management, login via Facebook are implemented.
[Click here to visit](http://baohan08.pythonanywhere.com)

## Database
To make it easy to deploy, SQLite is used as database. The database file is "movie.db" in the root directory.
To add more data, please modify "add_top250.py" in the root directory.

## Installation Instructions
1. Install Python 3, make sure to set environment variable correctly. https://www.python.org/
2. Install Django, https://docs.djangoproject.com/en/1.11/topics/install/#installing-official-release
3. In the teminal, input command: python manage.py runserver 8080
4. Open your web browser, input "localhost:8080"
5. P.S. If you fail running "python manage.py runserver 8080", try some other port numbers, like 8000.
