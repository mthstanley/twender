"""

contains configuration variables used throughout the twender package,
includes:
    twitter authentication keys and tokens
    twitter auth object
    tweepy object with access to twitter api
    valid_names dictionary object, which provides first names and respective gender
    mongodb client, twender_db and tweets collection
"""

import os
from os.path import join, dirname
import json

import pymongo
import tweepy
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# load dotenv configuration values into environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Collect static configuration
    COLLECT_STATIC_ROOT = os.path.join(BASEDIR, 'static')

    # Twitter configuration values
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    # Mongodb configuration
    MONGO_HOST = os.environ.get('MONGO_HOST')
    MONGO_PORT = os.environ.get('MONGO_PORT')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE')


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
