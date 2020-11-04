FROM python:3.8

RUN mkdir /scraper

WORKDIR /scraper

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN pip install psycopg2

ADD . .