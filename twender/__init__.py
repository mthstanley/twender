import sys

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_collect import Collect
from werkzeug.utils import find_modules, import_string
from config import config
import tweepy
import click
from bson.objectid import ObjectId

from utils.learnyouaclassifier import TwenderClassifier
from utils.tweepystreamer import TwenderStreamListener
from utils.names import valid_names

bootstrap = Bootstrap()
mongo = PyMongo()
collect = Collect()

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
    collect.init_app(app)


def register_cli(app):
    """
    param:
        app: flask app
    return:
        None
    description:
        register all flask command line tasks
    """
    @app.cli.command()
    @click.argument('src', nargs=-1)
    @click.option('--threshold', default=50, type=float,
            help='Accept name/gender label if the percentage occurence of that pair is higher than threshold')
    @click.option('--save/--no-save', default=False, help='Save valid names to database')
    def mkvalidnames(src, threshold, save):
        names = valid_names(list(src), threshold)
        print(names)
        if save:
            existing_names = mongo.db.validnames.find_one()
            if existing_names is not None:
                mongo.db.validnames.delete_one({'_id': ObjectId(existing_names['_id'])})
            mongo.db.validnames.insert_one(names)


    # TODO add solution for valid names
    @app.cli.command()
    @click.option('--numtweets', default=25, help='Number of tweets to collect')
    @click.option('--save/--no-save', default=False, help='Save collected names to database')
    def collecttweets(numtweets, save):
        with app.app_context():
            valid_names = mongo.db.validnames.find_one()

        listener = TwenderStreamListener(app.tweepy_api,
                mongo.db, valid_names, tweet_limit=numtweets)
        listener.save_to_db = save

        # create streamer, mixin our custom stream listener
        stream = tweepy.Stream(auth=app.tweepy_api.auth,
                listener=listener)

        # get all geotagged tweets that are in english
        stream.filter(locations=[-180,-90,180,90], languages=['en'])


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



def register_template_filters(app):
    """
    param:
        app: flask app
    return:
        None
    description:
        register jinja custom template filters
    """
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%H:%m %b %d, %y'):
        return value.strftime(format)


    @app.template_filter('twitterthumb')
    def twitterthumb(value, size="normal"):
        if size in ['bigger', 'mini', 'original']:
            if size == 'original':
                value = value.replace('_normal', '')
            else:
                value = value.replace('_normal', '_' + size)
        return value



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
    register_template_filters(app)

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
