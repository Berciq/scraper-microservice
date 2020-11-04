FROM python:3.8

RUN mkdir /api

WORKDIR /api

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install psycopg2

ADD . .