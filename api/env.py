import logging
import os
import sys
from os.path import abspath, dirname, join

basedir = abspath(dirname(dirname(__file__)))

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMAGES_STORE = os.environ.get('IMAGES_STORE')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://db_user:db_password@db:5432/')
    IMAGES_STORE = os.environ.get('IMAGES_STORE', '/storage/')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + join(basedir, "scrape_jobs.db")
    IMAGES_STORE = '/tmp/scraper/'
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    IMAGES_STORE = '/tmp/scraper-test/'
    DEBUG = True
    TESTING = True

if os.environ.get('FLASK_ENV', 'production') == 'production':
    print("Running app in production environment")
    configmodule = ProductionConfig()
elif "pytest" in sys.modules:
    print("Running app in testing environment")
    configmodule = TestingConfig()
else:
    print("Running app in development environment")
    configmodule = DevelopmentConfig()
