"""
views.py

contains the view routing functionality for the twender
web application
"""
import tweepy
from tweepy import TweepError
import json
import re
from flask import current_app, render_template, redirect, url_for, session, abort

from . import bp
from .forms import SearchForm

from utils.learnyouaclassifier import genderize


def parse_json_to_obj(cls, json):
    return cls(current_app.tweepy_api).parse(current_app.tweepy_api, json)


#index page route
@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        session['user'] = form.user._json
        return redirect(url_for('main.classify', screen_name=form.user.screen_name))

    return render_template('index.html', form=form)


#about page route
@bp.route('/about')
def about():
    return render_template('about.html')


#classification route, displayed when the user has
#been classified
@bp.route('/classify/<screen_name>')
def classify(screen_name):

    if 'user' in session and screen_name == session['user']['screen_name']:
        # parse user stored as json into User object
        user = parse_json_to_obj(tweepy.models.User, session['user'])
    else:
        try:
            user = current_app.tweepy_api.get_user(screen_name)
        except TweepError as error:
            abort(404)

    tweets = current_app.tweepy_api.user_timeline(id=user.screen_name, count=200)
    json_tweets = [tweet._json for tweet in tweets]
    classifications = current_app.classifier.classify(json_tweets)
    # unzip the zipped tweets and labels
    texts, labels = zip(*classifications)
    gender = genderize(labels)
    texts = [parse_json_to_obj(tweepy.models.Status, text) for text in texts]
    classifications = zip(texts, labels)
    return render_template('classify.html', user=user, tweets=classifications, gender=gender)
