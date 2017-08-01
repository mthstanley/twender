#!/usr/bin/env python
"""
tweepystreamer.py

contains custom tweepy streamer class, which is used to stream
tweets and collect tweets from users that have a first name which
is contained in the valid names dictionary, i.e. a first name for
which the gender is "known"
"""

import sys
import json
import re
import tweepy
from .tweets import pptweet
from .learnyouaclassifier import is_retweet

class TwenderStreamListener(tweepy.StreamListener):
    def __init__(self, api, db, valid_names, tweet_limit=100):
        """
        param:
            api: tweepy api object which will be used to allow the streamer
            access to twitter
            db: mongodb database instance, db must have tweets collection
            valid_names: dictionary of valid names (and their gender label) to
            accept from stream
        return:
            None
        description:
            initialization function for the twender streamer
        """
        self.api = api
        self.valid_names = valid_names
        super(tweepy.StreamListener, self).__init__()

        # set up a default limit for number of tweets to collect
        self.num_tweets = 0
        self.tweet_limit = 100
        self.db = db
        self.save_to_db = False


    def on_data(self, tweet):
        """
        param:
            tweet: tweepy status object received from the stream
        return:
            boolean as to whether the streamer has collected
            the tweet limit, if False streamer will stop
        """
        if self.num_tweets >= self.tweet_limit:
            return False

        # change the status object to a dictionary
        json_tweet = json.loads(tweet)
        name = self.has_valid_name(json_tweet)
        if name is not None and not is_retweet(json_tweet):
            # don't collect retweets as they are originally written
            # by someone else
            self.num_tweets += 1
            json_tweet['gender'] = self.valid_names[name]['gender']
            print('({user}, {gender})'.format(user=json_tweet['user']['name'],
                gender=json_tweet['gender']))
            pptweet(json_tweet)
            if self.save_to_db:
                self.db.tweets.insert(json_tweet)
        return True


    def on_error(self, status_code):
        print(status_code)
        if status_code == 420: # exceeded rate limit
            return False
        return True # don't stop stream on error


    def on_timeout(self):
        return True # don't stop the stream


    def has_valid_name(self, tweet):
        """
        param:
            tweet: tweet in dictionary form
        return:
            boolean, True if name is valid otherwise False
        description:
            returns True if the tweet has a username and the first word in the
            name is contained in the valid names dictionary
        """
        if 'user' in tweet:
            if 'name' in tweet['user']:
                # grab the first word and assume it is the first name
                first_name = tweet['user']['name'].split()[0]
                if first_name in self.valid_names:
                    return first_name

        return None

