FROM python:slim
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN chmod 777 -R /code/
RUN pip install -r requirements.txt
EXPOSE 8080
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
