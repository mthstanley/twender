from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from werkzeug.utils import find_modules, import_string
from config import config
import tweepy

from utils.analysis.learnyouaclassifier import TwenderClassifier

bootstrap = Bootstrap()
mongo = PyMongo()

def register_ext(app):
    """
    param:
        app: flask app
    return:
        None
    description:
        register all flask extension on the given flask application
        object
    """
    bootstrap.init_app(app)
    mongo.init_app(app)


def register_cli(app):
    """
    param:
        app: flask app
    return:
        None
    description:
        register all flask command line tasks
    """
    pass


def register_blueprints(app):
    """
    param:
        app: flask app
    return:
        None
    description:
        finds and registers all blueprints located in twender/blueprints
        blueprints most be located in a dir (python package) of the same
        name as the blueprint, and the blueprint itself must be named
        'bp'
    """
    for name in find_modules('twender.blueprints', include_packages=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def create_app(config_name):
    """
    param:
        config_name: name <string> of desired config to initialize app with
    return:
        flask application object
    description:
        factory function for application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_ext(app)
    register_cli(app)
    register_blueprints(app)

    # initialize tweepy api
    twitter_auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
            app.config['TWITTER_CONSUMER_SECRET'])
    twitter_auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
            app.config['TWITTER_ACCESS_TOKEN_SECRET'])
    app.tweepy_api = tweepy.API(twitter_auth)

    # initialize classifier
    app.classifier = TwenderClassifier()
    with app.app_context():
        app.classifier.train(mongo.db.tweets.find())


    return app
