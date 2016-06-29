#!/usr/bin/env python
"""
collect.py

used to collect tweets that have a name for which the gender
is known, then stores them in a mongo database, also allows
the user to specify the number of tweets to collect, the default is
100 tweets
"""

from twender import tweepy_api, twitter_auth
import tweepystreamer
import tweepy
import sys


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        tweet_limit = 100
    else:
        tweet_limit = int(sys.argv[1])

    twender_stream = tweepystreamer.TwenderStreamListener(tweepy_api)
    twender_stream.tweet_limit = tweet_limit

    # create streamer, mixin our custom stream listener
    strm_api = tweepy.streaming.Stream(twitter_auth, twender_stream)
     
    # get all geotagged tweets that are in english
    strm_api.filter(locations=[-180,-90,180,90], languages=['en'])
