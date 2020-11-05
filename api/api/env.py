import logging
import os
import sys
from os.path import abspath, dirname, join

basedir = abspath(dirname(dirname(dirname(__file__))))

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
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + join(basedir, "test.db")
    IMAGES_STORE = '/tmp/scraper-test/'
    DEBUG = False
    TESTING = True

if os.environ.get('FLASK_ENV', 'production') == 'production':
    configmodule = ProductionConfig()
elif "pytest" in sys.modules:
    configmodule = TestingConfig()
else:
    configmodule = DevelopmentConfig()
