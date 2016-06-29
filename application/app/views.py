"""
views.py

contains the view routing functionality for the twender
web application
"""

from flask import render_template, flash, redirect, g, url_for
from app import app
from .forms import SearchForm
from .models import tweet_classifier
from twender.analysis.learnyouaclassifier import genderize
from twender import tweepy_api, twender_db
import tweepy
import json
import re


@app.before_request
def before_request():
    g.search_form = SearchForm()


#index page route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', tweets=[], gender=-1)


#about page route
@app.route('/about')
def about():
    return render_template('about.html')


#search route, used when the user enters a search
#this route redirects to the classify route
@app.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('classify', query=g.search_form.search.data))


#classification route, displayed when the user has
#been classified
@app.route('/classify/<query>')
def classify(query):
    error = None
    try:
        tweets = tweepy_api.user_timeline(id=query, count=200)
        json_tweets = [tweet._json for tweet in tweets]
        classifications = tweet_classifier.classify(json_tweets)
       
        # unzip the zipped tweets and labels
        texts, labels = zip(*classifications)
        gender = genderize(labels)
        classifications = zip(texts, labels)
        return render_template('index.html', tweets=classifications, 
                gender=gender)
    except Exception as e:
        print(e)
        error = "Oops! I counld't find you."
        return render_template('index.html', error=error)
