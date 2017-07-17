"""

contains configuration variables used throughout the twender package,
includes:
    twitter authentication keys and tokens
    twitter auth object
    tweepy object with access to twitter api
    valid_names dictionary object, which provides first names and respective gender
    mongodb client, twender_db and tweets collection
"""

import tweepy
import json
import pymongo
import os
import twitter_config

consumer_key = twitter_config.CONSUMER_KEY
consumer_secret = twitter_config.CONSUMER_SECRET 

access_token = twitter_config.ACCESS_TOKEN 
access_token_secret = twitter_config.ACCESS_TOKEN_SECRET

twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
twitter_auth.set_access_token(access_token, access_token_secret)

tweepy_api = tweepy.API(twitter_auth)


with open('names/valid_names.json', 'r') as data_file:
    valid_names = json.load(data_file)


mongo_client = pymongo.MongoClient()
twender_db = mongo_client.twender_database
tweets = twender_db.tweets

