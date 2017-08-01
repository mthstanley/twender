#!/usr/bin/env python
"""
tweets.py

module for manipulating tweets from twitter api

contains function for printing a human readable version of a tweet
contains username, tweet text and time posted
"""
from textwrap import wrap

def pptweet(tweet):
    """
    param:
        tweet: dictionary representaion of tweet returned from twitter api
    return:
        None
    description:
        cleanly and clearly prints a given tweet, contains username, tweet
        body and time
    """
    separator = '*' * 20 + '\n'
    if 'user' in tweet and 'name' in tweet['user']:
        user_name = tweet['user']['name']
    else:
        user_name = 'unknown'
    # print around 80 characters on a line
    tweet_body = '\n'.join(wrap(tweet['text'], 80, break_long_words=False))
    created_at = tweet['created_at']
    output = '{user} says:\n{tweet}\nat {time}\n'.format(user=user_name,
            tweet=tweet_body,
            time=created_at)
    output = separator + output + separator
    print(output)


