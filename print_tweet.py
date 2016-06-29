#!/usr/bin/env python
"""
print_tweet.py

contains function for printing a human readable version of a tweet
contains username, tweet text and time posted
"""
from textwrap import wrap

def pretty_print(tweet):
    separator = '*' * 20 + '\n'
    user_name = tweet['user']['name']
    # print around 80 characters on a line
    tweet_body = '\n'.join(wrap(tweet['text'], 80, break_long_words=False))
    created_at = tweet['created_at']
    output = '{user} says:\n{tweet}\nat {time}\n'.format(user=user_name,
            tweet=tweet_body,
            time=created_at)
    output = separator + output + separator
    print(output)


